"""M-Wave9 — public-domain / HTTPS / DNS workflow contract.

Pins the wiring for the `gcp-search-mlops-gke.dev` serving path so a regression
cannot silently drop:
  - the canonical value source (env/config/setting.yaml::public_domain / dns_zone_name)
  - GKE Gateway: hostname, the `networking.gke.io/certmap` annotation, the
    reserved static IP pin (spec.addresses NamedAddress)
  - the `dns` Terraform module: reserved global IP, apex A record, Certificate
    Manager DNS-01 chain (dns_authorization → managed certificate → certificate_map
    → certificate_map_entry), and that the Cloud DNS zone is **read** (data source)
    not managed
  - dev/main.tf: module.dns wired with the -var values, kserve self-signed
    placeholder CN = public_domain, api_external_url derived from public_domain
  - apis.tf: dns.googleapis.com enabled

This is the contract test the M-Wave9 capability requires (incident-postmortem
→ contract test policy, docs/architecture/01 §0 / TASKS_ROADMAP §3.5).
"""

from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]


def _read(rel: str) -> str:
    return (REPO_ROOT / rel).read_text(encoding="utf-8")


def _setting_value(key: str) -> str:
    for raw in _read("env/config/setting.yaml").splitlines():
        line = raw.split("#", 1)[0].strip()
        if line.startswith(f"{key}:"):
            return line.split(":", 1)[1].strip().strip('"').strip("'")
    raise AssertionError(f"setting.yaml missing key: {key}")


# Default resource names in modules/dns/variables.tf — the Gateway annotation
# and the dev outputs must agree with these.
_CERTMAP_DEFAULT = "search-api-certmap"
_GATEWAY_IP_DEFAULT = "search-api-ip"


def test_setting_yaml_holds_canonical_domain_and_zone() -> None:
    domain = _setting_value("public_domain")
    zone = _setting_value("dns_zone_name")
    assert re.fullmatch(r"[a-z0-9.-]+\.[a-z]+", domain), f"unexpected domain shape: {domain}"
    assert re.fullmatch(r"[a-z0-9-]+", zone), f"unexpected dns_zone_name shape: {zone}"
    # `.dev` is HSTS-preloaded; the project intentionally targets it.
    assert domain.endswith(".dev"), "public_domain is expected to be a .dev domain"


def test_gateway_manifest_uses_setting_public_domain_and_certmap() -> None:
    domain = _setting_value("public_domain")
    gw = _read("infra/manifests/search-api/gateway.yaml")
    assert f'hostname: "{domain}"' in gw, (
        "Gateway listener hostname must match setting.yaml::public_domain"
    )
    assert f'- "{domain}"' in gw, "HTTPRoute hostnames must include setting.yaml::public_domain"
    assert "search-api.example.com" not in gw, (
        "legacy placeholder hostname leaked into gateway.yaml"
    )
    assert f"networking.gke.io/certmap: {_CERTMAP_DEFAULT}" in gw, (
        "Gateway must bind the Certificate Manager certmap (networking.gke.io/certmap)"
    )
    # static IP pinned via spec.addresses (NamedAddress) → breaks the A-record chicken-and-egg.
    assert "type: NamedAddress" in gw and _GATEWAY_IP_DEFAULT in gw, (
        "Gateway must pin the reserved global IP via spec.addresses NamedAddress"
    )
    # self-signed placeholder still referenced so the listener stays PROGRAMMED.
    assert "search-api-tls" in gw


def test_dns_module_has_static_ip_apex_a_and_cert_manager_chain() -> None:
    main = _read("infra/terraform/modules/dns/main.tf")
    # Zone is read, never managed.
    assert 'data "google_dns_managed_zone" "public"' in main
    assert 'resource "google_dns_managed_zone"' not in main
    # Reserved global external IP + apex A record pointing at it.
    assert 'resource "google_compute_global_address" "search_api"' in main
    assert 'resource "google_dns_record_set" "apex_a"' in main
    assert "google_compute_global_address.search_api.address" in main
    # Certificate Manager DNS-01 chain.
    assert 'resource "google_certificate_manager_dns_authorization" "search_api"' in main
    assert 'resource "google_certificate_manager_certificate" "search_api"' in main
    assert "google_certificate_manager_dns_authorization.search_api.id" in main, (
        "managed certificate must reference the DNS authorization"
    )
    assert 'resource "google_certificate_manager_certificate_map" "search_api"' in main
    assert 'resource "google_certificate_manager_certificate_map_entry" "search_api"' in main
    # The DNS authorization's CNAME record is published in the zone.
    assert "dns_resource_record[0].name" in main and "dns_resource_record[0].data" in main


