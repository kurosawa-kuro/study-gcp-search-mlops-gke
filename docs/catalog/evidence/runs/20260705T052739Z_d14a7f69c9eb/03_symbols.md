# Symbols

## .github/workflows/ci.yml

- L4: ci-job `pull_request`
- L6: ci-job `push`
- L8: ci-job `workflow_dispatch`
- L14: ci-job `lint-typecheck-test`
- L16: ci-job `strategy`
- L18: ci-job `matrix`
- L38: ci-job `dataform-check`

## .github/workflows/deploy-api.yml

- L4: ci-job `push`
- L6: ci-job `paths`
- L14: ci-job `workflow_dispatch`
- L28: ci-job `build-and-deploy`

## .github/workflows/deploy-dataform.yml

- L4: ci-job `push`
- L6: ci-job `paths`
- L10: ci-job `workflow_dispatch`
- L22: ci-job `push-definitions`

## .github/workflows/deploy-encoder-image.yml

- L9: ci-job `push`
- L11: ci-job `paths`
- L20: ci-job `workflow_dispatch`
- L33: ci-job `build-and-push`

## .github/workflows/deploy-pipeline.yml

- L13: ci-job `push`
- L15: ci-job `paths`
- L27: ci-job `workflow_dispatch`
- L39: ci-job `compile-and-upload`

## .github/workflows/deploy-reranker-image.yml

- L9: ci-job `push`
- L11: ci-job `paths`
- L20: ci-job `workflow_dispatch`
- L33: ci-job `build-and-push`

## .github/workflows/deploy-trainer-image.yml

- L8: ci-job `push`
- L10: ci-job `paths`
- L21: ci-job `workflow_dispatch`
- L34: ci-job `build-and-push`

## .github/workflows/terraform.yml

- L4: ci-job `pull_request`
- L7: ci-job `push`
- L10: ci-job `workflow_dispatch`
- L23: ci-job `plan`
- L79: ci-job `apply`

## app/api/dependencies.py

- L22: function `get_container`
- L34: function `get_search_service`
- L40: function `get_feedback_service`
- L46: function `get_request_id`

## app/api/mappers/search_mapper.py

- L25: function `_filters_from_pydantic`
- L49: function `search_request_to_input`
- L62: function `search_result_item_to_schema`
- L84: function `to_search_response`

## app/api/middleware/request_logging.py

- L20: function `_extract_trace`
- L33: class `RequestLoggingMiddleware`
- L34: method `__init__` parent=RequestLoggingMiddleware
- L38: method `dispatch` parent=RequestLoggingMiddleware (async)

## app/api/routers/admin_mlops_router.py

- L45: function `admin_mlops`
- L72: function `_collect_event_counts`
- L100: function `_collect_latest_dataset`
- L115: function `_collect_latest_metrics`

## app/api/routers/feedback_router.py

- L17: function `feedback`

## app/api/routers/health_router.py

- L18: function `healthz`
- L23: function `readyz`

## app/api/routers/model_router.py

- L30: function `model_metrics`
- L64: function `model_info`
- L77: function `model_data`

## app/api/routers/ops_router.py

- L30: function `_run_bq_query`
- L54: function `destroy_check`
- L92: function `search_volume`
- L108: function `runs_recent`
- L130: function `_as_int`
- L146: function `_as_float`

## app/api/routers/retrain_router.py

- L30: function `check_retrain`

## app/api/routers/search_router.py

- L19: function `search`

## app/api/routers/ui_router.py

- L19: function `build_ui_router`
- L24: function `ui_home`
- L38: function `ui_search_dev`
- L52: function `ui_model_metrics`
- L60: function `ui_data`
- L68: function `ui_ops`
- L76: function `ui_api_docs`
- L80: function `ui_property_detail`

## app/composition_root.py

- L50: class `Container`
- L105: class `ContainerBuilder`
- L114: method `__init__` parent=ContainerBuilder
- L129: method `_bigquery` parent=ContainerBuilder
- L148: method `build` parent=ContainerBuilder
- L221: method `_build_retrain_publisher` parent=ContainerBuilder
- L224: method `_build_ranking_log_publisher` parent=ContainerBuilder
- L227: method `_build_feedback_recorder` parent=ContainerBuilder
- L230: method `_build_data_catalog_reader` parent=ContainerBuilder
- L233: method `_build_candidate_retriever` parent=ContainerBuilder
- L240: method `_build_encoder_client` parent=ContainerBuilder
- L243: method `_build_reranker_client` parent=ContainerBuilder
- L246: method `_build_popularity_scorer` parent=ContainerBuilder

## app/container/infra.py

- L58: class `InfraBuilderContext`
- L61: method `_bigquery` parent=InfraBuilderContext
- L65: class `InfraComponents`
- L80: class `InfraBuilder`
- L81: method `__init__` parent=InfraBuilder
- L85: method `_settings` parent=InfraBuilder
- L88: method `build` parent=InfraBuilder
- L167: method `build_metrics_repository` parent=InfraBuilder
- L175: method `build_training_dataset_repository` parent=InfraBuilder
- L199: method `build_retrain_publisher` parent=InfraBuilder
- L208: method `build_ranking_log_publisher` parent=InfraBuilder
- L220: method `build_feedback_recorder` parent=InfraBuilder
- L232: method `build_event_writer` parent=InfraBuilder
- L257: method `build_synonym_expander` parent=InfraBuilder

## app/container/internal/optional_adapter.py

- L23: function `resolve_optional_adapter`

## app/container/ml.py

- L17: class `MlBuilderContext`
- L21: method `_bigquery` parent=MlBuilderContext
- L25: class `MlComponents`
- L29: class `MlBuilder`
- L30: method `__init__` parent=MlBuilder
- L34: method `_settings` parent=MlBuilder
- L38: method `_logger` parent=MlBuilder
- L41: method `build` parent=MlBuilder
- L46: method `build_popularity_scorer` parent=MlBuilder
- L61: method `_factory` parent=MlBuilder

## app/container/search.py

- L37: function `_resolve_index_endpoint_name`
- L44: class `SearchBuilderContext`
- L48: method `_bigquery` parent=SearchBuilderContext
- L52: class `SearchComponents`
- L60: class `SearchBuilder`
- L66: method `__init__` parent=SearchBuilder
- L70: method `_settings` parent=SearchBuilder
- L74: method `_logger` parent=SearchBuilder
- L77: method `build` parent=SearchBuilder
- L95: method `build_candidate_retriever` parent=SearchBuilder
- L125: method `resolve_feature_fetcher` parent=SearchBuilder
- L160: method `_build_vertex_vector_search` parent=SearchBuilder
- L197: method `_resolve_lexical_search` parent=SearchBuilder
- L221: method `build_encoder_client` parent=SearchBuilder
- L253: method `build_reranker_client` parent=SearchBuilder

## app/domain/candidate.py

- L21: class `Candidate`
- L41: class `RankedCandidate`

## app/domain/event.py

- L17: class `SearchEvent`
- L29: class `Impression`
- L43: class `UserAction`

## app/domain/labeling.py

- L8: class `RankingLabel`

## app/domain/retrieval.py

- L8: class `LexicalResult`
- L13: class `SemanticResult`

## app/domain/search.py

- L20: class `SearchFilters`
- L39: class `SearchInput`
- L49: class `SearchResultItem`
- L85: class `SearchOutput`

## app/domain/training.py

- L10: class `TrainingDatasetRef`
- L26: class `EvaluationMetric`

## app/main.py

- L74: function `_build_legacy_redirects`
- L80: function `_redirect` (async)
- L97: function `create_app`
- L104: function `lifespan` (async)
- L143: function `_root_redirect`

## app/observability.py

- L57: class `Observability`
- L68: method `from_env` parent=Observability
- L75: method `for_test` parent=Observability
- L85: method `get_logger` parent=Observability
- L88: method `expose_prometheus` parent=Observability
- L108: method `_build_tracker` parent=Observability
- L111: method `_record` parent=Observability

## app/schemas/admin_mlops.py

- L10: class `MetricSnapshot`
- L20: class `TrainingDatasetSnapshot`
- L27: class `EventCounts`
- L36: class `AdminMlopsResponse`

## app/schemas/model.py

- L13: class `CaseMetric`
- L24: class `AccuracySummary`
- L30: class `ModelMetricsResponse`
- L38: class `ModelInfoResponse`
- L55: class `DataPreviewTable`
- L65: class `ModelDataResponse`

## app/schemas/ops.py

- L8: class `DestroyCheckFindingResponse`
- L15: class `DestroyCheckSummaryResponse`
- L23: class `DestroyCheckResponse`
- L31: class `SearchVolumeResponse`
- L37: class `TrainingRunSummaryResponse`
- L46: class `RecentTrainingRunsResponse`

## app/schemas/search.py

- L15: class `SearchFilters`
- L23: class `SearchRequest`
- L29: class `SearchResultItem`
- L61: class `SearchResponse`
- L67: class `FeedbackRequest`
- L79: class `FeedbackResponse`

## app/services/adapters/bigquery_candidate_retriever.py

- L24: class `BigQueryCandidateRetriever`
- L41: method `__init__` parent=BigQueryCandidateRetriever
- L59: method `retrieve` parent=BigQueryCandidateRetriever
- L97: method `_enrich_from_bq` parent=BigQueryCandidateRetriever

## app/services/adapters/bigquery_data_catalog_reader.py

- L17: class `BigQueryDataCatalogReader`
- L18: method `__init__` parent=BigQueryDataCatalogReader
- L39: method `read_snapshot` parent=BigQueryDataCatalogReader
- L52: method `_properties_preview` parent=BigQueryDataCatalogReader
- L92: method `_features_preview` parent=BigQueryDataCatalogReader
- L134: method `_ranking_log_preview` parent=BigQueryDataCatalogReader
- L175: method `_embeddings_preview` parent=BigQueryDataCatalogReader
- L208: method `_training_runs_preview` parent=BigQueryDataCatalogReader
- L247: method `_user_actions_preview` parent=BigQueryDataCatalogReader
- L280: method `_ranking_labels_preview` parent=BigQueryDataCatalogReader
- L313: method `_scalar` parent=BigQueryDataCatalogReader
- L320: method `_query` parent=BigQueryDataCatalogReader
- L327: method `_row_to_dict` parent=BigQueryDataCatalogReader
- L337: method `_jsonish` parent=BigQueryDataCatalogReader

## app/services/adapters/bigquery_event_repository.py

- L14: class `BigQueryEventRepository`
- L15: method `__init__` parent=BigQueryEventRepository
- L29: method `read_search_events` parent=BigQueryEventRepository
- L59: method `read_impressions` parent=BigQueryEventRepository
- L105: method `read_user_actions` parent=BigQueryEventRepository
- L146: method `_query` parent=BigQueryEventRepository
- L162: function `_where_clause`
- L169: function `_scalar_params`
- L185: function `_optional_str`
- L189: function `_optional_int`
- L193: function `_optional_float`
- L197: function `_json_text`

## app/services/adapters/bigquery_label_repository.py

- L13: class `BigQueryLabelRepository`
- L14: method `__init__` parent=BigQueryLabelRepository
- L24: method `write_ranking_labels` parent=BigQueryLabelRepository
- L82: method `read_ranking_labels` parent=BigQueryLabelRepository

## app/services/adapters/bigquery_metrics_repository.py

- L14: class `BigQueryMetricsRepository`
- L23: method `__init__` parent=BigQueryMetricsRepository
- L33: method `write_evaluation_metrics` parent=BigQueryMetricsRepository
- L63: method `read_evaluation_metrics` parent=BigQueryMetricsRepository
- L120: method `latest_metrics` parent=BigQueryMetricsRepository

## app/services/adapters/bqml_popularity_scorer.py

- L26: class `BQMLPopularityScorer`
- L41: method `__init__` parent=BQMLPopularityScorer
- L56: method `score` parent=BQMLPopularityScorer

## app/services/adapters/cloud_logging_event_writer.py

- L21: class `CloudLoggingEventWriter`
- L22: method `emit_search_event` parent=CloudLoggingEventWriter
- L46: method `emit_impression` parent=CloudLoggingEventWriter
- L74: method `emit_user_action` parent=CloudLoggingEventWriter
- L92: method `_emit` parent=CloudLoggingEventWriter
- L100: method `_parse_json` parent=CloudLoggingEventWriter

## app/services/adapters/elasticsearch_lexical.py

- L15: class `ElasticsearchLexical`
- L18: method `__init__` parent=ElasticsearchLexical
- L38: method `_headers` parent=ElasticsearchLexical
- L44: method `search` parent=ElasticsearchLexical
- L100: function `_filters_to_es`

## app/services/adapters/feature_online_store_fetcher.py

- L31: class `FeatureOnlineStoreFetcher`
- L47: method `__init__` parent=FeatureOnlineStoreFetcher
- L64: method `_resolve_client` parent=FeatureOnlineStoreFetcher
- L94: method `_resolve_canonical_feature_view` parent=FeatureOnlineStoreFetcher
- L107: method `fetch` parent=FeatureOnlineStoreFetcher
- L124: method `_build_request` parent=FeatureOnlineStoreFetcher
- L140: function `_resource_part`
- L151: function `_row_from_response`
- L174: function `_safe_features`
- L181: function `_coerce_float`

## app/services/adapters/gcs_training_dataset_repository.py

- L27: class `GcsTrainingDatasetRepository`
- L28: method `__init__` parent=GcsTrainingDatasetRepository
- L41: method `_manifest_path` parent=GcsTrainingDatasetRepository
- L44: method `write_training_dataset` parent=GcsTrainingDatasetRepository
- L64: method `read_training_dataset` parent=GcsTrainingDatasetRepository
- L71: method `latest_training_dataset` parent=GcsTrainingDatasetRepository
- L75: method `_read_manifest` parent=GcsTrainingDatasetRepository

## app/services/adapters/internal/kserve_common.py

- L27: function `safe_json`
- L60: function `log_http_error_response`
- L88: function `is_v2_inference_url`
- L92: function `coerce_float_list`
- L98: function `response_summary`
- L110: function `extract_predictions`

## app/services/adapters/internal/pubsub_diagnostics.py

- L24: function `runtime_sa_hint`
- L34: function `log_publish_failure`
- L87: function `as_float`

## app/services/adapters/kserve_encoder.py

- L38: class `KServeEncoder`
- L41: method `__init__` parent=KServeEncoder
- L67: method `embed` parent=KServeEncoder
- L146: method `_validate_embedding` parent=KServeEncoder

## app/services/adapters/kserve_reranker.py

- L40: function `_extract_attributions`
- L99: class `KServeReranker`
- L107: method `__init__` parent=KServeReranker
- L137: method `predict` parent=KServeReranker
- L228: method `predict_with_explain` parent=KServeReranker
- L354: method `_coerce_score` parent=KServeReranker

## app/services/adapters/publisher.py

- L14: class `PubSubPublisher`
- L17: method `__init__` parent=PubSubPublisher
- L29: method `publish` parent=PubSubPublisher

## app/services/adapters/pubsub_event_writer.py

- L31: class `PubSubEventWriter`
- L34: method `__init__` parent=PubSubEventWriter
- L60: method `emit_search_event` parent=PubSubEventWriter
- L84: method `emit_impression` parent=PubSubEventWriter
- L112: method `emit_user_action` parent=PubSubEventWriter
- L130: method `_publish` parent=PubSubEventWriter
- L143: function `_now_iso`

## app/services/adapters/pubsub_feedback_recorder.py

- L15: class `PubSubFeedbackRecorder`
- L18: method `__init__` parent=PubSubFeedbackRecorder
- L30: method `record` parent=PubSubFeedbackRecorder

## app/services/adapters/pubsub_ranking_log_publisher.py

- L21: class `PubSubRankingLogPublisher`
- L24: method `__init__` parent=PubSubRankingLogPublisher
- L36: method `publish_candidates` parent=PubSubRankingLogPublisher

## app/services/adapters/redis_synonym_expander.py

- L33: class `RedisSynonymExpander`
- L44: method `__init__` parent=RedisSynonymExpander
- L55: method `expand` parent=RedisSynonymExpander
- L65: method `_expand_tokens` parent=RedisSynonymExpander
- L82: function `_decode`

## app/services/adapters/retrain.py

- L14: class `BigQueryRetrainQueries`
- L17: method `__init__` parent=BigQueryRetrainQueries
- L26: method `last_run_finished_at` parent=BigQueryRetrainQueries
- L35: method `feedback_rows_since` parent=BigQueryRetrainQueries
- L59: method `ndcg_in_window` parent=BigQueryRetrainQueries
- L81: function `create_retrain_queries`

## app/services/adapters/vertex_vector_search_semantic_search.py

- L38: class `VertexVectorSearchSemanticSearch`
- L59: method `__init__` parent=VertexVectorSearchSemanticSearch
- L83: method `_resolve_endpoint` parent=VertexVectorSearchSemanticSearch
- L97: method `search` parent=VertexVectorSearchSemanticSearch

## app/services/data_catalog_service.py

- L8: class `DataCatalogService`
- L9: method `__init__` parent=DataCatalogService
- L12: method `read_snapshot` parent=DataCatalogService

## app/services/feedback_service.py

- L21: class `FeedbackService`
- L22: method `__init__` parent=FeedbackService
- L31: method `record` parent=FeedbackService

## app/services/model_metrics_service.py

- L26: class `EvalCase`
- L37: class `CaseReport`
- L49: class `AccuracyReport`
- L59: function `load_cases`
- L96: function `_coerce_filters`
- L97: function `_as_int`
- L118: function `_dcg_binary`
- L122: function `_ndcg_at_k`
- L128: function `_hit_rate_at_k`
- L132: function `_mrr_at_k`
- L139: function `default_cases_path`
- L144: class `ModelMetricsService`
- L152: method `__init__` parent=ModelMetricsService
- L156: method `evaluate` parent=ModelMetricsService

## app/services/noop_adapters/noop_data_catalog_reader.py

- L8: class `NoopDataCatalogReader`
- L9: method `read_snapshot` parent=NoopDataCatalogReader

## app/services/noop_adapters/noop_event_repository.py

- L9: class `NoopEventRepository`
- L10: method `read_search_events` parent=NoopEventRepository
- L13: method `read_impressions` parent=NoopEventRepository
- L21: method `read_user_actions` parent=NoopEventRepository

## app/services/noop_adapters/noop_event_writer.py

- L7: class `NoopEventWriter`
- L8: method `emit_search_event` parent=NoopEventWriter
- L21: method `emit_impression` parent=NoopEventWriter
- L36: method `emit_user_action` parent=NoopEventWriter

## app/services/noop_adapters/noop_feedback_recorder.py

- L13: class `NoopFeedbackRecorder`
- L14: method `record` parent=NoopFeedbackRecorder

## app/services/noop_adapters/noop_label_repository.py

- L9: class `NoopLabelRepository`
- L10: method `write_ranking_labels` parent=NoopLabelRepository
- L13: method `read_ranking_labels` parent=NoopLabelRepository

## app/services/noop_adapters/noop_lexical_search.py

- L15: class `NoopLexicalSearch`
- L16: method `search` parent=NoopLexicalSearch

## app/services/noop_adapters/noop_metrics_repository.py

- L11: class `NoopMetricsRepository`
- L14: method `write_evaluation_metrics` parent=NoopMetricsRepository
- L17: method `read_evaluation_metrics` parent=NoopMetricsRepository
- L26: method `latest_metrics` parent=NoopMetricsRepository

## app/services/noop_adapters/noop_ranking_log_publisher.py

- L14: class `NoopRankingLogPublisher`
- L15: method `publish_candidates` parent=NoopRankingLogPublisher

## app/services/noop_adapters/noop_retrain_queries.py

- L10: class `NoopRetrainQueries`
- L11: method `last_run_finished_at` parent=NoopRetrainQueries
- L14: method `feedback_rows_since` parent=NoopRetrainQueries
- L17: method `ndcg_in_window` parent=NoopRetrainQueries

## app/services/noop_adapters/noop_synonym_expander.py

- L13: class `NoopSynonymExpander`
- L14: method `expand` parent=NoopSynonymExpander

## app/services/noop_adapters/noop_training_dataset_repository.py

- L11: class `NoopTrainingDatasetRepository`
- L14: method `write_training_dataset` parent=NoopTrainingDatasetRepository
- L17: method `read_training_dataset` parent=NoopTrainingDatasetRepository
- L24: method `latest_training_dataset` parent=NoopTrainingDatasetRepository

## app/services/protocols/candidate_retriever.py

- L20: class `CandidateRetriever`
- L38: method `retrieve` parent=CandidateRetriever

## app/services/protocols/data_catalog_reader.py

- L10: class `DataCatalogTablePreview`
- L21: class `DataCatalogSnapshot`
- L25: class `DataCatalogReader`
- L26: method `read_snapshot` parent=DataCatalogReader

## app/services/protocols/encoder_client.py

- L8: class `EncoderClient`
- L11: method `embed` parent=EncoderClient

## app/services/protocols/event_repository.py

- L9: class `EventRepository`
- L10: method `read_search_events` parent=EventRepository
- L12: method `read_impressions` parent=EventRepository
- L19: method `read_user_actions` parent=EventRepository

## app/services/protocols/event_writer.py

- L8: class `EventWriter`
- L9: method `emit_search_event` parent=EventWriter
- L21: method `emit_impression` parent=EventWriter
- L35: method `emit_user_action` parent=EventWriter

## app/services/protocols/feature_fetcher.py

- L29: class `FeatureRow`
- L52: class `FeatureFetcher`
- L63: method `fetch` parent=FeatureFetcher

## app/services/protocols/feedback_recorder.py

- L17: class `FeedbackRecorder`
- L27: method `record` parent=FeedbackRecorder

## app/services/protocols/label_repository.py

- L9: class `LabelRepository`
- L10: method `write_ranking_labels` parent=LabelRepository
- L12: method `read_ranking_labels` parent=LabelRepository

## app/services/protocols/lexical_search.py

- L18: class `LexicalSearchPort`
- L25: method `search` parent=LexicalSearchPort

## app/services/protocols/metrics_repository.py

- L16: class `MetricsRepository`
- L17: method `write_evaluation_metrics` parent=MetricsRepository
- L21: method `read_evaluation_metrics` parent=MetricsRepository
- L31: method `latest_metrics` parent=MetricsRepository

## app/services/protocols/popularity_scorer.py

- L14: class `PopularityScorer`
- L15: method `score` parent=PopularityScorer

## app/services/protocols/publisher.py

