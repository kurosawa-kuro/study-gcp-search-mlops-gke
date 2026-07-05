review_status: draft

id: decision_catalog_20260705T052739Z
domain: search+mlops
confidence: high
confidence_policy: capped_to_high (freshness=fresh, catalog_items=4, distinct_evidence_artifacts=34)
evidence_freshness: high
coverage_confidence: medium
meaning_quality: medium
high_end_ready: medium

# Decision Catalog (Draft)

fact_source: non_llm_scan
evidence_run_id: 20260705T052739Z_d14a7f69c9eb
machine_provenance: docs/catalog/evidence/evidence_index.jsonl

## scan_summary

### scan manifest / codebase footprint
- summary: スキャンは infra+python+web を対象に実行され、リポジトリには約 692 ファイル、3188 シンボル、888 件のテストが含まれる。プロジェクトは API、ML サービング、パイプライン、スクリプト、Terraform モジュールなど複数領域にまたがる。

### static signal counts
- summary: 静的シグナル集計では infra_surface や認証／シークレット関連のヒットが多数検出されている（infra_surface: 1620 hits, env_secret: 613 hits 等）。これは運用面で注意すべき領域が多いことを示す観察であり、検出は grep ベースの静的観察である。

### env / secret inventory
- summary: 環境変数参照が多数存在し、多くは redacted として検出されている。AIP_*、ELASTICSEARCH_*, REDIS_* 等が埋め込み／サービング／検索構成に利用される。

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
- 事実: リポジトリ内の FastAPI ルータとして /search を処理するモジュールが存在し、API ルーティング層から検索サービス層（search service）およびマッパーが呼び出される設計になっている。
- 意味あい:
  - 役割: パブリック検索 API のルータ／入口
  - 含意: このファイルは外部 HTTP リクエスト（検索クエリ）を受け取り、内部の検索サービスを呼び出す公開 API エンドポイント実装である。
  - 含意: 検索リクエストの受信から候補取得・ランク付け・レスポンス形成までのトラジェクトリの入口として機能しているため、リクエスト検証・トレース・ログ・呼び出し先の可用性が直接利用者体験に影響する。
  - 含意: テストコントラクト（unit/integration）やルータレベルの動作検証が多数存在することから、API 仕様の変更は広範なテスト影響を伴う可能性が高い（テスト数は scan manifest に記録されている）。
  - confidence: high

### app/services/adapters/kserve_encoder.py  {subject_kind: file}
- 事実: エンコーダ（埋め込み生成）に関するアダプタ実装がリポジトリに含まれており、KServe 経由でのモデル推論呼び出しや埋め込み検証機能が実装されている。
- 意味あい:
  - 役割: セマンティック検索用エンコーダアダプタ（KServe 経由）
  - 含意: 検索のセマンティック経路は埋め込みエンコーダを呼び出してクエリベクトルを生成することで機能しており、エンコーダ接続先の URL / ルート / ストレージ URI 等は環境変数で制御されることが証拠から分かる。
  - 含意: エンコーダの可用性・応答遅延・レスポンス検証は検索レイテンシと結果品質に直結するため、実行時構成（KServe endpoint, AIP_* 環境変数等）の管理が運用上重要である。
  - confidence: high

### scripts/setup/destroy_all.py  {subject_kind: file}
- 事実: デプロイ済みリソースを段階的に除去するためのスクリプト群（全体削除 / destroy_all 系ステップ）を含むスクリプト群が存在する。
- 意味あい:
  - 役割: インフラ破壊的操作を包含する運用スクリプト（destroy_all 系）
  - 含意: リポジトリには Terraform やクラウド操作を含む破壊的なライフサイクル操作を自動化するスクリプトが存在し、これらはインフラ面の大きな変更を引き起こす可能性がある。
  - 含意: 静的シグナル（high_risk_ops / infra_surface のヒット数）が多く検出されているため、これらスクリプトは運用面での扱いが慎重に行われる対象であることが示唆される（静的シグナルは観察結果であり、直接の実行証拠ではない）。
  - confidence: medium

### tests/ (test surface)  {subject_kind: test_surface}
- 事実: 多数のテストとテスト支援コードが含まれており、単体テスト、統合テスト、e2e テスト用の fixture や in-memory fakes が用意されている。
- 意味あい:
  - 役割: CI／デベロップメント向けの網羅的テスト基盤
  - 含意: テストスイート（合計 888 テスト）はコード変更時の回帰チェック手段を提供しており、API ルータやサービス、スクリプトの動作契約を維持するための自動化が整備されている。
  - 含意: テストに依存するリファクタや変更は、テスト群が期待する契約（入力／出力かたち）を満たす限り影響を検出しやすい。
  - confidence: high

## evidence_appendix

### スキャン制限（解析・grep の限界）
- summary: 本スキャンは行ベースのヒューリスティック抽出を使用しており、動的に生成されるシンボルやデコレータ登録されたルート、マクロ生成などは検出漏れがあり得る。grep の no‑hit は不存在の証明ではない。

### 環境変数／シークレット参照の範囲
- summary: 多数の環境変数（AIP_*, ELASTICSEARCH_URL, REDIS_* 等）参照が確認され、値は多くが redacted として検出されている。環境変数は実行時にシステム挙動を左右する構成ポイントになっている。

### 静的シグナル要約
- summary: 静的シグナル検出で infra_surface（1620 ヒット）、env_secret（613 ヒット）、high_risk_ops（602 ヒット）、auth_permission（759 ヒット）などが多数観測されている。これらはコード中の潜在的な運用・権限・秘密管理の注視点を示す観察である。

### プロジェクト構成スナップショット
- summary: リポジトリ全体のシンボル一覧とファイルツリーは豊富で、API 層、サービスアダプタ、ML サービング、パイプライン、スクリプト、Terraform モジュールなどマルチドメインで構成されている。
