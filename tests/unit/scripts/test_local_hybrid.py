from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

from scripts.setup import local_hybrid


def test_resolve_meili_master_key_prefers_local_secret() -> None:
    with (
        patch("scripts.setup.local_hybrid.secret", return_value="local-secret"),
        patch("scripts.setup.local_hybrid.gcloud") as gcloud_mock,
    ):
        assert (
            local_hybrid._resolve_meili_master_key(meili_base_url="https://meili.example.com")
            == "local-secret"
        )
    gcloud_mock.assert_not_called()


def test_resolve_meili_master_key_falls_back_to_secret_manager() -> None:
    with (
        patch("scripts.setup.local_hybrid.secret", return_value=""),
        patch(
            "scripts.setup.local_hybrid.env",
            side_effect=lambda name, default="": {
                "MEILI_MASTER_KEY_SECRET_ID": "meili-master-key",
                "PROJECT_ID": "mlops-dev-a",
            }.get(name, default),
        ),
        patch("scripts.setup.local_hybrid.gcloud", return_value="gcp-secret"),
    ):
        assert (
            local_hybrid._resolve_meili_master_key(meili_base_url="https://meili.example.com")
            == "gcp-secret"
        )


def test_resolve_meili_base_url_prefers_local_meili_when_available() -> None:
    with (
        patch(
            "scripts.setup.local_hybrid.env",
            side_effect=lambda name, default="": {
                "MEILI_BASE_URL": "",
                "LOCAL_MEILI_BASE_URL": "http://127.0.0.1:7700",
                "LOCAL_HYBRID_ALLOW_GCP_FALLBACK": "false",
            }.get(name, default),
        ),
        patch("scripts.setup.local_hybrid._http_available", return_value=True),
        patch("scripts.setup.local_hybrid.gcloud") as gcloud_mock,
    ):
        assert local_hybrid._resolve_meili_base_url() == "http://127.0.0.1:7700"
    gcloud_mock.assert_not_called()


def test_resolve_meili_base_url_disables_lexical_when_local_missing() -> None:
    with (
        patch(
            "scripts.setup.local_hybrid.env",
            side_effect=lambda name, default="": {
                "MEILI_BASE_URL": "",
                "LOCAL_MEILI_BASE_URL": "http://127.0.0.1:7700",
                "LOCAL_HYBRID_ALLOW_GCP_FALLBACK": "false",
            }.get(name, default),
        ),
        patch("scripts.setup.local_hybrid._http_available", return_value=False),
        patch("scripts.setup.local_hybrid.gcloud") as gcloud_mock,
    ):
        assert local_hybrid._resolve_meili_base_url() == ""
    gcloud_mock.assert_not_called()


def test_resolve_meili_master_key_uses_empty_key_for_local_meili() -> None:
    with (
        patch("scripts.setup.local_hybrid.secret", return_value=""),
        patch("scripts.setup.local_hybrid.env", return_value=""),
        patch("scripts.setup.local_hybrid.gcloud") as gcloud_mock,
    ):
        assert local_hybrid._resolve_meili_master_key(meili_base_url="http://127.0.0.1:7700") == ""
    gcloud_mock.assert_not_called()


def test_ensure_local_reranker_model_skips_existing_file(tmp_path: Path) -> None:
    model_path = tmp_path / "model.txt"
    model_path.write_text("ok", encoding="utf-8")
    with patch("scripts.setup.local_hybrid.run") as run_mock:
        local_hybrid._ensure_local_reranker_model(model_path)
    run_mock.assert_not_called()
