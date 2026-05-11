"""M-Wave9 — the public domain must be consistent across the source-of-truth and
its consumers: env/config/setting.yaml (canonical value), the GKE Gateway
manifest (listener hostname + HTTPRoute hostnames), and the certmap annotation.
"""

from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]


def _setting_value(key: str) -> str:
    text = (REPO_ROOT / "env" / "config" / "setting.yaml").read_text(encoding="utf-8")
    for raw in text.splitlines():
        line = raw.split("#", 1)[0].strip()
        if line.startswith(f"{key}:"):
            return line.split(":", 1)[1].strip().strip('"').strip("'")
    raise AssertionError(f"setting.yaml missing key: {key}")


def test_public_domain_is_a_dev_domain() -> None:
    domain = _setting_value("public_domain")
    assert domain, "public_domain must be non-empty"
    assert re.fullmatch(r"[a-z0-9.-]+\.[a-z]+", domain), f"unexpected domain shape: {domain}"


def test_gateway_manifest_uses_setting_public_domain() -> None:
    domain = _setting_value("public_domain")
    gw = (REPO_ROOT / "infra" / "manifests" / "search-api" / "gateway.yaml").read_text(
        encoding="utf-8"
    )
    # listener hostname + HTTPRoute hostnames both point at the canonical domain.
    assert f'hostname: "{domain}"' in gw, (
        "Gateway listener hostname must match setting.yaml::public_domain"
    )
    assert f'- "{domain}"' in gw, "HTTPRoute hostnames must include setting.yaml::public_domain"
    # Old placeholder must not leak back in.
    assert "search-api.example.com" not in gw, (
        "legacy placeholder hostname leaked into gateway.yaml"
    )
    # certmap annotation must be present (Certificate Manager-managed TLS).
    assert "networking.gke.io/certmap:" in gw, "Gateway must bind a Certificate Manager certmap"
    # static IP pinned via spec.addresses (NamedAddress) to break the A-record chicken-and-egg.
    assert "type: NamedAddress" in gw and "search-api-ip" in gw, (
        "Gateway must pin the reserved global IP"
    )


def test_dns_module_and_zone_name_present() -> None:
    """The dns module exists and dev/main.tf wires it with the setting.yaml zone."""
    assert (REPO_ROOT / "infra" / "terraform" / "modules" / "dns" / "main.tf").is_file()
    dev_main = (REPO_ROOT / "infra" / "terraform" / "environments" / "dev" / "main.tf").read_text(
        encoding="utf-8"
    )
    assert 'module "dns"' in dev_main
    assert "dns_zone_name = var.dns_zone_name" in dev_main
    assert "public_domain = var.public_domain" in dev_main
    # The zone name in setting.yaml must look like a Cloud DNS managed-zone name.
    zone = _setting_value("dns_zone_name")
    assert re.fullmatch(r"[a-z0-9-]+", zone), f"unexpected dns_zone_name shape: {zone}"