- L12: class `PredictionPublisher`
- L13: method `publish` parent=PredictionPublisher
- L16: class `NoopPublisher`
- L17: method `publish` parent=NoopPublisher

## app/services/protocols/ranking_log_publisher.py

- L24: class `RankingLogPublisher`
- L35: method `publish_candidates` parent=RankingLogPublisher

## app/services/protocols/reranker_client.py

- L8: class `RerankerClient`
- L11: method `predict` parent=RerankerClient
- L14: class `RerankerExplainer`
- L22: method `predict_with_explain` parent=RerankerExplainer

## app/services/protocols/retrain_queries.py

- L12: class `RetrainQueries`
- L13: method `last_run_finished_at` parent=RetrainQueries
- L14: method `feedback_rows_since` parent=RetrainQueries
- L15: method `ndcg_in_window` parent=RetrainQueries

## app/services/protocols/semantic_search.py

- L20: class `SemanticSearchPort`
- L28: method `search` parent=SemanticSearchPort

## app/services/protocols/synonym_expander.py

- L25: class `SynonymExpanderPort`
- L33: method `expand` parent=SynonymExpanderPort

## app/services/protocols/training_dataset_repository.py

- L18: class `TrainingDatasetRepository`
- L19: method `write_training_dataset` parent=TrainingDatasetRepository
- L23: method `read_training_dataset` parent=TrainingDatasetRepository
- L27: method `latest_training_dataset` parent=TrainingDatasetRepository

## app/services/ranking.py

- L31: function `_safe_publish_candidates`
- L84: function `_augment_with_fresh_features`
- L129: function `_build_feature_matrix`
- L143: function `_score_candidates`
- L148: function `_score_with_explain`
- L156: function `run_search`
- L271: function `rrf_fuse`

## app/services/retrain_policy.py

- L28: class `RetrainThresholds`
- L37: class `RetrainDecision`
- L46: function `evaluate`

## app/services/search_service.py

- L33: class `SearchServiceUnavailable`
- L40: class `SearchService`
- L48: method `__init__` parent=SearchService
- L79: method `reranker_model_path` parent=SearchService
- L82: method `search` parent=SearchService
- L188: function `_as_str`
- L196: function `_as_int`
- L212: function `_as_float`
- L228: function `_as_bool`
- L244: function `filters_from_dict`

## app/settings/api.py

- L12: class `FeatureFlags`
- L17: class `MessagingSettings`
- L28: class `KServeSettings`
- L35: class `PopularitySettings`
- L40: class `SynonymSettings`
- L48: class `ApiSettings`
- L115: method `feature_flags` parent=ApiSettings
- L122: method `messaging` parent=ApiSettings
- L133: method `kserve` parent=ApiSettings
- L142: method `popularity` parent=ApiSettings
- L149: method `synonym` parent=ApiSettings

## app/static/css/custom.css

- L2: custom-property `--bg-main`
- L3: custom-property `--bg-sub`
- L4: custom-property `--bg-hover`
- L5: custom-property `--border`
- L6: custom-property `--text-main`
- L7: custom-property `--text-sub`
- L8: custom-property `--text-disabled`
- L9: custom-property `--lime`
- L10: custom-property `--lime-hover`
- L11: custom-property `--pink`
- L12: custom-property `--pink-hover`
- L13: custom-property `--shadow`
- L24: selector `.admin-brand`
- L30: selector `.admin-nav-item--docs`
- L34: selector `.admin-nav-item--docs`
- L35: selector `.admin-nav-item--docs`
- L41: selector `.admin-sidebar-card`
- L45: selector `.admin-main`
- L50: selector `.admin-header,`
- L51: selector `.admin-content`
- L56: selector `.admin-main`
- L60: selector `.page-header`
- L69: selector `.eyebrow`
- L78: selector `.page-header`
- L79: selector `.panel`
- L80: selector `.feature-card`
- L84: selector `.page-copy,`
- L85: selector `.section-copy,`
- L86: selector `.status-note,`
- L87: selector `.search-state,`
- L88: selector `.feature-card`
- L92: selector `.page-header`
- L93: selector `.panel`
- L94: selector `.feature-card`
- L95: selector `.search-result-card`
- L99: selector `.search-shell`
- L104: selector `.panel`
- L111: selector `.panel,`
- L112: selector `.feature-card,`
- L113: selector `.status-card`
- L117: selector `.section-heading`
- L126: selector `.search-form`
- L127: selector `.search-form`
- L134: selector `.search-form`
- L138: selector `.search-form`
- L139: selector `.search-form`
- L140: selector `#fb-action`
- L147: selector `.search-form`
- L151: selector `.toggle-wrap`
- L158: selector `.toggle-wrap`
- L162: selector `.dev-controls`
- L167: selector `.action-row`
- L175: selector `.search-state`
- L180: selector `.panel`
- L181: selector `.panel`
- L182: selector `.panel`
- L183: selector `.panel`
- L184: selector `.panel`
- L185: selector `.search-result-card`
- L186: selector `.search-result-card`
- L187: selector `.status-card`
- L188: selector `.status-label`
- L192: selector `.panel`
- L198: selector `.status-grid`
- L205: selector `.status-card-danger`
- L209: selector `.status-card-wide`
- L213: selector `.ops-panel`
- L217: selector `.ops-panel-ok`
- L221: selector `.ops-panel-warn`
- L225: selector `.ops-panel-fail,`
- L226: selector `.ops-panel-error`
- L230: selector `.ops-item-list`
- L235: selector `.ops-item-list`
- L239: selector `.panel`
- L240: selector `.panel`
- L244: selector `#search-btn,`
- L245: selector `#acc-btn,`
- L246: selector `#data-btn`
- L253: selector `#search-btn`
- L254: selector `#acc-btn`
- L255: selector `#data-btn`
- L259: selector `#feedback-btn`
- L265: selector `#feedback-btn`
- L270: selector `.results-panel`
- L274: selector `.result-grid`
- L280: selector `.search-result-card`
- L295: selector `.search-result-card`
- L301: selector `.component-status-wrap,`
- L302: selector `.status-card,`
- L303: selector `.feature-card`
- L310: selector `.status-label`
- L319: selector `.status-card`
- L325: selector `.status-ok`
- L329: selector `.status-warn`
- L333: selector `.status-note`
- L368: selector `#result-card`
- L369: selector `#result-card`
- L370: selector `#result-card`
- L371: selector `#result-card`
- L372: selector `#result-card`
- L377: selector `#result-card`
- L381: selector `#result-card`
- L382: selector `#result-card`
- L386: selector `.table-scroll`
- L396: selector `.search-shell[data-page-mode="user"]`
- L401: selector `.search-shell[data-page-mode="user"]`
- L405: selector `.search-shell[data-page-mode="dev"]`
- L410: selector `.search-shell[data-page-mode="dev"]`
- L415: selector `.search-shell[data-page-mode="dev"]`
- L422: selector `.search-shell[data-page-mode="user"]`
- L426: selector `.search-shell[data-page-mode="dev"]`
- L430: selector `.result-grid`
- L434: selector `.component-status-wrap`
- L438: selector `#result-card`
- L439: selector `#result-card`
- L440: selector `#result-card`
- L441: selector `#result-card`
- L442: selector `#result-card`
- L449: selector `.admin-main`
- L453: selector `.component-status-wrap`
- L459: selector `.panel,`
- L460: selector `.feature-card`

## app/static/css/pico-admin-components.css

- L1: selector `.admin-brand`
- L8: selector `.admin-brand__mark`
- L19: selector `.admin-brand__eyebrow,`
- L20: selector `.admin-eyebrow`
- L27: selector `.admin-nav,`
- L28: selector `.admin-nav`
- L34: selector `.admin-nav`
- L41: selector `.admin-nav`
- L48: selector `.admin-nav`
- L56: selector `.admin-nav`
- L60: selector `.admin-nav`
- L66: selector `.admin-nav-item`
- L77: selector `.admin-nav-item`
- L78: selector `.admin-nav-item`
- L84: selector `.admin-nav-item[aria-current="page"]`
- L91: selector `.admin-card`
- L98: selector `.admin-card`
- L99: selector `.admin-card`
- L103: selector `.admin-card`
- L108: selector `.admin-card`
- L112: selector `.admin-card`
- L113: selector `.admin-card`
- L114: selector `.admin-card`
- L118: selector `.admin-card--compact`
- L122: selector `.admin-card--dense`
- L126: selector `.admin-hero`
- L135: selector `.admin-hero__lead`
- L139: selector `.admin-kpi`
- L144: selector `.admin-kpi--dense`
- L148: selector `.admin-kpi__value`
- L155: selector `.admin-kpi--dense`
- L159: selector `.admin-kpi__meta`
- L167: selector `.admin-badge`
- L183: selector `.admin-badge--neutral`
- L189: selector `.admin-badge--lime`
- L195: selector `.admin-badge--pink`
- L201: selector `.admin-stat-list,`
- L202: selector `.admin-list,`
- L203: selector `.admin-inline-list`
- L209: selector `.admin-stat-list`
- L214: selector `.admin-stat-row,`
- L215: selector `.admin-list`
- L222: selector `.admin-list`
- L227: selector `.admin-list--dense`
- L231: selector `.admin-list`
- L236: selector `.admin-list--dense`
- L240: selector `.admin-chart`
- L247: selector `.admin-chart--compact`
- L253: selector `.admin-chart--short`
- L259: selector `.admin-chart`
- L265: selector `.admin-table-wrap`
- L270: selector `.admin-table`
- L277: selector `.admin-table`
- L281: selector `.admin-table`
- L282: selector `.admin-table`
- L286: selector `.admin-table`
- L287: selector `.admin-table`
- L288: selector `.admin-table`
- L292: selector `.admin-table`
- L293: selector `.admin-table`
- L300: selector `.admin-table`
- L305: selector `.admin-table`
- L306: selector `.admin-table`
- L310: selector `.admin-table`
- L314: selector `.admin-table`
- L315: selector `.admin-table`
- L319: selector `.admin-pager`
- L329: selector `.admin-pager__summary`
- L334: selector `.admin-pager__nav`
- L342: selector `.admin-pager__button,`
- L343: selector `.admin-pager__ellipsis`
- L358: selector `.admin-pager__button`
- L359: selector `.admin-pager__button`
- L365: selector `.admin-pager__button[aria-current="page"]`
- L371: selector `.admin-pager__ellipsis`
- L377: selector `.admin-news-feed`
- L383: selector `.admin-news-card`
- L391: selector `.admin-news-card__meta`
- L399: selector `.admin-news-card__tags`
- L406: selector `.admin-news-card__action`
- L412: selector `.admin-news-card__action`
- L413: selector `.admin-news-card__action`
- L417: selector `.admin-news-card__thumb`
- L429: selector `.admin-news-card__thumb`
- L437: selector `.admin-news-card__thumb`
- L438: selector `.admin-news-card__eyebrow`
- L444: selector `.admin-news-card__eyebrow`
- L451: selector `.admin-news-card__thumb`
- L461: selector `.admin-news-card__thumb--economy`
- L468: selector `.admin-news-card__thumb--ai`
- L475: selector `.admin-news-card__thumb--alert`
- L482: selector `.admin-news-card__thumb--product`
- L489: selector `.admin-news-card__thumb--global`
- L496: selector `.admin-news-card__thumb--feature`
- L503: selector `.admin-news-card__content`
- L509: selector `.admin-news-card__content`
- L515: selector `.admin-news-card__content`
- L522: selector `.admin-news-card__content`
- L528: selector `.admin-news-feed`
- L533: selector `.admin-detail-grid`
- L539: selector `.admin-detail-item`
- L546: selector `.admin-detail-item`
- L553: selector `.admin-detail-item`
- L557: selector `.admin-checklist`
- L565: selector `.admin-avatar`
- L576: selector `.admin-avatar--image`
- L582: selector `.admin-avatar--image`
- L589: selector `.admin-user`
- L595: selector `.admin-user__meta`
- L599: selector `.admin-user__meta`
- L600: selector `.admin-metric`
- L605: selector `.admin-metric`
- L610: selector `.admin-progress`
- L618: selector `.admin-progress`
- L625: selector `.admin-note`
- L632: selector `.admin-note`
- L636: selector `.admin-note--neutral`
- L641: selector `.admin-actions`
- L648: selector `.admin-field-grid`
- L654: selector `.admin-card`
- L655: selector `.admin-card`
- L656: selector `.admin-card`
- L662: selector `.admin-card`
- L663: selector `.admin-card`
- L664: selector `.admin-card`
- L670: selector `.admin-card`
- L675: selector `.admin-switch-grid`
- L680: selector `.admin-switch`
- L691: selector `.admin-segmented`
- L701: selector `.admin-segmented`
- L709: selector `.admin-segmented`
- L710: selector `.admin-segmented`
- L715: selector `.admin-segmented`
- L725: selector `.admin-segmented`
- L726: selector `.admin-segmented`
- L731: selector `.admin-search`
- L737: selector `.admin-search`
- L742: selector `.admin-inline-control`
- L749: selector `.admin-inline-control`
- L754: selector `.admin-inline-control`
- L759: selector `.admin-header__actions`
- L760: selector `.admin-header__actions`
- L761: selector `.admin-header__actions`
- L770: selector `.admin-header-presence`
- L777: selector `.admin-header-presence`
- L781: selector `.admin-icon-button`
- L792: selector `.admin-icon-button__badge`
- L803: selector `.admin-user-chip`
- L817: selector `.admin-user-chip__caret`
- L822: selector `.admin-user-chip`
- L829: selector `.admin-pager__button`
- L834: selector `.admin-text-right`
- L838: selector `.admin-auth-card`
- L843: selector `.admin-auth-card`
- L847: selector `.admin-auth-links`
- L856: selector `.admin-header,`
- L857: selector `.admin-section-heading,`
- L858: selector `.admin-toolbar,`
- L859: selector `.admin-stat-row,`
- L860: selector `.admin-switch`
- L865: selector `.admin-field-grid`
- L869: selector `.admin-table`
- L873: selector `.admin-pager`
- L878: selector `.admin-pager__nav`
- L882: selector `.admin-news-feed`
- L886: selector `.admin-header-presence,`
- L887: selector `.admin-user-chip`
- L891: selector `.admin-inline-control`
- L897: selector `.admin-inline-control`
- L901: selector `.admin-detail-grid`
- L907: selector `.admin-news-feed`

## app/static/css/pico-admin-layout.css

- L5: selector `.admin-shell`
- L11: selector `.admin-sidebar`
- L22: selector `.admin-sidebar__inner`
- L31: selector `.admin-main`
- L36: selector `.admin-header`
- L44: selector `.admin-header__actions`
- L53: selector `.admin-content`
- L58: selector `.admin-auth`
- L64: selector `.admin-auth__panel`
- L70: selector `.admin-auth__aside`
- L78: selector `.admin-grid`
- L83: selector `.admin-grid--4`
- L87: selector `.admin-grid--6`
- L91: selector `.admin-grid--3`
- L95: selector `.admin-grid--2`
- L99: selector `.admin-grid--sidebar`
- L103: selector `.admin-section-heading`
- L111: selector `.admin-toolbar`
- L119: selector `.admin-toolbar__group`
- L126: selector `.admin-stack`
- L131: selector `.admin-dashboard__top,`
- L132: selector `.admin-dashboard__analytics,`
- L133: selector `.admin-dashboard__ops`
- L138: selector `.admin-dashboard__summary`
- L145: selector `.admin-dashboard__summary-copy`
- L149: selector `.admin-dashboard__top`
- L153: selector `.admin-dashboard__analytics`
- L157: selector `.admin-dashboard__ops`
- L161: selector `.admin-main`
- L168: selector `.admin-main`
- L172: selector `.admin-content`
- L176: selector `.admin-grid`
- L182: selector `.admin-main`
- L186: selector `.admin-content`
- L190: selector `.admin-grid`
- L194: selector `.admin-grid--sidebar`
- L198: selector `.admin-dashboard__top`
- L202: selector `.admin-dashboard__analytics`
- L206: selector `.admin-dashboard__ops`
- L212: selector `.admin-shell`
- L216: selector `.admin-grid--6,`
- L217: selector `.admin-grid--4`
- L221: selector `.admin-dashboard__top,`
- L222: selector `.admin-dashboard__summary,`
- L223: selector `.admin-dashboard__analytics,`
- L224: selector `.admin-dashboard__ops,`
- L225: selector `.admin-grid--sidebar`
- L230: selector `.admin-mobile-toggle`
- L234: selector `.admin-sidebar-backdrop`
- L238: selector `.admin-sidebar`
- L243: selector `.admin-shell`
- L247: selector `.admin-sidebar`
- L261: selector `.admin-main`
- L265: selector `.admin-mobile-toggle`
- L273: selector `.admin-sidebar-backdrop`
- L284: selector `.admin-sidebar`
- L288: selector `.admin-grid--3,`
- L289: selector `.admin-grid--2`
- L293: selector `.admin-auth`
- L297: selector `.admin-auth__panel,`
- L298: selector `.admin-auth__aside`
- L304: selector `.admin-header,`
- L305: selector `.admin-header__actions`
- L311: selector `.admin-header__actions`
- L315: selector `.admin-content,`
- L316: selector `.admin-grid`
- L320: selector `.admin-grid--4`

## app/static/css/pico-admin-theme.css

- L3: custom-property `--admin-bg-main`
- L4: custom-property `--admin-bg-sub`
- L5: custom-property `--admin-bg-elevated`
- L6: custom-property `--admin-bg-header`
- L7: custom-property `--admin-bg-hover`
- L8: custom-property `--admin-bg-active`
- L9: custom-property `--admin-bg-glass`
- L10: custom-property `--admin-border`
- L11: custom-property `--admin-border-strong`
- L12: custom-property `--admin-text-main`
- L13: custom-property `--admin-text-sub`
- L14: custom-property `--admin-text-muted`
- L15: custom-property `--admin-lime-main`
- L16: custom-property `--admin-lime-accent`
- L17: custom-property `--admin-lime-soft`
- L18: custom-property `--admin-lime-glow`
- L19: custom-property `--admin-pink-main`
- L20: custom-property `--admin-pink-soft`
- L21: custom-property `--admin-shadow`
- L22: custom-property `--admin-radius`
- L24: custom-property `--pico-background-color`
- L25: custom-property `--pico-color`
- L26: custom-property `--pico-muted-color`
- L27: custom-property `--pico-muted-border-color`
- L28: custom-property `--pico-primary`
- L29: custom-property `--pico-primary-hover`
- L30: custom-property `--pico-primary-focus`
- L31: custom-property `--pico-primary-inverse`
- L32: custom-property `--pico-secondary`
- L33: custom-property `--pico-secondary-hover`
- L34: custom-property `--pico-secondary-inverse`
- L35: custom-property `--pico-form-element-background-color`
- L36: custom-property `--pico-form-element-selected-background-color`
- L37: custom-property `--pico-form-element-border-color`
- L38: custom-property `--pico-form-element-active-border-color`
- L39: custom-property `--pico-form-element-focus-color`
- L40: custom-property `--pico-form-element-color`
- L41: custom-property `--pico-form-element-placeholder-color`
- L42: custom-property `--pico-card-background-color`
- L43: custom-property `--pico-card-border-color`
- L44: custom-property `--pico-card-sectioning-background-color`
- L45: custom-property `--pico-dropdown-background-color`
- L46: custom-property `--pico-dropdown-border-color`
- L47: custom-property `--pico-box-shadow`
- L48: custom-property `--pico-border-radius`
- L49: custom-property `--pico-spacing`
- L50: custom-property `--pico-font-family`
- L51: custom-property `--pico-line-height`

## app/static/js/search_ui.js

- L2: function `escapeHtml`
- L11: function `yen`
- L15: function `boolBadge`
- L21: function `num`
- L26: function `assessComponents`
- L62: function `renderPropertyCard`
- L101: function `buildFilters`
- L115: function `renderComponentStatus`
- L130: function `loadInfo` (async)
- L154: function `init` (test)
- L163: function `runSearch` (async)
- L269: function `sendFeedback` (async)

## app/templates/_feedback_panel.html

- L1: class `panel admin-card`
- L2: class `admin-card__body`
- L3: class `admin-section-heading`
- L5: class `eyebrow`
- L8: class `section-copy`
- L10: id `feedback-form`
- L11: class `grid`
- L14: id `fb-pid`
- L18: id `fb-action`
- L27: class `action-row`
- L28: id `feedback-btn`
- L29: class `search-state`
- L32: id `fb-result`

## app/templates/_search_form.html

- L1: class `panel admin-card`
- L2: class `admin-card__body`
- L3: class `admin-section-heading`
- L5: class `eyebrow`
- L8: class `section-copy`
- L10: id `search-form`
- L10: class `search-form`
- L13: id `q-query`
- L15: class `grid`
- L18: id `q-max-rent`
- L22: id `q-layout`
- L26: id `q-top-k`
- L29: class `grid`
- L32: id `q-max-walk-min`
- L36: id `q-max-age`
- L38: class `toggle-wrap`
- L39: id `q-pet-ok`
- L44: class `dev-controls`
- L45: class `toggle-wrap`
- L46: id `q-explain`
- L51: class `action-row`
- L52: id `search-btn`
- L53: id `search-state`
- L53: class `search-state`

## app/templates/_search_results.html

- L1: id `result-card`
- L1: class `panel admin-card results-panel`
- L2: class `admin-card__body`
- L3: class `admin-section-heading`
- L5: class `eyebrow`
- L8: id `result-meta`
- L8: class `section-copy`
- L12: class `component-status-wrap admin-grid admin-grid--3`
- L13: class `status-card admin-card admin-card--compact admin-card--dense`
- L14: class `status-label`
- L15: id `component-lexical-state`
- L16: id `component-lexical-note`
- L16: class `status-note`
- L18: class `status-card admin-card admin-card--compact admin-card--dense`
- L19: class `status-label`
- L20: id `component-semantic-state`
- L21: id `component-semantic-note`
- L21: class `status-note`
- L23: class `status-card admin-card admin-card--compact admin-card--dense`
- L24: class `status-label`
- L25: id `component-rerank-state`
- L26: id `component-rerank-note`
- L26: class `status-note`
- L31: id `result-rows`
- L31: class `result-grid`
- L36: class `admin-table-wrap table-scroll`
- L37: class `admin-table`
- L50: id `debug-rows`
- L56: id `result-json`

## app/templates/base.html

