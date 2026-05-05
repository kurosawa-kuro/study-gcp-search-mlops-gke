# Phase 7 ルート昇格 実行メモ

## 1. 今回の目的

- まずは **Phase 7 を repo ルートへ昇格**する
- **Meilisearch 廃止 / ECK / Elasticsearch 移行は今回やらない**
- ルート昇格後に、必要なら検索基盤の置換を別タスクとして扱う

---

## 2. 今回のスコープ

### やること

- `7/study-hybrid-search-gke/` を **canonical 実装**として扱う
- 親 repo ルートの README / CLAUDE / docs 導線を **Phase 7 起点**へ再定義する
- ルート直下の構成を、Phase 7 の構成に寄せる
- 旧 Phase 群 (`1/2/3/4/5/6/`) は **archive 扱い**へ寄せる
- CI / Makefile / import path / docs 内リンクを **ルート昇格後パス**へ合わせる

### やらないこと

- Meilisearch 廃止
- Elasticsearch / ECK 導入
- Vertex Vector Search の役割変更
- 検索アーキテクチャ自体の再設計
- ranking / rerank / event schema の意味変更

---

## 3. 完了条件

- repo ルートを開けば、**現役コードは Phase 7 相当**だと分かる
- ルート `README.md` が **Phase 7 canonical 起点**として読める
- ルート `CLAUDE.md` が **Phase 7 直結**の作業ガイドになる
- `make help` / `make verify-local-app` / `make verify-local-ml` などの **主要 local 導線**がルートまたは明確な入口から辿れる
- docs 内の「今触るべきコード」が **7/study-hybrid-search-gke** ではなく **昇格後の canonical path** を向く
- 旧 Phase は「現役コード」ではなく「archive / 学習履歴」として整理される

---

## 4. 実行方針

### 方針A: 段階移行

- いきなり物理移動せず、まず **論理的に Phase 7 を正本化**
- その後でファイル移動 / import path 変更を行う

### 方針B: Meili/ECK を切り離す

- 検索基盤の話を混ぜると差分が大きくなりすぎる
- 今回は **構造移行だけ**を独立 PR 群で進める

### 方針C: archive は削除より先に参照整理

- 旧 Phase はいきなり消さず、まず「現役でない」と分かる状態へ
- その後に archive branch / archive dir / docs/archive のどれで保全するか決める

---

## 5. PR シリーズ (今回対象)

### Wave 1: 正本宣言

- PR1: ルート `README.md` を「Phase 7 canonical 起点」へ書き換え
- PR2: ルート `CLAUDE.md` を「Phase 7 直結」前提へ整理
- PR3: ルート `docs/` の案内を「Phase 群の索引」から「Phase 7 正本 + archive 補助」へ変更

### Wave 2: 導線の正規化

- PR4: `7/study-hybrid-search-gke/docs/` 内で、canonical path 前提の docs 方針へ修正
- PR5: CI / Makefile / hook / script で `7/study-hybrid-search-gke` 前提になっている入口を洗い出す
- PR6: local 検証入口 (`verify-local-app` / `verify-local-ml` / `verify-local-hybrid`) を canonical 導線として固定

### Wave 3: 構造移行

- PR7: `7/study-hybrid-search-gke/` 配下を repo ルートへ移す具体手順を確定
- PR8: import path / relative path / workflow path / docs link を一括更新
- PR9: 旧 `7/study-hybrid-search-gke/` を archive or redirect 扱いへ

### Wave 4: 旧 Phase 整理

- PR10: `1/2/3/4/5/6/` を archive 扱いとして docs から明示
- PR11: root から現役入口を消し、archive 参照だけ残す

---

## 6. 実コードで先に調べるべき箇所

### load-bearing

- ルート [README.md](/home/ubuntu/repos/study-gcp-search-mlops-gke/README.md)
- ルート [CLAUDE.md](/home/ubuntu/repos/study-gcp-search-mlops-gke/CLAUDE.md)
- [7/study-hybrid-search-gke/README.md](/home/ubuntu/repos/study-gcp-search-mlops-gke/7/study-hybrid-search-gke/README.md)
- [7/study-hybrid-search-gke/CLAUDE.md](/home/ubuntu/repos/study-gcp-search-mlops-gke/7/study-hybrid-search-gke/CLAUDE.md)
- [7/study-hybrid-search-gke/Makefile](/home/ubuntu/repos/study-gcp-search-mlops-gke/7/study-hybrid-search-gke/Makefile)
- [7/study-hybrid-search-gke/.github/workflows](</home/ubuntu/repos/study-gcp-search-mlops-gke/7/study-hybrid-search-gke/.github/workflows>)

