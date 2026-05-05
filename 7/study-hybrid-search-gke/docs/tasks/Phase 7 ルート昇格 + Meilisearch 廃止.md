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

- **今すぐ着手すべきは Wave 1-2**
- 具体的には、まず **README / CLAUDE / docs の正本宣言** を先にやる
- その後に **構造移行の実ファイル移動** を行う
- Meilisearch 廃止は、この作業と混ぜない

---

## 9. 次アクション

1. ルート `README.md` / `CLAUDE.md` の Phase 7 正本化差分を作る
2. `7/study-hybrid-search-gke` の local 導線を canonical として宣言する
3. path 変更の影響一覧を docs に起こす
4. その後に物理移動 PR を切る
