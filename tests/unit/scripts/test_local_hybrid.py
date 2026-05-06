from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

from scripts.setup import local_hybrid


def test_resolve_elasticsearch_api_key_prefers_local_secret() -> None:
    with patch("scripts.setup.local_hybrid.secret", return_value="es-secret"):
        assert (
            local_hybrid._resolve_elasticsearch_api_key(elasticsearch_url="http://127.0.0.1:9200")
            == "es-secret"
        )


def test_resolve_elasticsearch_api_key_empty_when_no_url() -> None:
    assert local_hybrid._resolve_elasticsearch_api_key(elasticsearch_url="") == ""


def test_resolve_elasticsearch_url_prefers_explicit_env() -> None:
    with patch(
        "scripts.setup.local_hybrid.env",
        side_effect=lambda name, default="": {
            "ELASTICSEARCH_URL": "http://es.example:9200",
        }.get(name, default),
    ):
        assert local_hybrid._resolve_elasticsearch_url() == "http://es.example:9200"


def test_resolve_elasticsearch_url_uses_local_when_http_available() -> None:
    with (
        patch(
            "scripts.setup.local_hybrid.env",
            side_effect=lambda name, default="": {
                "ELASTICSEARCH_URL": "",
                "LOCAL_ELASTICSEARCH_URL": "http://127.0.0.1:9200",
            }.get(name, default),
        ),
        patch("scripts.setup.local_hybrid._http_available", return_value=True),
    ):
        assert local_hybrid._resolve_elasticsearch_url() == "http://127.0.0.1:9200"


def test_resolve_elasticsearch_url_returns_empty_when_unreachable() -> None:
    with (
        patch(
            "scripts.setup.local_hybrid.env",
            side_effect=lambda name, default="": {
                "ELASTICSEARCH_URL": "",
                "LOCAL_ELASTICSEARCH_URL": "http://127.0.0.1:9200",
            }.get(name, default),
        ),
        patch("scripts.setup.local_hybrid._http_available", return_value=False),
    ):
        assert local_hybrid._resolve_elasticsearch_url() == ""


def test_ensure_local_reranker_model_skips_existing_file(tmp_path: Path) -> None:
    model_path = tmp_path / "model.txt"
    model_path.write_text("ok", encoding="utf-8")
    with patch("scripts.setup.local_hybrid.run") as run_mock:
        local_hybrid._ensure_local_reranker_model(model_path)
    run_mock.assert_not_called()
