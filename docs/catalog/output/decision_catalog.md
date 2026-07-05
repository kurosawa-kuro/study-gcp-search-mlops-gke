review_status: adopted
id: decision_catalog_20260705T052739Z
domain: search+mlops
confidence: high

# Decision Catalog

fact_source: non_llm_scan
evidence_run_id: 20260705T052739Z_d14a7f69c9eb
machine_provenance: docs/catalog/evidence/evidence_index.jsonl

purpose: upper_model_input
catalog_id: decision_catalog_20260705T052739Z
domain: search+mlops
high_end_ready: medium

## repo_topology

- kind: software_project
- core_files:
- runtime_surfaces:
  - CLI arguments
- data_surfaces:
  - repo object state surfaces

## coverage_map

- scan_included_files: 692
- topology_files: 0
- catalog_core_items: 4
- covered_as_core:
  - app/api/routers/search_router.py
  - app/services/adapters/kserve_encoder.py
  - scripts/setup/destroy_all.py
- covered_as_appendix:
  - tests/ (test surface)
- omitted_or_low_signal:
  - reason: generated/vendor/test fixture/low-signal or scan metadata only

## scan_summary

- profile: infra+python+web
- profile_resolution: requested=auto detected=css,html,infra,node,python,typescript profiles_run=infra+python+web language=infra+python+web
- scan_included_files: 692
- symbols: 3188
- entrypoints: 92
- tests_detected: 888
- high_risk_ops_hits: 2
- no_hit_is_not_absence: true

## flow_items

### Observed Primary Flow Candidate: search request lifecycle  {subject_kind: evidence_inferred_flow}
- id: primary_task_lifecycle_candidate
- flow_type: primary_candidate
- grounding_level: medium
- basis:
  - app/api/routers/search_router.py
  - app/services/search_service.py
  - app/services/adapters/kserve_encoder.py
  - app/services/adapters/bigquery_candidate_retriever.py
  - app/api/mappers/search_mapper.py
- steps:
  - order: 1
    user_intent: ユーザはクエリを送信して関連結果を取得したい
    surface: candidate HTTP search API (e.g., /search) reception
    components: app/api/routers/search_router.py
    data_effect: 外部検索リクエスト（HTTP）を受け取りパースする。トレース / リクエストID を付与し、内部検索処理に委譲する入力が生成される。
    confidence: strong
  - order: 2
    user_intent: 受け取ったクエリを基に候補探索を実行したい
    surface: internal search service invocation (synchronous)
    components: app/services/search_service.py, app/api/mappers/search_mapper.py
    data_effect: 検索条件を内部入力（filters/flags/top_k 等）へ変換し、候補取得と後続のランク付け処理呼び出しを行う。候補プールが生成される。
    confidence: medium
  - order: 3
    user_intent: 関連コンテンツを外部データストア／ベクトル検索に照会したい
    surface: candidate retrieval calls to external adapters
    components: app/services/adapters/bigquery_candidate_retriever.py, app/services/adapters/vertex_vector_search_semantic_search.py, app/services/adapters/redis_synonym_expander.py
    data_effect: レキシカル／セマンティックの候補取得を外部サービス（BigQuery, Vertex AI, Redis）に問い合わせ、候補の集合が補強される。
    confidence: medium
  - order: 4
    user_intent: クエリの意味表現を数値化して類似検索に使いたい
    surface: candidate encoder inference (via KServe adapter)
    components: app/services/adapters/kserve_encoder.py
    data_effect: クエリ文を埋め込みベクトルへ変換するためのエンコーダ呼び出しが行われる（KServe経由）。生成されたベクトルはセマンティック検索や reranker に渡される。
    confidence: medium
  - order: 5
    user_intent: 最適だと判断される順序で結果を提示したい
    surface: candidate rerank and ranking-log publishing
    components: app/services/adapters/kserve_reranker.py, app/services/ranking.py, app/services/adapters/pubsub_ranking_log_publisher.py
    data_effect: 候補プールに対して再ランク（reranker）が実行され、最終結果が決定される。ランキングログやインプレッションイベントが発行される（ログ／PubSub など）。
    confidence: medium
  - order: 6
    user_intent: 検索結果を受け取り可視化／利用したい
    surface: HTTP response formation and send
    components: app/api/mappers/search_mapper.py, app/api/routers/search_router.py
    data_effect: 最終検索結果をレスポンススキーマへマッピングし、HTTP レスポンスとしてクライアントへ返す。リクエスト ID / トレース情報を含む場合がある。
    confidence: strong