- L13: class `admin-body`
- L14: class `admin-mobile-toggle secondary`
- L15: class `admin-sidebar-backdrop`
- L16: class `admin-shell`
- L17: class `admin-sidebar`
- L18: class `admin-sidebar__inner`
- L19: class `admin-brand`
- L20: class `admin-brand__mark`
- L23: class `admin-brand__eyebrow`
- L25: class `secondary`
- L28: class `admin-nav`
- L32: class `admin-nav-item`
- L33: class `admin-nav-item`
- L41: class `admin-nav-item`
- L42: class `admin-nav-item`
- L43: class `admin-nav-item`
- L44: class `admin-nav-item admin-nav-item--docs`
- L52: class `admin-main`
- L53: class `admin-header app-header`
- L55: class `admin-eyebrow`
- L56: class `app-header__title`
- L57: class `app-header__copy`
- L59: class `admin-header__actions`
- L60: class `admin-segmented`
- L67: class `secondary admin-user-chip`
- L68: class `admin-avatar`
- L69: class `admin-user__meta`
- L73: class `admin-user-chip__caret`

## app/templates/data.html

- L8: class `admin-content admin-stack`
- L9: class `panel admin-card`
- L10: class `admin-card__body action-row`
- L11: id `data-btn`
- L12: id `data-meta`
- L12: class `search-state`
- L16: id `data-tables`
- L16: class `admin-stack`
- L34: class `search-state`
- L38: class `panel admin-card`
- L39: class `admin-card__body`
- L40: class `admin-section-heading`
- L42: class `eyebrow`
- L45: class `section-copy`
- L47: class `section-copy`
- L49: class `admin-table-wrap table-scroll`
- L50: class `admin-table`
- L71: class `panel`

## app/templates/index.html

- L8: id `search-app`
- L8: class `admin-content search-shell`

## app/templates/model_metrics.html

- L8: class `admin-content admin-stack`
- L9: class `admin-card`
- L10: class `admin-card__body`
- L11: id `acc-form`
- L14: id `q-k`
- L16: id `acc-btn`
- L21: id `acc-summary-card`
- L21: class `admin-card`
- L22: class `admin-card__body`
- L23: class `admin-section-heading`
- L25: class `admin-eyebrow`
- L28: id `acc-meta`
- L30: class `admin-grid admin-grid--3`
- L31: id `acc-ndcg`
- L31: class `admin-card admin-card--compact admin-card--dense`
- L32: id `acc-hit`
- L32: class `admin-card admin-card--compact admin-card--dense`
- L33: id `acc-mrr`
- L33: class `admin-card admin-card--compact admin-card--dense`
- L38: id `acc-cases-card`
- L38: class `admin-card`
- L39: class `admin-card__body`
- L40: class `admin-section-heading`
- L41: class `admin-eyebrow`
- L43: class `admin-table-wrap table-scroll`
- L44: class `admin-table`
- L50: id `acc-rows`

## app/templates/ops.html

- L8: class `admin-content admin-stack`
- L9: class `panel admin-card`
- L10: class `admin-card__body action-row`
- L11: id `ops-btn`
- L12: id `ops-meta`
- L12: class `search-state`
- L16: class `admin-grid admin-grid--3 status-grid`
- L17: class `status-card admin-card admin-card--compact admin-card--dense`
- L18: class `status-label`
- L19: id `ops-ok`
- L21: class `status-card admin-card admin-card--compact admin-card--dense`
- L22: class `status-label`
- L23: id `ops-warn`
- L25: class `status-card status-card-danger admin-card admin-card--compact admin-card--dense`
- L26: class `status-label`
- L27: id `ops-bad`
- L31: class `admin-grid admin-grid--3 status-grid`
- L32: class `status-card admin-card admin-card--compact admin-card--dense`
- L33: class `status-label`
- L34: id `ops-search-volume`
- L35: id `ops-search-window`
- L35: class `status-note`
- L37: class `status-card status-card-wide admin-card admin-card--compact admin-card--dense`
- L38: class `status-label`
- L39: id `ops-runs-count`
- L40: class `status-note`
- L44: class `panel admin-card`
- L45: class `admin-card__body`
- L46: class `admin-section-heading`
- L48: class `eyebrow`
- L51: class `section-copy`
- L53: class `admin-table-wrap table-scroll`
- L54: class `admin-table`
- L65: id `ops-runs-rows`
- L73: id `ops-findings`
- L73: class `admin-grid admin-grid--2`
- L88: class `ops-item-list`
- L90: class `section-copy`
- L92: class `panel admin-card ops-panel ops-panel-${String(finding.severity || `
- L93: class `admin-card__body`
- L94: class `admin-section-heading`
- L96: class `eyebrow`
- L101: class `search-state`
- L148: class `panel`

## app/templates/property_detail.html

- L8: class `panel admin-card`
- L9: class `admin-card__body`
- L10: class `admin-section-heading`
- L12: class `eyebrow`
- L13: id `property-title`
- L14: id `request-id`
- L14: class `section-copy`
- L16: class `secondary`
- L19: class `grid`
- L34: class `section-copy`
- L38: class `action-row`
- L39: id `btn-favorite`
- L39: class `secondary`
- L40: id `btn-request-click`
- L40: class `secondary`
- L41: id `btn-request-complete`
- L43: id `emit-result`

## app/templates/search_dev.html

- L8: id `search-app`
- L8: class `admin-content search-shell`
- L13: class `panel admin-card`
- L14: class `admin-card__body`
- L15: class `admin-section-heading`
- L17: class `eyebrow`
- L20: class `section-copy`
- L22: class `action-row`
- L23: id `data-btn`
- L24: class `search-state`
- L26: class `table-scroll`
- L27: id `data-card`
- L27: class `admin-table`
- L28: id `data-rows`

## infra/run/services/composer_runner/Dockerfile

- L36: container-base-image `ghcr.io/astral-sh/uv:0.5.4-python3.12-bookworm-slim`
- L53: container-base-image `python:3.12-slim-bookworm`

## infra/run/services/encoder/Dockerfile

- L7: container-base-image `${ML_BUILDER_IMAGE}`
- L20: container-base-image `python:3.12-slim-bookworm`

## infra/run/services/ml_base/Dockerfile

- L6: container-base-image `ghcr.io/astral-sh/uv:0.5.4-python3.12-bookworm-slim`

## infra/run/services/reranker/Dockerfile

- L7: container-base-image `${ML_BUILDER_IMAGE}`
- L20: container-base-image `python:3.12-slim-bookworm`

## infra/run/services/search_api/Dockerfile

- L14: container-base-image `ghcr.io/astral-sh/uv:0.5.4-python3.12-bookworm-slim`
- L31: container-base-image `python:3.12-slim-bookworm`

## infra/terraform/environments/dev/apis.tf

- L36: gcp-resource `google_project_service.enabled`

## infra/terraform/modules/composer/main.tf

- L26: gcp-resource `google_composer_environment.this`

## infra/terraform/modules/data/main.tf

- L5: gcp-resource `google_bigquery_dataset.mlops`
- L11: gcp-resource `google_bigquery_dataset.feature_mart`
- L17: gcp-resource `google_bigquery_dataset.predictions`
- L23: gcp-resource `google_bigquery_table.training_runs`
- L112: gcp-resource `google_bigquery_table.property_features_daily`
- L142: gcp-resource `google_bigquery_table.property_features_online_latest`
- L166: gcp-resource `google_bigquery_table.property_embeddings`
- L182: gcp-resource `google_bigquery_table.search_logs`
- L214: gcp-resource `google_bigquery_table.ranking_log`
- L256: gcp-resource `google_bigquery_table.feedback_events`
- L275: gcp-resource `google_bigquery_table.search_events`
- L299: gcp-resource `google_bigquery_table.search_impressions`
- L325: gcp-resource `google_bigquery_table.user_actions`
- L346: gcp-resource `google_bigquery_table.ranking_labels`
- L366: gcp-resource `google_bigquery_table.evaluation_metrics`
- L389: gcp-resource `google_bigquery_table.validation_results`
- L409: gcp-resource `google_bigquery_table.model_monitoring_alerts`
- L434: gcp-resource `google_bigquery_table.ranking_log_hourly_ctr`
- L458: gcp-bucket `google_storage_bucket.models`
- L479: gcp-bucket `google_storage_bucket.artifacts`
- L495: gcp-bucket `google_storage_bucket.pipeline_root`
- L516: gcp-resource `google_artifact_registry_repository.mlops`
- L526: gcp-resource `google_secret_manager_secret.search_api_iap_oauth_client_secret`
- L545: gcp-resource `google_secret_manager_secret_version.search_api_iap_oauth_client_secret_dev_placeholder`
- L558: gcp-resource `google_bigquery_dataset_iam_member.api_mlops_viewer`
- L564: gcp-resource `google_bigquery_dataset_iam_member.api_feature_viewer`
- L570: gcp-resource `google_storage_bucket_iam_member.api_models_read`
- L576: gcp-resource `google_secret_manager_secret_iam_member.external_secrets_search_api_iap_oauth_client_secret_access`
- L583: gcp-resource `google_bigquery_dataset_iam_member.train_feature_viewer`
- L589: gcp-resource `google_bigquery_dataset_iam_member.train_mlops_editor`
- L595: gcp-resource `google_storage_bucket_iam_member.train_models_admin`
- L601: gcp-resource `google_storage_bucket_iam_member.train_pipeline_root_admin`
- L611: gcp-resource `google_bigquery_dataset_iam_member.embed_feature_viewer`
- L617: gcp-resource `google_bigquery_dataset_iam_member.embed_feature_editor`
- L623: gcp-resource `google_storage_bucket_iam_member.embed_models_viewer`
- L629: gcp-resource `google_bigquery_dataset_iam_member.pipeline_feature_viewer`
- L635: gcp-resource `google_bigquery_dataset_iam_member.pipeline_mlops_editor`
- L641: gcp-resource `google_storage_bucket_iam_member.pipeline_models_admin`
- L647: gcp-resource `google_storage_bucket_iam_member.pipeline_root_pipeline_admin`
- L656: gcp-resource `google_storage_bucket_iam_member.pipeline_root_composer_object_admin`
- L662: gcp-resource `google_storage_bucket_iam_member.endpoint_encoder_models_viewer`
- L668: gcp-resource `google_storage_bucket_iam_member.endpoint_reranker_models_viewer`
- L675: gcp-resource `google_bigquery_dataset_iam_member.dataform_feature_editor`
- L684: gcp-resource `google_bigquery_dataset_iam_member.dataform_mlops_editor`
- L698: gcp-resource `google_dataform_repository.main`
- L725: gcp-resource `google_dataform_repository_iam_member.admin_self`
- L737: gcp-resource `google_dataform_repository_iam_member.deployer_editor`

## infra/terraform/modules/dns/main.tf

- L28: gcp-resource `google_compute_global_address.search_api`
- L36: gcp-resource `google_dns_record_set.apex_a`
- L46: gcp-resource `google_certificate_manager_dns_authorization.search_api`
- L56: gcp-resource `google_dns_record_set.cert_auth_cname`
- L65: gcp-resource `google_certificate_manager_certificate.search_api`
- L79: gcp-resource `google_certificate_manager_certificate_map.search_api`
- L85: gcp-resource `google_certificate_manager_certificate_map_entry.search_api`

## infra/terraform/modules/elasticsearch/main.tf

- L1: terraform-resource `kubernetes_namespace.elastic_system`
- L10: terraform-resource `helm_release.eck_operator`

## infra/terraform/modules/gke/main.tf

- L9: gcp-resource `google_container_cluster.hybrid_search`
- L54: gcp-iam `google_service_account_iam_member.api_wi`
- L60: gcp-iam `google_service_account_iam_member.encoder_wi`
- L66: gcp-iam `google_service_account_iam_member.reranker_wi`
- L72: gcp-iam `google_service_account_iam_member.external_secrets_wi`

## infra/terraform/modules/iam/main.tf

- L3: gcp-service-account `google_service_account.api`
- L8: gcp-service-account `google_service_account.job_train`
- L13: gcp-service-account `google_service_account.job_embed`
- L18: gcp-service-account `google_service_account.dataform`
- L23: gcp-service-account `google_service_account.scheduler`
- L28: gcp-service-account `google_service_account.pipeline`
- L33: gcp-service-account `google_service_account.endpoint_encoder`
- L38: gcp-service-account `google_service_account.endpoint_reranker`
- L43: gcp-service-account `google_service_account.pipeline_trigger`
- L48: gcp-service-account `google_service_account.external_secrets`
- L55: gcp-resource `google_iam_workload_identity_pool.github`
- L60: gcp-resource `google_iam_workload_identity_pool_provider.github`
- L78: gcp-service-account `google_service_account.github_deployer`
- L83: gcp-iam `google_service_account_iam_member.github_wif_binding`
- L99: gcp-iam `google_service_account_iam_member.api_token_creator_for_admins`
- L108: gcp-iam `google_project_iam_member.github_deployer_editor`
- L114: gcp-iam `google_project_iam_member.github_deployer_sa_user`
- L122: gcp-iam `google_project_iam_member.api_bq_job_user`
- L136: gcp-iam `google_project_iam_member.gmp_compute_metric_writer`
- L146: gcp-iam `google_project_iam_member.api_aiplatform_user`
- L152: gcp-iam `google_project_iam_member.train_bq_job_user`
- L158: gcp-iam `google_project_iam_member.train_bq_read_session`
- L164: gcp-iam `google_project_iam_member.embed_bq_job_user`
- L170: gcp-iam `google_project_iam_member.embed_bq_read_session`
- L176: gcp-iam `google_project_iam_member.dataform_bq_job_user`
- L182: gcp-iam `google_project_iam_member.pipeline_bq_job_user`
- L188: gcp-iam `google_project_iam_member.pipeline_bq_read_session`
- L194: gcp-iam `google_project_iam_member.pipeline_aiplatform_user`
- L200: gcp-iam `google_project_iam_member.pipeline_trigger_aiplatform_user`
- L206: gcp-iam `google_project_iam_member.pipeline_trigger_eventarc_receiver`
- L212: gcp-iam `google_project_iam_member.pipeline_trigger_pubsub_subscriber`
- L218: gcp-iam `google_project_iam_member.pipeline_trigger_logging_writer`
- L224: gcp-iam `google_service_account_iam_member.pipeline_trigger_can_use_pipeline_sa`
- L234: gcp-iam `google_service_account_iam_member.composer_can_use_pipeline_sa`
- L240: gcp-iam `google_project_iam_member.endpoint_encoder_logging_writer`
- L246: gcp-iam `google_project_iam_member.endpoint_reranker_logging_writer`
- L269: gcp-iam `google_project_iam_member.endpoint_reranker_aiplatform_user`
- L293: gcp-service-account `google_service_account.composer`
- L298: gcp-iam `google_project_iam_member.composer_worker`
- L304: gcp-iam `google_project_iam_member.composer_aiplatform_user`
- L310: gcp-iam `google_project_iam_member.composer_bq_job_user`
- L316: gcp-iam `google_project_iam_member.composer_bq_data_viewer`
- L322: gcp-iam `google_project_iam_member.composer_run_invoker`
- L340: gcp-iam `google_project_iam_member.composer_artifactregistry_reader`
- L346: gcp-iam `google_project_iam_member.composer_storage_object_viewer`
- L354: gcp-iam `google_project_iam_member.github_deployer_composer_admin`

## infra/terraform/modules/kserve/main.tf

- L13: terraform-resource `kubernetes_namespace.search`
- L19: terraform-resource `kubernetes_namespace.inference`
- L26: terraform-resource `kubernetes_service_account.api`
- L36: terraform-resource `kubernetes_service_account.encoder`
- L46: terraform-resource `kubernetes_service_account.reranker`
- L66: terraform-resource `helm_release.cert_manager`
- L87: terraform-resource `helm_release.external_secrets`
- L139: terraform-resource `helm_release.kserve_crd`
- L150: terraform-resource `helm_release.kserve`

## infra/terraform/modules/kserve/tls_dev.tf

- L20: terraform-resource `tls_private_key.search_api_dev`
- L26: terraform-resource `tls_self_signed_cert.search_api_dev`
- L46: terraform-resource `kubernetes_secret.search_api_tls`

## infra/terraform/modules/messaging/main.tf

- L11: gcp-resource `google_pubsub_topic.ranking_log`
- L15: gcp-resource `google_pubsub_topic.search_feedback`
- L19: gcp-resource `google_pubsub_topic.retrain_trigger`
- L26: gcp-resource `google_pubsub_topic.search_events`
- L30: gcp-resource `google_pubsub_topic.search_impressions`
- L34: gcp-resource `google_pubsub_topic.user_actions`
- L38: gcp-resource `google_pubsub_topic_iam_member.api_publish_ranking_log`
- L44: gcp-resource `google_pubsub_topic_iam_member.api_publish_feedback`
- L50: gcp-resource `google_pubsub_topic_iam_member.api_publish_retrain`
- L56: gcp-resource `google_pubsub_topic_iam_member.scheduler_publish_retrain`
- L62: gcp-resource `google_pubsub_topic_iam_member.api_publish_search_events`
- L68: gcp-resource `google_pubsub_topic_iam_member.api_publish_search_impressions`
- L74: gcp-resource `google_pubsub_topic_iam_member.api_publish_user_actions`
- L80: gcp-resource `google_pubsub_subscription.ranking_log_to_bq`
- L100: gcp-resource `google_pubsub_subscription.search_feedback_to_bq`
- L120: gcp-resource `google_pubsub_subscription.search_events_to_bq`
- L140: gcp-resource `google_pubsub_subscription.search_impressions_to_bq`
- L160: gcp-resource `google_pubsub_subscription.user_actions_to_bq`
- L184: gcp-iam `google_project_iam_member.pubsub_bq_writer`
- L190: gcp-iam `google_project_iam_member.pubsub_bq_metadata_viewer`
- L206: gcp-resource `google_cloud_scheduler_job.check_retrain_daily`

## infra/terraform/modules/monitoring/main.tf

- L7: gcp-resource `google_logging_metric.api_error_rate`
- L23: gcp-resource `google_logging_metric.api_p95_latency`
- L54: gcp-resource `google_monitoring_notification_channel.email`
- L73: terraform-resource `time_sleep.wait_for_log_metric_indexing`
- L94: gcp-resource `google_monitoring_alert_policy.api_error_rate`
- L118: gcp-resource `google_monitoring_alert_policy.api_p95_latency`
- L153: gcp-resource `google_bigquery_data_transfer_config.property_feature_skew_check`
- L171: gcp-resource `google_bigquery_data_transfer_config.model_output_drift_check`

## infra/terraform/modules/redis_synonym/main.tf

- L13: gcp-resource `google_redis_instance.synonym`
- L40: gcp-resource `google_secret_manager_secret.redis_auth`
- L55: gcp-resource `google_secret_manager_secret_version.redis_auth`

## infra/terraform/modules/slo/main.tf

- L40: terraform-resource `namespace.${var.k8s_namespace}`
- L47: terraform-resource `service_name.${var.service_name}`
- L57: terraform-resource `namespace.${var.k8s_namespace}`
- L63: terraform-resource `service_name.${var.service_name}`
- L75: terraform-resource `namespace.${var.k8s_namespace}`
- L81: terraform-resource `service_name.${var.service_name}`
- L91: gcp-resource `google_monitoring_custom_service.search_api`
- L107: gcp-resource `google_monitoring_slo.availability`
- L130: gcp-resource `google_monitoring_slo.latency`
- L161: gcp-resource `google_monitoring_alert_policy.availability_fast_burn`
- L184: gcp-resource `google_monitoring_alert_policy.availability_slow_burn`
- L207: gcp-resource `google_monitoring_alert_policy.latency_fast_burn`
- L230: gcp-resource `google_monitoring_alert_policy.latency_slow_burn`

## infra/terraform/modules/streaming/main.tf

- L19: gcp-service-account `google_service_account.dataflow`
- L29: gcp-iam `google_project_iam_member.dataflow_pubsub_subscriber`
- L38: gcp-iam `google_project_iam_member.dataflow_worker`
- L46: gcp-iam `google_project_iam_member.dataflow_storage`
- L55: gcp-iam `google_project_iam_member.dataflow_bq_data_editor`
- L63: gcp-iam `google_project_iam_member.dataflow_bq_jobs`
- L71: gcp-resource `google_dataflow_flex_template_job.ranking_log_hourly_ctr`

## infra/terraform/modules/vector_search/main.tf

- L20: gcp-resource `google_vertex_ai_index.property_embeddings`
- L66: gcp-resource `google_vertex_ai_index_endpoint.property_embeddings`
- L83: gcp-resource `google_vertex_ai_index_endpoint_deployed_index.property_embeddings`

## infra/terraform/modules/vertex/main.tf

- L68: gcp-resource `google_pubsub_topic.model_monitoring_alerts`
- L72: gcp-resource `google_bigquery_dataset_iam_member.pubsub_mlops_editor`
- L78: gcp-resource `google_bigquery_dataset_iam_member.pubsub_mlops_metadata_viewer`
- L84: gcp-resource `google_pubsub_subscription.monitoring_alerts_to_bq`
- L110: gcp-resource `google_storage_bucket_object.pipeline_trigger_zip`
- L127: gcp-resource `google_cloudfunctions2_function.pipeline_trigger`
- L162: gcp-resource `google_cloud_run_service_iam_member.pipeline_trigger_invoker`
- L169: gcp-resource `google_eventarc_trigger.retrain_to_pipeline`
- L202: gcp-resource `google_eventarc_trigger.monitoring_to_pipeline`
- L244: gcp-resource `google_vertex_ai_feature_group.property_features`
- L260: gcp-resource `google_vertex_ai_feature_group_feature.property_features`
- L284: gcp-resource `google_vertex_ai_feature_online_store.property_features`
- L322: gcp-resource `google_vertex_ai_feature_online_store_featureview.property_features`
- L348: gcp-resource `google_vertex_ai_endpoint.encoder`
- L362: gcp-resource `google_vertex_ai_endpoint.reranker`
- L372: gcp-resource `google_storage_bucket_iam_member.endpoint_encoder_models_reader`
- L378: gcp-resource `google_storage_bucket_iam_member.endpoint_reranker_models_reader`

## ml/common/config/base.py

- L26: class `BaseAppSettings`
- L38: method `settings_customise_sources` parent=BaseAppSettings

## ml/common/config/embedding.py

- L6: class `EmbedSettings`

## ml/common/config/training.py

- L6: class `TrainSettings`

## ml/common/logging/structured_logging.py

- L14: class `CloudLoggingJsonFormatter`
- L25: method `format` parent=CloudLoggingJsonFormatter
- L40: function `configure_logging`
- L64: function `get_logger`

