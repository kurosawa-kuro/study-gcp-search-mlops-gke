# Phase 7 ルート昇格 + Meilisearch 廃止 + Elasticsearch on GKE 移行 整理

---

## 1. 全体方針

- チーム内教育資料の作成は完了したので、今後はphaseが不要。
- 個人技術検証プラットフォームとして再定義、Phase 構造を解体
- Phase 7 を repo ルートに昇格、canonical 起点とする
- Phase 1/2/3/4/6 は archive ブランチに退避、main から削除
- Phase 6 は `docs/pmle-prep/` に移植、論理 Phase 概念を解体
- 検索基盤を Meilisearch から Elasticsearch on ECK に全面移行
- `experiments/` 領域を新設、新技術検証は Phase 設計議論なしで開始可能に

---

## 2. ディレクトリ構造(移行後)

- ルート直下が現役構成、Phase 番号なし
- `ml/` がコード本体(embed / train / serve / sync)
- `pipeline/` が Vertex AI Pipelines + Composer DAG
- `terraform/stacks/` 配下に永続化レイヤごとのスタック
  - `persistent/`: GCS embedding archive(prevent_destroy)
  - `vector_search/`: Vertex Vector Search Index + Endpoint(prevent_destroy)
  - `elasticsearch/`: ECK Operator + Elasticsearch cluster(新規)
  - `core/`: Composer / GKE / Cloud Run / セッション都度破棄
- `experiments/` で新技術検証(Ray / vLLM / Kubeflow standalone 等)
- `docs/pmle-prep/` で PMLE 学習ドキュメント
- `archive/README.md` で archive ブランチへの参照のみ残す

---

## 3. Meilisearch 廃止の理由

- Phase 3-4 が archive 退避対象となり、Meili のメンテ動機が消滅
- Phase 7(=ルート昇格対象)は元々 Meili + ES 並存を計画していたが、Meili を残す合理性が消える
- ES が BM25 + dense_vector を1サービスで完結、Meili+別ベクトルストアより構成シンプル
- 業界標準 ES 経験のほうが転職アピール価値が高い
- BM25 スコア透明性(`explain=true`)で学習価値も高い
- 日本語処理は kuromoji analyzer で対応可能

---

## 4. Elasticsearch on GKE 採用の理由

- Cloud Run は構造的に不可(エフェメラルストレージ・スケールゼロ)
- GKE は Phase 7 で既に KServe 用に導入済み、追加学習コストほぼゼロ
- ECK Operator で Elasticsearch クラスタを宣言的に管理可能
- 転職アピール観点で「k8s Operator 経験」として ECK + KServe の2つを押さえられる
- セッション都度起動・終了のコスト最適化が GKE 上で実現可能

---

## 5. ES と Vertex Vector Search の役割分担

- Elasticsearch on ECK: lexical search(BM25)担当
- Vertex Vector Search: semantic search(dense vector)担当
- 統合: RRF または weighted score でハイブリッド
- LightGBM reranker(KServe)で最終ランキング
- 「マネージドベクトル検索 + セルフホスト全文検索」という実務頻出パターン

---

## 6. 3層永続化アーキテクチャ(ES側にも転用)

- Layer 1: GCS snapshot repository(prevent_destroy、無料)
  - ES snapshot を `gs://...es-snapshots/` に保存
- Layer 2: GKE PVC retain policy(永続・低コスト)
  - Pod 削除されても PV 残存、再起動時に即マウント
- Layer 3: ES Pod 本体 + Service(セッション都度起動・破棄)
  - 検証終了で `kubectl delete` で破棄
- Vertex Vector Search の3層思想を ES にも適用、コスト構造を統一

---

## 7. 移行 PR シリーズ(順序)

- PR1: archive ブランチ作成、phase1/2/3/4/6 を archive 側に保全
- PR2: main から phase1/2/3/4/6 ディレクトリ削除
- PR3: phase7/ をルートにフラット化(ml/ pipeline/ terraform/)
- PR4: docs/pmle-prep/ 作成(phase5/ から移植)
- PR5: phase5/ 削除
- PR6: README 全面書き換え(個人検証プラットフォームとして再定義)
- PR7: experiments/ ディレクトリ初期化
- PR8: Makefile / CI / import path 修正
- PR9: docs/conventions.md 作成(命名規則ロック)
- PR10: 3層永続化アーキテクチャ実装(Vertex Vector Search 側、5PR相当を統合)
- PR11: ECK Operator 導入(Helm / Terraform)
- PR12: Elasticsearch cluster manifest(PVC + GCS snapshot)
- PR13: ElasticsearchAdapter 実装(BM25 + kNN + ハイブリッド)
- PR14: Meilisearch adapter / docker-compose 削除
- PR15: KFP コンポーネントで multilingual-e5 embedding を ES に投入
- PR16: Composer DAG に ES index 更新ステップを統合
- PR17: A/B 評価パイプライン(NDCG@10 / Recall@K)で ES 単独構成を検証

---

## 8. 残るメンテ対象

- `ml/`(embed / train / serve / sync)
- `pipeline/`(Vertex AI Pipelines + Composer DAG)
- `terraform/stacks/`(persistent / vector_search / elasticsearch / core)
- `docs/pmle-prep/`(PMLE 学習)
- `experiments/`(新技術検証、自由領域)

---

## 9. archive 退避対象

- phase1/(ML基礎)
- phase2/(App / Pipeline / Port-Adapter)
- phase3/(Local ハイブリッド検索 + Meili)
- phase4/(GCP ログ基盤)
- phase6/(PMLE 論理学習)
- 退避先: archive ブランチ、main からは削除
- archive ブランチは凍結、commit しない方針

---

## 10. 転職アピール時の語り口

- 「Vertex AI + ECK on GKE + KServe による商品検索向けハイブリッド検索基盤」
- 「Vertex Vector Search(dense)+ Elasticsearch on ECK(lexical/BM25)+ KServe(reranker)」
- 「ECK Operator + GCS snapshot + PVC retain で 3層永続化、セッション都度起動でコスト最適化」
- 「KFP v2 SDK でパイプライン記述、Vertex AI Pipelines マネージド実行」
- 「k8s Operator 経験: KServe + ECK」
- 「`experiments/` で新技術検証(Ray / vLLM / Kubeflow standalone 等)を継続」

---

## 11. 着手順序の推奨

- 第1優先: 構造移行(PR1-9)、フラット化と archive 退避
- 第2優先: 3層永続化アーキテクチャ(PR10)、Vertex Vector Search のコスト最適化
- 第3優先: ECK + Elasticsearch 統合(PR11-17)、Meili 削除
- 第4優先: `experiments/` で次の検証(KubeRay / vLLM / Kubeflow standalone)

---

## 12. 注意点

- archive ブランチは作成後 commit しない、ブランチ保護を設定
- import path 変更で CI が一時的に壊れる、PR3 と PR8 を同一 PR にまとめる選択肢あり
- README 書き換え(PR6)を**最終段階で実施**、移行途中の状態を反映しない
- ECK 導入時、GKE Autopilot のリソース上限(Composer worker / KServe / ES の同居)を事前見積もり
- Elasticsearch 8.x は security デフォルト ON、ECK では証明書自動発行されるため明示的な無効化は不要