- cannot_conclude:
  - HTTP リクエスト -> サービス呼び出しの厳密な内部順序やエラーハンドリングの全ケースは静的シンボルのみでは完全に確定できない（動的ルーティングやデコレータ登録の可能性を含む）。
  - エンドユーザに公開される正確なエンドポイントパスやクエリパラメータのバリデーション要件は、サンプル実行や追加のコード読解を経ないと断定できない。

### Observed Destructive Flow Candidate: infra destroy / cleanup lifecycle  {subject_kind: evidence_inferred_flow}
- id: destructive_management_candidate
- flow_type: destructive_surface_candidate
- grounding_level: medium
- basis:
  - scripts/setup/destroy_all.py
- steps:
  - order: 1
    user_intent: テスト環境やデプロイ済リソースを一括で削除したい（クリア／破棄）
    surface: candidate destructive operation (scripts/setup/destroy_all entrypoint)
    components: scripts/setup/destroy_all.py
    data_effect: 破壊的操作の開始（destroy_all 系スクリプトの実行により、Terraform destroy、GCS バケットワイプ、Vertex endpoint の undeploy 等の一連操作を順次呼び出す）を示唆するコマンドがトリガされる可能性がある。
    confidence: medium
  - order: 2
    user_intent: 残存リソースやステートの整合性を回復しつつ削除を完了したい
    surface: candidate orchestration of multi-step infra cleanup
    components: scripts/domain/gcp/state_recovery.py, scripts/domain/gcp/vertex_cleanup.py, scripts/setup/destroy_all.py
    data_effect: 状態回復・未処理リソースのクリーンアップ・アンデプロイ作業が想定される。スクリプト内で複数の外部操作（gcloud, kubectl, terraform 等）を呼び出す可能性がある。
    confidence: weak
- cannot_conclude:
  - スクリプトの CLI 露出（どのコマンド名で実行されるか）、および用いる Terraform ワークスペースや実行パラメータの完全な一覧は、静的シンボル一覧だけでは確定できない（実行時パラメータや外部設定の変化を含む）。
  - このフローがリポジトリに存在することは確認できるが、実行が実際のクラウドリソースに対して即座に変化を与えた履歴までは静的証拠からは判定できない。

## catalog_items

### app/api/routers/search_router.py  {subject_kind: file}
- role: パブリック検索 API のルータ／入口
- implications:
  - このファイルは外部 HTTP リクエスト（検索クエリ）を受け取り、内部の検索サービスを呼び出す公開 API エンドポイント実装である。
  - 検索リクエストの受信から候補取得・ランク付け・レスポンス形成までのトラジェクトリの入口として機能しているため、リクエスト検証・トレース・ログ・呼び出し先の可用性が直接利用者体験に影響する。

### app/services/adapters/kserve_encoder.py  {subject_kind: file}
- role: セマンティック検索用エンコーダアダプタ（KServe 経由）
- implications:
  - 検索のセマンティック経路は埋め込みエンコーダを呼び出してクエリベクトルを生成することで機能しており、エンコーダ接続先の URL / ルート / ストレージ URI 等は環境変数で制御されることが証拠から分かる。
  - エンコーダの可用性・応答遅延・レスポンス検証は検索レイテンシと結果品質に直結するため、実行時構成（KServe endpoint, AIP_* 環境変数等）の管理が運用上重要である。

### scripts/setup/destroy_all.py  {subject_kind: file}
- role: インフラ破壊的操作を包含する運用スクリプト（destroy_all 系）
- implications:
  - リポジトリには Terraform やクラウド操作を含む破壊的なライフサイクル操作を自動化するスクリプトが存在し、これらはインフラ面の大きな変更を引き起こす可能性がある。
  - 静的シグナル（high_risk_ops / infra_surface のヒット数）が多く検出されているため、これらスクリプトは運用面での扱いが慎重に行われる対象であることが示唆される（静的シグナルは観察結果であり、直接の実行証拠ではない）。

### tests/ (test surface)  {subject_kind: test_surface}
- role: CI／デベロップメント向けの網羅的テスト基盤
- implications:
  - テストスイート（合計 888 テスト）はコード変更時の回帰チェック手段を提供しており、API ルータやサービス、スクリプトの動作契約を維持するための自動化が整備されている。
  - テストに依存するリファクタや変更は、テスト群が期待する契約（入力／出力かたち）を満たす限り影響を検出しやすい。

## evidence_appendix

- pointer: docs/catalog/evidence/evidence_index.jsonl
- pointer: docs/catalog/evidence/current_run_id