## ml/common/utils/run_id.py

- L7: function `generate_run_id`

## ml/data/datasets/embedding_batch.py

- L26: class `_Logger`
- L27: method `info` parent=_Logger
- L30: class `_Encoder`
- L33: method `encode_passages` parent=_Encoder
- L36: function `_text_for_embedding`
- L42: function `_hash`
- L50: function `run_embedding_batch`

## ml/data/feature_engineering/ranker_features.py

- L19: function `build_ranker_features`

## ml/data/loaders/embedding_store.py

- L20: class `PropertyText`
- L27: class `EmbeddingRow`
- L35: class `PropertyTextRepository`
- L36: method `fetch_all` parent=PropertyTextRepository
- L39: class `EmbeddingStore`
- L40: method `existing_hashes` parent=EmbeddingStore
- L41: method `upsert` parent=EmbeddingStore
- L44: class `BigQueryPropertyTextRepository`
- L47: method `__init__` parent=BigQueryPropertyTextRepository
- L60: method `fetch_all` parent=BigQueryPropertyTextRepository
- L77: class `BigQueryEmbeddingStore`
- L80: method `__init__` parent=BigQueryEmbeddingStore
- L93: method `existing_hashes` parent=BigQueryEmbeddingStore
- L98: method `upsert` parent=BigQueryEmbeddingStore

## ml/data/loaders/ranker_repository.py

- L28: class `RankerTrainingRepository`
- L29: method `fetch_training_rows` parent=RankerTrainingRepository
- L33: method `save_run` parent=RankerTrainingRepository
- L46: method `latest_model_path` parent=RankerTrainingRepository
- L91: class `BigQueryRankerRepository`
- L94: method `__init__` parent=BigQueryRankerRepository
- L115: method `fetch_training_rows` parent=BigQueryRankerRepository
- L141: method `save_run` parent=BigQueryRankerRepository
- L184: method `_log_vertex_experiment` parent=BigQueryRankerRepository
- L218: method `latest_model_path` parent=BigQueryRankerRepository
- L230: function `create_rank_repository`

## ml/evaluation/metrics/label_gain.py

- L17: function `assign_label`

## ml/evaluation/metrics/ranking.py

- L14: function `_dcg`
- L23: function `ndcg_at_k`
- L41: function `mean_average_precision`
- L57: function `recall_at_k`
- L74: function `_iter_groups`
- L84: function `evaluate`

## ml/labeling/policy.py

- L60: function `synthetic_label_source`
- L70: function `compute_label`

## ml/registry/adapters/vertex_model_registry.py

- L14: class `VertexModelRegistryAdapter`
- L15: method `__init__` parent=VertexModelRegistryAdapter
- L21: method `_init` parent=VertexModelRegistryAdapter
- L28: method `register` parent=VertexModelRegistryAdapter
- L54: method `promote` parent=VertexModelRegistryAdapter
- L69: method `resolve_alias` parent=VertexModelRegistryAdapter

## ml/registry/artifact_store.py

- L23: class `GcsPrefix`
- L28: method `parse` parent=GcsPrefix
- L36: method `child` parent=GcsPrefix
- L40: method `uri` parent=GcsPrefix
- L48: function `model_prefix`
- L53: function `upload_directory`
- L69: function `download_file`
- L79: class `ArtifactUploader`
- L80: method `upload` parent=ArtifactUploader
- L85: class `GcsArtifactUploader`
- L88: method `__init__` parent=GcsArtifactUploader
- L91: method `upload` parent=GcsArtifactUploader

## ml/registry/metadata_store.py

- L15: class `TrainingRun`
- L22: class `MetadataStore`
- L25: method `__init__` parent=MetadataStore
- L29: method `recent_runs` parent=MetadataStore

## ml/registry/model_registry.py

- L15: class `RegisteredModel`
- L26: class `ModelRegistry`
- L29: method `__init__` parent=ModelRegistry
- L33: method `promote` parent=ModelRegistry

## ml/registry/ports/model_registry.py

- L16: class `RegisteredModelRef`
- L24: class `ModelRegistryPort`
- L25: method `register` parent=ModelRegistryPort
- L33: method `promote` parent=ModelRegistryPort
- L41: method `resolve_alias` parent=ModelRegistryPort

## ml/serving/adapters/kserve_predictor.py

- L18: class `KServePredictorAdapter`
- L19: method `__init__` parent=KServePredictorAdapter
- L28: method `predict` parent=KServePredictorAdapter
- L39: method `predict_with_explain` parent=KServePredictorAdapter

## ml/serving/calibration.py

- L10: function `identity_calibrator`

## ml/serving/encoder.py

- L50: class `E5Encoder`
- L58: method `load` parent=E5Encoder
- L70: method `_encode` parent=E5Encoder
- L74: method `encode_queries` parent=E5Encoder
- L77: method `encode_passages` parent=E5Encoder
- L81: function `encode_query`
- L85: function `encode_passage`
- L89: class `EncoderInstance`
- L94: class `EncoderRequest`
- L98: class `EncoderResponse`
- L102: function `_download_artifact_dir`
- L125: function `_load_encoder`
- L138: function `_normalize_instance`
- L150: function `lifespan` (async)
- L160: function `health`
- L165: function `predict`
- L177: function `main`

## ml/serving/ports/predictor_service.py

- L16: class `PredictorService`
- L17: method `predict` parent=PredictorService
- L21: method `predict_with_explain` parent=PredictorService

## ml/serving/predictor.py

- L14: class `Predictor`
- L17: method `predict` parent=Predictor
- L21: class `RemotePredictorConfig`
- L28: method `endpoint_name` parent=RemotePredictorConfig

## ml/serving/reranker.py

- L30: class `RerankerParameters`
- L43: class `RerankerRequest`
- L48: class `RerankerResponse`
- L53: class `ExplainRequest`
- L58: class `ExplainResponse`
- L62: function `_load_booster`
- L74: function `_pred_contrib`
- L100: function `lifespan` (async)
- L110: function `health`
- L115: function `predict`
- L131: function `explain`
- L143: function `main`

## ml/streaming/adapters/dataflow_processor.py

- L13: class `DataflowStreamProcessor`
- L14: method `run` parent=DataflowStreamProcessor

## ml/streaming/container/Dockerfile

- L7: container-base-image `gcr.io/dataflow-templates-base/python3-template-launcher-base:latest`

## ml/streaming/pipeline.py

- L54: function `_parse_event`
- L67: function `_event_timestamp_seconds`
- L81: function `_to_kv`
- L94: function `_sum_pair`
- L100: function `_format_output_row`
- L118: function `run`
- L140: class `_AttachWindowTimestamps`
- L141: method `process` parent=_AttachWindowTimestamps
- L151: class `_CombineCountsFn`
- L152: method `create_accumulator` parent=_CombineCountsFn
- L155: method `add_input` parent=_CombineCountsFn
- L158: method `merge_accumulators` parent=_CombineCountsFn
- L165: method `extract_output` parent=_CombineCountsFn

## ml/streaming/ports/stream_processor.py

- L16: class `StreamConfig`
- L28: class `StreamProcessor`
- L29: method `run` parent=StreamProcessor

## ml/training/adapters/lightgbm_trainer.py

- L20: class `LightGBMModel`
- L30: method `__init__` parent=LightGBMModel
- L33: method `predict` parent=LightGBMModel
- L39: method `predict_with_explain` parent=LightGBMModel
- L58: method `save` parent=LightGBMModel
- L62: class `LightGBMRankerTrainer`
- L65: method `__init__` parent=LightGBMRankerTrainer
- L76: method `train` parent=LightGBMRankerTrainer

## ml/training/experiments/adapters/null_tracker.py

- L14: class `NullExperimentTracker`
- L17: method `__enter__` parent=NullExperimentTracker
- L20: method `__exit__` parent=NullExperimentTracker
- L28: method `log_metrics` parent=NullExperimentTracker
- L31: method `log_params` parent=NullExperimentTracker

## ml/training/experiments/adapters/vertex_experiments_tracker.py

- L28: class `VertexExperimentsTracker`
- L41: method `__init__` parent=VertexExperimentsTracker
- L53: method `__enter__` parent=VertexExperimentsTracker
- L61: method `__exit__` parent=VertexExperimentsTracker
- L74: method `log_metrics` parent=VertexExperimentsTracker
- L81: method `log_params` parent=VertexExperimentsTracker

## ml/training/experiments/ports/experiment_tracker.py

- L14: class `ExperimentTracker`
- L15: method `__enter__` parent=ExperimentTracker
- L16: method `__exit__` parent=ExperimentTracker
- L22: method `log_metrics` parent=ExperimentTracker
- L23: method `log_params` parent=ExperimentTracker

## ml/training/model_builder.py

- L24: function `synthetic_ranking_frames`
- L77: function `split_by_request_id`

## ml/training/ports/ranker_model.py

- L13: class `RankerModel`
- L21: method `predict` parent=RankerModel
- L25: method `predict_with_explain` parent=RankerModel
- L33: method `save` parent=RankerModel

## ml/training/ports/ranker_trainer.py

- L17: class `TrainingResult`
- L23: class `RankerTrainer`
- L32: method `train` parent=RankerTrainer

## ml/training/trainer.py

- L60: class `RankTrainResult`
- L67: class `RankTrainingArtifacts`
- L72: function `build_rank_params`
- L97: function `_group_sizes`
- L107: function `train`
- L166: function `write_artifacts`
- L195: function `_copy_if_requested`
- L203: function `_default_tracker_factory`
- L204: function `_build`
- L210: function `run`
- L311: function `_parse_args`
- L326: function `main`

## pipeline/batch_serving_job/main.py

- L24: function `property_search_batch_serve_pipeline`
- L32: function `get_pipeline`
- L36: function `main`

## pipeline/dags/_common.py

- L20: function `env`
- L26: function `project_id`
- L45: function `region`
- L49: function `vertex_location`
- L53: function `fixed_start_date`

## pipeline/dags/_pod.py

- L55: function `_composer_runner_image`
- L71: function `_propagated_env_vars`
- L92: function `python_pod`
- L133: function `gcloud_pod`

## pipeline/dags/daily_feature_refresh.py

- L34: function `_gate_daily_vvs_refresh`

## pipeline/dags/monitoring_validation.py

- L39: function `_resolve_sql_path`

## pipeline/dags/retrain_orchestration.py

- L32: function `_gate_auto_promote`

## pipeline/data_job/adapters/in_memory_vector_search_writer.py

- L13: class `InMemoryVectorSearchWriter`
- L16: method `__init__` parent=InMemoryVectorSearchWriter
- L21: method `upsert` parent=InMemoryVectorSearchWriter

## pipeline/data_job/adapters/vertex_vector_search_writer.py

- L29: class `VertexVectorSearchWriter`
- L46: method `__init__` parent=VertexVectorSearchWriter
- L71: method `_resolve_index` parent=VertexVectorSearchWriter
- L83: method `upsert` parent=VertexVectorSearchWriter
- L91: method `_to_sdk_datapoint` parent=VertexVectorSearchWriter
- L116: function `_chunked`

## pipeline/data_job/components/batch_predict_embeddings.py

- L10: function `batch_predict_embeddings`

## pipeline/data_job/components/load_properties.py

- L10: function `load_properties`

## pipeline/data_job/components/upsert_vector_search.py

- L28: function `upsert_vector_search`

## pipeline/data_job/components/write_embeddings.py

- L10: function `write_embeddings`

## pipeline/data_job/main.py

- L28: function `property_search_embed_pipeline`
- L79: function `build_pipeline_spec`
- L107: function `get_pipeline`
- L111: function `main`

## pipeline/data_job/ports/vector_search_writer.py

- L24: class `EmbeddingDatapoint`
- L37: class `VectorSearchWriter`
- L45: method `upsert` parent=VectorSearchWriter

## pipeline/evaluation_job/main.py

- L22: function `property_search_evaluate_pipeline`
- L32: function `get_pipeline`
- L36: function `main`

## pipeline/labeling_job/main.py

- L18: function `run`
- L63: function `main`

## pipeline/training_dataset_job/main.py

- L13: function `run`
- L34: function `main`

## pipeline/training_job/adapters/kfp_orchestrator.py

- L24: class `_Ref`
- L25: method `__init__` parent=_Ref
- L30: method `name` parent=_Ref
- L34: method `task` parent=_Ref
- L38: class `KFPOrchestrator`
- L39: method `__init__` parent=KFPOrchestrator
- L44: method `add_component` parent=KFPOrchestrator
- L49: method `add_dependency` parent=KFPOrchestrator
- L56: method `compile` parent=KFPOrchestrator
- L65: method `_pipeline_fn` parent=KFPOrchestrator
- L75: method `submit` parent=KFPOrchestrator

## pipeline/training_job/components/evaluate.py

- L7: function `evaluate_reranker`
- L15: function `_log`

## pipeline/training_job/components/load_features.py

- L28: function `load_features`
- L42: function `_log`

## pipeline/training_job/components/register_reranker.py

- L13: function `register_reranker`
- L26: function `_log`

## pipeline/training_job/components/train_reranker.py

- L27: function `train_reranker`
- L48: function `_log`

## pipeline/training_job/main.py

- L44: function `property_search_train_pipeline`
- L105: function `build_pipeline_spec`
- L134: function `get_pipeline`
- L138: function `main`

## pipeline/training_job/ports/pipeline_component.py

- L14: class `PipelineComponent`
- L18: method `name` parent=PipelineComponent
- L20: method `to_runtime_task` parent=PipelineComponent
- L25: class `PipelineComponentRef`
- L33: method `name` parent=PipelineComponentRef

## pipeline/training_job/ports/pipeline_orchestrator.py

- L17: class `PipelineConfig`
- L27: class `PipelineOrchestrator`
- L28: method `add_component` parent=PipelineOrchestrator
- L35: method `add_dependency` parent=PipelineOrchestrator
- L43: method `compile` parent=PipelineOrchestrator
- L47: method `submit` parent=PipelineOrchestrator

## pipeline/workflow/compile.py

- L61: function `compile_pipeline`
- L69: function `_target_path`
- L77: function `_spec`
- L84: function `_pipeline`
- L96: function `_coerce_parameter_value`
- L114: function `_merge_parameter_values`
- L127: function `_submit_pipeline`
- L151: function `submit_pipeline_yaml`
- L168: function `main`

## pipeline/workflow/trigger.py

- L19: function `_env`
- L26: function `_optional_json_env`
- L36: function `_decode_pubsub_message`
- L59: function `_merge_parameters`
- L69: function `_build_job_id`
- L75: function `trigger_pipeline`
- L114: function `submit_pipeline`

## pipeline/workflow/trigger_zip/main.py

- L19: function `_env`
- L26: function `_optional_json_env`
- L36: function `_decode_pubsub_message`
- L59: function `_merge_parameters`
- L69: function `_build_job_id`
- L75: function `trigger_pipeline`
- L114: function `submit_pipeline`

## scripts/_common.py

- L38: function `_load_flat_yaml`
- L68: function `_load_list_setting`
- L113: function `resolve_project_id`
- L135: function `env`
- L157: function `secret`
- L174: function `terraform_var_args`
- L189: function `gcs_bucket_name`
- L198: function `run`
- L232: function `gcloud`
- L238: function `resolve_git_sha`
- L259: function `cloud_run_url`
- L282: function `gateway_url`
- L315: function `identity_token`
- L321: class `ResolvedApiTarget`
- L339: method `call` parent=ResolvedApiTarget
- L360: function `_env_flag`
- L367: function `resolve_api_target`
- L421: function `http_json`
- L461: function `fail`
- L467: function `print_pretty`
- L475: function `submit_cloud_build_async`
- L500: function `wait_cloud_build`
- L509: function `_print_build_diagnostics`

## scripts/adapters/gcloud.py

- L24: function `gcloud_run`

## scripts/adapters/kubectl.py

- L23: function `kubectl_run`

## scripts/adapters/terraform.py

- L22: function `terraform_run`

## scripts/bqml/train_popularity.py

- L17: function `main`

## scripts/ci/layers.py

- L132: class `Violation`
- L140: method `__str__` parent=Violation
- L147: function `_imports_with_lines`
- L160: function `_matches`
- L165: function `_is_excluded`
- L171: function `find_rules_for_file`
- L193: function `find_violations`
- L210: function `discover_files`
- L241: function `main`

## scripts/ci/sync_configmap.py

- L38: function `render`
- L50: function `main`

## scripts/ci/sync_dataform.py

- L35: function `render`
- L53: function `main`

## scripts/deploy/api_gke.py

- L43: function `_step`
- L47: function `_info`
- L51: function `_error`
- L55: function `_diag`
- L68: function `_require`
- L75: function `_ensure_kubectl_context`
- L101: function `_dump_rollout_diagnostics`
- L139: function `main`

## scripts/deploy/api_gke_local.py

- L43: function `_step`
- L47: function `_info`
- L51: function `_error`
- L55: function `_diag`
- L68: function `_require`
- L75: function `_ensure_docker_buildx`
- L88: function `_ensure_ar_auth`
- L107: function `_ensure_kubectl_context`
- L124: function `main`

## scripts/deploy/build_all_local.py

- L50: function `_step`
- L54: function `_build`
- L81: function `main`

## scripts/deploy/build_kserve_images.py

- L53: function `_step`
- L57: function `_info`
- L61: function `_error`
- L65: function `_build_image`
- L103: function `_patch_inference_service_image`
- L122: function `_set_deployment_image`
- L134: function `main`

## scripts/deploy/build_kserve_images_local.py

- L24: function `_step`
- L28: function `_info`
- L32: function `_error`
- L36: function `_require`
- L43: function `_diag`
- L56: function `_ensure_docker_buildx`
- L66: function `_ensure_ar_auth`
- L83: function `_ensure_kubectl_context`
- L94: function `_build_local_image`
- L123: function `_patch_inference_service_image`
- L140: function `_set_deployment_image`
- L150: function `main`

## scripts/deploy/composer_deploy_dags.py

- L39: function `_terraform_output`
- L61: function `_list_top_level_dag_files`
- L75: function `_list_pipeline_pkg_files`
- L96: function `_list_data_files`
- L115: function `main`

## scripts/deploy/composer_runner.py

- L26: function `_step`
- L30: function `_info`
- L34: function `_error`
- L38: function `_require`
- L45: function `main`

## scripts/deploy/configmap_overlay.py

- L25: function `_terraform_output_map`
- L47: function `_feature_online_store_public_domain_from_api`
- L78: function `main`

## scripts/deploy/kserve_models.py

- L42: function `_step`
- L46: function `_info`
- L50: function `_error`
- L55: class `ModelVersion`
- L62: function `_require`
- L69: function `_resolve_latest`
- L139: function `_kubectl_patch`
- L163: function `_patch_reranker_storage_uri`
- L176: function `_patch_encoder_storage_uri`
- L197: function `_dump_diagnostics`
- L237: function `_wait_ready`
- L262: function `main`

## scripts/deploy/monitor.py

- L36: function `_parse_args`
- L77: function `_resolve_log_dir`
- L86: function `_utc_stamp`
- L90: function `_open_log_sink`
- L100: function `_resolve_command`
- L112: function `_build_describe`
- L135: class `MonitorState`
- L146: function `_now_utc`
- L150: function `_maybe_parse_step`
- L166: function `_maybe_parse_build_wait`
- L179: function `_print_heartbeat`
- L210: function `main`

## scripts/deploy/seed_lgbm_model.py

- L46: function `_step`
- L50: function `_info`
- L54: function `_resolve_bucket`
- L63: function `_existing_object_size`
- L85: function `_train_synthetic_model`
- L105: function `_upload`
- L110: function `main`

## scripts/domain/gcp/feature_view_sync.py

- L32: function `_terraform_output_map`
- L50: function `_access_token`
- L58: function `_request_json`
- L75: function `_feature_view_resource`
- L82: function `_latest_sync_name`
- L91: function `_list_syncs`
- L102: function `trigger_and_wait`
- L149: function `main`

## scripts/domain/gcp/gcs_cleanup.py

- L18: function `wipe_bucket`
- L38: function `wipe_all_terraform_managed_buckets`

## scripts/domain/gcp/state_recovery.py

- L156: function `_state_has`
- L169: function `_terraform_import`
- L184: function `_gcloud_json`
- L209: function `_recover_iam_sas`
- L237: function `_bq_exists`
- L247: function `_recover_bq`
- L275: function `_recover_pubsub`
- L322: function `_recover_cloudfunctions`
- L351: function `_recover_eventarc`
- L379: function `_recover_cloud_run`
- L407: function `_recover_artifact_registry`
- L437: function `_recover_secret_manager`
- L457: function `_recover_gcs_buckets`
- L488: function `_aiplatform_get`
- L504: function `_recover_feature_store`
- L591: function `_recover_dataform`
- L640: function `recover_orphan_gcp_resources`
- L672: function `main`

## scripts/domain/gcp/vertex_cleanup.py

- L24: function `undeploy_endpoint_models`
- L67: function `undeploy_all_endpoint_shells`
- L75: function `deployed_index_exists`
- L80: function `deployed_index_state`
- L115: function `undeploy_all_vvs_deployed_indexes`
- L181: function `wait_for_deployed_index_absent`

## scripts/domain/gcp/vertex_feature_store_wait.py

- L27: function `_access_token`
- L39: function `_rest_get`
- L54: function `_feature_group_ids`
- L67: function `_feature_online_store_ids`
- L80: function `wait_until_feature_store_names_released`
- L125: function `wait_until_feature_store_names_released_from_env`

## scripts/domain/gcp/vertex_import.py

- L28: function `_state_has`
- L40: function `_gcloud_first`
- L56: function `_terraform_import`
- L71: function `import_persistent_vvs_resources`

## scripts/domain/k8s/elasticsearch_wait.py

- L43: function `_read_health`
- L59: function `_read_phase`
- L74: function `wait_until_es_healthy`

## scripts/domain/k8s/kube_cleanup.py

- L27: function `delete_orphan_workloads`

## scripts/domain/k8s/kubectl_context.py

- L29: function `ensure`
- L45: function `wait_until_api_ready`

## scripts/domain/terraform/lock.py

- L38: function `should_auto_force_unlock`
- L47: function `parse_terraform_lock_id`
- L59: function `is_state_lock_error`
- L63: function `run_terraform_streaming_with_lock_retry`
- L119: function `_run_stream_capture`

## scripts/domain/terraform/stage_apply.py

- L40: function `terraform_apply_stage1_with_retries`

