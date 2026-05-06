from __future__ import annotations

from pathlib import Path

from app.settings import ApiSettings
from ml.common.config import base as base_config


def test_apisettings_loads_non_secret_values_from_setting_yaml(monkeypatch, tmp_path: Path) -> None:
    # `make check` exports PROJECT_ID via Makefile; env wins over yaml in
    # pydantic-settings precedence. Strip the relevant fields so this test
    # exercises the yaml source in isolation.
    for var in (
        "PROJECT_ID",
        "ELASTICSEARCH_URL",
        "ELASTICSEARCH_API_KEY",
    ):
        monkeypatch.delenv(var, raising=False)
    setting_path = tmp_path / "setting.yaml"
    credential_path = tmp_path / "credential.yaml"
    setting_path.write_text(
        "\n".join(
            [
                'project_id: "custom-project"',
                'elasticsearch_url: "http://elasticsearch.search.svc.cluster.local:9200"',
            ]
        ),
        encoding="utf-8",
    )
    credential_path.write_text("elasticsearch_api_key: local-es-key\n", encoding="utf-8")
    monkeypatch.setattr(base_config, "_SETTING_YAML", setting_path)
    monkeypatch.setattr(base_config, "_CREDENTIAL_YAML", credential_path)

    settings = ApiSettings()

    assert settings.project_id == "custom-project"
    assert settings.elasticsearch_url == "http://elasticsearch.search.svc.cluster.local:9200"
    assert settings.elasticsearch_api_key == "local-es-key"


def test_env_vars_override_yaml_sources(monkeypatch, tmp_path: Path) -> None:
    setting_path = tmp_path / "setting.yaml"
    credential_path = tmp_path / "credential.yaml"
    setting_path.write_text('project_id: "from-setting"\n', encoding="utf-8")
    credential_path.write_text('elasticsearch_api_key: "from-credential"\n', encoding="utf-8")
    monkeypatch.setattr(base_config, "_SETTING_YAML", setting_path)
    monkeypatch.setattr(base_config, "_CREDENTIAL_YAML", credential_path)
    monkeypatch.setenv("PROJECT_ID", "from-env")
    monkeypatch.setenv("ELASTICSEARCH_API_KEY", "env-key")

    settings = ApiSettings()

    assert settings.project_id == "from-env"
    assert settings.elasticsearch_api_key == "env-key"
