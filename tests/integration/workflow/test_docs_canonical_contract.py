"""canonical docs contract — section structure + cost estimate + test inventory 整合.

2026-05-12 以降の docs 構成:
- `01_仕様と設計.md` = skeleton (section 見出し + キーワードのみ。詳細は 03 へ集約)
- `03_実装カタログ.md` = 実装インデックス (現在地 / 実装マップ / API / Data / GCP / Test inventory /
  Decisions / Completion Log / Milestone Archive / Incident Archive)
- substantive な不変ルール (Composer 本線 = Vertex PipelineJobSchedule 完全撤去 等) は CLAUDE.md /
  TASKS_ROADMAP §3 が正本

本 test は (a) 01 が必要 section を保持、(b) 04/05 の canonical gate / PDCA フロー wording 維持、
(c) 03 の test inventory 整合、(d) runbook §1.4-bis のコスト見積もり (¥870-1,200 / 3h、当日 destroy
前提 — 過去の ¥9,000 padding ミス再発防止) を pin する。
"""

from __future__ import annotations

from tests.integration.workflow.conftest import read_repo_file as _read


def test_canonical_docs_describe_workflow_contract_goals() -> None:
    # 2026-05-12 以降の docs 構成: 01 は skeleton (section 見出し + キーワード) に縮約され、
    # 詳細な実装所在 / 完了ログ / incident は 03 に集約。下記 pin はその新構成に追従。
    spec = _read("docs/architecture/01_仕様と設計.md")
    validation = _read("docs/runbook/04_検証.md")
    operations = _read("docs/runbook/05_運用.md")
    catalog = _read("docs/architecture/03_実装カタログ.md")
    claude_md = _read("CLAUDE.md")

    for required in (
        "## 1. 不変条件",
        "中核",  # 中核5要素 / 中核 5 要素 のどちらの表記でも拾う
        "ゴール劣化禁止",
        "## 10. Workflow Contract",
        "deploy-all -> run-all -> destroy-all",
        "canonical serving path",
        "destroy",  # destroy後再現性 / destroy 後再現性
        "## 11. 実装状態への参照",
    ):
        assert required in spec, (
            f"spec (01_仕様と設計) lost workflow contract requirement: {required}"
        )
    # 01 が薄くなった分、ADC-free /livez boot 契約はコード側 (test_local_boot_contract) と
    # CLAUDE.md / README が正本になっている。
    assert "/livez" in claude_md

    for required in (
        "G3 | **3 種コンポーネント (load-bearing)**",
        "G4 | **canonical semantic / feature path**",
        "make ops-vertex-vector-search-smoke",
        "scripts.ops.vertex.feature_group",
    ):
        assert required in validation, f"validation guide lost canonical gate: {required}"

    for required in (
        "## 1. PDCA メインフロー (`make deploy-all` → `make run-all` → `make destroy-all`)",
        "make run-all           # = run-all-core + リアルタイム監視 (ops-run-all-monitor)",
        "ops-vertex-vector-search-smoke",
        "ops-vertex-feature-group",
    ):
        assert required in operations, (
            f"operations guide drifted from workflow contract: {required}"
        )

    for required in (
        "tests/integration/workflow/",
        "tests/e2e/",
        "setup/deploy_all.py",
        "ops/vertex/{models_list,pipeline_status,vector_search,feature_group,monitoring,explain}.py",
    ):
        assert required in catalog, (
            f"implementation catalog (03_実装カタログ) drifted from workflow/test inventory: {required}"
        )


def test_composer_canonical_doc_section_exists() -> None:
    """Composer 本線 orchestration の宣言が docs に残っていること。

    01 は skeleton に縮約され「## 4. Composer 本線 orchestration」+ 「禁止事項」だけを残す。
    substantive な不変ルール (Vertex `PipelineJobSchedule` 完全撤去 = 二重起動禁止) は CLAUDE.md /
    TASKS_ROADMAP §3.4 が正本なので、そちらで pin する。
    """
    spec = _read("docs/architecture/01_仕様と設計.md")
    for required in ("## 4. Composer 本線 orchestration", "3 DAG", "禁止事項"):
        assert required in spec, (
            f"docs/01 §4 lost Composer 本線 orchestration section: {required!r}"
        )
    claude_md = _read("CLAUDE.md")
    roadmap = _read("docs/tasks/TASKS_ROADMAP.md")
    assert "完全撤去" in claude_md, (
        "CLAUDE.md must pin 'Vertex PipelineJobSchedule は完全撤去 (二重起動禁止)'"
    )
    assert "PipelineJobSchedule" in roadmap, (
        "TASKS_ROADMAP must pin the Composer = 上位 / Vertex Pipelines = 下位 / PipelineJobSchedule 併存禁止 rule"
    )


def test_cost_estimate_documented_in_runbook() -> None:
    """Stage 3 コスト見積もり (3h 学習 1 回想定) が runbook §1.4-bis に明記
    されていること — 過去の ¥9,000 padding ミス再発防止の contract。

    user authoritative wording (2026-05-02 終端) を pin: 3h cycle ¥870-1,200 +
    Composer なし時 ¥570-900 + 常駐系 vs 従量系の分解 + 当日 destroy 前提 +
    destroy 漏れリスク 24h / 1 週間 / 月放置。
    """
    runbook = _read("docs/runbook/05_運用.md")
    assert "### 1.4-bis Composer / canonical 構成 フル構成のコスト見積もり" in runbook
    assert "¥870-1,200" in runbook, (
        "runbook must pin canonical 構成 full 3h cycle cost as ~¥870-1,200 (user authoritative)"
    )
    assert "¥570-900" in runbook, (
        "runbook must document the without-Composer alt cost ~¥570-900 / 3h"
    )
    assert "常駐系" in runbook and "従量系" in runbook, (
        "runbook must split cost into 常駐系 vs 従量系"
    )
    assert "当日 destroy 前提" in runbook, (
        "runbook must explicitly state 'same-day destroy' contract"
    )
    assert "destroy 漏れリスク" in runbook, (
        "runbook must document destroy-leak risk (the real failure mode)"
    )
    for leak_marker in ("24h 放置", "1 週間放置", "月放置"):
        assert leak_marker in runbook, (
            f"runbook must enumerate destroy-leak scenarios including {leak_marker}"
        )