## scripts/domain/terraform/state.py

- L19: function `state_list`
- L42: function `state_size`
- L53: function `addresses_starting_with`
- L67: function `is_in_state`
- L72: function `filter_targets_in_state`
- L86: function `state_rm`

## scripts/lib/bq_property_rows.py

- L10: function `load_properties_cleaned_rows`

## scripts/lib/config.py

- L57: function `generate_configmap_data`
- L97: function `render_configmap_yaml`

## scripts/lib/makefile_help.py

- L18: function `_format`
- L22: function `main`

## scripts/lib/step_timing.py

- L32: function `fmt_duration`
- L44: function `record`
- L67: function `_trim`
- L81: function `baselines`
- L103: function `print_eta`

## scripts/ops/accuracy_report.py

- L15: class `EvalCase`
- L23: function `_default_cases_path`
- L38: function `_load_cases`
- L90: function `_dcg_binary`
- L98: function `_ndcg_at_k_binary`
- L106: function `_hit_rate_at_k_binary`
- L110: function `_mrr_at_k_binary`
- L117: function `main`

## scripts/ops/check_retrain.py

- L14: function `_diag`
- L19: function `main`

## scripts/ops/composer_dag.py

- L24: function `_resolve`
- L28: function `_build_gcloud_cmd`
- L47: function `_parse_args`
- L74: function `main`

## scripts/ops/composer_task_states.py

- L22: function `_balanced_array_from`
- L52: function `extract_json_array`
- L71: function `_gcloud_composer`
- L95: function `_latest_run_id_from_list_runs`
- L105: function `fetch_task_states_json`
- L134: function `main`

## scripts/ops/destroy_check.py

- L42: class `Finding`
- L49: function `_parse_args`
- L62: function `_looks_like_api_disabled`
- L66: function `_run_json`
- L89: function `_run_bq_json`
- L108: function `_pluck`
- L117: function `_collect_gke_clusters`
- L124: function `_collect_cloud_run_services`
- L139: function `_collect_dataflow_jobs`
- L155: function `_collect_vertex_endpoints`
- L177: function `_collect_cloud_functions`
- L191: function `_collect_eventarc_triggers`
- L198: function `_collect_pubsub_topics`
- L210: function `_collect_pubsub_subscriptions`
- L229: function `_collect_buckets`
- L236: function `_collect_artifact_repos`
- L256: function `_collect_bq_datasets`
- L267: function `_classify_bucket_names`
- L284: function `_classify_artifact_repos`
- L295: function `_filter_high_cost_datasets`
- L299: function `_evaluate`
- L307: function `_render_text`
- L318: function `_render_json`
- L331: function `collect_findings`
- L382: function `main`

## scripts/ops/feedback.py

- L13: function `main`

## scripts/ops/label_seed.py

- L26: function `main`

## scripts/ops/livez.py

- L11: function `main`

## scripts/ops/promote.py

- L48: function `_log`
- L52: function `_resolve_display_name`
- L70: function `_list_versions`
- L76: function `_model_id_of`
- L81: function `_select_version`
- L124: function `_gsutil_ls`
- L133: function `_bst_rename_if_needed`
- L161: function `_set_production_alias`
- L179: function `_run_alias`
- L245: function `_env_fallback`
- L257: function `_env_flag`
- L262: function `main`

## scripts/ops/ranking.py

- L14: function `main`

## scripts/ops/register_model.py

- L24: function `_latest_pipeline_run`
- L40: function `_resolve_model_uri_from_gcs`
- L93: function `_upload_model`
- L123: function `main`

## scripts/ops/run_all.py

- L52: function `_run_make`
- L56: function `main`

## scripts/ops/search.py

- L15: function `_search_once`
- L20: function `main`

## scripts/ops/search_components.py

- L18: function `_diagnose_semantic_zero`
- L39: function `main`

## scripts/ops/slo_status.py

- L25: function `_terraform_output`
- L46: function `_default_service_id`
- L50: function `_describe_slo`
- L58: function `_burn_rate`
- L88: function `main`

## scripts/ops/submit_train_pipeline.py

- L25: function `main`

## scripts/ops/sync_elasticsearch.py

- L32: function `_log`
- L37: function `_headers`
- L45: function `_ensure_index`
- L74: function `_bulk_upsert`
- L106: function `_parse_args`
- L123: function `_maybe_port_forward_for_cluster_dns`
- L171: function `_run_sync_with_count`
- L225: function `run`
- L236: function `main`

## scripts/ops/sync_synonyms.py

- L35: function `_log`
- L39: function `_gcloud`
- L56: function `_resolve_redis_url`
- L96: function `_resolve_redis_auth`
- L117: function `_parse_args`
- L170: function `_load_dictionary`
- L186: function `main`

## scripts/ops/vertex/explain.py

- L26: function `main`

## scripts/ops/vertex/feature_group.py

- L39: function `_access_token`
- L47: function `_request_json`
- L59: function `_emit_404_diagnostics`
- L101: function `_canonical_feature_view_name`
- L115: function `main`

## scripts/ops/vertex/models_list.py

- L23: function `main`

## scripts/ops/vertex/monitoring.py

- L28: function `main`

## scripts/ops/vertex/pipeline_status.py

- L24: function `main`

## scripts/ops/vertex/pipeline_wait.py

- L24: function `_state_name`
- L40: function `_latest_job`
- L51: function `main`

## scripts/ops/vertex/vector_search.py

- L35: function `_terraform_output_map`
- L51: function `_build_probe_vector`
- L57: function `main`

## scripts/setup/backfill_vector_search_index.py

- L51: class `BackfillSpec`
- L59: function `_terraform_output_map`
- L74: function `build_spec`
- L116: function `_bq_iter_rows`
- L128: function `_to_datapoints`
- L138: function `_build_writer`
- L151: function `main`

## scripts/setup/create_schedule.py

- L12: function `build_schedule_specs`
- L47: function `main`

## scripts/setup/deploy_all.py

- L99: class `DeployStep`
- L115: function `_step`
- L131: function `_elapsed_since_step_start`
- L135: function `_step_done`
- L144: function `_run_tf_bootstrap`
- L148: function `_run_tf_init`
- L152: function `_run_recover_wif`
- L156: function `_run_sync_dataform`
- L160: function `_run_tf_plan`
- L164: function `_run_tf_apply`
- L168: function `_run_seed_lgbm_model`
- L172: function `_run_seed_test`
- L176: function `_run_sync_elasticsearch`
- L193: function `_run_trigger_feature_view_sync`
- L197: function `_run_backfill_vvs`
- L201: function `_run_apply_manifests`
- L216: function `_run_overlay_configmap`
- L220: function `_run_composer_deploy_dags`
- L224: function `_run_deploy_api`
- L228: function `_steps`
- L316: function `_parse_args`
- L333: function `_resolve_step_ref`
- L347: function `main`

## scripts/setup/destroy_all.py

- L141: class `DestroyStep`
- L161: function `_step`
- L177: function `_elapsed_since_step_start`
- L181: function `_step_done`
- L193: function `_common_vars`
- L203: function `_run_seed_clean`
- L207: function `_run_undeploy_vertex_endpoints`
- L215: function `_run_undeploy_vvs_deployed_indexes`
- L227: function `_run_state_rm_persistent_vvs`
- L249: function `_run_wipe_gcs_buckets`
- L256: function `_run_flip_deletion_protection`
- L289: function `_run_destroy_kserve`
- L333: function `_run_destroy_main`
- L383: function `_steps`
- L436: function `_parse_args`
- L453: function `_resolve_step_ref`
- L470: function `main`

## scripts/setup/doctor.py

- L27: function `_version`
- L33: function `main`

## scripts/setup/local_hybrid.py

- L37: function `_log`
- L41: function `_http_available`
- L56: function `_resolve_elasticsearch_url`
- L71: function `_resolve_elasticsearch_api_key`
- L80: function `_ensure_local_reranker_model`
- L92: function `_wait_http`
- L107: function `_port_in_use`
- L113: function `_spawn`
- L117: function `main`

## scripts/setup/print_github_variables.py

- L39: function `build_variable_rows`
- L54: function `build_gh_commands`
- L67: function `main`

## scripts/setup/recover_wif.py

- L38: function `_gcloud_capture`
- L53: function `recover`
- L163: function `main`

## scripts/setup/seed_minimal.py

- L41: function `_store_and_load_properties`
- L86: function `_vec_literal`
- L94: function `_bq`
- L107: function `main`

## scripts/setup/seed_minimal_clean.py

- L24: function `main`

## scripts/setup/setup_model_monitoring.py

- L22: function `build_monitoring_spec`
- L47: function `main`

## scripts/setup/tf_apply.py

- L42: function `main`

## scripts/setup/tf_bootstrap.py

- L32: function `main`

## scripts/setup/tf_init.py

- L17: function `main`

## scripts/setup/tf_plan.py

- L25: function `main`

## scripts/setup/upload_encoder_assets.py

- L33: function `build_upload_spec`
- L48: function `_download_model`
- L57: function `_iter_local_files`
- L61: function `_upload_directory`
- L84: function `_apply`
- L98: function `main`

## scripts/verify/_runner.py

- L20: function `_resolve_log_dir`
- L34: function `_utc_stamp`
- L38: function `_update_symlink`
- L45: function `run`

## scripts/verify/deploy_all.py

- L8: function `main`

## scripts/verify/destroy_all.py

- L8: function `main`

## scripts/verify/full_recreate.py

- L18: function `main`

## scripts/verify/live_acceptance.py

- L17: function `main`

## system_map.html

- L89: class `wrap`
- L92: class `subtitle`
- L96: class `panel`
- L102: class `stack-chip`
- L103: class `stack-chip`
- L104: class `stack-chip`
- L105: class `stack-chip`
- L106: class `stack-chip`
- L107: class `stack-chip`
- L108: class `stack-chip`
- L109: class `stack-chip`
- L116: class `tag web`
- L117: class `tag web`
- L118: class `tag web`
- L119: class `tag pipeline`
- L120: class `tag pipeline`
- L121: class `tag pipeline`
- L122: class `tag pipeline`
- L123: class `tag cli`
- L124: class `tag cli`
- L125: class `tag cli`
- L126: class `tag pipeline`
- L127: class `tag pipeline`
- L128: class `tag pipeline`
- L129: class `tag pipeline`
- L130: class `tag cli`
- L131: class `tag cli`
- L132: class `tag cli`
- L133: class `tag cli`
- L142: class `module`
- L143: class `tag domain`
- L144: class `resp`
- L145: class `deps`
- L146: class `deps`
- L148: class `module`
- L149: class `tag domain`
- L150: class `resp`
- L151: class `deps`
- L153: class `module`
- L154: class `tag domain`
- L155: class `resp`
- L157: class `module`
- L158: class `tag domain`
- L159: class `resp`
- L161: class `module`
- L162: class `tag domain`
- L163: class `resp`
- L165: class `module`
- L166: class `tag domain`
- L167: class `resp`
- L169: class `module`
- L170: class `tag domain`
- L171: class `resp`
- L176: class `module`
- L177: class `tag usecase`
- L178: class `resp`
- L179: class `deps`
- L181: class `module`
- L182: class `tag usecase`
- L183: class `resp`
- L185: class `module`
- L186: class `tag usecase`
- L187: class `resp`
- L189: class `module`
- L190: class `tag usecase`
- L191: class `resp`
- L193: class `module`
- L194: class `tag usecase`
- L195: class `resp`
- L200: class `module`
- L201: class `tag port`
- L202: class `resp`
- L204: class `module`
- L205: class `tag port`
- L206: class `resp`
- L211: class `grid-2`
- L212: class `module`
- L213: class `module`
- L214: class `module`
- L215: class `module`
- L216: class `module`
- L217: class `module`
- L218: class `module`
- L219: class `module`
- L220: class `module`
- L221: class `module`
- L222: class `module`
- L223: class `module`
- L224: class `module`
- L225: class `module`
- L226: class `module`
- L227: class `module`
- L228: class `module`
- L229: class `module`
- L230: class `module`
- L231: class `module`
- L236: class `module`
- L237: class `tag composition_root`
- L238: class `resp`
- L239: class `deps`
- L241: class `module`
- L242: class `tag composition_root`
- L243: class `resp`
- L245: class `module`
- L246: class `tag composition_root`
- L247: class `resp`
- L249: class `module`
- L250: class `tag composition_root`
- L251: class `resp`
- L256: class `module`
- L257: class `tag web`
- L258: class `resp`
- L260: class `row`
- L261: class `tag web`
- L262: class `tag web`
- L264: class `module`
- L265: class `tag web`
- L266: class `resp`
- L268: class `module`
- L269: class `tag web`
- L270: class `resp`
- L275: class `module`
- L276: class `tag cli`
- L277: class `resp`
- L279: class `module`
- L280: class `tag cli`
- L281: class `resp`
- L283: class `module`
- L284: class `tag cli`
- L285: class `resp`
- L287: class `module`
- L288: class `tag cli`
- L289: class `resp`
- L294: class `module`
- L295: class `module`
- L296: class `module`
- L297: class `module`
- L298: class `module`
- L299: class `module`
- L300: class `module`
- L304: class `module`
- L305: class `module`
- L306: class `module`
- L313: class `external`
- L314: class `flow-steps`
- L328: class `external`
- L332: class `external`
- L333: class `flow-steps`
- L339: class `external`
- L343: class `external`
- L344: class `flow-steps`
- L351: class `external`
- L355: class `external`
- L356: class `flow-steps`
- L366: class `external`
- L370: class `external`
- L371: class `flow-steps`
- L376: class `external`
- L380: class `external`
- L381: class `flow-steps`
- L386: class `external`
- L390: class `external`
- L391: class `flow-steps`
- L397: class `external`
- L401: class `external`
- L402: class `flow-steps`
- L407: class `external`
- L411: class `external`
- L412: class `flow-steps`
- L417: class `external`
- L421: class `external`
- L422: class `flow-steps`
- L428: class `external`
- L433: class `panel`
- L440: class `small`
- L444: class `small`
- L448: class `small`
- L462: class `small`
- L482: class `panel`
- L484: class `risk-row`
- L485: class `risk-row`
- L486: class `risk-row`
- L487: class `risk-row`
- L488: class `risk-row`
- L489: class `risk-row`
- L490: class `risk-row`
- L491: class `risk-row`
- L492: class `risk-row`
- L493: class `risk-row`
- L494: class `risk-row`
- L495: class `risk-row`
- L498: class `panel`
- L511: class `spacer`
- L512: class `small`

## tests/_fakes/in_memory_candidate_retriever.py

- L10: class `InMemoryCandidateRetriever`
- L18: method `__init__` parent=InMemoryCandidateRetriever
- L22: method `retrieve` parent=InMemoryCandidateRetriever
- L41: class `_RetrieveCall`
- L44: method `__init__` parent=_RetrieveCall

## tests/_fakes/in_memory_event_writer.py

- L7: class `InMemoryEventWriter`
- L8: method `__init__` parent=InMemoryEventWriter
- L14: method `emit_search_event` parent=InMemoryEventWriter
- L38: method `emit_impression` parent=InMemoryEventWriter
- L66: method `emit_user_action` parent=InMemoryEventWriter
- L84: method `_raise_if_needed` parent=InMemoryEventWriter

## tests/_fakes/in_memory_feature_fetcher.py

- L15: class `InMemoryFeatureFetcher`
- L18: method `__init__` parent=InMemoryFeatureFetcher
- L22: method `fetch` parent=InMemoryFeatureFetcher

## tests/_fakes/in_memory_feedback_recorder.py

- L11: class `FeedbackEvent`
- L17: class `InMemoryFeedbackRecorder`
- L18: method `__init__` parent=InMemoryFeedbackRecorder
- L22: method `record` parent=InMemoryFeedbackRecorder

## tests/_fakes/in_memory_lexical_search.py

- L10: class `InMemoryLexicalSearch`
- L18: method `__init__` parent=InMemoryLexicalSearch
- L22: method `search` parent=InMemoryLexicalSearch
- L36: class `_LexicalCall`
- L39: method `__init__` parent=_LexicalCall

## tests/_fakes/in_memory_metrics_repository.py

- L11: class `InMemoryMetricsRepository`
- L12: method `__init__` parent=InMemoryMetricsRepository
- L15: method `write_evaluation_metrics` parent=InMemoryMetricsRepository
- L18: method `read_evaluation_metrics` parent=InMemoryMetricsRepository
- L35: method `latest_metrics` parent=InMemoryMetricsRepository
- L46: method `metrics` parent=InMemoryMetricsRepository

## tests/_fakes/in_memory_ranking_log_publisher.py

- L12: class `RankingLogCall`
- L20: class `InMemoryRankingLogPublisher`
- L21: method `__init__` parent=InMemoryRankingLogPublisher
- L24: method `publish_candidates` parent=InMemoryRankingLogPublisher

## tests/_fakes/in_memory_semantic_search.py

- L10: class `InMemorySemanticSearch`
- L17: method `__init__` parent=InMemorySemanticSearch
- L27: method `search` parent=InMemorySemanticSearch
- L44: class `_SemanticCall`
- L47: method `__init__` parent=_SemanticCall

## tests/_fakes/in_memory_training_dataset_repository.py

- L11: class `InMemoryTrainingDatasetRepository`
- L12: method `__init__` parent=InMemoryTrainingDatasetRepository
- L15: method `write_training_dataset` parent=InMemoryTrainingDatasetRepository
- L18: method `read_training_dataset` parent=InMemoryTrainingDatasetRepository
- L25: method `latest_training_dataset` parent=InMemoryTrainingDatasetRepository
- L30: method `refs` parent=InMemoryTrainingDatasetRepository

## tests/_fakes/mock_prediction_publisher.py

- L8: class `MockPredictionPublisher`
- L9: method `__init__` parent=MockPredictionPublisher
- L13: method `publish` parent=MockPredictionPublisher

## tests/_fakes/mock_reranker_client.py

- L6: class `MockRerankerClient`
- L17: method `__init__` parent=MockRerankerClient
- L32: method `_scores` parent=MockRerankerClient
- L38: method `predict` parent=MockRerankerClient
- L42: method `predict_with_explain` parent=MockRerankerClient

## tests/_fakes/stub_encoder_client.py

- L10: class `StubEncoderClient`
- L20: method `__init__` parent=StubEncoderClient
- L32: method `embed` parent=StubEncoderClient
- L37: class `_EncoderCall`
- L40: method `__init__` parent=_EncoderCall
- L44: method `__repr__` parent=_EncoderCall

## tests/_fakes/stub_popularity_scorer.py

- L8: class `StubPopularityScorer`
- L9: method `__init__` parent=StubPopularityScorer
- L13: method `score` parent=StubPopularityScorer

## tests/_fakes/stub_retrain_queries.py

- L10: class `StubRetrainQueries`
- L18: method `__init__` parent=StubRetrainQueries
- L31: method `last_run_finished_at` parent=StubRetrainQueries
- L34: method `feedback_rows_since` parent=StubRetrainQueries
- L38: method `ndcg_in_window` parent=StubRetrainQueries

## tests/conftest.py

- L51: class `_StubDataCatalogReader`
- L52: method `read_snapshot` parent=_StubDataCatalogReader
- L74: function `fake_settings`
- L95: function `fake_encoder`
- L100: function `fake_reranker`
- L105: function `fake_candidate_retriever`
- L110: function `fake_ranking_log_publisher`
- L115: function `fake_feedback_recorder`
- L120: function `fake_event_writer`
- L125: function `fake_retrain_queries`
- L130: function `fake_retrain_publisher`
- L135: function `fake_feature_fetcher`
- L146: function `fake_container_factory`
- L161: function `test_x` (test)
- L168: function `_build`
- L229: function `fake_container`
- L236: function `fake_app`
- L263: function `fake_client`

## tests/e2e/live_acceptance_checks.py

- L15: function `run_live_acceptance_checks`
- L53: function `_run`

## tests/e2e/test_full_recreate_gate.py

- L37: function `_require_full_recreate` (test)
- L45: function `_run` (test)
- L60: function `test_full_recreate_acceptance_live` (test)

## tests/e2e/test_live_acceptance_gate.py

- L33: function `_require_acceptance_env` (test)
- L38: function `test_live_acceptance_on_existing_env` (test)

## tests/integration/infra/test_destroy_all_table_parity.py

- L35: function `_resources_with_deletion_protection` (test)
- L55: function `_destroy_all_targets` (test)
- L61: function `_destroy_bq_table_names` (test)
- L69: function `_destroy_gke_cluster_names` (test)
- L77: function `test_every_protected_bq_table_is_in_destroy_all_targets` (test)
- L92: function `test_destroy_all_bq_targets_do_not_reference_removed_tables` (test)
- L106: function `test_protected_gke_cluster_is_in_destroy_all_targets` (test)
- L123: function `test_protected_targets_baseline` (test)

## tests/integration/infra/test_infra_ranker_tables.py

- L27: function `_read` (test)
- L31: function `_extract_resource_block` (test)
- L54: function `test_property_features_daily_declared` (test)
- L61: function `test_property_embeddings_declared_with_repeated_float64` (test)
- L72: function `test_search_logs_declared` (test)
- L81: function `test_ranking_log_declared_with_dual_cluster` (test)
- L93: function `test_feedback_events_declared` (test)
- L99: function `test_search_events_declared` (test)
- L105: function `test_search_impressions_declared` (test)
- L111: function `test_user_actions_declared` (test)
- L118: function `test_ranking_labels_declared` (test)
- L127: function `test_training_runs_metrics_has_ranker_columns` (test)
- L134: function `test_training_runs_hyperparams_has_lambdarank_fields` (test)
- L142: function `test_legacy_predictions_log_removed` (test)

## tests/integration/infra/test_makefile.py

- L8: function `test_makefile_declares_destroy_coast_down_target` (test)

## tests/integration/infra/test_manifests_structure.py

- L28: function `_load` (test)
- L40: function `test_kustomization_lists_every_yaml_under_manifests` (test)
- L59: function `test_search_api_deployment_resource_limits_match_nonnegotiable` (test)
- L79: function `test_search_api_deployment_exposes_kserve_env_vars` (test)
- L120: function `test_search_api_secretstore_uses_gcpsm_provider` (test)
- L128: function `test_search_api_external_secret_syncs_iap_client_secret` (test)
- L143: function `test_search_api_deployment_probes_have_canonical_paths` (test)
- L172: function `test_search_api_hpa_bounds_and_thresholds` (test)
- L192: function `test_search_api_networkpolicy_allows_egress_to_kserve_inference` (test)
- L218: function `test_kserve_inferenceservice_has_correct_shape` (test)
- L233: function `test_kserve_reranker_uses_lightgbm_model_format` (test)
- L243: function `test_kserve_networkpolicy_restricts_ingress_to_search_namespace` (test)
- L264: function `test_search_api_iap_policy_targets_gateway_service_with_gcp_backend_policy` (test)
- L286: function `test_configmap_example_covers_expected_keys` (test)

