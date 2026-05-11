"""Unit tests for scripts._common.resolve_api_target.

Pins the canonical resolution contract:

    1. ``API_URL`` wins (mode=explicit). Token only when API_REQUIRE_TOKEN=truthy.
       ``API_HOST_HEADER`` / ``API_INSECURE_TLS`` で Host / TLS 検証を上書き可能。
    2. ``TARGET=local`` uses LOCAL_API_URL with no token, no Host override,
       verify_tls=True (mode=local).
    3. ``TARGET=gcp`` (default):
       - ``_common.PUBLIC_DOMAIN`` (= env/config/setting.yaml::public_domain) が
         truthy なら ``https://<public_domain>`` を返す。Google-managed cert
         なので ``verify_tls=True``、URL hostname が cert CN と一致するので
         Host ヘッダ上書きなし。``API_INSECURE_TLS`` で TLS 検証を切れる。
       - 空 (bootstrap 期、DNS / Certificate Manager 未 live) なら
         ``gateway_url()`` の Gateway 外部 IP に直叩き、``verify_tls=False``、
         ``Host: <DEFAULT_GATEWAY_HOST_HEADER>``。

The basis is intentionally small: it must not auto-detect modes or fall back.
"""

from __future__ import annotations

import pytest

from scripts import _common


@pytest.fixture(autouse=True)
def _clear_target_env(monkeypatch: pytest.MonkeyPatch) -> None:
    for key in (
        "TARGET",
        "LOCAL_API_URL",
        "API_URL",
        "API_REQUIRE_TOKEN",
        "API_HOST_HEADER",
        "API_INSECURE_TLS",
    ):
        monkeypatch.delenv(key, raising=False)


def test_explicit_api_url_wins_over_target_and_skips_token_by_default(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("API_URL", "https://search.example.com/")
    monkeypatch.setenv("TARGET", "gcp")
    monkeypatch.setattr(_common, "gateway_url", lambda: pytest.fail("must not call gateway_url"))
    monkeypatch.setattr(_common, "identity_token", lambda: pytest.fail("must not mint a token"))

    resolved = _common.resolve_api_target()

    assert resolved.mode == "explicit"
    assert resolved.url == "https://search.example.com"
    assert resolved.token is None
    assert resolved.host_header is None
    assert resolved.verify_tls is True


def test_explicit_api_url_honors_host_and_insecure_overrides(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("API_URL", "https://1.2.3.4")
    monkeypatch.setenv("API_HOST_HEADER", "search-api.example.com")
    monkeypatch.setenv("API_INSECURE_TLS", "true")

    resolved = _common.resolve_api_target()

    assert resolved.host_header == "search-api.example.com"
    assert resolved.verify_tls is False


@pytest.mark.parametrize("flag", ["1", "true", "yes", "on", "TRUE", "On"])
def test_explicit_api_url_mints_token_when_require_token_truthy(
    monkeypatch: pytest.MonkeyPatch, flag: str
) -> None:
    monkeypatch.setenv("API_URL", "https://search.example.com")
    monkeypatch.setenv("API_REQUIRE_TOKEN", flag)
    monkeypatch.setattr(_common, "identity_token", lambda: "token-xyz")

    resolved = _common.resolve_api_target()

    assert resolved.mode == "explicit"
    assert resolved.token == "token-xyz"


def test_target_local_uses_default_local_url_without_token(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("TARGET", "local")
    monkeypatch.setattr(_common, "identity_token", lambda: pytest.fail("local must not mint token"))

    resolved = _common.resolve_api_target()

    assert resolved.mode == "local"
    assert resolved.url == "http://127.0.0.1:8080"
    assert resolved.token is None
    assert resolved.host_header is None
    assert resolved.verify_tls is True


def test_target_local_honors_local_api_url_override(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("TARGET", "local")
    monkeypatch.setenv("LOCAL_API_URL", "http://127.0.0.1:18080/")

    resolved = _common.resolve_api_target()

    assert resolved.mode == "local"
    assert resolved.url == "http://127.0.0.1:18080"


def test_target_gcp_default_uses_public_domain_with_valid_tls(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """M-Wave9 canonical: public domain is set → https://<domain>, real cert."""
    monkeypatch.setattr(_common, "PUBLIC_DOMAIN", "gcp-search-mlops-gke.dev")
    monkeypatch.setattr(
        _common,
        "gateway_url",
        lambda: pytest.fail("must not fall back to gateway_url when PUBLIC_DOMAIN set"),
    )
    monkeypatch.setattr(_common, "identity_token", lambda: pytest.fail("gcp must not mint token"))

    resolved = _common.resolve_api_target()

    assert resolved.mode == "gcp"
    assert resolved.url == "https://gcp-search-mlops-gke.dev"
    assert resolved.token is None
    assert resolved.host_header is None
    assert resolved.verify_tls is True


def test_target_gcp_public_domain_honors_insecure_tls_override(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(_common, "PUBLIC_DOMAIN", "gcp-search-mlops-gke.dev")
    monkeypatch.setenv("API_INSECURE_TLS", "true")

    resolved = _common.resolve_api_target()

    assert resolved.url == "https://gcp-search-mlops-gke.dev"
    assert resolved.verify_tls is False


def test_target_gcp_falls_back_to_gateway_ip_when_public_domain_empty(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Bootstrap (no public domain yet): direct Gateway IP + Host + insecure TLS."""
    monkeypatch.setattr(_common, "PUBLIC_DOMAIN", "")
    monkeypatch.setattr(_common, "DEFAULT_GATEWAY_HOST_HEADER", "search-api.example.com")
    monkeypatch.setattr(_common, "gateway_url", lambda: "https://34.128.173.247")
    monkeypatch.setattr(_common, "identity_token", lambda: pytest.fail("gcp must not mint token"))

    resolved = _common.resolve_api_target()

    assert resolved.mode == "gcp"
    assert resolved.url == "https://34.128.173.247"
    assert resolved.host_header == "search-api.example.com"
    assert resolved.verify_tls is False


def test_target_gcp_fallback_honors_api_host_header_override(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(_common, "PUBLIC_DOMAIN", "")
    monkeypatch.setattr(_common, "gateway_url", lambda: "https://34.128.173.247")
    monkeypatch.setenv("API_HOST_HEADER", "custom.example.com")

    resolved = _common.resolve_api_target()

    assert resolved.mode == "gcp"
    assert resolved.host_header == "custom.example.com"


def test_unknown_target_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("TARGET", "staging")

    with pytest.raises(ValueError, match="TARGET must be either 'local' or 'gcp'"):
        _common.resolve_api_target()
