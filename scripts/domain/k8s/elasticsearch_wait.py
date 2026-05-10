"""Wait for ECK-managed Elasticsearch to become healthy before sync.

2026-05-09 incident postmortem:
- step 10 (`sync-elasticsearch`) executed immediately after step 9 (`apply-manifests`)
  while ECK was still bootstrapping the ES cluster.
- ES pod was Running 1/1 but ECK status was `Phase=ApplyingChanges Health=unknown`,
  and the HTTP API responded with `Server disconnected without sending a response`
  (= TLS handshake / auth not yet ready).
- `sync_elasticsearch.py` gives up immediately on httpx error and the deploy-all
  step fails with no retry, forcing the whole pipeline to stall.

Fix: poll the ECK Elasticsearch CR's `.status.health` until it reports `green`
or `yellow` (= shards allocated, API reachable). The poll itself is cheap
(`kubectl get` per 15s) and bounded by `timeout_s`. If the cluster is genuinely
broken (license reconcile stall, see `docs/troubleshooting/eck-license-reconcile-stall.md`),
the wait will time out and the operator can then judge: keep debugging vs.
destroy-all the cluster.
"""

from __future__ import annotations

import time

from scripts.adapters.kubectl import kubectl_run

# ECK Elasticsearch CR location. Override only if the manifest moves.
DEFAULT_NAMESPACE = "search"
DEFAULT_NAME = "elasticsearch"

# Poll cadence and overall timeout. Real ECK bootstrap on a freshly created GKE
# cluster typically reaches `green/yellow` within 60-180s; 300s (5 min) gives a
# generous margin while still failing fast if the ECK Operator is wedged.
POLL_INTERVAL_S = 15
DEFAULT_TIMEOUT_S = 300

# `green` = all shards assigned, `yellow` = primaries assigned but some replicas
# unallocated (single-node CR is always yellow at best because replicas have
# nowhere to go). Both states accept `_count` / `_bulk` requests, which is what
# `sync_elasticsearch.py` needs.
HEALTHY_STATES = ("green", "yellow")


def _read_health(namespace: str, name: str) -> str:
    """Return current `.status.health` value (empty string if not set yet)."""
    proc = kubectl_run("-n",
            namespace,
            "get",
            "elasticsearch",
            name,
            "-o",
            "jsonpath={.status.health}",
        capture=True,
        check=False,
    )
    return proc.stdout.strip()


def _read_phase(namespace: str, name: str) -> str:
    proc = kubectl_run("-n",
            namespace,
            "get",
            "elasticsearch",
            name,
            "-o",
            "jsonpath={.status.phase}",
        capture=True,
        check=False,
    )
    return proc.stdout.strip()


def wait_until_es_healthy(
    namespace: str = DEFAULT_NAMESPACE,
    name: str = DEFAULT_NAME,
    timeout_s: int = DEFAULT_TIMEOUT_S,
) -> str:
    """Block until ECK Elasticsearch CR `.status.health` is `green` or `yellow`.

    Returns the final health value on success. Raises ``TimeoutError`` if the
    cluster does not reach a healthy state within ``timeout_s`` — typically a
    sign of ECK Operator reconcile stall (see incident memo).
    """
    deadline = time.monotonic() + timeout_s
    last_health = ""
    last_phase = ""
    print(
        f"==> wait_until_es_healthy: namespace={namespace} name={name} "
        f"timeout={timeout_s}s healthy_states={HEALTHY_STATES}"
    )
    while time.monotonic() < deadline:
        health = _read_health(namespace, name)
        phase = _read_phase(namespace, name)
        if health in HEALTHY_STATES:
            print(f"    ES ready: health={health} phase={phase}")
            return health
        if health != last_health or phase != last_phase:
            print(f"    health={health or '(unset)'} phase={phase or '(unset)'}")
            last_health = health
            last_phase = phase
        time.sleep(POLL_INTERVAL_S)
    elapsed = timeout_s
    raise TimeoutError(
        f"Elasticsearch CR {namespace}/{name} did not reach health in "
        f"{HEALTHY_STATES} within {elapsed}s. Last seen: health={last_health!r} "
        f"phase={last_phase!r}. See "
        "docs/troubleshooting/eck-license-reconcile-stall.md for recovery."
    )