## tests/integration/infra/test_public_domain_consistency.py

- L28: function `_read` (test)
- L32: function `_setting_value` (test)
- L46: function `test_setting_yaml_holds_canonical_domain_and_zone` (test)
- L55: function `test_gateway_manifest_uses_setting_public_domain_and_certmap` (test)
- L76: function `test_dns_module_has_static_ip_apex_a_and_cert_manager_chain` (test)
- L97: function `test_dns_module_defaults_match_gateway_annotation` (test)
- L107: function `test_dev_main_wires_dns_module_and_passes_public_domain_everywhere` (test)
- L125: function `test_apis_tf_enables_cloud_dns` (test)
- L131: function `test_variables_tf_declares_public_domain_and_zone_without_default` (test)
- L140: function `test_canonical_tf_var_names_includes_public_domain_and_zone` (test)
- L151: function `test_makefile_exports_public_domain_and_zone` (test)
- L160: function `test_tf_plan_feeds_terraform_the_canonical_var_set` (test)
- L180: function `test_tf_apply_stage1_targets_includes_module_dns` (test)
- L190: function `test_build_all_local_is_single_line_script_call` (test)

## tests/integration/infra/test_terraform_module_structure.py

- L27: function `_modules` (test)
- L33: function `test_module_has_required_file` (test)
- L41: function `test_every_variable_has_description` (test)

## tests/integration/infra/test_workflows_structure.py

- L40: function `test_workflow_file_exists` (test)
- L47: function `test_retired_workflows_are_absent` (test)
- L68: function `test_deploy_workflows_request_oidc_token` (test)
- L75: function `test_encoder_image_workflow_paths` (test)
- L81: function `test_reranker_image_workflow_paths` (test)
- L87: function `test_trainer_image_workflow_paths` (test)
- L93: function `test_pipeline_workflow_paths` (test)
- L102: function `test_api_workflow_keeps_broad_filter_and_rolls_out_via_kubectl` (test)

## tests/integration/parity/parity_invariant.py

- L35: function `read_text`
- L40: function `flat_yaml`
- L54: function `extract_terraform_block`

## tests/integration/parity/test_api_route_prefixes.py

- L54: function `app_no_lifespan` (test)
- L66: class `_NoopContainer`
- L69: function `_build` (test)
- L81: function `_all_paths` (test)
- L91: function `_classify` (test)
- L103: function `test_all_routes_belong_to_a_known_axis` (test)
- L117: function `test_canonical_public_endpoints_exist` (test)
- L124: function `test_canonical_ops_endpoints_exist` (test)
- L139: function `test_legacy_paths_redirect_to_new_prefix` (test)
- L158: function `test_probes_are_not_namespaced` (test)
- L170: function `test_metrics_endpoint_at_root` (test)
- L176: function `test_legacy_redirects_excluded_from_openapi_schema` (test)
- L183: function `test_canonical_paths_appear_in_openapi_schema` (test)
- L197: function `test_route_iap_policy_documents_prefix_axes` (test)

## tests/integration/parity/test_codebase_invariants.py

- L44: function `_walk_files` (test)
- L57: function `_find_substring_hits` (test)
- L71: function `test_w2_8_legacy_tokens_absent_in_python_trees` (test)
- L81: function `test_w2_8_legacy_tokens_absent_in_manifests_yaml` (test)
- L91: function `test_lexical_es_canonical_no_meilisearch_in_app` (test)
- L101: function `test_makefile_has_no_removed_sync_meili_target` (test)
- L108: function `test_pyproject_has_no_sync_meili_console_script` (test)
- L115: function `test_search_api_deployment_has_no_meili_env_refs` (test)
- L121: function `test_es_networkpolicy_allows_eck_operator_namespace` (test)
- L139: function `test_es_manifest_pins_http_and_anonymous_auth` (test)

## tests/integration/parity/test_configmap_drift.py

- L37: function `test_committed_configmap_matches_generator_output` (test)
- L46: function `test_configmap_keys_cover_every_deployment_reference` (test)
- L80: function `test_generated_configmap_keeps_deployment_referenced_keys` (test)

## tests/integration/parity/test_dataform_workflow_settings.py

- L21: function `test_generator_includes_every_required_dataform_key` (test)
- L34: function `test_generator_values_match_setting_yaml` (test)
- L52: function `test_setting_yaml_has_all_required_keys` (test)

## tests/integration/parity/test_event_schema_parity.py

- L51: function `test_app_emit_keys_match_domain_action_type` (test)
- L60: function `test_app_emit_keys_match_pydantic_feedback_request` (test)
- L75: function `test_app_emit_keys_match_terraform_user_actions_description` (test)
- L91: function `test_terraform_user_actions_description_excludes_synthetic` (test)
- L110: function `_load_synthetic_yaml` (test)
- L120: function `test_synthetic_yaml_action_types_match_policy` (test)
- L128: function `test_synthetic_yaml_weights_match_policy` (test)
- L138: function `test_synthetic_yaml_label_source_format` (test)
- L154: function `test_action_weights_is_app_emit_union_synthetic_no_overlap` (test)
- L168: function `test_canonical_weight_values_pinned` (test)
- L191: function `test_evaluation_metrics_table_declared` (test)
- L221: function `test_ranking_labels_description_documents_label_source_canonical` (test)

## tests/integration/parity/test_feature_parity_feature_group.py

- L31: function `_extract_feature_group_block` (test)
- L41: function `_extract_feature_group_names` (test)
- L45: function `_extract_feature_group_value_types` (test)
- L49: function `test_vertex_feature_group_order_matches_property_side_cols` (test)
- L57: function `test_vertex_feature_group_uses_double_features` (test)

## tests/integration/parity/test_feature_parity_ranking.py

- L37: function `_extract_ranking_log_fields` (test)
- L50: function `test_feature_cols_ranker_has_ten_columns` (test)
- L54: function `test_feature_cols_ranker_no_duplicates` (test)
- L61: function `test_build_ranker_features_keys_match_schema_exactly` (test)
- L82: function `test_infra_ranking_log_features_order_matches_schema` (test)
- L90: function `test_infra_ranking_log_features_are_float64_nullable` (test)
- L104: function `test_dataform_property_features_has_behavioral_cols` (test)

## tests/integration/parity/test_feature_parity_sql_ranker.py

- L28: function `_extract_unpivot_feature_lists` (test)
- L38: function `test_ranker_sql_file_exists` (test)
- L42: function `test_ranker_sql_has_both_unpivots` (test)
- L50: function `test_ranker_unpivot_matches_property_side_cols` (test)
- L61: function `test_ranker_sql_reads_ranking_log_not_predictions_log` (test)

## tests/integration/pipeline/test_pipeline_compile.py

- L10: function `test_build_embed_pipeline_spec_contains_expected_steps` (test)
- L17: function `test_build_train_pipeline_spec_contains_expected_steps` (test)
- L29: function `test_coerce_parameter_value_handles_primitives_and_json` (test)
- L37: function `test_merge_parameter_values_overrides_defaults` (test)

## tests/integration/workflow/conftest.py

- L38: function `read_repo_file`

## tests/integration/workflow/test_composer_dags_contract.py

- L24: function `test_dag_files_have_valid_python_syntax` (test)
- L35: function `test_dag_files_pin_canonical_schedule_and_dag_id` (test)
- L50: function `test_dag_schedules_are_valid_5_field_cron` (test)
- L67: function `test_dag_schedules_avoid_simultaneous_run` (test)
- L89: function `test_dag_files_avoid_kfp_2_16_module_level_compile_import` (test)
- L97: function `test_retrain_dag_is_canonical_retrain_trigger` (test)
- L112: function `test_dag_files_call_only_existing_scripts` (test)
- L134: function `test_layers_rules_isolate_pipeline_dags_from_app_imports` (test)

## tests/integration/workflow/test_composer_gcloud_json_contract.py

- L18: function `test_extract_json_array_skips_executing_command_prologue` (test)
- L32: function `test_extract_json_array_prefers_array_of_objects_over_inner_brackets` (test)
- L40: function `test_extract_json_array_handles_empty_array` (test)
- L46: function `test_latest_run_id_from_list_runs_finds_manual_run_id` (test)
- L55: function `test_balanced_array_respects_string_literals_with_brackets` (test)
- L65: function `test_extract_json_array_missing_array_raises` (test)

## tests/integration/workflow/test_composer_module_contract.py

- L22: function `test_composer_module_exists_with_required_files` (test)
- L29: function `test_composer_module_uses_gen3_image_with_enable_flag_gate` (test)
- L47: function `test_composer_env_variables_avoid_reserved_names` (test)
- L84: function `test_composer_image_version_is_known_supported_form` (test)
- L94: function `test_composer_environment_uses_correct_region_var` (test)
- L104: function `test_composer_environment_has_proper_create_destroy_timeouts` (test)
- L111: function `test_composer_workloads_have_max_count_to_bound_cost` (test)
- L126: function `test_composer_module_workloads_config_has_scheduler_web_worker` (test)
- L132: function `test_composer_module_outputs_dag_bucket_and_airflow_uri` (test)
- L142: function `test_composer_module_wired_into_dev_environment_with_correct_depends_on` (test)
- L154: function `test_composer_module_passes_required_terraform_inputs` (test)
- L176: function `test_dev_environment_has_composer_variables_and_outputs` (test)
- L195: function `test_enable_composer_default_is_flipped_to_true` (test)
- L206: function `test_iam_module_provisions_sa_composer_with_required_roles` (test)
- L229: function `test_composer_sa_used_in_workload_identity_binding_chain` (test)
- L242: function `test_composer_sa_email_consumed_by_module` (test)
- L247: function `test_tf_apply_stage1_targets_includes_module_composer` (test)
- L254: function `test_composer_deploy_dags_step_inserted_between_overlay_and_deploy_api` (test)
- L270: function `test_deploy_all_step_runner_imports_composer_deploy_dags` (test)
- L280: function `test_composer_deploy_dags_early_returns_when_disabled` (test)
- L286: function `_fake_run` (test)
- L294: function `test_composer_deploy_dags_uses_gsutil_m_for_parallel_upload` (test)
- L299: function `test_composer_dag_bucket_terraform_output_consumed_by_deploy_script` (test)
- L311: function `test_makefile_exposes_composer_deploy_dags_and_smoke_targets` (test)
- L329: function `test_composer_runner_dockerfile_does_not_bake_setting_yaml` (test)
- L343: function `test_make_composer_env_default_matches_terraform_default` (test)
- L363: function `test_pyproject_does_not_pull_apache_airflow_into_runtime` (test)

## tests/integration/workflow/test_deploy_all_contract.py

- L26: function `test_deploy_all_step_sequence_pins_one_shot_pdca_contract` (test)
- L50: function `test_deploy_all_seed_test_runs_before_feature_view_sync` (test)
- L68: function `test_deploy_all_overlay_configmap_runs_before_deploy_api` (test)
- L77: function `test_configmap_overlay_injects_live_vertex_outputs` (test)
- L84: function `_fake_generate` (test)
- L126: function `test_configmap_overlay_fills_fos_endpoint_from_api_when_terraform_empty` (test)
- L135: function `_fake_generate` (test)
- L171: function `test_local_boot_contract_does_not_require_adc_when_search_disabled` (test)
- L178: function `_forbidden` (test)
- L198: function `test_run_all_core_pins_canonical_validation_path` (test)
- L240: function `test_wait_for_deployed_index_absent_is_idempotent_on_resume` (test)
- L259: function `test_deploy_all_waits_vertex_feature_store_and_retries_stage1_on_409` (test)
- L271: function `test_run_all_core_steps_all_have_makefile_targets` (test)

## tests/integration/workflow/test_destroy_all_contract.py

- L15: function `test_destroy_all_keeps_pdca_reproducibility_guards` (test)
- L30: function `test_destroy_all_destroy_apply_symmetry` (test)
- L56: function `test_destroy_all_undeploys_vertex_endpoint_models_before_destroy` (test)
- L67: function `test_destroy_all_proactively_undeploys_stale_vvs_indexes` (test)
- L85: function `test_destroy_all_flips_bq_deletion_protection_before_destroy` (test)
- L105: function `test_destroy_all_force_destroys_blocking_gcs_buckets` (test)
- L113: function `test_recover_wif_handles_soft_delete_undelete` (test)
- L127: function `test_sync_elasticsearch_step_waits_for_es_health_first` (test)
- L179: function `test_destroy_all_provides_step_slicing_symmetric_with_deploy_all` (test)
- L228: function `test_tf_apply_invokes_recover_wif_as_pre_step` (test)
- L255: function `test_destroy_all_persists_vvs_index_and_endpoint` (test)
- L316: function `test_no_vertex_pipeline_job_schedule_resource_in_terraform` (test)
- L340: function `test_runbook_documents_emergency_kill_switch_for_composer_gke_cloudrun` (test)
- L368: function `test_runbook_documents_orphan_state_cleanup_after_emergency_delete` (test)
- L394: function `test_deploy_all_invokes_state_recovery_before_tf_apply` (test)
- L454: function `test_state_recovery_iam_sa_mapping_matches_terraform` (test)
- L478: function `test_runbook_warns_against_bare_state_rm_without_state_recovery` (test)
- L501: function `test_destroy_all_lessons_learned_documented_in_roadmap` (test)

## tests/integration/workflow/test_docs_canonical_contract.py

- L20: function `test_canonical_docs_describe_workflow_contract_goals` (test)
- L75: function `test_composer_canonical_doc_section_exists` (test)
- L97: function `test_cost_estimate_documented_in_runbook` (test)

## tests/integration/workflow/test_elasticsearch_workflow_contract.py

- L12: function `test_makefile_exposes_sync_elasticsearch_canonical_target` (test)
- L20: function `test_run_all_core_keeps_sync_elasticsearch_before_search_smokes` (test)
- L35: function `test_deploy_all_sync_elasticsearch_step_wiring_stays_canonical` (test)
- L48: function `test_docs_runbook_and_catalog_pin_elasticsearch_workflow` (test)

## tests/integration/workflow/test_ground_truth_contract.py

- L17: function `test_makefile_exposes_ground_truth_targets` (test)
- L44: function `test_kserve_dockerfiles_use_split_ml_extras` (test)
- L57: function `test_training_pipeline_contract_uses_ranking_labels_not_feedback_events` (test)
- L78: function `test_dataform_and_app_contract_use_canonical_event_schema` (test)

## tests/integration/workflow/test_infra_apis_contract.py

- L16: function `test_required_apis_cover_all_modules_actually_used` (test)
- L74: function `test_all_modules_use_consistent_region_var` (test)
- L92: function `test_gke_two_stage_apply_pattern_preserved` (test)
- L106: function `test_search_api_image_lifecycle_ignore_changes_pinned` (test)
- L113: function `test_ops_vertex_all_includes_vvs_and_feature_view_checks` (test)

## tests/integration/workflow/test_local_workflow_contract.py

- L13: function `test_verify_local_hybrid_recipe_pins_fast_local_order` (test)
- L42: function `test_verify_local_app_contract_pins_local_only_scope` (test)
- L53: function `test_verify_local_ml_contract_pins_local_only_scope` (test)
- L65: function `test_ui_templates_fetch_canonical_api_v1_and_ops_paths` (test)
- L86: function `test_ops_scripts_use_canonical_api_v1_and_ops_paths` (test)
- L118: function `test_readme_documents_local_verification_entrypoints` (test)
- L131: function `test_runbook_pins_local_hybrid_required_env_exports` (test)

## tests/integration/workflow/test_vertex_pipeline_submit_contract.py

- L13: function `test_pipeline_wait_resolves_project_via_common_helper` (test)
- L19: function `test_submit_train_pipeline_resolves_project_via_common_helper` (test)
- L25: function `test_common_documents_gcp_project_precedence_in_resolve_project_id` (test)

## tests/integration/workflow/test_vertex_resources_contract.py

- L16: function `test_vvs_module_lifecycle_protects_against_stale_id_recreation` (test)
- L37: function `test_vvs_module_min_max_replica_pinned_to_one_for_dev` (test)
- L58: function `test_feature_view_online_serving_source_is_direct_bigquery` (test)
- L85: function `test_legacy_cloud_scheduler_demoted_to_monthly_smoke` (test)
- L93: function `test_legacy_cloud_function_eventarc_marked_as_smoke` (test)
- L100: function `test_retrain_router_marked_as_smoke_endpoint` (test)

## tests/unit/app/conftest.py

- L28: function `app_with_search_stub`
- L71: function `search_client`

## tests/unit/app/test_adapters.py

- L17: function `_fake_httpx_client` (test)
- L28: function `test_create_retrain_queries_wires_bigquery_client` (test)
- L46: function `test_pubsub_publisher_publishes_json_bytes` (test)
- L65: function `test_kserve_encoder_parses_embedding_dict_response_v1` (test)
- L85: function `test_kserve_reranker_parses_scalar_scores_v1` (test)
- L101: function `test_kserve_encoder_parses_v2_open_inference_response` (test)
- L112: function `test_kserve_reranker_predict_with_explain_via_predict_route` (test)
- L148: function `test_kserve_reranker_predict_with_explain_via_dedicated_url` (test)
- L186: function `test_kserve_reranker_predict_with_explain_degrades_when_attrs_missing` (test)
- L202: function `test_kserve_reranker_predict_with_explain_empty_instances_short_circuits` (test)
- L211: function `test_kserve_reranker_predict_with_explain_v2_degrades_to_predict_only` (test)
- L251: function `test_kserve_reranker_satisfies_reranker_explainer_protocol` (test)
- L261: function `test_kserve_encoder_rejects_html_error_page_as_non_json` (test)
- L287: function `test_kserve_encoder_rejects_empty_embedding_vector` (test)
- L296: function `test_kserve_encoder_enforces_768d_by_default` (test)
- L310: function `test_kserve_encoder_rejects_nan_in_embedding` (test)
- L319: function `test_kserve_encoder_rejects_inf_in_embedding` (test)
- L328: function `test_kserve_reranker_rejects_score_count_mismatch` (test)
- L341: function `test_kserve_reranker_predict_with_explain_logs_count_mismatch_and_degrades` (test)
- L375: function `test_kserve_reranker_parses_v2_attributions_output` (test)

## tests/unit/app/test_api_contract_template.py

- L10: function `_search_payload` (test)
- L18: function `_assert_search_shape` (test)
- L25: function `_assert_trace_identifier` (test)
- L30: function `_assert_result_item_required_fields` (test)
- L36: function `_assert_feedback_shape` (test)
- L40: function `_replace_search_container` (test)
- L55: function `test_api_contract_readyz_returns_ok` (test)
- L64: function `test_api_contract_search_success_shape` (test)
- L70: function `test_api_contract_search_has_trace_identifier` (test)
- L76: function `test_api_contract_search_result_item_required_fields` (test)
- L82: function `test_api_contract_feedback_accepts_click` (test)
- L94: function `test_api_contract_search_validation_error` (test)
- L101: function `test_api_contract_feedback_rejects_unknown_action` (test)
- L112: function `test_api_contract_feedback_validation_error` (test)
- L121: function `test_api_contract_search_unavailable_behavior` (test)

## tests/unit/app/test_bq_retrain_queries.py

- L11: function `_client_with_rows` (test)
- L17: function `_make_q` (test)
- L24: function `test_last_run_finished_at_returns_timestamp` (test)
- L30: function `test_last_run_finished_at_returns_none_when_null` (test)
- L35: function `test_last_run_finished_at_returns_none_when_empty_result` (test)
- L40: function `test_feedback_rows_since_casts_to_int` (test)
- L52: function `test_feedback_rows_since_returns_none_on_exception` (test)
- L60: function `test_ndcg_in_window_returns_float` (test)
- L68: function `test_ndcg_in_window_returns_none_when_no_runs` (test)

## tests/unit/app/test_check_retrain_endpoint.py

- L7: class `_FakeQueries`
- L8: method `__init__` parent=_FakeQueries (test)
- L19: method `last_run_finished_at` parent=_FakeQueries (test)
- L22: method `feedback_rows_since` parent=_FakeQueries (test)
- L25: method `ndcg_in_window` parent=_FakeQueries (test)
- L31: class `_RecordingTrigger`
- L32: method `__init__` parent=_RecordingTrigger (test)
- L35: method `publish` parent=_RecordingTrigger (test)
- L39: function `test_check_retrain_does_nothing_when_fresh` (test)
- L56: function `test_check_retrain_publishes_when_feedback_threshold_exceeded` (test)
- L75: function `test_check_retrain_publishes_when_ndcg_drops` (test)

## tests/unit/app/test_elasticsearch_lexical.py

- L11: function `test_elasticsearch_lexical_maps_hits_to_lexical_result` (test)
- L38: function `test_elasticsearch_lexical_returns_empty_on_exception` (test)

## tests/unit/app/test_event_repositories.py

- L11: function `_result_with_rows` (test)
- L17: function `test_bigquery_event_repository_reads_search_events_with_since_param` (test)
- L49: function `test_bigquery_event_repository_reads_impressions_and_user_actions` (test)
- L92: function `test_bigquery_label_repository_write_ranking_labels_merges_rows` (test)
- L120: function `test_bigquery_label_repository_reads_labels` (test)

## tests/unit/app/test_explain.py

- L19: class `_FakeRetriever`
- L22: method `retrieve` parent=_FakeRetriever (test)
- L34: class `_FakePublisher`
- L37: method `publish_candidates` parent=_FakePublisher (test)
- L56: class `_PlainReranker`
- L59: method `predict` parent=_PlainReranker (test)
- L63: class `_ExplainReranker`
- L66: method `predict` parent=_ExplainReranker (test)
- L69: method `predict_with_explain` parent=_ExplainReranker (test)
- L82: function `_candidate` (test)
- L100: function `test_run_search_returns_attributions_when_reranker_supports_explain` (test)
- L127: function `test_run_search_falls_back_to_no_attributions_when_reranker_lacks_explain` (test)

## tests/unit/app/test_feature_fetcher_adapters.py