def test_dns_module_defaults_match_gateway_annotation() -> None:
    variables = _read("infra/terraform/modules/dns/variables.tf")
    m_map = re.search(
        r'variable "certificate_map_name".*?default\s*=\s*"([^"]+)"', variables, re.DOTALL
    )
    m_ip = re.search(r'variable "gateway_ip_name".*?default\s*=\s*"([^"]+)"', variables, re.DOTALL)
    assert m_map and m_map.group(1) == _CERTMAP_DEFAULT
    assert m_ip and m_ip.group(1) == _GATEWAY_IP_DEFAULT


def test_dev_main_wires_dns_module_and_passes_public_domain_everywhere() -> None:
    dev_main = _read("infra/terraform/environments/dev/main.tf")
    assert 'module "dns"' in dev_main
    assert "public_domain = var.public_domain" in dev_main
    assert "dns_zone_name = var.dns_zone_name" in dev_main
    # kserve self-signed placeholder CN must match the real domain.
    assert "tls_cn = var.public_domain" in dev_main
    # composer / messaging API URL derived from the public domain (no two-pass apply).
    assert (
        'var.api_external_url != "" ? var.api_external_url : "https://${var.public_domain}"'
        in dev_main
    )
    # dev outputs expose the dns module surface.
    dev_outputs = _read("infra/terraform/environments/dev/outputs.tf")
    for out in ("public_domain", "gateway_ip_name", "certificate_map_name", "certificate_name"):
        assert f'output "{out}"' in dev_outputs


def test_apis_tf_enables_cloud_dns() -> None:
    apis = _read("infra/terraform/environments/dev/apis.tf")
    assert '"dns.googleapis.com"' in apis
    assert '"certificatemanager.googleapis.com"' in apis


def test_variables_tf_declares_public_domain_and_zone_without_default() -> None:
    variables = _read("infra/terraform/environments/dev/variables.tf")
    for name in ("public_domain", "dns_zone_name"):
        block = re.search(rf'variable "{name}" \{{.*?\n\}}', variables, re.DOTALL)
        assert block, f"variables.tf missing variable {name}"
        assert "default" not in block.group(0), f"{name} must not have a default (fail loud)"
        assert "validation {" in block.group(0), f"{name} should have a validation block"


def test_canonical_tf_var_names_includes_public_domain_and_zone() -> None:
    common = _read("scripts/_common.py")
    m = re.search(
        r"CANONICAL_TF_VAR_NAMES\s*:\s*tuple\[str, \.\.\.\]\s*=\s*\(([^)]*)\)", common, re.DOTALL
    )
    assert m, "CANONICAL_TF_VAR_NAMES tuple not found in scripts/_common.py"
    body = m.group(1)
    for name in ("GITHUB_REPO", "ONCALL_EMAIL", "PUBLIC_DOMAIN", "DNS_ZONE_NAME"):
        assert f'"{name}"' in body, f"CANONICAL_TF_VAR_NAMES missing {name}"


def test_makefile_exports_public_domain_and_zone() -> None:
    makefile = _read("Makefile")
    assert "PUBLIC_DOMAIN ?= $(call _yaml_get,public_domain)" in makefile
    assert "DNS_ZONE_NAME ?= $(call _yaml_get,dns_zone_name)" in makefile
    # both must be on the `export` line so terraform_var_args() / env() see them.
    export_line = next(line for line in makefile.splitlines() if line.startswith("export "))
    assert "PUBLIC_DOMAIN" in export_line and "DNS_ZONE_NAME" in export_line


def test_tf_apply_stage1_targets_includes_module_dns() -> None:
    """`module.dns` は `TF_APPLY_STAGE1_TARGETS` に含まれること — Certificate Manager の
    DNS-01 検証を deploy の残り (kserve / configmap / composer-dags / deploy-api) の間に
    進ませ、`kubectl apply -k` で Gateway が certmap を bind する頃には cert が ACTIVE に
    なっているようにするため (module.composer と同じ理由)。"""
    from scripts.domain.terraform.stage_apply import TF_APPLY_STAGE1_TARGETS

    assert "module.dns" in TF_APPLY_STAGE1_TARGETS


def test_build_all_local_is_single_line_script_call() -> None:
    """Makefile 破綻防止仕様: 複数行アクションは禁止 — `build-all-local` は
    `scripts/deploy/build_all_local.py` を 1 行で呼ぶだけ。"""
    makefile = _read("Makefile")
    m = re.search(r"^build-all-local:.*?\n((?:\t.*\n)+)", makefile, re.MULTILINE)
    assert m, "build-all-local target not found"
    recipe_lines = [ln for ln in m.group(1).splitlines() if ln.strip()]
    assert recipe_lines == ["\tuv run python -u -m scripts.deploy.build_all_local"], (
        f"build-all-local must be a single-line script call, got: {recipe_lines}"
    )
    assert (REPO_ROOT / "scripts" / "deploy" / "build_all_local.py").is_file()