### path 変更の影響が大きい

- `scripts/` 配下の repo root 前提 path
- `pipeline/dags/` の参照 path
- `infra/terraform/**` の相対 path
- `docs/**` の内部リンク
- `.claude/hooks` / `.github/agents` / `.github/skills`

---

## 7. 今回の非スコープを明記

以下は **別タスク** として扱う:

- Meilisearch 廃止
- Elasticsearch adapter 実装
- ECK operator 導入
- ES snapshot / PVC retain 3層永続化
- KFP / Composer による ES index 更新

つまり、今回の問いは:

> 「検索基盤を何にするか」ではなく、  
> 「Phase 7 を repo の現役正本にするには何を動かすか」

に限定する。

---

## 8. いまの結論

- **Wave 1-2 の文書導線整理は先行着手済み**
- 具体的には、root `README.md` / `CLAUDE.md` / `docs/README.md` / `docs/{tasks,runbook,architecture,phases}/README.md` を
  **Phase 7 正本 + 旧 Phase 補助入口** の構図へ寄せた
- 追加で、root `AGENTS.md` / `docs/tasks/02_移行ロードマップ.md` / `docs/conventions/フォルダ-ファイル.md` /
  `tools/generate_makefile_md.sh` も Phase 7 正本前提へ同期した
- 次の主戦場は **Wave 3 の影響一覧固定と構造移行の実ファイル移動**
- Meilisearch 廃止は、この作業と混ぜない

---

## 9. Wave 3 影響一覧

### A. root 直下の入口

- `README.md`
- `CLAUDE.md`
- `AGENTS.md`
- `docs/README.md`

### B. root docs の canonical link 群

- `docs/architecture/01_仕様と設計.md`
- `docs/architecture/03_実装カタログ.md`
- `docs/runbook/04_検証.md`
- `docs/runbook/05_運用.md`
- `docs/tasks/02_移行ロードマップ.md`
- `docs/教育資料/02_移行ロードマップ.md`
- `docs/conventions/フォルダ-ファイル.md`

### C. 旧 Phase docs からの Phase 7 参照

- `2/**/docs/architecture/01_仕様と設計.md`
- `3/**/docs/tasks/TASKS.md`
- `3/**/docs/tasks/02_移行ロードマップ.md`
- `4/**/docs/architecture/01_仕様と設計.md`
- `4/**/docs/tasks/02_移行ロードマップ.md`
- `5/**/docs/architecture/01_仕様と設計.md`
- `5/**/docs/tasks/02_移行ロードマップ.md`
- `6/**/docs/architecture/01_仕様と設計.md`
- `6/**/docs/tasks/02_移行ロードマップ.md`

### D. root 補助ファイル

- `tools/generate_makefile_md.sh`
- `.claude/hooks/show-tasks.sh`
- `.claude/hooks/check-layers.sh`
- `.github/agents/gcp-mlops-theme-research.agent.md`
- `.github/skills/phase-doc-sync/SKILL.md`

### E. Phase 7 内で root 昇格時に崩れる絶対パス / 相対パス

- `7/study-hybrid-search-gke/docs/tasks/TASKS.md`
- `7/study-hybrid-search-gke/docs/runbook/05_運用.md`
- `7/study-hybrid-search-gke/tests/e2e/test_phase7_full_recreate_gate.py`
- `7/study-hybrid-search-gke/CLAUDE.md`

### F. workflow / CI / deploy path

- `7/study-hybrid-search-gke/.github/workflows/*.yml`
- `7/study-hybrid-search-gke/Makefile`
- `7/study-hybrid-search-gke/scripts/**`

### G. 物理移動時の優先順位

1. `README.md` / `CLAUDE.md` / `AGENTS.md`
2. root `docs/` ハブ
3. `7/study-hybrid-search-gke/.github/workflows`
4. `7/study-hybrid-search-gke/Makefile` / `scripts/` / `tests/`
5. 旧 Phase docs の canonical link 置換

---

## 10. 次アクション

1. root 昇格で壊れる path の inventory をこの文書で固定
2. `7/study-hybrid-search-gke` 内の絶対パス / `cd 7/study-hybrid-search-gke` 記述を洗う
3. workflow / Makefile / scripts の root 移動差分を先に機械的に出す
4. その後に物理移動 PR を切る