- L24: function `_make_feature_value` (test)
- L32: function `_make_feature` (test)
- L39: function `_fos_client_returning` (test)
- L43: function `_fetch` (test)
- L55: function `test_fos_fetcher_extracts_three_known_features` (test)
- L81: function `test_fos_fetcher_ignores_unknown_feature_names` (test)
- L104: function `test_fos_fetcher_returns_all_none_when_per_id_call_raises` (test)
- L108: function `_fetch` (test)
- L132: function `test_fos_fetcher_returns_empty_for_empty_input` (test)
- L143: function `test_fos_fetcher_raises_when_endpoint_resolver_returns_empty` (test)
- L153: function `test_fos_fetcher_rejects_empty_feature_view` (test)
- L161: function `test_fos_fetcher_canonicalizes_feature_view_name_via_admin_lookup` (test)
- L164: class `_AdminClient`
- L165: method `__init__` parent=_AdminClient (test)
- L168: method `get_feature_view` parent=_AdminClient (test)
- L178: class `_DataKey`
- L179: method `__init__` parent=_DataKey (test)
- L182: class `_Request`
- L183: method `__init__` parent=_Request (test)
- L187: class `_ServingClient`
- L188: method `__init__` parent=_ServingClient (test)
- L191: method `fetch_feature_values` parent=_ServingClient (test)

## tests/unit/app/test_feedback_handler_http.py

- L6: function `test_feedback_endpoint_records_event` (test)
- L21: function `test_feedback_endpoint_rejects_invalid_action` (test)
- L30: function `test_feedback_endpoint_accepts_all_canonical_actions` (test)

## tests/unit/app/test_feedback_service.py

- L9: function `test_record_returns_true_on_success` (test)
- L23: function `test_record_returns_false_on_publish_failure` (test)
- L32: function `test_record_emits_new_user_action_contract` (test)

## tests/unit/app/test_health_handler.py

- L6: function `test_livez_returns_ok` (test)
- L12: function `test_healthz_returns_ok` (test)
- L17: function `test_readyz_returns_ready_when_search_wired` (test)
- L25: function `test_readyz_returns_loading_when_retriever_missing` (test)

## tests/unit/app/test_kserve_wiring.py

- L23: function `_settings` (test)
- L37: function `_build_encoder_client` (test)
- L41: function `_build_reranker_client` (test)
- L50: function `test_apisettings_kserve_fields_default_to_empty_string` (test)
- L67: function `test_apisettings_kserve_fields_populated_from_env` (test)
- L97: function `test_apisettings_exposes_grouped_views_for_flags_messaging_and_popularity` (test)
- L122: function `test_build_encoder_client_returns_none_when_url_empty` (test)
- L130: function `test_build_encoder_client_instantiates_kserve_encoder_when_url_set` (test)
- L146: function `test_build_reranker_client_returns_none_when_enable_rerank_false` (test)
- L152: function `test_build_reranker_client_returns_none_when_url_empty` (test)
- L158: function `test_build_reranker_client_instantiates_with_explain_url_when_set` (test)
- L175: function `test_build_reranker_client_passes_none_when_explain_url_is_empty_string` (test)
- L192: function `test_build_reranker_client_handles_whitespace_explain_url` (test)
- L211: function `test_build_reranker_client_has_predict_with_explain_for_ranking_gate` (test)

## tests/unit/app/test_local_boot_contract.py

- L23: function `test_container_builder_avoids_gcp_clients_when_search_disabled` (test)
- L32: function `_forbidden` (test)

## tests/unit/app/test_logging_middleware.py

- L12: function `test_middleware_generates_request_id_when_absent` (test)
- L19: function `test_middleware_preserves_client_supplied_request_id` (test)
- L25: function `test_middleware_request_id_matches_search_response` (test)

## tests/unit/app/test_main_routing.py

- L29: function `app_no_lifespan` (test)
- L40: class `_NoopContainer`
- L43: function `_build` (test)
- L55: function `test_root_redirects_to_ui` (test)
- L62: function `test_ui_home_returns_html` (test)
- L70: function `test_ui_dev_returns_html` (test)
- L77: function `test_ui_model_metrics_returns_html` (test)
- L84: function `test_ui_data_returns_html` (test)
- L91: function `test_ui_ops_returns_html` (test)
- L98: function `test_metrics_serves_prometheus_exposition` (test)
- L115: function `test_metrics_emits_slo_compatible_labels` (test)
- L136: function `test_livez_unconditional` (test)

## tests/unit/app/test_model_handler.py

- L31: function `_build_client` (test)
- L42: function `_wire_candidates` (test)
- L63: function `test_model_metrics_returns_summary_and_per_case` (test)
- L86: function `test_model_metrics_503_when_service_missing` (test)
- L99: function `test_model_metrics_rejects_invalid_k` (test)
- L109: function `test_model_info_reports_container_state` (test)
- L126: function `test_model_data_returns_preview_tables` (test)
- L141: function `test_load_cases_rejects_empty_file` (test)
- L150: function `test_evaluate_default_cases_returns_report` (test)

## tests/unit/app/test_observability.py

- L18: function `test_for_test_uses_stdlib_logger_and_default_service` (test)
- L29: function `test_for_test_accepts_custom_service_name` (test)
- L34: function `test_from_env_reads_otel_service_name` (test)
- L45: function `test_from_env_default_matches_slo_label_contract` (test)

## tests/unit/app/test_ops_handler.py

- L14: function `_build_test_app` (test)
- L22: function `test_destroy_check_returns_summary` (test)
- L45: function `test_search_volume_returns_summary` (test)
- L65: function `test_runs_recent_returns_rows` (test)
- L90: function `test_search_volume_returns_503_with_json_detail_on_bq_error` (test)
- L104: function `test_runs_recent_returns_503_with_json_detail_on_bq_error` (test)

## tests/unit/app/test_optional_adapter_helper.py

- L19: function `test_returns_none_when_disabled_without_calling_factory` (test)
- L22: function `factory` (test)
- L37: function `test_returns_factory_result_when_enabled` (test)
- L48: function `test_swallows_factory_exception_and_logs_with_name` (test)
- L51: function `factory` (test)

## tests/unit/app/test_publisher.py

- L11: function `test_noop_publisher_accepts_any_payload` (test)

## tests/unit/app/test_pubsub_event_writer.py

- L19: function `_client_for` (test)
- L24: function `topic_path` (test)
- L31: function `_build` (test)
- L43: function `test_emit_search_event_publishes_to_search_events_topic` (test)
- L70: function `test_emit_impression_publishes_to_search_impressions_topic` (test)
- L95: function `test_emit_user_action_publishes_to_user_actions_topic` (test)
- L115: function `test_publish_failure_is_logged_and_reraised` (test)
- L134: function `_api_settings` (test)
- L147: function `test_build_event_writer_selects_pubsub_when_topics_set` (test)
- L169: function `test_build_event_writer_falls_back_to_cloud_logging_when_topic_missing` (test)

## tests/unit/app/test_ranking_service.py

- L15: class `_FakeRetriever`
- L19: method `retrieve` parent=_FakeRetriever (test)
- L32: class `_FakePublisher`
- L35: method `publish_candidates` parent=_FakePublisher (test)
- L55: class `_StubReranker`
- L58: method `predict` parent=_StubReranker (test)
- L62: function `_candidate` (test)
- L83: function `test_run_search_preserves_lexical_order` (test)
- L99: function `test_run_search_final_rank_equals_lexical_rank_without_reranker` (test)
- L117: function `test_run_search_continues_when_publisher_raises` (test)
- L126: class `_FailingPublisher`
- L127: method `__init__` parent=_FailingPublisher (test)
- L130: method `publish_candidates` parent=_FailingPublisher (test)
- L151: function `test_run_search_publishes_full_pool_not_just_top_k` (test)
- L167: function `test_run_search_forwards_filters_to_retriever` (test)
- L186: function `test_run_search_empty_result` (test)
- L207: function `test_run_search_rerank_reverses_order_when_reranker_says_so` (test)
- L230: function `test_run_search_rerank_truncates_to_top_k` (test)
- L249: function `test_run_search_rerank_with_higher_score_wins` (test)
- L252: class `_ForceWinReranker`
- L253: method `predict` parent=_ForceWinReranker (test)
- L273: function `test_run_search_rerank_tie_breaks_by_lexical_then_semantic_rank` (test)
- L274: class `_TieReranker`
- L275: method `predict` parent=_TieReranker (test)

## tests/unit/app/test_retrain.py

- L10: class `FakeQueries`
- L11: method `__init__` parent=FakeQueries (test)
- L24: method `last_run_finished_at` parent=FakeQueries (test)
- L27: method `feedback_rows_since` parent=FakeQueries (test)
- L30: method `ndcg_in_window` parent=FakeQueries (test)
- L42: function `test_no_reason_no_retrain` (test)
- L54: function `test_feedback_rows_trigger` (test)
- L66: function `test_feedback_rows_below_threshold_does_not_trigger` (test)
- L74: function `test_ndcg_drop_triggers_retrain` (test)
- L85: function `test_ndcg_improvement_does_not_trigger` (test)
- L94: function `test_ndcg_missing_does_not_trigger` (test)
- L103: function `test_ndcg_small_drop_below_threshold` (test)
- L113: function `test_custom_ndcg_threshold_flips_decision` (test)
- L124: function `test_staleness_trigger` (test)
- L136: function `test_no_prior_run_triggers` (test)
- L143: function `test_custom_feedback_threshold` (test)
- L154: function `test_custom_stale_days_triggers_on_shorter_window` (test)
- L165: function `test_decision_exposes_ranker_fields` (test)

## tests/unit/app/test_run_search_feature_fetcher.py

- L34: function `_candidate` (test)
- L63: function `test_augment_overwrites_three_dynamic_features` (test)
- L81: function `test_augment_preserves_bq_value_when_fos_field_is_none` (test)
- L96: function `test_augment_keeps_candidate_unchanged_when_id_not_in_fos` (test)
- L109: function `test_augment_returns_empty_list_for_empty_input` (test)
- L115: function `test_augment_calls_fetch_once_with_all_property_ids` (test)
- L129: function `test_run_search_default_feature_fetcher_is_none_no_fetch_happens` (test)
- L155: function `test_run_search_with_feature_fetcher_merges_before_reranker_predict` (test)
- L189: function `test_run_search_swallows_feature_fetcher_failure_and_continues` (test)
- L196: class `_ExplodingFetcher`
- L197: method `fetch` parent=_ExplodingFetcher (test)
- L223: function `test_container_dataclass_has_feature_fetcher_field` (test)
- L237: function `test_search_service_accepts_feature_fetcher_kwarg` (test)
- L247: function `test_run_search_signature_lists_feature_fetcher_with_default_none` (test)

## tests/unit/app/test_search_api.py

- L10: function `_search_payload` (test)
- L18: function `_replace_search_container` (test)
- L33: function `test_search_returns_200_with_results` (test)
- L41: function `test_search_results_preserve_lexical_rank_when_rerank_disabled` (test)
- L50: function `test_search_emits_ranking_log` (test)
- L64: function `test_search_top_k_truncates_response` (test)
- L72: function `test_search_rejects_empty_query` (test)
- L79: function `test_search_503_when_disabled` (test)
- L88: function `test_feedback_accepts_click` (test)
- L105: function `test_feedback_rejects_unknown_action` (test)
- L116: function `test_readyz_ok_when_search_enabled` (test)
- L127: function `test_readyz_503_when_retriever_missing` (test)
- L136: function `test_readyz_503_when_encoder_missing` (test)
- L145: function `test_healthz_unconditional` (test)
- L154: function `test_readyz_reports_rerank_disabled_when_client_missing` (test)
- L163: function `test_readyz_reports_rerank_enabled_when_client_set` (test)
- L166: class `_StubReranker`
- L169: method `predict` parent=_StubReranker (test)
- L184: function `test_search_returns_scores_when_reranker_loaded` (test)
- L187: class `_StubReranker`
- L190: method `predict` parent=_StubReranker (test)
- L209: function `test_ranking_log_receives_scores_when_reranker_loaded` (test)
- L212: class `_StubReranker`
- L215: method `predict` parent=_StubReranker (test)

## tests/unit/app/test_search_builder_canonical.py

- L37: class `_FakeContext`
- L38: method `__init__` parent=_FakeContext (test)
- L42: method `_bigquery` parent=_FakeContext (test)
- L46: function `_settings` (test)
- L66: function `_builder` (test)
- L75: function `test_build_vertex_vector_search_assembles_endpoint_resource_name` (test)
- L85: function `test_build_vertex_vector_search_accepts_fully_qualified_endpoint_name` (test)
- L100: function `test_build_vertex_vector_search_fails_loud_when_endpoint_missing` (test)
- L106: function `test_build_vertex_vector_search_fails_loud_when_deployed_id_missing` (test)
- L117: function `test_resolve_feature_fetcher_returns_fos_when_fully_configured` (test)
- L126: function `test_resolve_feature_fetcher_fails_loud_when_store_missing` (test)
- L132: function `test_resolve_feature_fetcher_fails_loud_when_view_missing` (test)
- L138: function `test_resolve_feature_fetcher_fails_loud_when_endpoint_missing` (test)
- L149: function `test_resolve_lexical_returns_elasticsearch_when_url_configured` (test)
- L158: function `test_resolve_lexical_fails_loud_when_es_backend_enable_search_no_lexical_url` (test)
- L164: function `test_resolve_lexical_noop_when_search_disabled_and_no_lexical_urls` (test)

## tests/unit/app/test_search_handler_http.py

- L13: function `_candidate` (test)
- L33: function `test_search_endpoint_returns_results` (test)
- L53: function `test_search_endpoint_503_when_retriever_unavailable` (test)
- L84: function `test_search_endpoint_explain_returns_attributions` (test)
- L102: function `test_search_endpoint_emits_canonical_event_logs` (test)

## tests/unit/app/test_search_mapper.py

- L14: function `test_search_request_to_input_propagates_filters_and_flags` (test)
- L33: function `test_to_search_response_maps_items` (test)

## tests/unit/app/test_search_service.py

- L26: function `_make_candidate` (test)
- L45: function `_build_service` (test)
- L75: function `test_search_returns_items_sorted_by_final_rank` (test)
- L89: function `test_search_calls_publisher_once_with_full_pool` (test)
- L106: function `test_search_uses_reranker_scores_when_available` (test)
- L123: function `test_search_raises_unavailable_when_retriever_missing` (test)
- L136: function `test_search_raises_unavailable_when_encoder_missing` (test)
- L149: function `test_search_populates_popularity_score_when_scorer_present` (test)
- L160: function `test_search_emits_search_event_and_impressions` (test)

## tests/unit/app/test_settings_sources.py

- L9: function `test_apisettings_loads_non_secret_values_from_setting_yaml` (test)
- L41: function `test_env_vars_override_yaml_sources` (test)

## tests/unit/app/test_synonym_expander.py

- L33: function `_b` (test)
- L38: class `_FakeRedis`
- L42: method `__init__` parent=_FakeRedis (test)
- L45: method `smembers` parent=_FakeRedis (test)
- L49: class `_FlakyRedis`
- L52: method `smembers` parent=_FlakyRedis (test)
- L56: function `test_noop_returns_query_unchanged` (test)
- L61: function `test_redis_expands_known_tokens_with_synonyms` (test)
- L81: function `test_redis_keeps_query_when_no_synonyms_known` (test)
- L86: function `test_redis_returns_original_on_backend_failure` (test)
- L92: function `test_redis_caps_synonyms_per_token` (test)
- L103: function `test_redis_dedupes_across_tokens` (test)
- L119: function `test_redis_handles_string_decoded_values` (test)
- L122: class `_StrRedis`
- L123: method `smembers` parent=_StrRedis (test)

## tests/unit/app/test_vertex_vector_search_semantic_search.py

- L25: function `_make_neighbor` (test)
- L38: function `_factory_returning` (test)
- L45: function `_adapter` (test)
- L60: function `test_search_converts_neighbors_to_semantic_results_in_distance_order` (test)
- L81: function `test_search_returns_empty_when_no_neighbors` (test)
- L86: function `test_search_returns_empty_when_response_is_empty` (test)
- L100: function `test_search_passes_top_k_and_query_vector_and_deployed_index_id` (test)
- L120: function `test_search_ignores_filters_in_pr1_known_limitation` (test)
- L149: function `test_endpoint_factory_called_with_resource_name_once` (test)
- L155: function `factory` (test)
- L174: function `test_search_handles_missing_distance_attribute_as_max_distance` (test)
- L202: function `test_constructor_rejects_empty_required_args` (test)

## tests/unit/arch/test_import_boundaries.py

- L32: function `test_no_forbidden_imports` (test)

## tests/unit/ml/common/test_gcs.py

- L4: function `test_parse_round_trip` (test)
- L11: function `test_parse_bucket_only` (test)
- L18: function `test_parse_trailing_slash` (test)
- L23: function `test_child_and_uri` (test)
- L29: function `test_model_prefix_layout` (test)
- L35: function `test_parse_rejects_non_gcs` (test)

## tests/unit/ml/common/test_gcs_io.py

- L14: function `test_upload_directory_recurses_and_returns_uris` (test)
- L44: function `test_upload_directory_handles_empty_prefix` (test)
- L61: function `test_download_file_writes_to_local_path` (test)

## tests/unit/ml/common/test_logging.py

- L7: function `test_json_formatter_basic` (test)
- L25: function `test_json_formatter_extras` (test)

## tests/unit/ml/common/test_run_id.py

- L6: function `test_generate_run_id_format` (test)
- L11: function `test_generate_run_id_uniqueness` (test)

## tests/unit/ml/data/test_bigquery_ranker_repository.py

- L14: function `_make_repo` (test)
- L26: function `test_fetch_training_rows_builds_parameterized_query` (test)
- L61: function `test_save_run_records_ranker_metrics` (test)
- L103: function `test_save_run_raises_on_insert_errors` (test)
- L120: function `test_latest_model_path_returns_none_when_empty` (test)
- L126: function `test_latest_model_path_returns_model_path` (test)
- L134: function `test_save_run_dual_writes_to_vertex_experiments` (test)
- L169: function `test_save_run_skips_vertex_experiments_without_env` (test)

## tests/unit/ml/data/test_embedding_batch.py

- L14: class `_FakeEncoder`
- L17: method `encode_passages` parent=_FakeEncoder (test)
- L20: method `encode_queries` parent=_FakeEncoder (test)
- L25: class `_FakeRepo`
- L28: method `fetch_all` parent=_FakeRepo (test)
- L33: class `_FakeStore`
- L36: method `existing_hashes` parent=_FakeStore (test)
- L39: method `upsert` parent=_FakeStore (test)
- L45: class `_CaptureLogger`
- L46: method `__init__` parent=_CaptureLogger (test)
- L49: method `info` parent=_CaptureLogger (test)
- L53: function `test_encodes_all_on_empty_store` (test)
- L69: function `test_skips_unchanged_rows_on_rerun` (test)
- L80: function `test_re_encodes_when_text_changes` (test)

## tests/unit/ml/data/test_feature_engineering_ranker.py

- L6: function `test_build_ranker_features_keys_match_feature_cols_ranker` (test)
- L25: function `test_build_ranker_features_numeric_coercion` (test)
- L47: function `test_build_ranker_features_handles_missing_behavior` (test)

## tests/unit/ml/evaluation/test_label_gain.py

- L6: function `test_request_complete_beats_favorite_beats_click` (test)
- L12: function `test_empty_or_unknown_returns_zero` (test)

## tests/unit/ml/evaluation/test_ranking_metrics.py

- L8: function `test_ndcg_perfect_ranking_is_one` (test)
- L14: function `test_ndcg_reversed_is_below_one` (test)
- L20: function `test_ndcg_all_zero_labels_is_zero` (test)
- L26: function `test_map_relevant_at_top_is_one` (test)
- L32: function `test_map_no_relevance_is_zero` (test)
- L38: function `test_recall_at_k_basic` (test)
- L45: function `test_evaluate_over_groups_returns_all_three_keys` (test)
- L56: function `test_evaluate_empty_input` (test)

## tests/unit/ml/test_encoder_server.py

- L8: class `_FakeEncoder`
- L9: method `_encode` parent=_FakeEncoder (test)
- L13: function `test_normalize_instance_accepts_prefixed_string` (test)
- L17: function `test_normalize_instance_accepts_legacy_object_payload` (test)
- L22: function `test_predict_accepts_mixed_request_shapes` (test)

## tests/unit/ml/test_lightgbm_trainer_adapter.py

- L18: function `test_lightgbm_trainer_satisfies_ranker_trainer_protocol` (test)

## tests/unit/ml/training/test_cli_run.py

- L17: class `_InMemoryRepo`
- L18: method `__init__` parent=_InMemoryRepo (test)
- L22: method `fetch_training_rows` parent=_InMemoryRepo (test)
- L25: method `save_run` parent=_InMemoryRepo (test)
- L46: method `latest_model_path` parent=_InMemoryRepo (test)
- L50: class `_StubUploader`
- L51: method `__init__` parent=_StubUploader (test)
- L54: method `upload` parent=_StubUploader (test)
- L59: class `_StubTracker`
- L60: method `__init__` parent=_StubTracker (test)
- L63: method `__enter__` parent=_StubTracker (test)
- L66: method `__exit__` parent=_StubTracker (test)
- L69: method `log_metrics` parent=_StubTracker (test)
- L73: function `_tracker_factory` (test)
- L77: function `test_split_by_request_id_keeps_groups_intact` (test)
- L85: function `test_split_by_request_id_empty` (test)
- L91: function `test_run_non_dry_run_happy_path` (test)
- L114: function `test_run_non_dry_run_raises_on_empty_dataset` (test)
- L126: function `test_run_dry_run_skips_upload_and_save` (test)
- L143: function `_frozen_time` (test)

## tests/unit/ml/training/test_trainer.py

- L18: function `_synthetic_frame` (test)
- L45: function `test_group_sizes_contiguous` (test)
- L51: function `test_group_sizes_empty` (test)
- L57: function `test_rank_train_produces_booster` (test)
- L95: function `test_rank_train_missing_columns_raises` (test)

## tests/unit/ml/training/test_vertex_experiments_tracker.py

- L19: function `fake_aiplatform` (test)
- L38: function `test_enter_initializes_aiplatform_and_starts_run` (test)
- L55: function `test_log_metrics_filters_non_numeric` (test)
- L69: function `test_log_params_filters_non_scalar_and_none` (test)
- L91: function `test_exit_propagates_aiplatform_exit_then_clears_handle` (test)
- L105: function `test_satisfies_experiment_tracker_protocol` (test)

## tests/unit/pipeline/dags/test_dag_files.py

- L41: function `test_dag_file_is_syntactically_valid` (test)
- L47: function `test_dag_id_matches_filename_stem` (test)
- L57: function `test_dag_has_schedule_and_catchup_false` (test)
- L67: function `test_dag_does_not_use_bash_operator` (test)
- L88: function `test_retrain_orchestration_invokes_compile_via_pod_runner_not_import` (test)
- L110: function `test_dag_uses_pod_or_provider_operator` (test)
- L127: function `test_monitoring_validation_sql_paths_resolve_to_real_files` (test)
- L142: function `test_all_dag_files_present` (test)

## tests/unit/pipeline/test_data_job_dag_wiring.py

- L26: function `_main_source` (test)
- L35: function `test_pipeline_signature_declares_strangler_off_defaults` (test)
- L50: function `test_build_pipeline_spec_lists_vector_search_params_with_strangler_defaults` (test)
- L58: function `test_build_pipeline_spec_steps_include_upsert_vector_search` (test)
- L74: function `test_pipeline_body_invokes_upsert_vector_search` (test)
- L81: function `test_pipeline_imports_upsert_component` (test)

## tests/unit/pipeline/test_ground_truth_jobs.py

- L11: function `test_labeling_job_builds_labels_from_impressions_and_actions` (test)
- L16: class `_FakeEventRepository`
- L17: method `read_impressions` parent=_FakeEventRepository (test)
- L43: method `read_user_actions` parent=_FakeEventRepository (test)
- L59: class `_FakeLabelRepository`
- L60: method `write_ranking_labels` parent=_FakeLabelRepository (test)
- L85: function `test_training_dataset_job_exports_relevance_label_csv` (test)
- L108: class `_FakeRepository`
- L109: method `fetch_training_rows` parent=_FakeRepository (test)

## tests/unit/pipeline/test_kfp_orchestrator.py

- L21: class `_StubComponent`
- L22: method `__init__` parent=_StubComponent (test)
- L26: method `name` parent=_StubComponent (test)
- L29: method `to_runtime_task` parent=_StubComponent (test)
- L35: function `test_kfp_orchestrator_satisfies_protocol` (test)

## tests/unit/pipeline/test_pipeline_trigger.py

- L13: function `test_decode_pubsub_message_reads_json_payload` (test)
- L21: function `test_decode_pubsub_message_returns_empty_when_payload_missing` (test)
- L27: function `test_merge_parameters_promotes_reasons` (test)
- L35: function `test_merge_parameters_overrides_defaults_with_event_payload` (test)
- L55: function `test_build_job_id_uses_prefix` (test)

## tests/unit/pipeline/test_vector_search_writer.py

- L29: function `_datapoint` (test)
- L38: function `test_in_memory_writer_records_datapoints` (test)
- L51: function `test_in_memory_writer_is_idempotent` (test)
- L61: function `test_in_memory_writer_skips_empty_batch` (test)
- L73: function `_index_with_recorder` (test)
- L78: function `_upsert` (test)
- L85: function `test_vertex_writer_calls_upsert_datapoints_with_payload` (test)
- L103: function `test_vertex_writer_chunks_large_batches` (test)
- L127: function `test_vertex_writer_skips_empty_batch` (test)
- L141: function `test_vertex_writer_resolves_index_once` (test)
- L144: function `factory` (test)
- L171: function `test_vertex_writer_rejects_invalid_args` (test)

## tests/unit/scripts/test_adapters.py

- L16: class `_FakeProc`
- L17: method `__init__` parent=_FakeProc (test)
- L22: function `test_kubectl_run_prefixes_kubectl_to_args` (test)
- L30: function `test_kubectl_run_forwards_capture_check_timeout` (test)
- L43: function `test_kubectl_run_forwards_input_for_stdin_apply` (test)
- L51: function `test_terraform_run_inserts_chdir_flag` (test)
- L59: function `test_terraform_run_omits_chdir_when_none` (test)
- L67: function `test_gcloud_run_prefixes_gcloud_to_args` (test)
- L80: function `test_gcloud_run_forwards_capture_check_timeout` (test)

## tests/unit/scripts/test_common_resolve_project.py

- L10: function `test_resolve_project_id_prefers_gcp_project` (test)
- L16: function `test_resolve_project_id_falls_back_to_project_id` (test)
- L22: function `test_resolve_project_id_falls_back_to_defaults` (test)
- L29: function `test_env_project_id_reads_gcp_project_when_project_id_empty` (test)
- L37: function `test_env_gcp_project_reads_project_id_when_gcp_empty` (test)

## tests/unit/scripts/test_composer_deploy_dags.py

- L23: function `_fake_run_factory` (test)
- L24: function `_fake_run` (test)
- L33: function `test_main_early_returns_when_dag_bucket_empty` (test)
- L46: function `test_main_uploads_dags_when_bucket_set` (test)
- L51: function `_fake_terraform_run` (test)
- L58: function `_fake_run` (test)
- L115: function `test_main_raises_when_terraform_output_fails` (test)
- L125: function `test_main_raises_on_invalid_json` (test)
- L135: function `test_top_level_dag_listing_excludes_underscore_files` (test)
- L150: function `test_pipeline_pkg_files_listed_with_gcs_relative_paths` (test)
- L166: function `test_data_files_listed_for_sql_assets` (test)

## tests/unit/scripts/test_composer_task_states.py

- L8: function `test_extract_json_array_strips_prologue` (test)
- L18: function `test_latest_run_id_first_row` (test)

## tests/unit/scripts/test_configmap_overlay.py

- L13: function `test_feature_online_store_public_domain_from_api_parses_rest_shape` (test)
- L33: function `test_feature_online_store_public_domain_from_api_returns_empty_on_missing_domain` (test)

## tests/unit/scripts/test_deploy_all_step_timing.py

- L24: function `_reset_globals` (test)
- L32: function `test_step_first_call_emits_header_without_elapsed_anchor` (test)
- L45: function `test_step_subsequent_calls_emit_elapsed_anchor` (test)
- L65: function `test_step_done_emits_elapsed_line_matching_monitor_contract` (test)
- L83: function `test_step_done_noop_before_any_step` (test)
- L91: function `test_resolve_step_ref_accepts_number_and_name` (test)
- L97: function `test_main_honors_from_step_and_to_step` (test)
- L102: function `_runner` (test)
- L103: function `_run` (test)
- L130: function `test_main_prints_failure_summary_for_nonzero_step` (test)
- L152: function `test_run_tf_apply_uses_staged_apply_and_waits_for_readiness` (test)
- L156: function `_fake_stage1` (test)
- L159: function `_fake_stream` (test)
- L211: function `test_run_sync_elasticsearch_uses_project_and_default_cluster_url` (test)
- L234: function `test_run_sync_elasticsearch_propagates_nonzero_exit` (test)
- L243: function `test_main_invokes_precondition_before_run` (test)
- L250: function `fake_pre` (test)
- L253: function `fake_run` (test)
- L280: function `test_main_skips_precondition_when_none` (test)
- L284: function `fake_run` (test)
- L307: function `test_main_propagates_precondition_exception_as_step_failure` (test)
- L312: function `fake_pre` (test)
- L317: function `fake_run` (test)

## tests/unit/scripts/test_destroy_check.py

- L6: function `test_classify_bucket_names_splits_fail_and_warn` (test)
- L28: function `test_classify_artifact_repos_splits_google_managed_repo` (test)
- L35: function `test_filter_high_cost_datasets_ignores_unrelated_datasets` (test)
- L41: function `test_looks_like_api_disabled_detects_disabled_service_errors` (test)

## tests/unit/scripts/test_elasticsearch_wait.py

- L24: class `_FakeProc`
- L25: method `__init__` parent=_FakeProc (test)
- L31: function `test_wait_returns_immediately_on_green` (test)
- L44: function `test_wait_accepts_yellow_for_single_node_cluster` (test)
- L57: function `test_wait_polls_until_health_becomes_green` (test)
- L62: function `fake_kubectl_run` (test)
- L83: function `test_wait_raises_timeout_on_stuck_unknown` (test)
- L104: function `test_healthy_states_pin_green_and_yellow` (test)

## tests/unit/scripts/test_infra_cleanup.py

- L17: function `_completed` (test)
- L24: function `test_delete_orphan_workloads_invokes_two_kubectl_deletes` (test)
- L27: function `_fake_run` (test)
- L44: function `test_delete_orphan_workloads_swallows_kubectl_failure` (test)
- L47: function `_fake_run` (test)
- L60: function `test_wipe_bucket_passes_recursive_glob` (test)
- L64: function `_fake_run` (test)
- L83: function `test_wipe_all_iterates_bucket_suffixes` (test)
- L87: function `_fake_run` (test)
- L107: function `test_undeploy_endpoint_models_skips_when_endpoint_absent` (test)
- L114: function `test_undeploy_endpoint_models_skips_when_no_deployed` (test)
- L122: function `test_undeploy_endpoint_models_iterates_deployed_models` (test)
- L126: function `_fake_run` (test)
- L144: function `test_deployed_index_exists_reads_index_endpoint_payload` (test)
- L156: function `test_wait_for_deployed_index_absent_polls_until_stale_index_disappears` (test)
- L176: function `test_wait_for_deployed_index_absent_early_exits_on_ready_state` (test)
- L192: function `test_deployed_index_state_classifies_ready_vs_transitional` (test)

## tests/unit/scripts/test_infra_feature_view_sync.py

- L9: class `_FakeResponse`
- L10: method `__init__` parent=_FakeResponse (test)
- L13: method `read` parent=_FakeResponse (test)
- L16: method `__enter__` parent=_FakeResponse (test)
- L19: method `__exit__` parent=_FakeResponse (test)
- L23: function `test_main_skips_when_fos_outputs_are_empty` (test)
- L34: function `test_trigger_and_wait_posts_sync_then_polls_until_complete` (test)
- L37: function `_fake_urlopen` (test)

## tests/unit/scripts/test_infra_terraform_state.py

- L19: function `_completed` (test)
- L25: function `test_state_list_returns_empty_on_cli_failure` (test)
- L30: function `test_state_list_returns_lines_when_present` (test)
- L36: function `test_state_size_counts_addresses` (test)
- L41: function `test_state_size_zero_on_cli_failure` (test)
- L46: function `test_addresses_starting_with_filters_by_prefix` (test)
- L56: function `test_is_in_state_true_when_address_present` (test)
- L63: function `test_filter_targets_keeps_only_in_state` (test)
- L78: function `test_state_rm_returns_true_on_success` (test)
- L83: function `test_state_rm_returns_false_on_failure` (test)
- L93: function `test_state_list_passes_env_when_supplied` (test)
- L97: function `_fake_run` (test)

## tests/unit/scripts/test_kserve_models_deploy.py

- L27: class `_FakeModel`
- L32: method `__init__` parent=_FakeModel (test)
- L47: function `_install_fake_aiplatform` (test)
- L77: function `test_resolve_latest_prefers_model_with_production_alias` (test)
- L114: function `test_resolve_latest_falls_back_to_first_when_no_production_alias` (test)
- L140: function `test_resolve_latest_raises_when_no_models` (test)
- L148: function `test_resolve_latest_raises_when_artifact_uri_missing` (test)
- L175: function `_capture_kubectl_patch_call` (test)
- L180: function `fake_run` (test)
- L192: function `_capture_kubectl_run_call` (test)
- L201: function `fake_kubectl_run` (test)
- L213: function `test_patch_reranker_storage_uri_emits_expected_kubectl_shape` (test)
- L243: function `test_patch_encoder_storage_uri_is_noop_under_hf_runtime` (test)
- L265: function `test_resolve_latest_warns_on_production_alias_fallback` (test)

## tests/unit/scripts/test_lib_config.py

- L36: function `test_configmap_keys_pin` (test)
- L40: function `test_generate_configmap_data_returns_all_keys_strings` (test)
- L49: function `test_committed_example_defaults_are_empty_for_vertex_resources` (test)
- L64: function `test_generate_configmap_data_passes_through_live_vertex_outputs` (test)
- L81: function `test_render_committed_form_matches_example_yaml` (test)
- L94: function `test_render_runtime_form_omits_header` (test)
- L106: function `test_render_values_are_double_quoted` (test)

## tests/unit/scripts/test_lib_gcp_resources.py

- L18: function `test_vertex_endpoints_pin` (test)
- L25: function `test_bucket_suffixes_pin` (test)
- L29: function `test_default_names_pin` (test)
- L33: function `test_vertex_model_names_pin` (test)
- L37: function `test_endpoint_names_have_endpoint_suffix` (test)
- L49: function `test_model_names_no_endpoint_suffix` (test)

## tests/unit/scripts/test_local_hybrid.py

- L9: function `test_resolve_elasticsearch_api_key_prefers_local_secret` (test)
- L17: function `test_resolve_elasticsearch_api_key_empty_when_no_url` (test)
- L21: function `test_resolve_elasticsearch_url_prefers_explicit_env` (test)
- L31: function `test_resolve_elasticsearch_url_uses_local_when_http_available` (test)
- L45: function `test_resolve_elasticsearch_url_returns_empty_when_unreachable` (test)
- L59: function `test_ensure_local_reranker_model_skips_existing_file` (test)

## tests/unit/scripts/test_monitor.py

- L20: function `test_step_regex_matches_deploy_all_step_log_format` (test)
- L33: function `test_step_regex_matches_single_space` (test)
- L40: function `test_step_regex_ignores_unrelated_lines` (test)
- L49: function `test_build_wait_regex_extracts_build_id_and_timeout` (test)
- L57: function `test_build_wait_regex_requires_numeric_timeout` (test)
- L62: function `test_maybe_parse_step_updates_state_and_clears_build_tracking` (test)
- L81: function `test_maybe_parse_step_noop_for_unrelated_line` (test)
- L89: function `test_maybe_parse_build_wait_records_build_id_and_start_time` (test)
- L101: function `test_maybe_parse_build_wait_noop_for_unrelated_line` (test)

## tests/unit/scripts/test_promote.py

- L22: class `_FakeRegistry`
- L23: method `__init__` parent=_FakeRegistry (test)
- L27: method `add_version_aliases` parent=_FakeRegistry (test)
- L30: method `remove_version_aliases` parent=_FakeRegistry (test)
- L34: class `_FakeModel`
- L35: method `__init__` parent=_FakeModel (test)
- L42: function `_args` (test)
- L55: function `test_resolve_display_name_uses_model_not_endpoint` (test)
- L70: function `test_resolve_display_name_env_override_uses_model_named_var` (test)
- L86: function `test_select_version_picks_explicit_version_id` (test)
- L93: function `test_select_version_picks_alias` (test)
- L100: function `test_select_version_errors_when_no_selector_matches` (test)
- L106: function `test_set_production_alias_moves_alias_between_versions` (test)
- L114: function `test_set_production_alias_dry_run_does_not_call_registry` (test)
- L122: function `test_run_alias_fails_fast_when_artifact_uri_is_empty` (test)
- L139: function `test_run_alias_applies_when_artifact_uri_has_objects` (test)
- L154: function `test_bst_rename_no_op_when_bst_already_exists` (test)
- L164: function `test_bst_rename_plans_copy_in_dry_run` (test)
- L168: function `_fail_cp` (test)
- L176: function `test_bst_rename_returns_none_when_neither_file_present` (test)

## tests/unit/scripts/test_repo_relative_paths.py

- L28: function `test_scripts_parents_paths_resolve` (test)

## tests/unit/scripts/test_resolve_api_target.py

- L29: function `_clear_target_env` (test)
- L41: function `test_explicit_api_url_wins_over_target_and_skips_token_by_default` (test)
- L58: function `test_explicit_api_url_honors_host_and_insecure_overrides` (test)
- L72: function `test_explicit_api_url_mints_token_when_require_token_truthy` (test)
- L85: function `test_target_local_uses_default_local_url_without_token` (test)
- L100: function `test_target_local_honors_local_api_url_override` (test)
- L110: function `test_target_gcp_default_uses_public_domain_with_valid_tls` (test)
- L131: function `test_target_gcp_public_domain_honors_insecure_tls_override` (test)
- L143: function `test_target_gcp_falls_back_to_gateway_ip_when_public_domain_empty` (test)
- L160: function `test_target_gcp_fallback_honors_api_host_header_override` (test)
- L173: function `test_unknown_target_raises` (test)

## tests/unit/scripts/test_run_all_orchestrator.py

- L22: function `_isolate_csv` (test)
- L26: function `test_steps_are_the_canonical_validation_sequence` (test)
- L53: function `test_main_runs_every_step_in_order_then_records_ok` (test)
- L56: function `_fake_run` (test)
- L70: function `test_main_fails_fast_on_first_nonzero_step` (test)
- L73: function `_fake_run` (test)
- L90: function `test_makefile_run_all_core_delegates_to_orchestrator` (test)

## tests/unit/scripts/test_setup_policy_guard.py

- L8: function `_read` (test)
- L12: function `test_setup_scripts_use_canonical_and_ci_import_paths` (test)
- L25: function `test_setup_scripts_target_dev_terraform_environment` (test)
- L42: function `test_api_deploy_targets_gke_rollout_path` (test)
- L51: function `test_makefile_has_canonical_ops_targets` (test)
- L62: function `test_makefile_sync_elasticsearch_passes_required_args` (test)
- L84: function `test_seed_and_feature_group_contract_pin_feature_timestamp` (test)

## tests/unit/scripts/test_step_timing.py

- L19: function `_isolate_csv` (test)
- L23: function `test_fmt_duration_human_readable` (test)
- L32: function `test_record_writes_header_then_rows_and_baselines_use_median_of_ok_runs` (test)
- L52: function `test_record_keeps_only_recent_runs_per_step_for_the_median` (test)
- L61: function `test_record_is_best_effort_and_never_raises` (test)
- L70: function `test_print_eta_no_history` (test)
- L75: function `test_print_eta_sums_known_step_baselines` (test)
- L87: function `test_print_eta_all_known_uses_tilde_prefix` (test)

## tests/unit/scripts/test_submit_train_pipeline.py

- L12: function `test_main_requires_pipeline_root_bucket` (test)
- L20: function `env_no_bucket` (test)
- L29: function `test_main_calls_compile_with_expanded_argv` (test)

## tests/unit/scripts/test_subprocess_run_kwargs_guard.py

- L24: function `_is_subprocess_run` (test)
- L35: function `_offending_calls` (test)
- L45: function `test_no_raw_subprocess_run_capture_kwarg` (test)

## tests/unit/scripts/test_sync_elasticsearch_exit_codes.py

- L14: function `test_run_returns_one_when_project_id_missing` (test)
- L21: function `test_run_returns_one_when_es_url_missing` (test)

## tests/unit/scripts/test_terraform_lock.py

- L12: function `test_parse_lock_id_from_terraform_stderr` (test)
- L22: function `test_is_state_lock_error` (test)
- L27: function `test_should_auto_force_unlock_aliases` (test)
- L44: function `test_parse_lock_id_handles_real_ansi_color_output` (test)
- L72: function `test_parse_lock_id_returns_none_when_absent` (test)

## tests/unit/scripts/test_vertex_feature_store_wait.py

- L10: function `test_wait_until_feature_store_names_released_exits_when_empty` (test)
- L15: function `fake_token` (test)
- L18: function `fake_rest` (test)
- L38: function `test_wait_until_feature_store_names_released_times_out` (test)
- L39: function `fake_token` (test)
- L42: function `fake_rest` (test)

## tests/unit/scripts/test_vertex_ops_scripts.py

- L13: function `test_vector_search_probe_vector_has_expected_shape` (test)
- L20: function `test_ops_search_retries_transient_timeout` (test)
- L26: function `_fake_once` (test)
- L41: function `test_ops_search_fails_after_retry_budget` (test)
- L51: function `test_backfill_build_spec_reads_required_env` (test)
- L69: function `test_backfill_build_spec_falls_back_to_terraform_output` (test)
- L87: function `test_backfill_build_spec_rejects_non_int_batch_size` (test)
- L103: function `test_feature_group_uses_feature_view_env` (test)
- L112: class `_AdminClient`
- L113: method `__init__` parent=_AdminClient (test)
- L116: method `get_feature_online_store` parent=_AdminClient (test)
- L129: method `get_feature_view` parent=_AdminClient (test)
- L139: class `_DataKey`
- L140: method `__init__` parent=_DataKey (test)
- L143: class `_Request`
- L144: method `__init__` parent=_Request (test)
- L148: class `_ServingClient`
- L149: method `__init__` parent=_ServingClient (test)
- L152: method `fetch_feature_values` parent=_ServingClient (test)
- L187: function `test_feature_group_404_emits_sync_and_bq_diagnostics` (test)
- L194: class `_NotFoundError`
- L197: class `_AdminClient`
- L198: method `__init__` parent=_AdminClient (test)
- L201: method `get_feature_online_store` parent=_AdminClient (test)
- L213: method `get_feature_view` parent=_AdminClient (test)
- L222: class `_DataKey`
- L223: method `__init__` parent=_DataKey (test)
- L226: class `_Request`
- L227: method `__init__` parent=_Request (test)
- L231: class `_ServingClient`
- L232: method `__init__` parent=_ServingClient (test)
- L235: method `fetch_feature_values` parent=_ServingClient (test)
- L286: function `test_vector_search_resolves_ids_from_terraform_outputs` (test)
- L294: class `_Endpoint`
- L295: method `__init__` parent=_Endpoint (test)
- L298: method `find_neighbors` parent=_Endpoint (test)
- L302: class `_AiPlatform`
- L306: method `init` parent=_AiPlatform (test)
- L329: function `_clear_aiplatform_sys_modules` (test)
- L337: function `test_pipeline_wait_passes_when_latest_run_succeeds` (test)
- L354: class `_State`
- L355: method `__init__` parent=_State (test)
- L360: function `fake_latest` (test)
- L381: function `test_pipeline_wait_resolves_project_from_gcp_project` (test)
- L399: class `_State`
- L400: method `__init__` parent=_State (test)
- L403: function `fake_latest` (test)
- L422: function `test_pipeline_wait_fails_when_latest_run_fails` (test)
- L437: class `_State`
- L438: method `__init__` parent=_State (test)
- L441: function `fake_latest` (test)

## tools/check_docker_layout.py

- L13: class `CheckResult`
- L21: function `_exists`
- L25: function `_check_required`
- L49: function `_check_unexpected_suffix_dockerfiles`
- L67: function `_check_phase_layout_and_naming`
- L136: function `main`

