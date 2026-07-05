# LLM Context Pack

## Mandatory Rules

- Do not create, overwrite, or backfill Evidence. `evidence/` is read-only Non-LLM input.
- Create `catalog_items` by repo object, not by Evidence artifact. One item key must be a file/module/symbol/entrypoint/env/dependency/test surface in the target repo.
- Evidence artifacts are inputs only. Never make `00_scan_manifest.md`, `03_symbols.md`, `30_static_signal_hits.md`, `99_scan_limitations.md`, `grep`, `change_signal`, `/`, or `src/` into a catalog item.
- Cover every relevant Evidence Index row by attaching evidence_ids to repo-object items, `scan_summary`, or `evidence_appendix`; do not silently drop evidence.
- Facts must describe the target object, not the existence of Evidence Pack files.
- Put count-only grep totals, no-hit notes, parser limitations, scan manifest/metrics/file tree, generic public API listings, and generic change signals in `scan_summary` or `evidence_appendix`, not in `catalog_items`.
- Dependency inventory and test evidence are not mere appendix when present. Create repo-object catalog items for dependency surface (`Cargo.toml` or package manifest) and test surface (`test_count`, test modules, or test files) when the evidence exists.
- A catalog item must be self-contained: an upper model must not need to open `evidence/` or `src/` to understand the object state. Do not write `refer to the evidence file`, `当該ファイルを参照`, or equivalent.
- `scan_summary` and `evidence_appendix` must also be self-contained summaries. Do not write `詳細は証拠`, `証拠を参照`, `文脈確認が必要`, or other next-action wording anywhere in the output.
- Meaning must pass the repo-specific test: could this role/implication have been written without seeing this repo? If yes, move it to appendix or rewrite it around concrete target paths/symbols.
- Add `flow_items` as first-class observed flow candidates when command/entrypoint/symbol evidence exposes connected movement. Use the name `Observed Primary Flow Candidate` conceptually, but the machine label should be descriptive such as `primary_task_lifecycle_candidate`, `destructive_management_candidate`, or `clear_all_surface_candidate`.
- Flow items are descriptive mirror material, not recommendations. Do not call a flow Golden Path or Critical User Journey as fact.
- Keep primary lifecycle and destructive management flows separate. The primary candidate must not include remove/delete/clear steps or basis entries. Clear-all is distinct from remove and must not be merged into the remove flow. If clear evidence exists, create a separate `clear_all_surface_candidate` with `flow_type: destructive_surface_candidate`; when CLI exposure is uncertain, use `surface: candidate clear operation` and put the exposure gap in `cannot_conclude`.
- Do not write real subcommand names such as `task add` unless Command variants or CLI parse evidence confirms that exact surface. If not confirmed, use candidate language such as `candidate add operation` / `candidate list operation` / `candidate status update operation`.
- Each flow must include `basis` and each step must include `user_intent`, `surface`, `components`, `data_effect`, `confidence`, and `evidence_ids` in JSON. Markdown body will render semantic fields only; evidence_ids remain machine-only. If call graph evidence is not available, set `grounding_level: weak` and put the limitation in `cannot_conclude`.
- A grep no-hit is not proof that something does not exist.
- Do not infer, reconstruct, or preserve secret values.
- Keep fact fields Non-LLM and observational; put role and current implications in meaning.
- Do not include advice, recommendations, next actions, validation plans, rollback plans, or change boundaries.

## Domain Selection Rules

- `domain` は scan profile ではなく、target の実コード・entrypoint・domain evidence から見える主対象を書く。
- `profiles_run` / `detected_profiles` に `infra` が含まれていても、それだけで `domain: infra` にしない。YAML/JSON/config は補助 evidence として扱う。
- `domain: infra` は `domain/00_infra_resources.md` に具体的な Terraform / GitHub Actions / Dockerfile resource, job, image, or secret/env reference が観測される場合だけ使う。
- `domain/00_infra_resources.md` が `status: no infra domain evidence detected` の場合、小さな CLI / library / web app の domain を infra にしない。

## Machine Provenance Boundary（重要）

JSON では、下の Evidence IDs 表にある `evidence_id` を `evidence_ids` に入れて接地を示す。存在しない id は禁止。
ただし `evidence_ids` は machine join key であり、最上位モデルの新しいアイディア・設計判断には寄与しない。
最終 Markdown 本体には program が `evidence_ids` / file / line / scan_id / sha256 を一切出さない。完全な machine provenance は `evidence_index.jsonl` sidecar に隔離する。

## Evidence IDs（catalog_items で使える evidence_id）

| evidence_id | file | lines |
|---|---|---|
| ev.00_scan_manifest_md | evidence/00_scan_manifest.md | 1-46 |
| ev.00_evidence_freshness_md | evidence/00_evidence_freshness.md | 1-12 |
| ev.01_file_tree_md | evidence/01_file_tree.md | 1-694 |
| ev.02_files_json | evidence/02_files.json | 1-694 |
| ev.03_symbols_md | evidence/03_symbols.md | 1-4405 |
| ev.03_symbols_md.github_workflows_ci_yml | evidence/03_symbols.md | 3-12 |
| ev.03_symbols_md.github_workflows_deploy_api_yml | evidence/03_symbols.md | 13-19 |
| ev.03_symbols_md.github_workflows_deploy_dataform_yml | evidence/03_symbols.md | 20-26 |
| ev.03_symbols_md.github_workflows_deploy_encoder_image_yml | evidence/03_symbols.md | 27-33 |
| ev.03_symbols_md.github_workflows_deploy_pipeline_yml | evidence/03_symbols.md | 34-40 |
| ev.03_symbols_md.github_workflows_deploy_reranker_image_yml | evidence/03_symbols.md | 41-47 |
| ev.03_symbols_md.github_workflows_deploy_trainer_image_yml | evidence/03_symbols.md | 48-54 |
| ev.03_symbols_md.github_workflows_terraform_yml | evidence/03_symbols.md | 55-62 |
| ev.03_symbols_md.app_api_dependencies_py | evidence/03_symbols.md | 63-69 |
| ev.03_symbols_md.app_api_mappers_search_mapper_py | evidence/03_symbols.md | 70-76 |
| ev.03_symbols_md.app_api_middleware_request_logging_py | evidence/03_symbols.md | 77-83 |
| ev.03_symbols_md.app_api_routers_admin_mlops_router_py | evidence/03_symbols.md | 84-90 |
| ev.03_symbols_md.app_api_routers_feedback_router_py | evidence/03_symbols.md | 91-94 |
| ev.03_symbols_md.app_api_routers_health_router_py | evidence/03_symbols.md | 95-99 |
| ev.03_symbols_md.app_api_routers_model_router_py | evidence/03_symbols.md | 100-105 |
| ev.03_symbols_md.app_api_routers_ops_router_py | evidence/03_symbols.md | 106-114 |
| ev.03_symbols_md.app_api_routers_retrain_router_py | evidence/03_symbols.md | 115-118 |
| ev.03_symbols_md.app_api_routers_search_router_py | evidence/03_symbols.md | 119-122 |
| ev.03_symbols_md.app_api_routers_ui_router_py | evidence/03_symbols.md | 123-133 |
| ev.03_symbols_md.app_composition_root_py | evidence/03_symbols.md | 134-149 |
| ev.03_symbols_md.app_container_infra_py | evidence/03_symbols.md | 150-166 |
| ev.03_symbols_md.app_container_internal_optional_adapter_py | evidence/03_symbols.md | 167-170 |
| ev.03_symbols_md.app_container_ml_py | evidence/03_symbols.md | 171-183 |
| ev.03_symbols_md.app_container_search_py | evidence/03_symbols.md | 184-201 |
| ev.03_symbols_md.app_domain_candidate_py | evidence/03_symbols.md | 202-206 |
| ev.03_symbols_md.app_domain_event_py | evidence/03_symbols.md | 207-212 |
| ev.03_symbols_md.app_domain_labeling_py | evidence/03_symbols.md | 213-216 |
| ev.03_symbols_md.app_domain_retrieval_py | evidence/03_symbols.md | 217-221 |
| ev.03_symbols_md.app_domain_search_py | evidence/03_symbols.md | 222-228 |
| ev.03_symbols_md.app_domain_training_py | evidence/03_symbols.md | 229-233 |
| ev.03_symbols_md.app_main_py | evidence/03_symbols.md | 234-241 |
| ev.03_symbols_md.app_observability_py | evidence/03_symbols.md | 242-251 |
| ev.03_symbols_md.app_schemas_admin_mlops_py | evidence/03_symbols.md | 252-258 |
| ev.03_symbols_md.app_schemas_model_py | evidence/03_symbols.md | 259-267 |
| ev.03_symbols_md.app_schemas_ops_py | evidence/03_symbols.md | 268-276 |
| ev.03_symbols_md.app_schemas_search_py | evidence/03_symbols.md | 277-285 |
| ev.03_symbols_md.app_services_adapters_bigquery_candidate_retriever_py | evidence/03_symbols.md | 286-292 |
| ev.03_symbols_md.app_services_adapters_bigquery_data_catalog_reader_py | evidence/03_symbols.md | 293-309 |
| ev.03_symbols_md.app_services_adapters_bigquery_event_repository_py | evidence/03_symbols.md | 310-324 |
| ev.03_symbols_md.app_services_adapters_bigquery_label_repository_py | evidence/03_symbols.md | 325-331 |
| ev.03_symbols_md.app_services_adapters_bigquery_metrics_repository_py | evidence/03_symbols.md | 332-339 |
| ev.03_symbols_md.app_services_adapters_bqml_popularity_scorer_py | evidence/03_symbols.md | 340-345 |
| ev.03_symbols_md.app_services_adapters_cloud_logging_event_writer_py | evidence/03_symbols.md | 346-354 |
| ev.03_symbols_md.app_services_adapters_elasticsearch_lexical_py | evidence/03_symbols.md | 355-362 |
| ev.03_symbols_md.app_services_adapters_feature_online_store_fetcher_py | evidence/03_symbols.md | 363-375 |
| ev.03_symbols_md.app_services_adapters_gcs_training_dataset_repository_py | evidence/03_symbols.md | 376-385 |
| ev.03_symbols_md.app_services_adapters_internal_kserve_common_py | evidence/03_symbols.md | 386-394 |
| ev.03_symbols_md.app_services_adapters_internal_pubsub_diagnostics_py | evidence/03_symbols.md | 395-400 |
| ev.03_symbols_md.app_services_adapters_kserve_encoder_py | evidence/03_symbols.md | 401-407 |
| ev.03_symbols_md.app_services_adapters_kserve_reranker_py | evidence/03_symbols.md | 408-416 |
| ev.03_symbols_md.app_services_adapters_publisher_py | evidence/03_symbols.md | 417-422 |
| ev.03_symbols_md.app_services_adapters_pubsub_event_writer_py | evidence/03_symbols.md | 423-432 |
| ev.03_symbols_md.app_services_adapters_pubsub_feedback_recorder_py | evidence/03_symbols.md | 433-438 |
| ev.03_symbols_md.app_services_adapters_pubsub_ranking_log_publisher_py | evidence/03_symbols.md | 439-444 |
| ev.03_symbols_md.app_services_adapters_redis_synonym_expander_py | evidence/03_symbols.md | 445-452 |
| ev.03_symbols_md.app_services_adapters_retrain_py | evidence/03_symbols.md | 453-461 |
| ev.03_symbols_md.app_services_adapters_vertex_vector_search_semantic_search_py | evidence/03_symbols.md | 462-468 |
| ev.03_symbols_md.app_services_data_catalog_service_py | evidence/03_symbols.md | 469-474 |
| ev.03_symbols_md.app_services_feedback_service_py | evidence/03_symbols.md | 475-480 |
| ev.03_symbols_md.app_services_model_metrics_service_py | evidence/03_symbols.md | 481-497 |
| ev.03_symbols_md.app_services_noop_adapters_noop_data_catalog_reader_py | evidence/03_symbols.md | 498-502 |
| ev.03_symbols_md.app_services_noop_adapters_noop_event_repository_py | evidence/03_symbols.md | 503-509 |
| ev.03_symbols_md.app_services_noop_adapters_noop_event_writer_py | evidence/03_symbols.md | 510-516 |
| ev.03_symbols_md.app_services_noop_adapters_noop_feedback_recorder_py | evidence/03_symbols.md | 517-521 |
| ev.03_symbols_md.app_services_noop_adapters_noop_label_repository_py | evidence/03_symbols.md | 522-527 |
| ev.03_symbols_md.app_services_noop_adapters_noop_lexical_search_py | evidence/03_symbols.md | 528-532 |
| ev.03_symbols_md.app_services_noop_adapters_noop_metrics_repository_py | evidence/03_symbols.md | 533-539 |
| ev.03_symbols_md.app_services_noop_adapters_noop_ranking_log_publisher_py | evidence/03_symbols.md | 540-544 |
| ev.03_symbols_md.app_services_noop_adapters_noop_retrain_queries_py | evidence/03_symbols.md | 545-551 |
| ev.03_symbols_md.app_services_noop_adapters_noop_synonym_expander_py | evidence/03_symbols.md | 552-556 |
| ev.03_symbols_md.app_services_noop_adapters_noop_training_dataset_repository_py | evidence/03_symbols.md | 557-563 |
| ev.03_symbols_md.app_services_protocols_candidate_retriever_py | evidence/03_symbols.md | 564-568 |
| ev.03_symbols_md.app_services_protocols_data_catalog_reader_py | evidence/03_symbols.md | 569-575 |
| ev.03_symbols_md.app_services_protocols_encoder_client_py | evidence/03_symbols.md | 576-580 |
| ev.03_symbols_md.app_services_protocols_event_repository_py | evidence/03_symbols.md | 581-587 |
| ev.03_symbols_md.app_services_protocols_event_writer_py | evidence/03_symbols.md | 588-594 |
| ev.03_symbols_md.app_services_protocols_feature_fetcher_py | evidence/03_symbols.md | 595-600 |
| ev.03_symbols_md.app_services_protocols_feedback_recorder_py | evidence/03_symbols.md | 601-605 |
| ev.03_symbols_md.app_services_protocols_label_repository_py | evidence/03_symbols.md | 606-611 |
| ev.03_symbols_md.app_services_protocols_lexical_search_py | evidence/03_symbols.md | 612-616 |
| ev.03_symbols_md.app_services_protocols_metrics_repository_py | evidence/03_symbols.md | 617-623 |
| ev.03_symbols_md.app_services_protocols_popularity_scorer_py | evidence/03_symbols.md | 624-628 |
| ev.03_symbols_md.app_services_protocols_publisher_py | evidence/03_symbols.md | 629-635 |
| ev.03_symbols_md.app_services_protocols_ranking_log_publisher_py | evidence/03_symbols.md | 636-640 |
| ev.03_symbols_md.app_services_protocols_reranker_client_py | evidence/03_symbols.md | 641-647 |
| ev.03_symbols_md.app_services_protocols_retrain_queries_py | evidence/03_symbols.md | 648-654 |
| ev.03_symbols_md.app_services_protocols_semantic_search_py | evidence/03_symbols.md | 655-659 |
| ev.03_symbols_md.app_services_protocols_synonym_expander_py | evidence/03_symbols.md | 660-664 |
| ev.03_symbols_md.app_services_protocols_training_dataset_repository_py | evidence/03_symbols.md | 665-671 |
| ev.03_symbols_md.app_services_ranking_py | evidence/03_symbols.md | 672-681 |
| ev.03_symbols_md.app_services_retrain_policy_py | evidence/03_symbols.md | 682-687 |
| ev.03_symbols_md.app_services_search_service_py | evidence/03_symbols.md | 688-700 |
| ev.03_symbols_md.app_settings_api_py | evidence/03_symbols.md | 701-714 |
| ev.03_symbols_md.app_static_css_custom_css | evidence/03_symbols.md | 715-839 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css | evidence/03_symbols.md | 840-1013 |
| ev.03_symbols_md.app_static_css_pico_admin_layout_css | evidence/03_symbols.md | 1014-1083 |
| ev.03_symbols_md.app_static_css_pico_admin_theme_css | evidence/03_symbols.md | 1084-1134 |
| ev.03_symbols_md.app_static_js_search_ui_js | evidence/03_symbols.md | 1135-1149 |
| ev.03_symbols_md.app_templates__feedback_panel_html | evidence/03_symbols.md | 1150-1165 |
| ev.03_symbols_md.app_templates__search_form_html | evidence/03_symbols.md | 1166-1192 |
| ev.03_symbols_md.app_templates__search_results_html | evidence/03_symbols.md | 1193-1224 |
| ev.03_symbols_md.app_templates_base_html | evidence/03_symbols.md | 1225-1255 |
| ev.03_symbols_md.app_templates_data_html | evidence/03_symbols.md | 1256-1276 |
| ev.03_symbols_md.app_templates_index_html | evidence/03_symbols.md | 1277-1281 |
| ev.03_symbols_md.app_templates_model_metrics_html | evidence/03_symbols.md | 1282-1311 |
| ev.03_symbols_md.app_templates_ops_html | evidence/03_symbols.md | 1312-1358 |
| ev.03_symbols_md.app_templates_property_detail_html | evidence/03_symbols.md | 1359-1378 |
| ev.03_symbols_md.app_templates_search_dev_html | evidence/03_symbols.md | 1379-1395 |
| ev.03_symbols_md.infra_run_services_composer_runner_dockerfile | evidence/03_symbols.md | 1396-1400 |
| ev.03_symbols_md.infra_run_services_encoder_dockerfile | evidence/03_symbols.md | 1401-1405 |
| ev.03_symbols_md.infra_run_services_ml_base_dockerfile | evidence/03_symbols.md | 1406-1409 |
| ev.03_symbols_md.infra_run_services_reranker_dockerfile | evidence/03_symbols.md | 1410-1414 |
| ev.03_symbols_md.infra_run_services_search_api_dockerfile | evidence/03_symbols.md | 1415-1419 |
| ev.03_symbols_md.infra_terraform_environments_dev_apis_tf | evidence/03_symbols.md | 1420-1423 |
| ev.03_symbols_md.infra_terraform_modules_composer_main_tf | evidence/03_symbols.md | 1424-1427 |
| ev.03_symbols_md.infra_terraform_modules_data_main_tf | evidence/03_symbols.md | 1428-1477 |
| ev.03_symbols_md.infra_terraform_modules_dns_main_tf | evidence/03_symbols.md | 1478-1487 |
| ev.03_symbols_md.infra_terraform_modules_elasticsearch_main_tf | evidence/03_symbols.md | 1488-1492 |
| ev.03_symbols_md.infra_terraform_modules_gke_main_tf | evidence/03_symbols.md | 1493-1500 |
| ev.03_symbols_md.infra_terraform_modules_iam_main_tf | evidence/03_symbols.md | 1501-1549 |
| ev.03_symbols_md.infra_terraform_modules_kserve_main_tf | evidence/03_symbols.md | 1550-1561 |
| ev.03_symbols_md.infra_terraform_modules_kserve_tls_dev_tf | evidence/03_symbols.md | 1562-1567 |
| ev.03_symbols_md.infra_terraform_modules_messaging_main_tf | evidence/03_symbols.md | 1568-1591 |
| ev.03_symbols_md.infra_terraform_modules_monitoring_main_tf | evidence/03_symbols.md | 1592-1602 |
| ev.03_symbols_md.infra_terraform_modules_redis_synonym_main_tf | evidence/03_symbols.md | 1603-1608 |
| ev.03_symbols_md.infra_terraform_modules_slo_main_tf | evidence/03_symbols.md | 1609-1624 |
| ev.03_symbols_md.infra_terraform_modules_streaming_main_tf | evidence/03_symbols.md | 1625-1634 |
| ev.03_symbols_md.infra_terraform_modules_vector_search_main_tf | evidence/03_symbols.md | 1635-1640 |
| ev.03_symbols_md.infra_terraform_modules_vertex_main_tf | evidence/03_symbols.md | 1641-1660 |
| ev.03_symbols_md.ml_common_config_base_py | evidence/03_symbols.md | 1661-1665 |
| ev.03_symbols_md.ml_common_config_embedding_py | evidence/03_symbols.md | 1666-1669 |
| ev.03_symbols_md.ml_common_config_training_py | evidence/03_symbols.md | 1670-1673 |
| ev.03_symbols_md.ml_common_logging_structured_logging_py | evidence/03_symbols.md | 1674-1680 |
| ev.03_symbols_md.ml_common_utils_run_id_py | evidence/03_symbols.md | 1681-1684 |
| ev.03_symbols_md.ml_data_datasets_embedding_batch_py | evidence/03_symbols.md | 1685-1694 |
| ev.03_symbols_md.ml_data_feature_engineering_ranker_features_py | evidence/03_symbols.md | 1695-1698 |
| ev.03_symbols_md.ml_data_loaders_embedding_store_py | evidence/03_symbols.md | 1699-1715 |
| ev.03_symbols_md.ml_data_loaders_ranker_repository_py | evidence/03_symbols.md | 1716-1729 |
| ev.03_symbols_md.ml_evaluation_metrics_label_gain_py | evidence/03_symbols.md | 1730-1733 |
| ev.03_symbols_md.ml_evaluation_metrics_ranking_py | evidence/03_symbols.md | 1734-1742 |
| ev.03_symbols_md.ml_labeling_policy_py | evidence/03_symbols.md | 1743-1747 |
| ev.03_symbols_md.ml_registry_adapters_vertex_model_registry_py | evidence/03_symbols.md | 1748-1756 |
| ev.03_symbols_md.ml_registry_artifact_store_py | evidence/03_symbols.md | 1757-1771 |
| ev.03_symbols_md.ml_registry_metadata_store_py | evidence/03_symbols.md | 1772-1778 |
| ev.03_symbols_md.ml_registry_model_registry_py | evidence/03_symbols.md | 1779-1785 |
| ev.03_symbols_md.ml_registry_ports_model_registry_py | evidence/03_symbols.md | 1786-1793 |
| ev.03_symbols_md.ml_serving_adapters_kserve_predictor_py | evidence/03_symbols.md | 1794-1800 |
| ev.03_symbols_md.ml_serving_calibration_py | evidence/03_symbols.md | 1801-1804 |
| ev.03_symbols_md.ml_serving_encoder_py | evidence/03_symbols.md | 1805-1824 |
| ev.03_symbols_md.ml_serving_ports_predictor_service_py | evidence/03_symbols.md | 1825-1830 |
| ev.03_symbols_md.ml_serving_predictor_py | evidence/03_symbols.md | 1831-1837 |
| ev.03_symbols_md.ml_serving_reranker_py | evidence/03_symbols.md | 1838-1852 |
| ev.03_symbols_md.ml_streaming_adapters_dataflow_processor_py | evidence/03_symbols.md | 1853-1857 |
| ev.03_symbols_md.ml_streaming_container_dockerfile | evidence/03_symbols.md | 1858-1861 |
| ev.03_symbols_md.ml_streaming_pipeline_py | evidence/03_symbols.md | 1862-1877 |
| ev.03_symbols_md.ml_streaming_ports_stream_processor_py | evidence/03_symbols.md | 1878-1883 |
| ev.03_symbols_md.ml_training_adapters_lightgbm_trainer_py | evidence/03_symbols.md | 1884-1894 |
| ev.03_symbols_md.ml_training_experiments_adapters_null_tracker_py | evidence/03_symbols.md | 1895-1902 |
| ev.03_symbols_md.ml_training_experiments_adapters_vertex_experiments_tracker_py | evidence/03_symbols.md | 1903-1911 |
| ev.03_symbols_md.ml_training_experiments_ports_experiment_tracker_py | evidence/03_symbols.md | 1912-1919 |
| ev.03_symbols_md.ml_training_model_builder_py | evidence/03_symbols.md | 1920-1924 |
| ev.03_symbols_md.ml_training_ports_ranker_model_py | evidence/03_symbols.md | 1925-1931 |
| ev.03_symbols_md.ml_training_ports_ranker_trainer_py | evidence/03_symbols.md | 1932-1937 |
| ev.03_symbols_md.ml_training_trainer_py | evidence/03_symbols.md | 1938-1952 |
| ev.03_symbols_md.pipeline_batch_serving_job_main_py | evidence/03_symbols.md | 1953-1958 |
| ev.03_symbols_md.pipeline_dags__common_py | evidence/03_symbols.md | 1959-1966 |
| ev.03_symbols_md.pipeline_dags__pod_py | evidence/03_symbols.md | 1967-1973 |
| ev.03_symbols_md.pipeline_dags_daily_feature_refresh_py | evidence/03_symbols.md | 1974-1977 |
| ev.03_symbols_md.pipeline_dags_monitoring_validation_py | evidence/03_symbols.md | 1978-1981 |
| ev.03_symbols_md.pipeline_dags_retrain_orchestration_py | evidence/03_symbols.md | 1982-1985 |
| ev.03_symbols_md.pipeline_data_job_adapters_in_memory_vector_search_writer_py | evidence/03_symbols.md | 1986-1991 |
| ev.03_symbols_md.pipeline_data_job_adapters_vertex_vector_search_writer_py | evidence/03_symbols.md | 1992-2000 |
| ev.03_symbols_md.pipeline_data_job_components_batch_predict_embeddings_py | evidence/03_symbols.md | 2001-2004 |
| ev.03_symbols_md.pipeline_data_job_components_load_properties_py | evidence/03_symbols.md | 2005-2008 |
| ev.03_symbols_md.pipeline_data_job_components_upsert_vector_search_py | evidence/03_symbols.md | 2009-2012 |
| ev.03_symbols_md.pipeline_data_job_components_write_embeddings_py | evidence/03_symbols.md | 2013-2016 |
| ev.03_symbols_md.pipeline_data_job_main_py | evidence/03_symbols.md | 2017-2023 |
| ev.03_symbols_md.pipeline_data_job_ports_vector_search_writer_py | evidence/03_symbols.md | 2024-2029 |
| ev.03_symbols_md.pipeline_evaluation_job_main_py | evidence/03_symbols.md | 2030-2035 |
| ev.03_symbols_md.pipeline_labeling_job_main_py | evidence/03_symbols.md | 2036-2040 |
| ev.03_symbols_md.pipeline_training_dataset_job_main_py | evidence/03_symbols.md | 2041-2045 |
| ev.03_symbols_md.pipeline_training_job_adapters_kfp_orchestrator_py | evidence/03_symbols.md | 2046-2059 |
| ev.03_symbols_md.pipeline_training_job_components_evaluate_py | evidence/03_symbols.md | 2060-2064 |
| ev.03_symbols_md.pipeline_training_job_components_load_features_py | evidence/03_symbols.md | 2065-2069 |
| ev.03_symbols_md.pipeline_training_job_components_register_reranker_py | evidence/03_symbols.md | 2070-2074 |
| ev.03_symbols_md.pipeline_training_job_components_train_reranker_py | evidence/03_symbols.md | 2075-2079 |
| ev.03_symbols_md.pipeline_training_job_main_py | evidence/03_symbols.md | 2080-2086 |
| ev.03_symbols_md.pipeline_training_job_ports_pipeline_component_py | evidence/03_symbols.md | 2087-2094 |
| ev.03_symbols_md.pipeline_training_job_ports_pipeline_orchestrator_py | evidence/03_symbols.md | 2095-2103 |
| ev.03_symbols_md.pipeline_workflow_compile_py | evidence/03_symbols.md | 2104-2115 |
| ev.03_symbols_md.pipeline_workflow_trigger_py | evidence/03_symbols.md | 2116-2125 |
| ev.03_symbols_md.pipeline_workflow_trigger_zip_main_py | evidence/03_symbols.md | 2126-2135 |
| ev.03_symbols_md.scripts__common_py | evidence/03_symbols.md | 2136-2161 |
| ev.03_symbols_md.scripts_adapters_gcloud_py | evidence/03_symbols.md | 2162-2165 |
| ev.03_symbols_md.scripts_adapters_kubectl_py | evidence/03_symbols.md | 2166-2169 |
| ev.03_symbols_md.scripts_adapters_terraform_py | evidence/03_symbols.md | 2170-2173 |
| ev.03_symbols_md.scripts_bqml_train_popularity_py | evidence/03_symbols.md | 2174-2177 |
| ev.03_symbols_md.scripts_ci_layers_py | evidence/03_symbols.md | 2178-2189 |
| ev.03_symbols_md.scripts_ci_sync_configmap_py | evidence/03_symbols.md | 2190-2194 |
| ev.03_symbols_md.scripts_ci_sync_dataform_py | evidence/03_symbols.md | 2195-2199 |
| ev.03_symbols_md.scripts_deploy_api_gke_py | evidence/03_symbols.md | 2200-2210 |
| ev.03_symbols_md.scripts_deploy_api_gke_local_py | evidence/03_symbols.md | 2211-2222 |
| ev.03_symbols_md.scripts_deploy_build_all_local_py | evidence/03_symbols.md | 2223-2228 |
| ev.03_symbols_md.scripts_deploy_build_kserve_images_py | evidence/03_symbols.md | 2229-2238 |
| ev.03_symbols_md.scripts_deploy_build_kserve_images_local_py | evidence/03_symbols.md | 2239-2253 |
| ev.03_symbols_md.scripts_deploy_composer_deploy_dags_py | evidence/03_symbols.md | 2254-2261 |
| ev.03_symbols_md.scripts_deploy_composer_runner_py | evidence/03_symbols.md | 2262-2269 |
| ev.03_symbols_md.scripts_deploy_configmap_overlay_py | evidence/03_symbols.md | 2270-2275 |
| ev.03_symbols_md.scripts_deploy_kserve_models_py | evidence/03_symbols.md | 2276-2290 |
| ev.03_symbols_md.scripts_deploy_monitor_py | evidence/03_symbols.md | 2291-2305 |
| ev.03_symbols_md.scripts_deploy_seed_lgbm_model_py | evidence/03_symbols.md | 2306-2315 |
| ev.03_symbols_md.scripts_domain_gcp_feature_view_sync_py | evidence/03_symbols.md | 2316-2326 |
| ev.03_symbols_md.scripts_domain_gcp_gcs_cleanup_py | evidence/03_symbols.md | 2327-2331 |
| ev.03_symbols_md.scripts_domain_gcp_state_recovery_py | evidence/03_symbols.md | 2332-2352 |
| ev.03_symbols_md.scripts_domain_gcp_vertex_cleanup_py | evidence/03_symbols.md | 2353-2361 |
| ev.03_symbols_md.scripts_domain_gcp_vertex_feature_store_wait_py | evidence/03_symbols.md | 2362-2370 |
| ev.03_symbols_md.scripts_domain_gcp_vertex_import_py | evidence/03_symbols.md | 2371-2377 |
| ev.03_symbols_md.scripts_domain_k8s_elasticsearch_wait_py | evidence/03_symbols.md | 2378-2383 |
| ev.03_symbols_md.scripts_domain_k8s_kube_cleanup_py | evidence/03_symbols.md | 2384-2387 |
| ev.03_symbols_md.scripts_domain_k8s_kubectl_context_py | evidence/03_symbols.md | 2388-2392 |
| ev.03_symbols_md.scripts_domain_terraform_lock_py | evidence/03_symbols.md | 2393-2400 |
| ev.03_symbols_md.scripts_domain_terraform_stage_apply_py | evidence/03_symbols.md | 2401-2404 |
| ev.03_symbols_md.scripts_domain_terraform_state_py | evidence/03_symbols.md | 2405-2413 |
| ev.03_symbols_md.scripts_lib_bq_property_rows_py | evidence/03_symbols.md | 2414-2417 |
| ev.03_symbols_md.scripts_lib_config_py | evidence/03_symbols.md | 2418-2422 |
| ev.03_symbols_md.scripts_lib_makefile_help_py | evidence/03_symbols.md | 2423-2427 |
| ev.03_symbols_md.scripts_lib_step_timing_py | evidence/03_symbols.md | 2428-2435 |
| ev.03_symbols_md.scripts_ops_accuracy_report_py | evidence/03_symbols.md | 2436-2446 |
| ev.03_symbols_md.scripts_ops_check_retrain_py | evidence/03_symbols.md | 2447-2451 |
| ev.03_symbols_md.scripts_ops_composer_dag_py | evidence/03_symbols.md | 2452-2458 |
| ev.03_symbols_md.scripts_ops_composer_task_states_py | evidence/03_symbols.md | 2459-2467 |
| ev.03_symbols_md.scripts_ops_destroy_check_py | evidence/03_symbols.md | 2468-2495 |
| ev.03_symbols_md.scripts_ops_feedback_py | evidence/03_symbols.md | 2496-2499 |
| ev.03_symbols_md.scripts_ops_label_seed_py | evidence/03_symbols.md | 2500-2503 |
| ev.03_symbols_md.scripts_ops_livez_py | evidence/03_symbols.md | 2504-2507 |
| ev.03_symbols_md.scripts_ops_promote_py | evidence/03_symbols.md | 2508-2522 |
| ev.03_symbols_md.scripts_ops_ranking_py | evidence/03_symbols.md | 2523-2526 |
| ev.03_symbols_md.scripts_ops_register_model_py | evidence/03_symbols.md | 2527-2533 |
| ev.03_symbols_md.scripts_ops_run_all_py | evidence/03_symbols.md | 2534-2538 |
| ev.03_symbols_md.scripts_ops_search_py | evidence/03_symbols.md | 2539-2543 |
| ev.03_symbols_md.scripts_ops_search_components_py | evidence/03_symbols.md | 2544-2548 |
| ev.03_symbols_md.scripts_ops_slo_status_py | evidence/03_symbols.md | 2549-2556 |
| ev.03_symbols_md.scripts_ops_submit_train_pipeline_py | evidence/03_symbols.md | 2557-2560 |
| ev.03_symbols_md.scripts_ops_sync_elasticsearch_py | evidence/03_symbols.md | 2561-2572 |
| ev.03_symbols_md.scripts_ops_sync_synonyms_py | evidence/03_symbols.md | 2573-2582 |
| ev.03_symbols_md.scripts_ops_vertex_explain_py | evidence/03_symbols.md | 2583-2586 |
| ev.03_symbols_md.scripts_ops_vertex_feature_group_py | evidence/03_symbols.md | 2587-2594 |
| ev.03_symbols_md.scripts_ops_vertex_models_list_py | evidence/03_symbols.md | 2595-2598 |
| ev.03_symbols_md.scripts_ops_vertex_monitoring_py | evidence/03_symbols.md | 2599-2602 |
| ev.03_symbols_md.scripts_ops_vertex_pipeline_status_py | evidence/03_symbols.md | 2603-2606 |
| ev.03_symbols_md.scripts_ops_vertex_pipeline_wait_py | evidence/03_symbols.md | 2607-2612 |
| ev.03_symbols_md.scripts_ops_vertex_vector_search_py | evidence/03_symbols.md | 2613-2618 |
| ev.03_symbols_md.scripts_setup_backfill_vector_search_index_py | evidence/03_symbols.md | 2619-2628 |
| ev.03_symbols_md.scripts_setup_create_schedule_py | evidence/03_symbols.md | 2629-2633 |
| ev.03_symbols_md.scripts_setup_deploy_all_py | evidence/03_symbols.md | 2634-2659 |
| ev.03_symbols_md.scripts_setup_destroy_all_py | evidence/03_symbols.md | 2660-2679 |
| ev.03_symbols_md.scripts_setup_doctor_py | evidence/03_symbols.md | 2680-2684 |
| ev.03_symbols_md.scripts_setup_local_hybrid_py | evidence/03_symbols.md | 2685-2696 |
| ev.03_symbols_md.scripts_setup_print_github_variables_py | evidence/03_symbols.md | 2697-2702 |
| ev.03_symbols_md.scripts_setup_recover_wif_py | evidence/03_symbols.md | 2703-2708 |
| ev.03_symbols_md.scripts_setup_seed_minimal_py | evidence/03_symbols.md | 2709-2715 |
| ev.03_symbols_md.scripts_setup_seed_minimal_clean_py | evidence/03_symbols.md | 2716-2719 |
| ev.03_symbols_md.scripts_setup_setup_model_monitoring_py | evidence/03_symbols.md | 2720-2724 |
| ev.03_symbols_md.scripts_setup_tf_apply_py | evidence/03_symbols.md | 2725-2728 |
| ev.03_symbols_md.scripts_setup_tf_bootstrap_py | evidence/03_symbols.md | 2729-2732 |
| ev.03_symbols_md.scripts_setup_tf_init_py | evidence/03_symbols.md | 2733-2736 |
| ev.03_symbols_md.scripts_setup_tf_plan_py | evidence/03_symbols.md | 2737-2740 |
| ev.03_symbols_md.scripts_setup_upload_encoder_assets_py | evidence/03_symbols.md | 2741-2749 |
| ev.03_symbols_md.scripts_verify__runner_py | evidence/03_symbols.md | 2750-2756 |
| ev.03_symbols_md.scripts_verify_deploy_all_py | evidence/03_symbols.md | 2757-2760 |
| ev.03_symbols_md.scripts_verify_destroy_all_py | evidence/03_symbols.md | 2761-2764 |
| ev.03_symbols_md.scripts_verify_full_recreate_py | evidence/03_symbols.md | 2765-2768 |
| ev.03_symbols_md.scripts_verify_live_acceptance_py | evidence/03_symbols.md | 2769-2772 |
| ev.03_symbols_md.system_map_html | evidence/03_symbols.md | 2773-2969 |
| ev.03_symbols_md.tests__fakes_in_memory_candidate_retriever_py | evidence/03_symbols.md | 2970-2977 |
| ev.03_symbols_md.tests__fakes_in_memory_event_writer_py | evidence/03_symbols.md | 2978-2986 |
| ev.03_symbols_md.tests__fakes_in_memory_feature_fetcher_py | evidence/03_symbols.md | 2987-2992 |
| ev.03_symbols_md.tests__fakes_in_memory_feedback_recorder_py | evidence/03_symbols.md | 2993-2999 |
| ev.03_symbols_md.tests__fakes_in_memory_lexical_search_py | evidence/03_symbols.md | 3000-3007 |
| ev.03_symbols_md.tests__fakes_in_memory_metrics_repository_py | evidence/03_symbols.md | 3008-3016 |
| ev.03_symbols_md.tests__fakes_in_memory_ranking_log_publisher_py | evidence/03_symbols.md | 3017-3023 |
| ev.03_symbols_md.tests__fakes_in_memory_semantic_search_py | evidence/03_symbols.md | 3024-3031 |
| ev.03_symbols_md.tests__fakes_in_memory_training_dataset_repository_py | evidence/03_symbols.md | 3032-3040 |
| ev.03_symbols_md.tests__fakes_mock_prediction_publisher_py | evidence/03_symbols.md | 3041-3046 |
| ev.03_symbols_md.tests__fakes_mock_reranker_client_py | evidence/03_symbols.md | 3047-3054 |
| ev.03_symbols_md.tests__fakes_stub_encoder_client_py | evidence/03_symbols.md | 3055-3063 |
| ev.03_symbols_md.tests__fakes_stub_popularity_scorer_py | evidence/03_symbols.md | 3064-3069 |
| ev.03_symbols_md.tests__fakes_stub_retrain_queries_py | evidence/03_symbols.md | 3070-3077 |
| ev.03_symbols_md.tests_conftest_py | evidence/03_symbols.md | 3078-3098 |
| ev.03_symbols_md.tests_e2e_live_acceptance_checks_py | evidence/03_symbols.md | 3099-3103 |
| ev.03_symbols_md.tests_e2e_test_full_recreate_gate_py | evidence/03_symbols.md | 3104-3109 |
| ev.03_symbols_md.tests_e2e_test_live_acceptance_gate_py | evidence/03_symbols.md | 3110-3114 |
| ev.03_symbols_md.tests_integration_infra_test_destroy_all_table_parity_py | evidence/03_symbols.md | 3115-3125 |
| ev.03_symbols_md.tests_integration_infra_test_infra_ranker_tables_py | evidence/03_symbols.md | 3126-3142 |
| ev.03_symbols_md.tests_integration_infra_test_makefile_py | evidence/03_symbols.md | 3143-3146 |
| ev.03_symbols_md.tests_integration_infra_test_manifests_structure_py | evidence/03_symbols.md | 3147-3163 |
| ev.03_symbols_md.tests_integration_infra_test_public_domain_consistency_py | evidence/03_symbols.md | 3164-3180 |
| ev.03_symbols_md.tests_integration_infra_test_terraform_module_structure_py | evidence/03_symbols.md | 3181-3186 |
| ev.03_symbols_md.tests_integration_infra_test_workflows_structure_py | evidence/03_symbols.md | 3187-3197 |
| ev.03_symbols_md.tests_integration_parity_parity_invariant_py | evidence/03_symbols.md | 3198-3203 |
| ev.03_symbols_md.tests_integration_parity_test_api_route_prefixes_py | evidence/03_symbols.md | 3204-3220 |
| ev.03_symbols_md.tests_integration_parity_test_codebase_invariants_py | evidence/03_symbols.md | 3221-3233 |
| ev.03_symbols_md.tests_integration_parity_test_configmap_drift_py | evidence/03_symbols.md | 3234-3239 |
| ev.03_symbols_md.tests_integration_parity_test_dataform_workflow_settings_py | evidence/03_symbols.md | 3240-3245 |
| ev.03_symbols_md.tests_integration_parity_test_event_schema_parity_py | evidence/03_symbols.md | 3246-3260 |
| ev.03_symbols_md.tests_integration_parity_test_feature_parity_feature_group_py | evidence/03_symbols.md | 3261-3268 |
| ev.03_symbols_md.tests_integration_parity_test_feature_parity_ranking_py | evidence/03_symbols.md | 3269-3278 |
| ev.03_symbols_md.tests_integration_parity_test_feature_parity_sql_ranker_py | evidence/03_symbols.md | 3279-3286 |
| ev.03_symbols_md.tests_integration_pipeline_test_pipeline_compile_py | evidence/03_symbols.md | 3287-3293 |
| ev.03_symbols_md.tests_integration_workflow_conftest_py | evidence/03_symbols.md | 3294-3297 |
| ev.03_symbols_md.tests_integration_workflow_test_composer_dags_contract_py | evidence/03_symbols.md | 3298-3308 |
| ev.03_symbols_md.tests_integration_workflow_test_composer_gcloud_json_contract_py | evidence/03_symbols.md | 3309-3317 |
| ev.03_symbols_md.tests_integration_workflow_test_composer_module_contract_py | evidence/03_symbols.md | 3318-3347 |
| ev.03_symbols_md.tests_integration_workflow_test_deploy_all_contract_py | evidence/03_symbols.md | 3348-3363 |
| ev.03_symbols_md.tests_integration_workflow_test_destroy_all_contract_py | evidence/03_symbols.md | 3364-3384 |
| ev.03_symbols_md.tests_integration_workflow_test_docs_canonical_contract_py | evidence/03_symbols.md | 3385-3390 |
| ev.03_symbols_md.tests_integration_workflow_test_elasticsearch_workflow_contract_py | evidence/03_symbols.md | 3391-3397 |
| ev.03_symbols_md.tests_integration_workflow_test_ground_truth_contract_py | evidence/03_symbols.md | 3398-3404 |
| ev.03_symbols_md.tests_integration_workflow_test_infra_apis_contract_py | evidence/03_symbols.md | 3405-3412 |
| ev.03_symbols_md.tests_integration_workflow_test_local_workflow_contract_py | evidence/03_symbols.md | 3413-3422 |
| ev.03_symbols_md.tests_integration_workflow_test_vertex_pipeline_submit_contract_py | evidence/03_symbols.md | 3423-3428 |
| ev.03_symbols_md.tests_integration_workflow_test_vertex_resources_contract_py | evidence/03_symbols.md | 3429-3437 |
| ev.03_symbols_md.tests_unit_app_conftest_py | evidence/03_symbols.md | 3438-3442 |
| ev.03_symbols_md.tests_unit_app_test_adapters_py | evidence/03_symbols.md | 3443-3465 |
| ev.03_symbols_md.tests_unit_app_test_api_contract_template_py | evidence/03_symbols.md | 3466-3483 |
| ev.03_symbols_md.tests_unit_app_test_bq_retrain_queries_py | evidence/03_symbols.md | 3484-3495 |
| ev.03_symbols_md.tests_unit_app_test_check_retrain_endpoint_py | evidence/03_symbols.md | 3496-3509 |
| ev.03_symbols_md.tests_unit_app_test_elasticsearch_lexical_py | evidence/03_symbols.md | 3510-3514 |
| ev.03_symbols_md.tests_unit_app_test_event_repositories_py | evidence/03_symbols.md | 3515-3522 |
| ev.03_symbols_md.tests_unit_app_test_explain_py | evidence/03_symbols.md | 3523-3537 |
| ev.03_symbols_md.tests_unit_app_test_feature_fetcher_adapters_py | evidence/03_symbols.md | 3538-3562 |
| ev.03_symbols_md.tests_unit_app_test_feedback_handler_http_py | evidence/03_symbols.md | 3563-3568 |
| ev.03_symbols_md.tests_unit_app_test_feedback_service_py | evidence/03_symbols.md | 3569-3574 |
| ev.03_symbols_md.tests_unit_app_test_health_handler_py | evidence/03_symbols.md | 3575-3581 |
| ev.03_symbols_md.tests_unit_app_test_kserve_wiring_py | evidence/03_symbols.md | 3582-3598 |
| ev.03_symbols_md.tests_unit_app_test_local_boot_contract_py | evidence/03_symbols.md | 3599-3603 |
| ev.03_symbols_md.tests_unit_app_test_logging_middleware_py | evidence/03_symbols.md | 3604-3609 |
| ev.03_symbols_md.tests_unit_app_test_main_routing_py | evidence/03_symbols.md | 3610-3624 |
| ev.03_symbols_md.tests_unit_app_test_model_handler_py | evidence/03_symbols.md | 3625-3636 |
| ev.03_symbols_md.tests_unit_app_test_observability_py | evidence/03_symbols.md | 3637-3643 |
| ev.03_symbols_md.tests_unit_app_test_ops_handler_py | evidence/03_symbols.md | 3644-3652 |
| ev.03_symbols_md.tests_unit_app_test_optional_adapter_helper_py | evidence/03_symbols.md | 3653-3660 |
| ev.03_symbols_md.tests_unit_app_test_publisher_py | evidence/03_symbols.md | 3661-3664 |
| ev.03_symbols_md.tests_unit_app_test_pubsub_event_writer_py | evidence/03_symbols.md | 3665-3677 |
| ev.03_symbols_md.tests_unit_app_test_ranking_service_py | evidence/03_symbols.md | 3678-3704 |
| ev.03_symbols_md.tests_unit_app_test_retrain_py | evidence/03_symbols.md | 3705-3725 |
| ev.03_symbols_md.tests_unit_app_test_run_search_feature_fetcher_py | evidence/03_symbols.md | 3726-3742 |
| ev.03_symbols_md.tests_unit_app_test_search_api_py | evidence/03_symbols.md | 3743-3769 |
| ev.03_symbols_md.tests_unit_app_test_search_builder_canonical_py | evidence/03_symbols.md | 3770-3788 |
| ev.03_symbols_md.tests_unit_app_test_search_handler_http_py | evidence/03_symbols.md | 3789-3796 |
| ev.03_symbols_md.tests_unit_app_test_search_mapper_py | evidence/03_symbols.md | 3797-3801 |
| ev.03_symbols_md.tests_unit_app_test_search_service_py | evidence/03_symbols.md | 3802-3813 |
| ev.03_symbols_md.tests_unit_app_test_settings_sources_py | evidence/03_symbols.md | 3814-3818 |
| ev.03_symbols_md.tests_unit_app_test_synonym_expander_py | evidence/03_symbols.md | 3819-3836 |
| ev.03_symbols_md.tests_unit_app_test_vertex_vector_search_semantic_search_py | evidence/03_symbols.md | 3837-3851 |
| ev.03_symbols_md.tests_unit_arch_test_import_boundaries_py | evidence/03_symbols.md | 3852-3855 |
| ev.03_symbols_md.tests_unit_ml_common_test_gcs_py | evidence/03_symbols.md | 3856-3864 |
| ev.03_symbols_md.tests_unit_ml_common_test_gcs_io_py | evidence/03_symbols.md | 3865-3870 |
| ev.03_symbols_md.tests_unit_ml_common_test_logging_py | evidence/03_symbols.md | 3871-3875 |
| ev.03_symbols_md.tests_unit_ml_common_test_run_id_py | evidence/03_symbols.md | 3876-3880 |
| ev.03_symbols_md.tests_unit_ml_data_test_bigquery_ranker_repository_py | evidence/03_symbols.md | 3881-3891 |
| ev.03_symbols_md.tests_unit_ml_data_test_embedding_batch_py | evidence/03_symbols.md | 3892-3908 |
| ev.03_symbols_md.tests_unit_ml_data_test_feature_engineering_ranker_py | evidence/03_symbols.md | 3909-3914 |
| ev.03_symbols_md.tests_unit_ml_evaluation_test_label_gain_py | evidence/03_symbols.md | 3915-3919 |
| ev.03_symbols_md.tests_unit_ml_evaluation_test_ranking_metrics_py | evidence/03_symbols.md | 3920-3930 |
| ev.03_symbols_md.tests_unit_ml_test_encoder_server_py | evidence/03_symbols.md | 3931-3938 |
| ev.03_symbols_md.tests_unit_ml_test_lightgbm_trainer_adapter_py | evidence/03_symbols.md | 3939-3942 |
| ev.03_symbols_md.tests_unit_ml_training_test_cli_run_py | evidence/03_symbols.md | 3943-3965 |
| ev.03_symbols_md.tests_unit_ml_training_test_trainer_py | evidence/03_symbols.md | 3966-3973 |
| ev.03_symbols_md.tests_unit_ml_training_test_vertex_experiments_tracker_py | evidence/03_symbols.md | 3974-3982 |
| ev.03_symbols_md.tests_unit_pipeline_dags_test_dag_files_py | evidence/03_symbols.md | 3983-3993 |
| ev.03_symbols_md.tests_unit_pipeline_test_data_job_dag_wiring_py | evidence/03_symbols.md | 3994-4002 |
| ev.03_symbols_md.tests_unit_pipeline_test_ground_truth_jobs_py | evidence/03_symbols.md | 4003-4014 |
| ev.03_symbols_md.tests_unit_pipeline_test_kfp_orchestrator_py | evidence/03_symbols.md | 4015-4022 |
| ev.03_symbols_md.tests_unit_pipeline_test_pipeline_trigger_py | evidence/03_symbols.md | 4023-4030 |
| ev.03_symbols_md.tests_unit_pipeline_test_vector_search_writer_py | evidence/03_symbols.md | 4031-4045 |
| ev.03_symbols_md.tests_unit_scripts_test_adapters_py | evidence/03_symbols.md | 4046-4057 |
| ev.03_symbols_md.tests_unit_scripts_test_common_resolve_project_py | evidence/03_symbols.md | 4058-4065 |
| ev.03_symbols_md.tests_unit_scripts_test_composer_deploy_dags_py | evidence/03_symbols.md | 4066-4079 |
| ev.03_symbols_md.tests_unit_scripts_test_composer_task_states_py | evidence/03_symbols.md | 4080-4084 |
| ev.03_symbols_md.tests_unit_scripts_test_configmap_overlay_py | evidence/03_symbols.md | 4085-4089 |
| ev.03_symbols_md.tests_unit_scripts_test_deploy_all_step_timing_py | evidence/03_symbols.md | 4090-4115 |
| ev.03_symbols_md.tests_unit_scripts_test_destroy_check_py | evidence/03_symbols.md | 4116-4122 |
| ev.03_symbols_md.tests_unit_scripts_test_elasticsearch_wait_py | evidence/03_symbols.md | 4123-4133 |
| ev.03_symbols_md.tests_unit_scripts_test_infra_cleanup_py | evidence/03_symbols.md | 4134-4153 |
| ev.03_symbols_md.tests_unit_scripts_test_infra_feature_view_sync_py | evidence/03_symbols.md | 4154-4164 |
| ev.03_symbols_md.tests_unit_scripts_test_infra_terraform_state_py | evidence/03_symbols.md | 4165-4179 |
| ev.03_symbols_md.tests_unit_scripts_test_kserve_models_deploy_py | evidence/03_symbols.md | 4180-4196 |
| ev.03_symbols_md.tests_unit_scripts_test_lib_config_py | evidence/03_symbols.md | 4197-4206 |
| ev.03_symbols_md.tests_unit_scripts_test_lib_gcp_resources_py | evidence/03_symbols.md | 4207-4215 |
| ev.03_symbols_md.tests_unit_scripts_test_local_hybrid_py | evidence/03_symbols.md | 4216-4224 |
| ev.03_symbols_md.tests_unit_scripts_test_monitor_py | evidence/03_symbols.md | 4225-4236 |
| ev.03_symbols_md.tests_unit_scripts_test_promote_py | evidence/03_symbols.md | 4237-4259 |
| ev.03_symbols_md.tests_unit_scripts_test_repo_relative_paths_py | evidence/03_symbols.md | 4260-4263 |
| ev.03_symbols_md.tests_unit_scripts_test_resolve_api_target_py | evidence/03_symbols.md | 4264-4277 |
| ev.03_symbols_md.tests_unit_scripts_test_run_all_orchestrator_py | evidence/03_symbols.md | 4278-4287 |
| ev.03_symbols_md.tests_unit_scripts_test_setup_policy_guard_py | evidence/03_symbols.md | 4288-4297 |
| ev.03_symbols_md.tests_unit_scripts_test_step_timing_py | evidence/03_symbols.md | 4298-4308 |
| ev.03_symbols_md.tests_unit_scripts_test_submit_train_pipeline_py | evidence/03_symbols.md | 4309-4314 |
| ev.03_symbols_md.tests_unit_scripts_test_subprocess_run_kwargs_guard_py | evidence/03_symbols.md | 4315-4320 |
| ev.03_symbols_md.tests_unit_scripts_test_sync_elasticsearch_exit_codes_py | evidence/03_symbols.md | 4321-4325 |
| ev.03_symbols_md.tests_unit_scripts_test_terraform_lock_py | evidence/03_symbols.md | 4326-4333 |
| ev.03_symbols_md.tests_unit_scripts_test_vertex_feature_store_wait_py | evidence/03_symbols.md | 4334-4342 |
| ev.03_symbols_md.tests_unit_scripts_test_vertex_ops_scripts_py | evidence/03_symbols.md | 4343-4396 |
| ev.03_symbols_md.tools_check_docker_layout_py | evidence/03_symbols.md | 4397-4405 |
| ev.03_symbols_md.github_workflows_ci_yml.pull_request.l5 | evidence/03_symbols.md | 5-5 |
| ev.03_symbols_md.github_workflows_ci_yml.push.l6 | evidence/03_symbols.md | 6-6 |
| ev.03_symbols_md.github_workflows_ci_yml.workflow_dispatch.l7 | evidence/03_symbols.md | 7-7 |
| ev.03_symbols_md.github_workflows_ci_yml.lint_typecheck_test.l8 | evidence/03_symbols.md | 8-8 |
| ev.03_symbols_md.github_workflows_ci_yml.strategy.l9 | evidence/03_symbols.md | 9-9 |
| ev.03_symbols_md.github_workflows_ci_yml.matrix.l10 | evidence/03_symbols.md | 10-10 |
| ev.03_symbols_md.github_workflows_ci_yml.dataform_check.l11 | evidence/03_symbols.md | 11-11 |
| ev.03_symbols_md.github_workflows_deploy_api_yml.push.l15 | evidence/03_symbols.md | 15-15 |
| ev.03_symbols_md.github_workflows_deploy_api_yml.paths.l16 | evidence/03_symbols.md | 16-16 |
| ev.03_symbols_md.github_workflows_deploy_api_yml.workflow_dispatch.l17 | evidence/03_symbols.md | 17-17 |
| ev.03_symbols_md.github_workflows_deploy_api_yml.build_and_deploy.l18 | evidence/03_symbols.md | 18-18 |
| ev.03_symbols_md.github_workflows_deploy_dataform_yml.push.l22 | evidence/03_symbols.md | 22-22 |
| ev.03_symbols_md.github_workflows_deploy_dataform_yml.paths.l23 | evidence/03_symbols.md | 23-23 |
| ev.03_symbols_md.github_workflows_deploy_dataform_yml.workflow_dispatch.l24 | evidence/03_symbols.md | 24-24 |
| ev.03_symbols_md.github_workflows_deploy_dataform_yml.push_definitions.l25 | evidence/03_symbols.md | 25-25 |
| ev.03_symbols_md.github_workflows_deploy_encoder_image_yml.push.l29 | evidence/03_symbols.md | 29-29 |
| ev.03_symbols_md.github_workflows_deploy_encoder_image_yml.paths.l30 | evidence/03_symbols.md | 30-30 |
| ev.03_symbols_md.github_workflows_deploy_encoder_image_yml.workflow_dispatch.l31 | evidence/03_symbols.md | 31-31 |
| ev.03_symbols_md.github_workflows_deploy_encoder_image_yml.build_and_push.l32 | evidence/03_symbols.md | 32-32 |
| ev.03_symbols_md.github_workflows_deploy_pipeline_yml.push.l36 | evidence/03_symbols.md | 36-36 |
| ev.03_symbols_md.github_workflows_deploy_pipeline_yml.paths.l37 | evidence/03_symbols.md | 37-37 |
| ev.03_symbols_md.github_workflows_deploy_pipeline_yml.workflow_dispatch.l38 | evidence/03_symbols.md | 38-38 |
| ev.03_symbols_md.github_workflows_deploy_pipeline_yml.compile_and_upload.l39 | evidence/03_symbols.md | 39-39 |
| ev.03_symbols_md.github_workflows_deploy_reranker_image_yml.push.l43 | evidence/03_symbols.md | 43-43 |
| ev.03_symbols_md.github_workflows_deploy_reranker_image_yml.paths.l44 | evidence/03_symbols.md | 44-44 |
| ev.03_symbols_md.github_workflows_deploy_reranker_image_yml.workflow_dispatch.l45 | evidence/03_symbols.md | 45-45 |
| ev.03_symbols_md.github_workflows_deploy_reranker_image_yml.build_and_push.l46 | evidence/03_symbols.md | 46-46 |
| ev.03_symbols_md.github_workflows_deploy_trainer_image_yml.push.l50 | evidence/03_symbols.md | 50-50 |
| ev.03_symbols_md.github_workflows_deploy_trainer_image_yml.paths.l51 | evidence/03_symbols.md | 51-51 |
| ev.03_symbols_md.github_workflows_deploy_trainer_image_yml.workflow_dispatch.l52 | evidence/03_symbols.md | 52-52 |
| ev.03_symbols_md.github_workflows_deploy_trainer_image_yml.build_and_push.l53 | evidence/03_symbols.md | 53-53 |
| ev.03_symbols_md.github_workflows_terraform_yml.pull_request.l57 | evidence/03_symbols.md | 57-57 |
| ev.03_symbols_md.github_workflows_terraform_yml.push.l58 | evidence/03_symbols.md | 58-58 |
| ev.03_symbols_md.github_workflows_terraform_yml.workflow_dispatch.l59 | evidence/03_symbols.md | 59-59 |
| ev.03_symbols_md.github_workflows_terraform_yml.plan.l60 | evidence/03_symbols.md | 60-60 |
| ev.03_symbols_md.github_workflows_terraform_yml.apply.l61 | evidence/03_symbols.md | 61-61 |
| ev.03_symbols_md.app_api_dependencies_py.get_container.l65 | evidence/03_symbols.md | 65-65 |
| ev.03_symbols_md.app_api_dependencies_py.get_search_service.l66 | evidence/03_symbols.md | 66-66 |
| ev.03_symbols_md.app_api_dependencies_py.get_feedback_service.l67 | evidence/03_symbols.md | 67-67 |
| ev.03_symbols_md.app_api_dependencies_py.get_request_id.l68 | evidence/03_symbols.md | 68-68 |
| ev.03_symbols_md.app_api_mappers_search_mapper_py.filters_from_pydantic.l72 | evidence/03_symbols.md | 72-72 |
| ev.03_symbols_md.app_api_mappers_search_mapper_py.search_request_to_input.l73 | evidence/03_symbols.md | 73-73 |
| ev.03_symbols_md.app_api_mappers_search_mapper_py.search_result_item_to_schema.l74 | evidence/03_symbols.md | 74-74 |
| ev.03_symbols_md.app_api_mappers_search_mapper_py.to_search_response.l75 | evidence/03_symbols.md | 75-75 |
| ev.03_symbols_md.app_api_middleware_request_logging_py.extract_trace.l79 | evidence/03_symbols.md | 79-79 |
| ev.03_symbols_md.app_api_middleware_request_logging_py.requestloggingmiddleware.l80 | evidence/03_symbols.md | 80-80 |
| ev.03_symbols_md.app_api_middleware_request_logging_py.init.l81 | evidence/03_symbols.md | 81-81 |
| ev.03_symbols_md.app_api_middleware_request_logging_py.dispatch.l82 | evidence/03_symbols.md | 82-82 |
| ev.03_symbols_md.app_api_routers_admin_mlops_router_py.admin_mlops.l86 | evidence/03_symbols.md | 86-86 |
| ev.03_symbols_md.app_api_routers_admin_mlops_router_py.collect_event_counts.l87 | evidence/03_symbols.md | 87-87 |
| ev.03_symbols_md.app_api_routers_admin_mlops_router_py.collect_latest_dataset.l88 | evidence/03_symbols.md | 88-88 |
| ev.03_symbols_md.app_api_routers_admin_mlops_router_py.collect_latest_metrics.l89 | evidence/03_symbols.md | 89-89 |
| ev.03_symbols_md.app_api_routers_feedback_router_py.feedback.l93 | evidence/03_symbols.md | 93-93 |
| ev.03_symbols_md.app_api_routers_health_router_py.healthz.l97 | evidence/03_symbols.md | 97-97 |
| ev.03_symbols_md.app_api_routers_health_router_py.readyz.l98 | evidence/03_symbols.md | 98-98 |
| ev.03_symbols_md.app_api_routers_model_router_py.model_metrics.l102 | evidence/03_symbols.md | 102-102 |
| ev.03_symbols_md.app_api_routers_model_router_py.model_info.l103 | evidence/03_symbols.md | 103-103 |
| ev.03_symbols_md.app_api_routers_model_router_py.model_data.l104 | evidence/03_symbols.md | 104-104 |
| ev.03_symbols_md.app_api_routers_ops_router_py.run_bq_query.l108 | evidence/03_symbols.md | 108-108 |
| ev.03_symbols_md.app_api_routers_ops_router_py.destroy_check.l109 | evidence/03_symbols.md | 109-109 |
| ev.03_symbols_md.app_api_routers_ops_router_py.search_volume.l110 | evidence/03_symbols.md | 110-110 |
| ev.03_symbols_md.app_api_routers_ops_router_py.runs_recent.l111 | evidence/03_symbols.md | 111-111 |
| ev.03_symbols_md.app_api_routers_ops_router_py.as_int.l112 | evidence/03_symbols.md | 112-112 |
| ev.03_symbols_md.app_api_routers_ops_router_py.as_float.l113 | evidence/03_symbols.md | 113-113 |
| ev.03_symbols_md.app_api_routers_retrain_router_py.check_retrain.l117 | evidence/03_symbols.md | 117-117 |
| ev.03_symbols_md.app_api_routers_search_router_py.search.l121 | evidence/03_symbols.md | 121-121 |
| ev.03_symbols_md.app_api_routers_ui_router_py.build_ui_router.l125 | evidence/03_symbols.md | 125-125 |
| ev.03_symbols_md.app_api_routers_ui_router_py.ui_home.l126 | evidence/03_symbols.md | 126-126 |
| ev.03_symbols_md.app_api_routers_ui_router_py.ui_search_dev.l127 | evidence/03_symbols.md | 127-127 |
| ev.03_symbols_md.app_api_routers_ui_router_py.ui_model_metrics.l128 | evidence/03_symbols.md | 128-128 |
| ev.03_symbols_md.app_api_routers_ui_router_py.ui_data.l129 | evidence/03_symbols.md | 129-129 |
| ev.03_symbols_md.app_api_routers_ui_router_py.ui_ops.l130 | evidence/03_symbols.md | 130-130 |
| ev.03_symbols_md.app_api_routers_ui_router_py.ui_api_docs.l131 | evidence/03_symbols.md | 131-131 |
| ev.03_symbols_md.app_api_routers_ui_router_py.ui_property_detail.l132 | evidence/03_symbols.md | 132-132 |
| ev.03_symbols_md.app_composition_root_py.container.l136 | evidence/03_symbols.md | 136-136 |
| ev.03_symbols_md.app_composition_root_py.containerbuilder.l137 | evidence/03_symbols.md | 137-137 |
| ev.03_symbols_md.app_composition_root_py.init.l138 | evidence/03_symbols.md | 138-138 |
| ev.03_symbols_md.app_composition_root_py.bigquery.l139 | evidence/03_symbols.md | 139-139 |
| ev.03_symbols_md.app_composition_root_py.build.l140 | evidence/03_symbols.md | 140-140 |
| ev.03_symbols_md.app_composition_root_py.build_retrain_publisher.l141 | evidence/03_symbols.md | 141-141 |
| ev.03_symbols_md.app_composition_root_py.build_ranking_log_publisher.l142 | evidence/03_symbols.md | 142-142 |
| ev.03_symbols_md.app_composition_root_py.build_feedback_recorder.l143 | evidence/03_symbols.md | 143-143 |
| ev.03_symbols_md.app_composition_root_py.build_data_catalog_reader.l144 | evidence/03_symbols.md | 144-144 |
| ev.03_symbols_md.app_composition_root_py.build_candidate_retriever.l145 | evidence/03_symbols.md | 145-145 |
| ev.03_symbols_md.app_composition_root_py.build_encoder_client.l146 | evidence/03_symbols.md | 146-146 |
| ev.03_symbols_md.app_composition_root_py.build_reranker_client.l147 | evidence/03_symbols.md | 147-147 |
| ev.03_symbols_md.app_composition_root_py.build_popularity_scorer.l148 | evidence/03_symbols.md | 148-148 |
| ev.03_symbols_md.app_container_infra_py.infrabuildercontext.l152 | evidence/03_symbols.md | 152-152 |
| ev.03_symbols_md.app_container_infra_py.bigquery.l153 | evidence/03_symbols.md | 153-153 |
| ev.03_symbols_md.app_container_infra_py.infracomponents.l154 | evidence/03_symbols.md | 154-154 |
| ev.03_symbols_md.app_container_infra_py.infrabuilder.l155 | evidence/03_symbols.md | 155-155 |
| ev.03_symbols_md.app_container_infra_py.init.l156 | evidence/03_symbols.md | 156-156 |
| ev.03_symbols_md.app_container_infra_py.settings.l157 | evidence/03_symbols.md | 157-157 |
| ev.03_symbols_md.app_container_infra_py.build.l158 | evidence/03_symbols.md | 158-158 |
| ev.03_symbols_md.app_container_infra_py.build_metrics_repository.l159 | evidence/03_symbols.md | 159-159 |
| ev.03_symbols_md.app_container_infra_py.build_training_dataset_repository.l160 | evidence/03_symbols.md | 160-160 |
| ev.03_symbols_md.app_container_infra_py.build_retrain_publisher.l161 | evidence/03_symbols.md | 161-161 |
| ev.03_symbols_md.app_container_infra_py.build_ranking_log_publisher.l162 | evidence/03_symbols.md | 162-162 |
| ev.03_symbols_md.app_container_infra_py.build_feedback_recorder.l163 | evidence/03_symbols.md | 163-163 |
| ev.03_symbols_md.app_container_infra_py.build_event_writer.l164 | evidence/03_symbols.md | 164-164 |
| ev.03_symbols_md.app_container_infra_py.build_synonym_expander.l165 | evidence/03_symbols.md | 165-165 |
| ev.03_symbols_md.app_container_internal_optional_adapter_py.resolve_optional_adapter.l169 | evidence/03_symbols.md | 169-169 |
| ev.03_symbols_md.app_container_ml_py.mlbuildercontext.l173 | evidence/03_symbols.md | 173-173 |
| ev.03_symbols_md.app_container_ml_py.bigquery.l174 | evidence/03_symbols.md | 174-174 |
| ev.03_symbols_md.app_container_ml_py.mlcomponents.l175 | evidence/03_symbols.md | 175-175 |
| ev.03_symbols_md.app_container_ml_py.mlbuilder.l176 | evidence/03_symbols.md | 176-176 |
| ev.03_symbols_md.app_container_ml_py.init.l177 | evidence/03_symbols.md | 177-177 |
| ev.03_symbols_md.app_container_ml_py.settings.l178 | evidence/03_symbols.md | 178-178 |
| ev.03_symbols_md.app_container_ml_py.logger.l179 | evidence/03_symbols.md | 179-179 |
| ev.03_symbols_md.app_container_ml_py.build.l180 | evidence/03_symbols.md | 180-180 |
| ev.03_symbols_md.app_container_ml_py.build_popularity_scorer.l181 | evidence/03_symbols.md | 181-181 |
| ev.03_symbols_md.app_container_ml_py.factory.l182 | evidence/03_symbols.md | 182-182 |
| ev.03_symbols_md.app_container_search_py.resolve_index_endpoint_name.l186 | evidence/03_symbols.md | 186-186 |
| ev.03_symbols_md.app_container_search_py.searchbuildercontext.l187 | evidence/03_symbols.md | 187-187 |
| ev.03_symbols_md.app_container_search_py.bigquery.l188 | evidence/03_symbols.md | 188-188 |
| ev.03_symbols_md.app_container_search_py.searchcomponents.l189 | evidence/03_symbols.md | 189-189 |
| ev.03_symbols_md.app_container_search_py.searchbuilder.l190 | evidence/03_symbols.md | 190-190 |
| ev.03_symbols_md.app_container_search_py.init.l191 | evidence/03_symbols.md | 191-191 |
| ev.03_symbols_md.app_container_search_py.settings.l192 | evidence/03_symbols.md | 192-192 |
| ev.03_symbols_md.app_container_search_py.logger.l193 | evidence/03_symbols.md | 193-193 |
| ev.03_symbols_md.app_container_search_py.build.l194 | evidence/03_symbols.md | 194-194 |
| ev.03_symbols_md.app_container_search_py.build_candidate_retriever.l195 | evidence/03_symbols.md | 195-195 |
| ev.03_symbols_md.app_container_search_py.resolve_feature_fetcher.l196 | evidence/03_symbols.md | 196-196 |
| ev.03_symbols_md.app_container_search_py.build_vertex_vector_search.l197 | evidence/03_symbols.md | 197-197 |
| ev.03_symbols_md.app_container_search_py.resolve_lexical_search.l198 | evidence/03_symbols.md | 198-198 |
| ev.03_symbols_md.app_container_search_py.build_encoder_client.l199 | evidence/03_symbols.md | 199-199 |
| ev.03_symbols_md.app_container_search_py.build_reranker_client.l200 | evidence/03_symbols.md | 200-200 |
| ev.03_symbols_md.app_domain_candidate_py.candidate.l204 | evidence/03_symbols.md | 204-204 |
| ev.03_symbols_md.app_domain_candidate_py.rankedcandidate.l205 | evidence/03_symbols.md | 205-205 |
| ev.03_symbols_md.app_domain_event_py.searchevent.l209 | evidence/03_symbols.md | 209-209 |
| ev.03_symbols_md.app_domain_event_py.impression.l210 | evidence/03_symbols.md | 210-210 |
| ev.03_symbols_md.app_domain_event_py.useraction.l211 | evidence/03_symbols.md | 211-211 |
| ev.03_symbols_md.app_domain_labeling_py.rankinglabel.l215 | evidence/03_symbols.md | 215-215 |
| ev.03_symbols_md.app_domain_retrieval_py.lexicalresult.l219 | evidence/03_symbols.md | 219-219 |
| ev.03_symbols_md.app_domain_retrieval_py.semanticresult.l220 | evidence/03_symbols.md | 220-220 |
| ev.03_symbols_md.app_domain_search_py.searchfilters.l224 | evidence/03_symbols.md | 224-224 |
| ev.03_symbols_md.app_domain_search_py.searchinput.l225 | evidence/03_symbols.md | 225-225 |
| ev.03_symbols_md.app_domain_search_py.searchresultitem.l226 | evidence/03_symbols.md | 226-226 |
| ev.03_symbols_md.app_domain_search_py.searchoutput.l227 | evidence/03_symbols.md | 227-227 |
| ev.03_symbols_md.app_domain_training_py.trainingdatasetref.l231 | evidence/03_symbols.md | 231-231 |
| ev.03_symbols_md.app_domain_training_py.evaluationmetric.l232 | evidence/03_symbols.md | 232-232 |
| ev.03_symbols_md.app_main_py.build_legacy_redirects.l236 | evidence/03_symbols.md | 236-236 |
| ev.03_symbols_md.app_main_py.redirect.l237 | evidence/03_symbols.md | 237-237 |
| ev.03_symbols_md.app_main_py.create_app.l238 | evidence/03_symbols.md | 238-238 |
| ev.03_symbols_md.app_main_py.lifespan.l239 | evidence/03_symbols.md | 239-239 |
| ev.03_symbols_md.app_main_py.root_redirect.l240 | evidence/03_symbols.md | 240-240 |
| ev.03_symbols_md.app_observability_py.observability.l244 | evidence/03_symbols.md | 244-244 |
| ev.03_symbols_md.app_observability_py.from_env.l245 | evidence/03_symbols.md | 245-245 |
| ev.03_symbols_md.app_observability_py.for_test.l246 | evidence/03_symbols.md | 246-246 |
| ev.03_symbols_md.app_observability_py.get_logger.l247 | evidence/03_symbols.md | 247-247 |
| ev.03_symbols_md.app_observability_py.expose_prometheus.l248 | evidence/03_symbols.md | 248-248 |
| ev.03_symbols_md.app_observability_py.build_tracker.l249 | evidence/03_symbols.md | 249-249 |
| ev.03_symbols_md.app_observability_py.record.l250 | evidence/03_symbols.md | 250-250 |
| ev.03_symbols_md.app_schemas_admin_mlops_py.metricsnapshot.l254 | evidence/03_symbols.md | 254-254 |
| ev.03_symbols_md.app_schemas_admin_mlops_py.trainingdatasetsnapshot.l255 | evidence/03_symbols.md | 255-255 |
| ev.03_symbols_md.app_schemas_admin_mlops_py.eventcounts.l256 | evidence/03_symbols.md | 256-256 |
| ev.03_symbols_md.app_schemas_admin_mlops_py.adminmlopsresponse.l257 | evidence/03_symbols.md | 257-257 |
| ev.03_symbols_md.app_schemas_model_py.casemetric.l261 | evidence/03_symbols.md | 261-261 |
| ev.03_symbols_md.app_schemas_model_py.accuracysummary.l262 | evidence/03_symbols.md | 262-262 |
| ev.03_symbols_md.app_schemas_model_py.modelmetricsresponse.l263 | evidence/03_symbols.md | 263-263 |
| ev.03_symbols_md.app_schemas_model_py.modelinforesponse.l264 | evidence/03_symbols.md | 264-264 |
| ev.03_symbols_md.app_schemas_model_py.datapreviewtable.l265 | evidence/03_symbols.md | 265-265 |
| ev.03_symbols_md.app_schemas_model_py.modeldataresponse.l266 | evidence/03_symbols.md | 266-266 |
| ev.03_symbols_md.app_schemas_ops_py.destroycheckfindingresponse.l270 | evidence/03_symbols.md | 270-270 |
| ev.03_symbols_md.app_schemas_ops_py.destroychecksummaryresponse.l271 | evidence/03_symbols.md | 271-271 |
| ev.03_symbols_md.app_schemas_ops_py.destroycheckresponse.l272 | evidence/03_symbols.md | 272-272 |
| ev.03_symbols_md.app_schemas_ops_py.searchvolumeresponse.l273 | evidence/03_symbols.md | 273-273 |
| ev.03_symbols_md.app_schemas_ops_py.trainingrunsummaryresponse.l274 | evidence/03_symbols.md | 274-274 |
| ev.03_symbols_md.app_schemas_ops_py.recenttrainingrunsresponse.l275 | evidence/03_symbols.md | 275-275 |
| ev.03_symbols_md.app_schemas_search_py.searchfilters.l279 | evidence/03_symbols.md | 279-279 |
| ev.03_symbols_md.app_schemas_search_py.searchrequest.l280 | evidence/03_symbols.md | 280-280 |
| ev.03_symbols_md.app_schemas_search_py.searchresultitem.l281 | evidence/03_symbols.md | 281-281 |
| ev.03_symbols_md.app_schemas_search_py.searchresponse.l282 | evidence/03_symbols.md | 282-282 |
| ev.03_symbols_md.app_schemas_search_py.feedbackrequest.l283 | evidence/03_symbols.md | 283-283 |
| ev.03_symbols_md.app_schemas_search_py.feedbackresponse.l284 | evidence/03_symbols.md | 284-284 |
| ev.03_symbols_md.app_services_adapters_bigquery_candidate_retriever_py.bigquerycandidateretriever.l288 | evidence/03_symbols.md | 288-288 |
| ev.03_symbols_md.app_services_adapters_bigquery_candidate_retriever_py.init.l289 | evidence/03_symbols.md | 289-289 |
| ev.03_symbols_md.app_services_adapters_bigquery_candidate_retriever_py.retrieve.l290 | evidence/03_symbols.md | 290-290 |
| ev.03_symbols_md.app_services_adapters_bigquery_candidate_retriever_py.enrich_from_bq.l291 | evidence/03_symbols.md | 291-291 |
| ev.03_symbols_md.app_services_adapters_bigquery_data_catalog_reader_py.bigquerydatacatalogreader.l295 | evidence/03_symbols.md | 295-295 |
| ev.03_symbols_md.app_services_adapters_bigquery_data_catalog_reader_py.init.l296 | evidence/03_symbols.md | 296-296 |
| ev.03_symbols_md.app_services_adapters_bigquery_data_catalog_reader_py.read_snapshot.l297 | evidence/03_symbols.md | 297-297 |
| ev.03_symbols_md.app_services_adapters_bigquery_data_catalog_reader_py.properties_preview.l298 | evidence/03_symbols.md | 298-298 |
| ev.03_symbols_md.app_services_adapters_bigquery_data_catalog_reader_py.features_preview.l299 | evidence/03_symbols.md | 299-299 |
| ev.03_symbols_md.app_services_adapters_bigquery_data_catalog_reader_py.ranking_log_preview.l300 | evidence/03_symbols.md | 300-300 |
| ev.03_symbols_md.app_services_adapters_bigquery_data_catalog_reader_py.embeddings_preview.l301 | evidence/03_symbols.md | 301-301 |
| ev.03_symbols_md.app_services_adapters_bigquery_data_catalog_reader_py.training_runs_preview.l302 | evidence/03_symbols.md | 302-302 |
| ev.03_symbols_md.app_services_adapters_bigquery_data_catalog_reader_py.user_actions_preview.l303 | evidence/03_symbols.md | 303-303 |
| ev.03_symbols_md.app_services_adapters_bigquery_data_catalog_reader_py.ranking_labels_preview.l304 | evidence/03_symbols.md | 304-304 |
| ev.03_symbols_md.app_services_adapters_bigquery_data_catalog_reader_py.scalar.l305 | evidence/03_symbols.md | 305-305 |
| ev.03_symbols_md.app_services_adapters_bigquery_data_catalog_reader_py.query.l306 | evidence/03_symbols.md | 306-306 |
| ev.03_symbols_md.app_services_adapters_bigquery_data_catalog_reader_py.row_to_dict.l307 | evidence/03_symbols.md | 307-307 |
| ev.03_symbols_md.app_services_adapters_bigquery_data_catalog_reader_py.jsonish.l308 | evidence/03_symbols.md | 308-308 |
| ev.03_symbols_md.app_services_adapters_bigquery_event_repository_py.bigqueryeventrepository.l312 | evidence/03_symbols.md | 312-312 |
| ev.03_symbols_md.app_services_adapters_bigquery_event_repository_py.init.l313 | evidence/03_symbols.md | 313-313 |
| ev.03_symbols_md.app_services_adapters_bigquery_event_repository_py.read_search_events.l314 | evidence/03_symbols.md | 314-314 |
| ev.03_symbols_md.app_services_adapters_bigquery_event_repository_py.read_impressions.l315 | evidence/03_symbols.md | 315-315 |
| ev.03_symbols_md.app_services_adapters_bigquery_event_repository_py.read_user_actions.l316 | evidence/03_symbols.md | 316-316 |
| ev.03_symbols_md.app_services_adapters_bigquery_event_repository_py.query.l317 | evidence/03_symbols.md | 317-317 |
| ev.03_symbols_md.app_services_adapters_bigquery_event_repository_py.where_clause.l318 | evidence/03_symbols.md | 318-318 |
| ev.03_symbols_md.app_services_adapters_bigquery_event_repository_py.scalar_params.l319 | evidence/03_symbols.md | 319-319 |
| ev.03_symbols_md.app_services_adapters_bigquery_event_repository_py.optional_str.l320 | evidence/03_symbols.md | 320-320 |
| ev.03_symbols_md.app_services_adapters_bigquery_event_repository_py.optional_int.l321 | evidence/03_symbols.md | 321-321 |
| ev.03_symbols_md.app_services_adapters_bigquery_event_repository_py.optional_float.l322 | evidence/03_symbols.md | 322-322 |
| ev.03_symbols_md.app_services_adapters_bigquery_event_repository_py.json_text.l323 | evidence/03_symbols.md | 323-323 |
| ev.03_symbols_md.app_services_adapters_bigquery_label_repository_py.bigquerylabelrepository.l327 | evidence/03_symbols.md | 327-327 |
| ev.03_symbols_md.app_services_adapters_bigquery_label_repository_py.init.l328 | evidence/03_symbols.md | 328-328 |
| ev.03_symbols_md.app_services_adapters_bigquery_label_repository_py.write_ranking_labels.l329 | evidence/03_symbols.md | 329-329 |
| ev.03_symbols_md.app_services_adapters_bigquery_label_repository_py.read_ranking_labels.l330 | evidence/03_symbols.md | 330-330 |
| ev.03_symbols_md.app_services_adapters_bigquery_metrics_repository_py.bigquerymetricsrepository.l334 | evidence/03_symbols.md | 334-334 |
| ev.03_symbols_md.app_services_adapters_bigquery_metrics_repository_py.init.l335 | evidence/03_symbols.md | 335-335 |
| ev.03_symbols_md.app_services_adapters_bigquery_metrics_repository_py.write_evaluation_metrics.l336 | evidence/03_symbols.md | 336-336 |
| ev.03_symbols_md.app_services_adapters_bigquery_metrics_repository_py.read_evaluation_metrics.l337 | evidence/03_symbols.md | 337-337 |
| ev.03_symbols_md.app_services_adapters_bigquery_metrics_repository_py.latest_metrics.l338 | evidence/03_symbols.md | 338-338 |
| ev.03_symbols_md.app_services_adapters_bqml_popularity_scorer_py.bqmlpopularityscorer.l342 | evidence/03_symbols.md | 342-342 |
| ev.03_symbols_md.app_services_adapters_bqml_popularity_scorer_py.init.l343 | evidence/03_symbols.md | 343-343 |
| ev.03_symbols_md.app_services_adapters_bqml_popularity_scorer_py.score.l344 | evidence/03_symbols.md | 344-344 |
| ev.03_symbols_md.app_services_adapters_cloud_logging_event_writer_py.cloudloggingeventwriter.l348 | evidence/03_symbols.md | 348-348 |
| ev.03_symbols_md.app_services_adapters_cloud_logging_event_writer_py.emit_search_event.l349 | evidence/03_symbols.md | 349-349 |
| ev.03_symbols_md.app_services_adapters_cloud_logging_event_writer_py.emit_impression.l350 | evidence/03_symbols.md | 350-350 |
| ev.03_symbols_md.app_services_adapters_cloud_logging_event_writer_py.emit_user_action.l351 | evidence/03_symbols.md | 351-351 |
| ev.03_symbols_md.app_services_adapters_cloud_logging_event_writer_py.emit.l352 | evidence/03_symbols.md | 352-352 |
| ev.03_symbols_md.app_services_adapters_cloud_logging_event_writer_py.parse_json.l353 | evidence/03_symbols.md | 353-353 |
| ev.03_symbols_md.app_services_adapters_elasticsearch_lexical_py.elasticsearchlexical.l357 | evidence/03_symbols.md | 357-357 |
| ev.03_symbols_md.app_services_adapters_elasticsearch_lexical_py.init.l358 | evidence/03_symbols.md | 358-358 |
| ev.03_symbols_md.app_services_adapters_elasticsearch_lexical_py.headers.l359 | evidence/03_symbols.md | 359-359 |
| ev.03_symbols_md.app_services_adapters_elasticsearch_lexical_py.search.l360 | evidence/03_symbols.md | 360-360 |
| ev.03_symbols_md.app_services_adapters_elasticsearch_lexical_py.filters_to_es.l361 | evidence/03_symbols.md | 361-361 |
| ev.03_symbols_md.app_services_adapters_feature_online_store_fetcher_py.featureonlinestorefetcher.l365 | evidence/03_symbols.md | 365-365 |
| ev.03_symbols_md.app_services_adapters_feature_online_store_fetcher_py.init.l366 | evidence/03_symbols.md | 366-366 |
| ev.03_symbols_md.app_services_adapters_feature_online_store_fetcher_py.resolve_client.l367 | evidence/03_symbols.md | 367-367 |
| ev.03_symbols_md.app_services_adapters_feature_online_store_fetcher_py.resolve_canonical_feature_view.l368 | evidence/03_symbols.md | 368-368 |
| ev.03_symbols_md.app_services_adapters_feature_online_store_fetcher_py.fetch.l369 | evidence/03_symbols.md | 369-369 |
| ev.03_symbols_md.app_services_adapters_feature_online_store_fetcher_py.build_request.l370 | evidence/03_symbols.md | 370-370 |
| ev.03_symbols_md.app_services_adapters_feature_online_store_fetcher_py.resource_part.l371 | evidence/03_symbols.md | 371-371 |
| ev.03_symbols_md.app_services_adapters_feature_online_store_fetcher_py.row_from_response.l372 | evidence/03_symbols.md | 372-372 |
| ev.03_symbols_md.app_services_adapters_feature_online_store_fetcher_py.safe_features.l373 | evidence/03_symbols.md | 373-373 |
| ev.03_symbols_md.app_services_adapters_feature_online_store_fetcher_py.coerce_float.l374 | evidence/03_symbols.md | 374-374 |
| ev.03_symbols_md.app_services_adapters_gcs_training_dataset_repository_py.gcstrainingdatasetrepository.l378 | evidence/03_symbols.md | 378-378 |
| ev.03_symbols_md.app_services_adapters_gcs_training_dataset_repository_py.init.l379 | evidence/03_symbols.md | 379-379 |
| ev.03_symbols_md.app_services_adapters_gcs_training_dataset_repository_py.manifest_path.l380 | evidence/03_symbols.md | 380-380 |
| ev.03_symbols_md.app_services_adapters_gcs_training_dataset_repository_py.write_training_dataset.l381 | evidence/03_symbols.md | 381-381 |
| ev.03_symbols_md.app_services_adapters_gcs_training_dataset_repository_py.read_training_dataset.l382 | evidence/03_symbols.md | 382-382 |
| ev.03_symbols_md.app_services_adapters_gcs_training_dataset_repository_py.latest_training_dataset.l383 | evidence/03_symbols.md | 383-383 |
| ev.03_symbols_md.app_services_adapters_gcs_training_dataset_repository_py.read_manifest.l384 | evidence/03_symbols.md | 384-384 |
| ev.03_symbols_md.app_services_adapters_internal_kserve_common_py.safe_json.l388 | evidence/03_symbols.md | 388-388 |
| ev.03_symbols_md.app_services_adapters_internal_kserve_common_py.log_http_error_response.l389 | evidence/03_symbols.md | 389-389 |
| ev.03_symbols_md.app_services_adapters_internal_kserve_common_py.is_v2_inference_url.l390 | evidence/03_symbols.md | 390-390 |
| ev.03_symbols_md.app_services_adapters_internal_kserve_common_py.coerce_float_list.l391 | evidence/03_symbols.md | 391-391 |
| ev.03_symbols_md.app_services_adapters_internal_kserve_common_py.response_summary.l392 | evidence/03_symbols.md | 392-392 |
| ev.03_symbols_md.app_services_adapters_internal_kserve_common_py.extract_predictions.l393 | evidence/03_symbols.md | 393-393 |
| ev.03_symbols_md.app_services_adapters_internal_pubsub_diagnostics_py.runtime_sa_hint.l397 | evidence/03_symbols.md | 397-397 |
| ev.03_symbols_md.app_services_adapters_internal_pubsub_diagnostics_py.log_publish_failure.l398 | evidence/03_symbols.md | 398-398 |
| ev.03_symbols_md.app_services_adapters_internal_pubsub_diagnostics_py.as_float.l399 | evidence/03_symbols.md | 399-399 |
| ev.03_symbols_md.app_services_adapters_kserve_encoder_py.kserveencoder.l403 | evidence/03_symbols.md | 403-403 |
| ev.03_symbols_md.app_services_adapters_kserve_encoder_py.init.l404 | evidence/03_symbols.md | 404-404 |
| ev.03_symbols_md.app_services_adapters_kserve_encoder_py.embed.l405 | evidence/03_symbols.md | 405-405 |
| ev.03_symbols_md.app_services_adapters_kserve_encoder_py.validate_embedding.l406 | evidence/03_symbols.md | 406-406 |
| ev.03_symbols_md.app_services_adapters_kserve_reranker_py.extract_attributions.l410 | evidence/03_symbols.md | 410-410 |
| ev.03_symbols_md.app_services_adapters_kserve_reranker_py.kservereranker.l411 | evidence/03_symbols.md | 411-411 |
| ev.03_symbols_md.app_services_adapters_kserve_reranker_py.init.l412 | evidence/03_symbols.md | 412-412 |
| ev.03_symbols_md.app_services_adapters_kserve_reranker_py.predict.l413 | evidence/03_symbols.md | 413-413 |
| ev.03_symbols_md.app_services_adapters_kserve_reranker_py.predict_with_explain.l414 | evidence/03_symbols.md | 414-414 |
| ev.03_symbols_md.app_services_adapters_kserve_reranker_py.coerce_score.l415 | evidence/03_symbols.md | 415-415 |
| ev.03_symbols_md.app_services_adapters_publisher_py.pubsubpublisher.l419 | evidence/03_symbols.md | 419-419 |
| ev.03_symbols_md.app_services_adapters_publisher_py.init.l420 | evidence/03_symbols.md | 420-420 |
| ev.03_symbols_md.app_services_adapters_publisher_py.publish.l421 | evidence/03_symbols.md | 421-421 |
| ev.03_symbols_md.app_services_adapters_pubsub_event_writer_py.pubsubeventwriter.l425 | evidence/03_symbols.md | 425-425 |
| ev.03_symbols_md.app_services_adapters_pubsub_event_writer_py.init.l426 | evidence/03_symbols.md | 426-426 |
| ev.03_symbols_md.app_services_adapters_pubsub_event_writer_py.emit_search_event.l427 | evidence/03_symbols.md | 427-427 |
| ev.03_symbols_md.app_services_adapters_pubsub_event_writer_py.emit_impression.l428 | evidence/03_symbols.md | 428-428 |
| ev.03_symbols_md.app_services_adapters_pubsub_event_writer_py.emit_user_action.l429 | evidence/03_symbols.md | 429-429 |
| ev.03_symbols_md.app_services_adapters_pubsub_event_writer_py.publish.l430 | evidence/03_symbols.md | 430-430 |
| ev.03_symbols_md.app_services_adapters_pubsub_event_writer_py.now_iso.l431 | evidence/03_symbols.md | 431-431 |
| ev.03_symbols_md.app_services_adapters_pubsub_feedback_recorder_py.pubsubfeedbackrecorder.l435 | evidence/03_symbols.md | 435-435 |
| ev.03_symbols_md.app_services_adapters_pubsub_feedback_recorder_py.init.l436 | evidence/03_symbols.md | 436-436 |
| ev.03_symbols_md.app_services_adapters_pubsub_feedback_recorder_py.record.l437 | evidence/03_symbols.md | 437-437 |
| ev.03_symbols_md.app_services_adapters_pubsub_ranking_log_publisher_py.pubsubrankinglogpublisher.l441 | evidence/03_symbols.md | 441-441 |
| ev.03_symbols_md.app_services_adapters_pubsub_ranking_log_publisher_py.init.l442 | evidence/03_symbols.md | 442-442 |
| ev.03_symbols_md.app_services_adapters_pubsub_ranking_log_publisher_py.publish_candidates.l443 | evidence/03_symbols.md | 443-443 |
| ev.03_symbols_md.app_services_adapters_redis_synonym_expander_py.redissynonymexpander.l447 | evidence/03_symbols.md | 447-447 |
| ev.03_symbols_md.app_services_adapters_redis_synonym_expander_py.init.l448 | evidence/03_symbols.md | 448-448 |
| ev.03_symbols_md.app_services_adapters_redis_synonym_expander_py.expand.l449 | evidence/03_symbols.md | 449-449 |
| ev.03_symbols_md.app_services_adapters_redis_synonym_expander_py.expand_tokens.l450 | evidence/03_symbols.md | 450-450 |
| ev.03_symbols_md.app_services_adapters_redis_synonym_expander_py.decode.l451 | evidence/03_symbols.md | 451-451 |
| ev.03_symbols_md.app_services_adapters_retrain_py.bigqueryretrainqueries.l455 | evidence/03_symbols.md | 455-455 |
| ev.03_symbols_md.app_services_adapters_retrain_py.init.l456 | evidence/03_symbols.md | 456-456 |
| ev.03_symbols_md.app_services_adapters_retrain_py.last_run_finished_at.l457 | evidence/03_symbols.md | 457-457 |
| ev.03_symbols_md.app_services_adapters_retrain_py.feedback_rows_since.l458 | evidence/03_symbols.md | 458-458 |
| ev.03_symbols_md.app_services_adapters_retrain_py.ndcg_in_window.l459 | evidence/03_symbols.md | 459-459 |
| ev.03_symbols_md.app_services_adapters_retrain_py.create_retrain_queries.l460 | evidence/03_symbols.md | 460-460 |
| ev.03_symbols_md.app_services_adapters_vertex_vector_search_semantic_search_py.vertexvectorsearchsemanticsearch.l464 | evidence/03_symbols.md | 464-464 |
| ev.03_symbols_md.app_services_adapters_vertex_vector_search_semantic_search_py.init.l465 | evidence/03_symbols.md | 465-465 |
| ev.03_symbols_md.app_services_adapters_vertex_vector_search_semantic_search_py.resolve_endpoint.l466 | evidence/03_symbols.md | 466-466 |
| ev.03_symbols_md.app_services_adapters_vertex_vector_search_semantic_search_py.search.l467 | evidence/03_symbols.md | 467-467 |
| ev.03_symbols_md.app_services_data_catalog_service_py.datacatalogservice.l471 | evidence/03_symbols.md | 471-471 |
| ev.03_symbols_md.app_services_data_catalog_service_py.init.l472 | evidence/03_symbols.md | 472-472 |
| ev.03_symbols_md.app_services_data_catalog_service_py.read_snapshot.l473 | evidence/03_symbols.md | 473-473 |
| ev.03_symbols_md.app_services_feedback_service_py.feedbackservice.l477 | evidence/03_symbols.md | 477-477 |
| ev.03_symbols_md.app_services_feedback_service_py.init.l478 | evidence/03_symbols.md | 478-478 |
| ev.03_symbols_md.app_services_feedback_service_py.record.l479 | evidence/03_symbols.md | 479-479 |
| ev.03_symbols_md.app_services_model_metrics_service_py.evalcase.l483 | evidence/03_symbols.md | 483-483 |
| ev.03_symbols_md.app_services_model_metrics_service_py.casereport.l484 | evidence/03_symbols.md | 484-484 |
| ev.03_symbols_md.app_services_model_metrics_service_py.accuracyreport.l485 | evidence/03_symbols.md | 485-485 |
| ev.03_symbols_md.app_services_model_metrics_service_py.load_cases.l486 | evidence/03_symbols.md | 486-486 |
| ev.03_symbols_md.app_services_model_metrics_service_py.coerce_filters.l487 | evidence/03_symbols.md | 487-487 |
| ev.03_symbols_md.app_services_model_metrics_service_py.as_int.l488 | evidence/03_symbols.md | 488-488 |
| ev.03_symbols_md.app_services_model_metrics_service_py.dcg_binary.l489 | evidence/03_symbols.md | 489-489 |
| ev.03_symbols_md.app_services_model_metrics_service_py.ndcg_at_k.l490 | evidence/03_symbols.md | 490-490 |
| ev.03_symbols_md.app_services_model_metrics_service_py.hit_rate_at_k.l491 | evidence/03_symbols.md | 491-491 |
| ev.03_symbols_md.app_services_model_metrics_service_py.mrr_at_k.l492 | evidence/03_symbols.md | 492-492 |
| ev.03_symbols_md.app_services_model_metrics_service_py.default_cases_path.l493 | evidence/03_symbols.md | 493-493 |
| ev.03_symbols_md.app_services_model_metrics_service_py.modelmetricsservice.l494 | evidence/03_symbols.md | 494-494 |
| ev.03_symbols_md.app_services_model_metrics_service_py.init.l495 | evidence/03_symbols.md | 495-495 |
| ev.03_symbols_md.app_services_model_metrics_service_py.evaluate.l496 | evidence/03_symbols.md | 496-496 |
| ev.03_symbols_md.app_services_noop_adapters_noop_data_catalog_reader_py.noopdatacatalogreader.l500 | evidence/03_symbols.md | 500-500 |
| ev.03_symbols_md.app_services_noop_adapters_noop_data_catalog_reader_py.read_snapshot.l501 | evidence/03_symbols.md | 501-501 |
| ev.03_symbols_md.app_services_noop_adapters_noop_event_repository_py.noopeventrepository.l505 | evidence/03_symbols.md | 505-505 |
| ev.03_symbols_md.app_services_noop_adapters_noop_event_repository_py.read_search_events.l506 | evidence/03_symbols.md | 506-506 |
| ev.03_symbols_md.app_services_noop_adapters_noop_event_repository_py.read_impressions.l507 | evidence/03_symbols.md | 507-507 |
| ev.03_symbols_md.app_services_noop_adapters_noop_event_repository_py.read_user_actions.l508 | evidence/03_symbols.md | 508-508 |
| ev.03_symbols_md.app_services_noop_adapters_noop_event_writer_py.noopeventwriter.l512 | evidence/03_symbols.md | 512-512 |
| ev.03_symbols_md.app_services_noop_adapters_noop_event_writer_py.emit_search_event.l513 | evidence/03_symbols.md | 513-513 |
| ev.03_symbols_md.app_services_noop_adapters_noop_event_writer_py.emit_impression.l514 | evidence/03_symbols.md | 514-514 |
| ev.03_symbols_md.app_services_noop_adapters_noop_event_writer_py.emit_user_action.l515 | evidence/03_symbols.md | 515-515 |
| ev.03_symbols_md.app_services_noop_adapters_noop_feedback_recorder_py.noopfeedbackrecorder.l519 | evidence/03_symbols.md | 519-519 |
| ev.03_symbols_md.app_services_noop_adapters_noop_feedback_recorder_py.record.l520 | evidence/03_symbols.md | 520-520 |
| ev.03_symbols_md.app_services_noop_adapters_noop_label_repository_py.nooplabelrepository.l524 | evidence/03_symbols.md | 524-524 |
| ev.03_symbols_md.app_services_noop_adapters_noop_label_repository_py.write_ranking_labels.l525 | evidence/03_symbols.md | 525-525 |
| ev.03_symbols_md.app_services_noop_adapters_noop_label_repository_py.read_ranking_labels.l526 | evidence/03_symbols.md | 526-526 |
| ev.03_symbols_md.app_services_noop_adapters_noop_lexical_search_py.nooplexicalsearch.l530 | evidence/03_symbols.md | 530-530 |
| ev.03_symbols_md.app_services_noop_adapters_noop_lexical_search_py.search.l531 | evidence/03_symbols.md | 531-531 |
| ev.03_symbols_md.app_services_noop_adapters_noop_metrics_repository_py.noopmetricsrepository.l535 | evidence/03_symbols.md | 535-535 |
| ev.03_symbols_md.app_services_noop_adapters_noop_metrics_repository_py.write_evaluation_metrics.l536 | evidence/03_symbols.md | 536-536 |
| ev.03_symbols_md.app_services_noop_adapters_noop_metrics_repository_py.read_evaluation_metrics.l537 | evidence/03_symbols.md | 537-537 |
| ev.03_symbols_md.app_services_noop_adapters_noop_metrics_repository_py.latest_metrics.l538 | evidence/03_symbols.md | 538-538 |
| ev.03_symbols_md.app_services_noop_adapters_noop_ranking_log_publisher_py.nooprankinglogpublisher.l542 | evidence/03_symbols.md | 542-542 |
| ev.03_symbols_md.app_services_noop_adapters_noop_ranking_log_publisher_py.publish_candidates.l543 | evidence/03_symbols.md | 543-543 |
| ev.03_symbols_md.app_services_noop_adapters_noop_retrain_queries_py.noopretrainqueries.l547 | evidence/03_symbols.md | 547-547 |
| ev.03_symbols_md.app_services_noop_adapters_noop_retrain_queries_py.last_run_finished_at.l548 | evidence/03_symbols.md | 548-548 |
| ev.03_symbols_md.app_services_noop_adapters_noop_retrain_queries_py.feedback_rows_since.l549 | evidence/03_symbols.md | 549-549 |
| ev.03_symbols_md.app_services_noop_adapters_noop_retrain_queries_py.ndcg_in_window.l550 | evidence/03_symbols.md | 550-550 |
| ev.03_symbols_md.app_services_noop_adapters_noop_synonym_expander_py.noopsynonymexpander.l554 | evidence/03_symbols.md | 554-554 |
| ev.03_symbols_md.app_services_noop_adapters_noop_synonym_expander_py.expand.l555 | evidence/03_symbols.md | 555-555 |
| ev.03_symbols_md.app_services_noop_adapters_noop_training_dataset_repository_py.nooptrainingdatasetrepository.l559 | evidence/03_symbols.md | 559-559 |
| ev.03_symbols_md.app_services_noop_adapters_noop_training_dataset_repository_py.write_training_dataset.l560 | evidence/03_symbols.md | 560-560 |
| ev.03_symbols_md.app_services_noop_adapters_noop_training_dataset_repository_py.read_training_dataset.l561 | evidence/03_symbols.md | 561-561 |
| ev.03_symbols_md.app_services_noop_adapters_noop_training_dataset_repository_py.latest_training_dataset.l562 | evidence/03_symbols.md | 562-562 |
| ev.03_symbols_md.app_services_protocols_candidate_retriever_py.candidateretriever.l566 | evidence/03_symbols.md | 566-566 |
| ev.03_symbols_md.app_services_protocols_candidate_retriever_py.retrieve.l567 | evidence/03_symbols.md | 567-567 |
| ev.03_symbols_md.app_services_protocols_data_catalog_reader_py.datacatalogtablepreview.l571 | evidence/03_symbols.md | 571-571 |
| ev.03_symbols_md.app_services_protocols_data_catalog_reader_py.datacatalogsnapshot.l572 | evidence/03_symbols.md | 572-572 |
| ev.03_symbols_md.app_services_protocols_data_catalog_reader_py.datacatalogreader.l573 | evidence/03_symbols.md | 573-573 |
| ev.03_symbols_md.app_services_protocols_data_catalog_reader_py.read_snapshot.l574 | evidence/03_symbols.md | 574-574 |
| ev.03_symbols_md.app_services_protocols_encoder_client_py.encoderclient.l578 | evidence/03_symbols.md | 578-578 |
| ev.03_symbols_md.app_services_protocols_encoder_client_py.embed.l579 | evidence/03_symbols.md | 579-579 |
| ev.03_symbols_md.app_services_protocols_event_repository_py.eventrepository.l583 | evidence/03_symbols.md | 583-583 |
| ev.03_symbols_md.app_services_protocols_event_repository_py.read_search_events.l584 | evidence/03_symbols.md | 584-584 |
| ev.03_symbols_md.app_services_protocols_event_repository_py.read_impressions.l585 | evidence/03_symbols.md | 585-585 |
| ev.03_symbols_md.app_services_protocols_event_repository_py.read_user_actions.l586 | evidence/03_symbols.md | 586-586 |
| ev.03_symbols_md.app_services_protocols_event_writer_py.eventwriter.l590 | evidence/03_symbols.md | 590-590 |
| ev.03_symbols_md.app_services_protocols_event_writer_py.emit_search_event.l591 | evidence/03_symbols.md | 591-591 |
| ev.03_symbols_md.app_services_protocols_event_writer_py.emit_impression.l592 | evidence/03_symbols.md | 592-592 |
| ev.03_symbols_md.app_services_protocols_event_writer_py.emit_user_action.l593 | evidence/03_symbols.md | 593-593 |
| ev.03_symbols_md.app_services_protocols_feature_fetcher_py.featurerow.l597 | evidence/03_symbols.md | 597-597 |
| ev.03_symbols_md.app_services_protocols_feature_fetcher_py.featurefetcher.l598 | evidence/03_symbols.md | 598-598 |
| ev.03_symbols_md.app_services_protocols_feature_fetcher_py.fetch.l599 | evidence/03_symbols.md | 599-599 |
| ev.03_symbols_md.app_services_protocols_feedback_recorder_py.feedbackrecorder.l603 | evidence/03_symbols.md | 603-603 |
| ev.03_symbols_md.app_services_protocols_feedback_recorder_py.record.l604 | evidence/03_symbols.md | 604-604 |
| ev.03_symbols_md.app_services_protocols_label_repository_py.labelrepository.l608 | evidence/03_symbols.md | 608-608 |
| ev.03_symbols_md.app_services_protocols_label_repository_py.write_ranking_labels.l609 | evidence/03_symbols.md | 609-609 |
| ev.03_symbols_md.app_services_protocols_label_repository_py.read_ranking_labels.l610 | evidence/03_symbols.md | 610-610 |
| ev.03_symbols_md.app_services_protocols_lexical_search_py.lexicalsearchport.l614 | evidence/03_symbols.md | 614-614 |
| ev.03_symbols_md.app_services_protocols_lexical_search_py.search.l615 | evidence/03_symbols.md | 615-615 |
| ev.03_symbols_md.app_services_protocols_metrics_repository_py.metricsrepository.l619 | evidence/03_symbols.md | 619-619 |
| ev.03_symbols_md.app_services_protocols_metrics_repository_py.write_evaluation_metrics.l620 | evidence/03_symbols.md | 620-620 |
| ev.03_symbols_md.app_services_protocols_metrics_repository_py.read_evaluation_metrics.l621 | evidence/03_symbols.md | 621-621 |
| ev.03_symbols_md.app_services_protocols_metrics_repository_py.latest_metrics.l622 | evidence/03_symbols.md | 622-622 |
| ev.03_symbols_md.app_services_protocols_popularity_scorer_py.popularityscorer.l626 | evidence/03_symbols.md | 626-626 |
| ev.03_symbols_md.app_services_protocols_popularity_scorer_py.score.l627 | evidence/03_symbols.md | 627-627 |
| ev.03_symbols_md.app_services_protocols_publisher_py.predictionpublisher.l631 | evidence/03_symbols.md | 631-631 |
| ev.03_symbols_md.app_services_protocols_publisher_py.publish.l632 | evidence/03_symbols.md | 632-632 |
| ev.03_symbols_md.app_services_protocols_publisher_py.nooppublisher.l633 | evidence/03_symbols.md | 633-633 |
| ev.03_symbols_md.app_services_protocols_publisher_py.publish.l634 | evidence/03_symbols.md | 634-634 |
| ev.03_symbols_md.app_services_protocols_ranking_log_publisher_py.rankinglogpublisher.l638 | evidence/03_symbols.md | 638-638 |
| ev.03_symbols_md.app_services_protocols_ranking_log_publisher_py.publish_candidates.l639 | evidence/03_symbols.md | 639-639 |
| ev.03_symbols_md.app_services_protocols_reranker_client_py.rerankerclient.l643 | evidence/03_symbols.md | 643-643 |
| ev.03_symbols_md.app_services_protocols_reranker_client_py.predict.l644 | evidence/03_symbols.md | 644-644 |
| ev.03_symbols_md.app_services_protocols_reranker_client_py.rerankerexplainer.l645 | evidence/03_symbols.md | 645-645 |
| ev.03_symbols_md.app_services_protocols_reranker_client_py.predict_with_explain.l646 | evidence/03_symbols.md | 646-646 |
| ev.03_symbols_md.app_services_protocols_retrain_queries_py.retrainqueries.l650 | evidence/03_symbols.md | 650-650 |
| ev.03_symbols_md.app_services_protocols_retrain_queries_py.last_run_finished_at.l651 | evidence/03_symbols.md | 651-651 |
| ev.03_symbols_md.app_services_protocols_retrain_queries_py.feedback_rows_since.l652 | evidence/03_symbols.md | 652-652 |
| ev.03_symbols_md.app_services_protocols_retrain_queries_py.ndcg_in_window.l653 | evidence/03_symbols.md | 653-653 |
| ev.03_symbols_md.app_services_protocols_semantic_search_py.semanticsearchport.l657 | evidence/03_symbols.md | 657-657 |
| ev.03_symbols_md.app_services_protocols_semantic_search_py.search.l658 | evidence/03_symbols.md | 658-658 |
| ev.03_symbols_md.app_services_protocols_synonym_expander_py.synonymexpanderport.l662 | evidence/03_symbols.md | 662-662 |
| ev.03_symbols_md.app_services_protocols_synonym_expander_py.expand.l663 | evidence/03_symbols.md | 663-663 |
| ev.03_symbols_md.app_services_protocols_training_dataset_repository_py.trainingdatasetrepository.l667 | evidence/03_symbols.md | 667-667 |
| ev.03_symbols_md.app_services_protocols_training_dataset_repository_py.write_training_dataset.l668 | evidence/03_symbols.md | 668-668 |
| ev.03_symbols_md.app_services_protocols_training_dataset_repository_py.read_training_dataset.l669 | evidence/03_symbols.md | 669-669 |
| ev.03_symbols_md.app_services_protocols_training_dataset_repository_py.latest_training_dataset.l670 | evidence/03_symbols.md | 670-670 |
| ev.03_symbols_md.app_services_ranking_py.safe_publish_candidates.l674 | evidence/03_symbols.md | 674-674 |
| ev.03_symbols_md.app_services_ranking_py.augment_with_fresh_features.l675 | evidence/03_symbols.md | 675-675 |
| ev.03_symbols_md.app_services_ranking_py.build_feature_matrix.l676 | evidence/03_symbols.md | 676-676 |
| ev.03_symbols_md.app_services_ranking_py.score_candidates.l677 | evidence/03_symbols.md | 677-677 |
| ev.03_symbols_md.app_services_ranking_py.score_with_explain.l678 | evidence/03_symbols.md | 678-678 |
| ev.03_symbols_md.app_services_ranking_py.run_search.l679 | evidence/03_symbols.md | 679-679 |
| ev.03_symbols_md.app_services_ranking_py.rrf_fuse.l680 | evidence/03_symbols.md | 680-680 |
| ev.03_symbols_md.app_services_retrain_policy_py.retrainthresholds.l684 | evidence/03_symbols.md | 684-684 |
| ev.03_symbols_md.app_services_retrain_policy_py.retraindecision.l685 | evidence/03_symbols.md | 685-685 |
| ev.03_symbols_md.app_services_retrain_policy_py.evaluate.l686 | evidence/03_symbols.md | 686-686 |
| ev.03_symbols_md.app_services_search_service_py.searchserviceunavailable.l690 | evidence/03_symbols.md | 690-690 |
| ev.03_symbols_md.app_services_search_service_py.searchservice.l691 | evidence/03_symbols.md | 691-691 |
| ev.03_symbols_md.app_services_search_service_py.init.l692 | evidence/03_symbols.md | 692-692 |
| ev.03_symbols_md.app_services_search_service_py.reranker_model_path.l693 | evidence/03_symbols.md | 693-693 |
| ev.03_symbols_md.app_services_search_service_py.search.l694 | evidence/03_symbols.md | 694-694 |
| ev.03_symbols_md.app_services_search_service_py.as_str.l695 | evidence/03_symbols.md | 695-695 |
| ev.03_symbols_md.app_services_search_service_py.as_int.l696 | evidence/03_symbols.md | 696-696 |
| ev.03_symbols_md.app_services_search_service_py.as_float.l697 | evidence/03_symbols.md | 697-697 |
| ev.03_symbols_md.app_services_search_service_py.as_bool.l698 | evidence/03_symbols.md | 698-698 |
| ev.03_symbols_md.app_services_search_service_py.filters_from_dict.l699 | evidence/03_symbols.md | 699-699 |
| ev.03_symbols_md.app_settings_api_py.featureflags.l703 | evidence/03_symbols.md | 703-703 |
| ev.03_symbols_md.app_settings_api_py.messagingsettings.l704 | evidence/03_symbols.md | 704-704 |
| ev.03_symbols_md.app_settings_api_py.kservesettings.l705 | evidence/03_symbols.md | 705-705 |
| ev.03_symbols_md.app_settings_api_py.popularitysettings.l706 | evidence/03_symbols.md | 706-706 |
| ev.03_symbols_md.app_settings_api_py.synonymsettings.l707 | evidence/03_symbols.md | 707-707 |
| ev.03_symbols_md.app_settings_api_py.apisettings.l708 | evidence/03_symbols.md | 708-708 |
| ev.03_symbols_md.app_settings_api_py.feature_flags.l709 | evidence/03_symbols.md | 709-709 |
| ev.03_symbols_md.app_settings_api_py.messaging.l710 | evidence/03_symbols.md | 710-710 |
| ev.03_symbols_md.app_settings_api_py.kserve.l711 | evidence/03_symbols.md | 711-711 |
| ev.03_symbols_md.app_settings_api_py.popularity.l712 | evidence/03_symbols.md | 712-712 |
| ev.03_symbols_md.app_settings_api_py.synonym.l713 | evidence/03_symbols.md | 713-713 |
| ev.03_symbols_md.app_static_css_custom_css.bg_main.l717 | evidence/03_symbols.md | 717-717 |
| ev.03_symbols_md.app_static_css_custom_css.bg_sub.l718 | evidence/03_symbols.md | 718-718 |
| ev.03_symbols_md.app_static_css_custom_css.bg_hover.l719 | evidence/03_symbols.md | 719-719 |
| ev.03_symbols_md.app_static_css_custom_css.border.l720 | evidence/03_symbols.md | 720-720 |
| ev.03_symbols_md.app_static_css_custom_css.text_main.l721 | evidence/03_symbols.md | 721-721 |
| ev.03_symbols_md.app_static_css_custom_css.text_sub.l722 | evidence/03_symbols.md | 722-722 |
| ev.03_symbols_md.app_static_css_custom_css.text_disabled.l723 | evidence/03_symbols.md | 723-723 |
| ev.03_symbols_md.app_static_css_custom_css.lime.l724 | evidence/03_symbols.md | 724-724 |
| ev.03_symbols_md.app_static_css_custom_css.lime_hover.l725 | evidence/03_symbols.md | 725-725 |
| ev.03_symbols_md.app_static_css_custom_css.pink.l726 | evidence/03_symbols.md | 726-726 |
| ev.03_symbols_md.app_static_css_custom_css.pink_hover.l727 | evidence/03_symbols.md | 727-727 |
| ev.03_symbols_md.app_static_css_custom_css.shadow.l728 | evidence/03_symbols.md | 728-728 |
| ev.03_symbols_md.app_static_css_custom_css.admin_brand.l729 | evidence/03_symbols.md | 729-729 |
| ev.03_symbols_md.app_static_css_custom_css.admin_nav_item__docs.l730 | evidence/03_symbols.md | 730-730 |
| ev.03_symbols_md.app_static_css_custom_css.admin_nav_item__docs.l731 | evidence/03_symbols.md | 731-731 |
| ev.03_symbols_md.app_static_css_custom_css.admin_nav_item__docs.l732 | evidence/03_symbols.md | 732-732 |
| ev.03_symbols_md.app_static_css_custom_css.admin_sidebar_card.l733 | evidence/03_symbols.md | 733-733 |
| ev.03_symbols_md.app_static_css_custom_css.admin_main.l734 | evidence/03_symbols.md | 734-734 |
| ev.03_symbols_md.app_static_css_custom_css.admin_header.l735 | evidence/03_symbols.md | 735-735 |
| ev.03_symbols_md.app_static_css_custom_css.admin_content.l736 | evidence/03_symbols.md | 736-736 |
| ev.03_symbols_md.app_static_css_custom_css.admin_main.l737 | evidence/03_symbols.md | 737-737 |
| ev.03_symbols_md.app_static_css_custom_css.page_header.l738 | evidence/03_symbols.md | 738-738 |
| ev.03_symbols_md.app_static_css_custom_css.eyebrow.l739 | evidence/03_symbols.md | 739-739 |
| ev.03_symbols_md.app_static_css_custom_css.page_header.l740 | evidence/03_symbols.md | 740-740 |
| ev.03_symbols_md.app_static_css_custom_css.panel.l741 | evidence/03_symbols.md | 741-741 |
| ev.03_symbols_md.app_static_css_custom_css.feature_card.l742 | evidence/03_symbols.md | 742-742 |
| ev.03_symbols_md.app_static_css_custom_css.page_copy.l743 | evidence/03_symbols.md | 743-743 |
| ev.03_symbols_md.app_static_css_custom_css.section_copy.l744 | evidence/03_symbols.md | 744-744 |
| ev.03_symbols_md.app_static_css_custom_css.status_note.l745 | evidence/03_symbols.md | 745-745 |
| ev.03_symbols_md.app_static_css_custom_css.search_state.l746 | evidence/03_symbols.md | 746-746 |
| ev.03_symbols_md.app_static_css_custom_css.feature_card.l747 | evidence/03_symbols.md | 747-747 |
| ev.03_symbols_md.app_static_css_custom_css.page_header.l748 | evidence/03_symbols.md | 748-748 |
| ev.03_symbols_md.app_static_css_custom_css.panel.l749 | evidence/03_symbols.md | 749-749 |
| ev.03_symbols_md.app_static_css_custom_css.feature_card.l750 | evidence/03_symbols.md | 750-750 |
| ev.03_symbols_md.app_static_css_custom_css.search_result_card.l751 | evidence/03_symbols.md | 751-751 |
| ev.03_symbols_md.app_static_css_custom_css.search_shell.l752 | evidence/03_symbols.md | 752-752 |
| ev.03_symbols_md.app_static_css_custom_css.panel.l753 | evidence/03_symbols.md | 753-753 |
| ev.03_symbols_md.app_static_css_custom_css.panel.l754 | evidence/03_symbols.md | 754-754 |
| ev.03_symbols_md.app_static_css_custom_css.feature_card.l755 | evidence/03_symbols.md | 755-755 |
| ev.03_symbols_md.app_static_css_custom_css.status_card.l756 | evidence/03_symbols.md | 756-756 |
| ev.03_symbols_md.app_static_css_custom_css.section_heading.l757 | evidence/03_symbols.md | 757-757 |
| ev.03_symbols_md.app_static_css_custom_css.search_form.l758 | evidence/03_symbols.md | 758-758 |
| ev.03_symbols_md.app_static_css_custom_css.search_form.l759 | evidence/03_symbols.md | 759-759 |
| ev.03_symbols_md.app_static_css_custom_css.search_form.l760 | evidence/03_symbols.md | 760-760 |
| ev.03_symbols_md.app_static_css_custom_css.search_form.l761 | evidence/03_symbols.md | 761-761 |
| ev.03_symbols_md.app_static_css_custom_css.search_form.l762 | evidence/03_symbols.md | 762-762 |
| ev.03_symbols_md.app_static_css_custom_css.fb_action.l763 | evidence/03_symbols.md | 763-763 |
| ev.03_symbols_md.app_static_css_custom_css.search_form.l764 | evidence/03_symbols.md | 764-764 |
| ev.03_symbols_md.app_static_css_custom_css.toggle_wrap.l765 | evidence/03_symbols.md | 765-765 |
| ev.03_symbols_md.app_static_css_custom_css.toggle_wrap.l766 | evidence/03_symbols.md | 766-766 |
| ev.03_symbols_md.app_static_css_custom_css.dev_controls.l767 | evidence/03_symbols.md | 767-767 |
| ev.03_symbols_md.app_static_css_custom_css.action_row.l768 | evidence/03_symbols.md | 768-768 |
| ev.03_symbols_md.app_static_css_custom_css.search_state.l769 | evidence/03_symbols.md | 769-769 |
| ev.03_symbols_md.app_static_css_custom_css.panel.l770 | evidence/03_symbols.md | 770-770 |
| ev.03_symbols_md.app_static_css_custom_css.panel.l771 | evidence/03_symbols.md | 771-771 |
| ev.03_symbols_md.app_static_css_custom_css.panel.l772 | evidence/03_symbols.md | 772-772 |
| ev.03_symbols_md.app_static_css_custom_css.panel.l773 | evidence/03_symbols.md | 773-773 |
| ev.03_symbols_md.app_static_css_custom_css.panel.l774 | evidence/03_symbols.md | 774-774 |
| ev.03_symbols_md.app_static_css_custom_css.search_result_card.l775 | evidence/03_symbols.md | 775-775 |
| ev.03_symbols_md.app_static_css_custom_css.search_result_card.l776 | evidence/03_symbols.md | 776-776 |
| ev.03_symbols_md.app_static_css_custom_css.status_card.l777 | evidence/03_symbols.md | 777-777 |
| ev.03_symbols_md.app_static_css_custom_css.status_label.l778 | evidence/03_symbols.md | 778-778 |
| ev.03_symbols_md.app_static_css_custom_css.panel.l779 | evidence/03_symbols.md | 779-779 |
| ev.03_symbols_md.app_static_css_custom_css.status_grid.l780 | evidence/03_symbols.md | 780-780 |
| ev.03_symbols_md.app_static_css_custom_css.status_card_danger.l781 | evidence/03_symbols.md | 781-781 |
| ev.03_symbols_md.app_static_css_custom_css.status_card_wide.l782 | evidence/03_symbols.md | 782-782 |
| ev.03_symbols_md.app_static_css_custom_css.ops_panel.l783 | evidence/03_symbols.md | 783-783 |
| ev.03_symbols_md.app_static_css_custom_css.ops_panel_ok.l784 | evidence/03_symbols.md | 784-784 |
| ev.03_symbols_md.app_static_css_custom_css.ops_panel_warn.l785 | evidence/03_symbols.md | 785-785 |
| ev.03_symbols_md.app_static_css_custom_css.ops_panel_fail.l786 | evidence/03_symbols.md | 786-786 |
| ev.03_symbols_md.app_static_css_custom_css.ops_panel_error.l787 | evidence/03_symbols.md | 787-787 |
| ev.03_symbols_md.app_static_css_custom_css.ops_item_list.l788 | evidence/03_symbols.md | 788-788 |
| ev.03_symbols_md.app_static_css_custom_css.ops_item_list.l789 | evidence/03_symbols.md | 789-789 |
| ev.03_symbols_md.app_static_css_custom_css.panel.l790 | evidence/03_symbols.md | 790-790 |
| ev.03_symbols_md.app_static_css_custom_css.panel.l791 | evidence/03_symbols.md | 791-791 |
| ev.03_symbols_md.app_static_css_custom_css.search_btn.l792 | evidence/03_symbols.md | 792-792 |
| ev.03_symbols_md.app_static_css_custom_css.acc_btn.l793 | evidence/03_symbols.md | 793-793 |
| ev.03_symbols_md.app_static_css_custom_css.data_btn.l794 | evidence/03_symbols.md | 794-794 |
| ev.03_symbols_md.app_static_css_custom_css.search_btn.l795 | evidence/03_symbols.md | 795-795 |
| ev.03_symbols_md.app_static_css_custom_css.acc_btn.l796 | evidence/03_symbols.md | 796-796 |
| ev.03_symbols_md.app_static_css_custom_css.data_btn.l797 | evidence/03_symbols.md | 797-797 |
| ev.03_symbols_md.app_static_css_custom_css.feedback_btn.l798 | evidence/03_symbols.md | 798-798 |
| ev.03_symbols_md.app_static_css_custom_css.feedback_btn.l799 | evidence/03_symbols.md | 799-799 |
| ev.03_symbols_md.app_static_css_custom_css.results_panel.l800 | evidence/03_symbols.md | 800-800 |
| ev.03_symbols_md.app_static_css_custom_css.result_grid.l801 | evidence/03_symbols.md | 801-801 |
| ev.03_symbols_md.app_static_css_custom_css.search_result_card.l802 | evidence/03_symbols.md | 802-802 |
| ev.03_symbols_md.app_static_css_custom_css.search_result_card.l803 | evidence/03_symbols.md | 803-803 |
| ev.03_symbols_md.app_static_css_custom_css.component_status_wrap.l804 | evidence/03_symbols.md | 804-804 |
| ev.03_symbols_md.app_static_css_custom_css.status_card.l805 | evidence/03_symbols.md | 805-805 |
| ev.03_symbols_md.app_static_css_custom_css.feature_card.l806 | evidence/03_symbols.md | 806-806 |
| ev.03_symbols_md.app_static_css_custom_css.status_label.l807 | evidence/03_symbols.md | 807-807 |
| ev.03_symbols_md.app_static_css_custom_css.status_card.l808 | evidence/03_symbols.md | 808-808 |
| ev.03_symbols_md.app_static_css_custom_css.status_ok.l809 | evidence/03_symbols.md | 809-809 |
| ev.03_symbols_md.app_static_css_custom_css.status_warn.l810 | evidence/03_symbols.md | 810-810 |
| ev.03_symbols_md.app_static_css_custom_css.status_note.l811 | evidence/03_symbols.md | 811-811 |
| ev.03_symbols_md.app_static_css_custom_css.result_card.l812 | evidence/03_symbols.md | 812-812 |
| ev.03_symbols_md.app_static_css_custom_css.result_card.l813 | evidence/03_symbols.md | 813-813 |
| ev.03_symbols_md.app_static_css_custom_css.result_card.l814 | evidence/03_symbols.md | 814-814 |
| ev.03_symbols_md.app_static_css_custom_css.result_card.l815 | evidence/03_symbols.md | 815-815 |
| ev.03_symbols_md.app_static_css_custom_css.result_card.l816 | evidence/03_symbols.md | 816-816 |
| ev.03_symbols_md.app_static_css_custom_css.result_card.l817 | evidence/03_symbols.md | 817-817 |
| ev.03_symbols_md.app_static_css_custom_css.result_card.l818 | evidence/03_symbols.md | 818-818 |
| ev.03_symbols_md.app_static_css_custom_css.result_card.l819 | evidence/03_symbols.md | 819-819 |
| ev.03_symbols_md.app_static_css_custom_css.table_scroll.l820 | evidence/03_symbols.md | 820-820 |
| ev.03_symbols_md.app_static_css_custom_css.search_shell_data_page_mode__user.l821 | evidence/03_symbols.md | 821-821 |
| ev.03_symbols_md.app_static_css_custom_css.search_shell_data_page_mode__user.l822 | evidence/03_symbols.md | 822-822 |
| ev.03_symbols_md.app_static_css_custom_css.search_shell_data_page_mode__dev.l823 | evidence/03_symbols.md | 823-823 |
| ev.03_symbols_md.app_static_css_custom_css.search_shell_data_page_mode__dev.l824 | evidence/03_symbols.md | 824-824 |
| ev.03_symbols_md.app_static_css_custom_css.search_shell_data_page_mode__dev.l825 | evidence/03_symbols.md | 825-825 |
| ev.03_symbols_md.app_static_css_custom_css.search_shell_data_page_mode__user.l826 | evidence/03_symbols.md | 826-826 |
| ev.03_symbols_md.app_static_css_custom_css.search_shell_data_page_mode__dev.l827 | evidence/03_symbols.md | 827-827 |
| ev.03_symbols_md.app_static_css_custom_css.result_grid.l828 | evidence/03_symbols.md | 828-828 |
| ev.03_symbols_md.app_static_css_custom_css.component_status_wrap.l829 | evidence/03_symbols.md | 829-829 |
| ev.03_symbols_md.app_static_css_custom_css.result_card.l830 | evidence/03_symbols.md | 830-830 |
| ev.03_symbols_md.app_static_css_custom_css.result_card.l831 | evidence/03_symbols.md | 831-831 |
| ev.03_symbols_md.app_static_css_custom_css.result_card.l832 | evidence/03_symbols.md | 832-832 |
| ev.03_symbols_md.app_static_css_custom_css.result_card.l833 | evidence/03_symbols.md | 833-833 |
| ev.03_symbols_md.app_static_css_custom_css.result_card.l834 | evidence/03_symbols.md | 834-834 |
| ev.03_symbols_md.app_static_css_custom_css.admin_main.l835 | evidence/03_symbols.md | 835-835 |
| ev.03_symbols_md.app_static_css_custom_css.component_status_wrap.l836 | evidence/03_symbols.md | 836-836 |
| ev.03_symbols_md.app_static_css_custom_css.panel.l837 | evidence/03_symbols.md | 837-837 |
| ev.03_symbols_md.app_static_css_custom_css.feature_card.l838 | evidence/03_symbols.md | 838-838 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_brand.l842 | evidence/03_symbols.md | 842-842 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_brand__mark.l843 | evidence/03_symbols.md | 843-843 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_brand__eyebrow.l844 | evidence/03_symbols.md | 844-844 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_eyebrow.l845 | evidence/03_symbols.md | 845-845 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_nav.l846 | evidence/03_symbols.md | 846-846 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_nav.l847 | evidence/03_symbols.md | 847-847 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_nav.l848 | evidence/03_symbols.md | 848-848 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_nav.l849 | evidence/03_symbols.md | 849-849 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_nav.l850 | evidence/03_symbols.md | 850-850 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_nav.l851 | evidence/03_symbols.md | 851-851 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_nav.l852 | evidence/03_symbols.md | 852-852 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_nav_item.l853 | evidence/03_symbols.md | 853-853 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_nav_item.l854 | evidence/03_symbols.md | 854-854 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_nav_item.l855 | evidence/03_symbols.md | 855-855 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_nav_item_aria_current__page.l856 | evidence/03_symbols.md | 856-856 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_card.l857 | evidence/03_symbols.md | 857-857 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_card.l858 | evidence/03_symbols.md | 858-858 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_card.l859 | evidence/03_symbols.md | 859-859 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_card.l860 | evidence/03_symbols.md | 860-860 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_card.l861 | evidence/03_symbols.md | 861-861 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_card.l862 | evidence/03_symbols.md | 862-862 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_card.l863 | evidence/03_symbols.md | 863-863 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_card.l864 | evidence/03_symbols.md | 864-864 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_card__compact.l865 | evidence/03_symbols.md | 865-865 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_card__dense.l866 | evidence/03_symbols.md | 866-866 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_hero.l867 | evidence/03_symbols.md | 867-867 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_hero__lead.l868 | evidence/03_symbols.md | 868-868 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_kpi.l869 | evidence/03_symbols.md | 869-869 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_kpi__dense.l870 | evidence/03_symbols.md | 870-870 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_kpi__value.l871 | evidence/03_symbols.md | 871-871 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_kpi__dense.l872 | evidence/03_symbols.md | 872-872 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_kpi__meta.l873 | evidence/03_symbols.md | 873-873 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_badge.l874 | evidence/03_symbols.md | 874-874 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_badge__neutral.l875 | evidence/03_symbols.md | 875-875 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_badge__lime.l876 | evidence/03_symbols.md | 876-876 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_badge__pink.l877 | evidence/03_symbols.md | 877-877 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_stat_list.l878 | evidence/03_symbols.md | 878-878 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_list.l879 | evidence/03_symbols.md | 879-879 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_inline_list.l880 | evidence/03_symbols.md | 880-880 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_stat_list.l881 | evidence/03_symbols.md | 881-881 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_stat_row.l882 | evidence/03_symbols.md | 882-882 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_list.l883 | evidence/03_symbols.md | 883-883 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_list.l884 | evidence/03_symbols.md | 884-884 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_list__dense.l885 | evidence/03_symbols.md | 885-885 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_list.l886 | evidence/03_symbols.md | 886-886 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_list__dense.l887 | evidence/03_symbols.md | 887-887 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_chart.l888 | evidence/03_symbols.md | 888-888 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_chart__compact.l889 | evidence/03_symbols.md | 889-889 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_chart__short.l890 | evidence/03_symbols.md | 890-890 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_chart.l891 | evidence/03_symbols.md | 891-891 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_table_wrap.l892 | evidence/03_symbols.md | 892-892 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_table.l893 | evidence/03_symbols.md | 893-893 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_table.l894 | evidence/03_symbols.md | 894-894 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_table.l895 | evidence/03_symbols.md | 895-895 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_table.l896 | evidence/03_symbols.md | 896-896 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_table.l897 | evidence/03_symbols.md | 897-897 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_table.l898 | evidence/03_symbols.md | 898-898 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_table.l899 | evidence/03_symbols.md | 899-899 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_table.l900 | evidence/03_symbols.md | 900-900 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_table.l901 | evidence/03_symbols.md | 901-901 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_table.l902 | evidence/03_symbols.md | 902-902 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_table.l903 | evidence/03_symbols.md | 903-903 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_table.l904 | evidence/03_symbols.md | 904-904 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_table.l905 | evidence/03_symbols.md | 905-905 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_table.l906 | evidence/03_symbols.md | 906-906 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_table.l907 | evidence/03_symbols.md | 907-907 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_pager.l908 | evidence/03_symbols.md | 908-908 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_pager__summary.l909 | evidence/03_symbols.md | 909-909 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_pager__nav.l910 | evidence/03_symbols.md | 910-910 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_pager__button.l911 | evidence/03_symbols.md | 911-911 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_pager__ellipsis.l912 | evidence/03_symbols.md | 912-912 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_pager__button.l913 | evidence/03_symbols.md | 913-913 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_pager__button.l914 | evidence/03_symbols.md | 914-914 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_pager__button_aria_current__page.l915 | evidence/03_symbols.md | 915-915 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_pager__ellipsis.l916 | evidence/03_symbols.md | 916-916 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_news_feed.l917 | evidence/03_symbols.md | 917-917 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_news_card.l918 | evidence/03_symbols.md | 918-918 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_news_card__meta.l919 | evidence/03_symbols.md | 919-919 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_news_card__tags.l920 | evidence/03_symbols.md | 920-920 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_news_card__action.l921 | evidence/03_symbols.md | 921-921 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_news_card__action.l922 | evidence/03_symbols.md | 922-922 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_news_card__action.l923 | evidence/03_symbols.md | 923-923 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_news_card__thumb.l924 | evidence/03_symbols.md | 924-924 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_news_card__thumb.l925 | evidence/03_symbols.md | 925-925 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_news_card__thumb.l926 | evidence/03_symbols.md | 926-926 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_news_card__eyebrow.l927 | evidence/03_symbols.md | 927-927 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_news_card__eyebrow.l928 | evidence/03_symbols.md | 928-928 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_news_card__thumb.l929 | evidence/03_symbols.md | 929-929 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_news_card__thumb__economy.l930 | evidence/03_symbols.md | 930-930 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_news_card__thumb__ai.l931 | evidence/03_symbols.md | 931-931 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_news_card__thumb__alert.l932 | evidence/03_symbols.md | 932-932 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_news_card__thumb__product.l933 | evidence/03_symbols.md | 933-933 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_news_card__thumb__global.l934 | evidence/03_symbols.md | 934-934 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_news_card__thumb__feature.l935 | evidence/03_symbols.md | 935-935 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_news_card__content.l936 | evidence/03_symbols.md | 936-936 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_news_card__content.l937 | evidence/03_symbols.md | 937-937 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_news_card__content.l938 | evidence/03_symbols.md | 938-938 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_news_card__content.l939 | evidence/03_symbols.md | 939-939 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_news_feed.l940 | evidence/03_symbols.md | 940-940 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_detail_grid.l941 | evidence/03_symbols.md | 941-941 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_detail_item.l942 | evidence/03_symbols.md | 942-942 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_detail_item.l943 | evidence/03_symbols.md | 943-943 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_detail_item.l944 | evidence/03_symbols.md | 944-944 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_checklist.l945 | evidence/03_symbols.md | 945-945 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_avatar.l946 | evidence/03_symbols.md | 946-946 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_avatar__image.l947 | evidence/03_symbols.md | 947-947 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_avatar__image.l948 | evidence/03_symbols.md | 948-948 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_user.l949 | evidence/03_symbols.md | 949-949 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_user__meta.l950 | evidence/03_symbols.md | 950-950 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_user__meta.l951 | evidence/03_symbols.md | 951-951 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_metric.l952 | evidence/03_symbols.md | 952-952 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_metric.l953 | evidence/03_symbols.md | 953-953 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_progress.l954 | evidence/03_symbols.md | 954-954 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_progress.l955 | evidence/03_symbols.md | 955-955 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_note.l956 | evidence/03_symbols.md | 956-956 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_note.l957 | evidence/03_symbols.md | 957-957 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_note__neutral.l958 | evidence/03_symbols.md | 958-958 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_actions.l959 | evidence/03_symbols.md | 959-959 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_field_grid.l960 | evidence/03_symbols.md | 960-960 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_card.l961 | evidence/03_symbols.md | 961-961 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_card.l962 | evidence/03_symbols.md | 962-962 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_card.l963 | evidence/03_symbols.md | 963-963 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_card.l964 | evidence/03_symbols.md | 964-964 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_card.l965 | evidence/03_symbols.md | 965-965 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_card.l966 | evidence/03_symbols.md | 966-966 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_card.l967 | evidence/03_symbols.md | 967-967 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_switch_grid.l968 | evidence/03_symbols.md | 968-968 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_switch.l969 | evidence/03_symbols.md | 969-969 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_segmented.l970 | evidence/03_symbols.md | 970-970 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_segmented.l971 | evidence/03_symbols.md | 971-971 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_segmented.l972 | evidence/03_symbols.md | 972-972 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_segmented.l973 | evidence/03_symbols.md | 973-973 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_segmented.l974 | evidence/03_symbols.md | 974-974 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_segmented.l975 | evidence/03_symbols.md | 975-975 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_segmented.l976 | evidence/03_symbols.md | 976-976 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_search.l977 | evidence/03_symbols.md | 977-977 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_search.l978 | evidence/03_symbols.md | 978-978 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_inline_control.l979 | evidence/03_symbols.md | 979-979 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_inline_control.l980 | evidence/03_symbols.md | 980-980 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_inline_control.l981 | evidence/03_symbols.md | 981-981 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_header__actions.l982 | evidence/03_symbols.md | 982-982 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_header__actions.l983 | evidence/03_symbols.md | 983-983 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_header__actions.l984 | evidence/03_symbols.md | 984-984 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_header_presence.l985 | evidence/03_symbols.md | 985-985 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_header_presence.l986 | evidence/03_symbols.md | 986-986 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_icon_button.l987 | evidence/03_symbols.md | 987-987 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_icon_button__badge.l988 | evidence/03_symbols.md | 988-988 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_user_chip.l989 | evidence/03_symbols.md | 989-989 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_user_chip__caret.l990 | evidence/03_symbols.md | 990-990 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_user_chip.l991 | evidence/03_symbols.md | 991-991 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_pager__button.l992 | evidence/03_symbols.md | 992-992 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_text_right.l993 | evidence/03_symbols.md | 993-993 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_auth_card.l994 | evidence/03_symbols.md | 994-994 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_auth_card.l995 | evidence/03_symbols.md | 995-995 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_auth_links.l996 | evidence/03_symbols.md | 996-996 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_header.l997 | evidence/03_symbols.md | 997-997 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_section_heading.l998 | evidence/03_symbols.md | 998-998 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_toolbar.l999 | evidence/03_symbols.md | 999-999 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_stat_row.l1000 | evidence/03_symbols.md | 1000-1000 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_switch.l1001 | evidence/03_symbols.md | 1001-1001 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_field_grid.l1002 | evidence/03_symbols.md | 1002-1002 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_table.l1003 | evidence/03_symbols.md | 1003-1003 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_pager.l1004 | evidence/03_symbols.md | 1004-1004 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_pager__nav.l1005 | evidence/03_symbols.md | 1005-1005 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_news_feed.l1006 | evidence/03_symbols.md | 1006-1006 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_header_presence.l1007 | evidence/03_symbols.md | 1007-1007 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_user_chip.l1008 | evidence/03_symbols.md | 1008-1008 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_inline_control.l1009 | evidence/03_symbols.md | 1009-1009 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_inline_control.l1010 | evidence/03_symbols.md | 1010-1010 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_detail_grid.l1011 | evidence/03_symbols.md | 1011-1011 |
| ev.03_symbols_md.app_static_css_pico_admin_components_css.admin_news_feed.l1012 | evidence/03_symbols.md | 1012-1012 |
| ev.03_symbols_md.app_static_css_pico_admin_layout_css.admin_shell.l1016 | evidence/03_symbols.md | 1016-1016 |
| ev.03_symbols_md.app_static_css_pico_admin_layout_css.admin_sidebar.l1017 | evidence/03_symbols.md | 1017-1017 |
| ev.03_symbols_md.app_static_css_pico_admin_layout_css.admin_sidebar__inner.l1018 | evidence/03_symbols.md | 1018-1018 |
| ev.03_symbols_md.app_static_css_pico_admin_layout_css.admin_main.l1019 | evidence/03_symbols.md | 1019-1019 |
| ev.03_symbols_md.app_static_css_pico_admin_layout_css.admin_header.l1020 | evidence/03_symbols.md | 1020-1020 |
| ev.03_symbols_md.app_static_css_pico_admin_layout_css.admin_header__actions.l1021 | evidence/03_symbols.md | 1021-1021 |
| ev.03_symbols_md.app_static_css_pico_admin_layout_css.admin_content.l1022 | evidence/03_symbols.md | 1022-1022 |
| ev.03_symbols_md.app_static_css_pico_admin_layout_css.admin_auth.l1023 | evidence/03_symbols.md | 1023-1023 |
| ev.03_symbols_md.app_static_css_pico_admin_layout_css.admin_auth__panel.l1024 | evidence/03_symbols.md | 1024-1024 |
| ev.03_symbols_md.app_static_css_pico_admin_layout_css.admin_auth__aside.l1025 | evidence/03_symbols.md | 1025-1025 |
| ev.03_symbols_md.app_static_css_pico_admin_layout_css.admin_grid.l1026 | evidence/03_symbols.md | 1026-1026 |
| ev.03_symbols_md.app_static_css_pico_admin_layout_css.admin_grid__4.l1027 | evidence/03_symbols.md | 1027-1027 |
| ev.03_symbols_md.app_static_css_pico_admin_layout_css.admin_grid__6.l1028 | evidence/03_symbols.md | 1028-1028 |
| ev.03_symbols_md.app_static_css_pico_admin_layout_css.admin_grid__3.l1029 | evidence/03_symbols.md | 1029-1029 |
| ev.03_symbols_md.app_static_css_pico_admin_layout_css.admin_grid__2.l1030 | evidence/03_symbols.md | 1030-1030 |
| ev.03_symbols_md.app_static_css_pico_admin_layout_css.admin_grid__sidebar.l1031 | evidence/03_symbols.md | 1031-1031 |
| ev.03_symbols_md.app_static_css_pico_admin_layout_css.admin_section_heading.l1032 | evidence/03_symbols.md | 1032-1032 |
| ev.03_symbols_md.app_static_css_pico_admin_layout_css.admin_toolbar.l1033 | evidence/03_symbols.md | 1033-1033 |
| ev.03_symbols_md.app_static_css_pico_admin_layout_css.admin_toolbar__group.l1034 | evidence/03_symbols.md | 1034-1034 |
| ev.03_symbols_md.app_static_css_pico_admin_layout_css.admin_stack.l1035 | evidence/03_symbols.md | 1035-1035 |
| ev.03_symbols_md.app_static_css_pico_admin_layout_css.admin_dashboard__top.l1036 | evidence/03_symbols.md | 1036-1036 |
| ev.03_symbols_md.app_static_css_pico_admin_layout_css.admin_dashboard__analytics.l1037 | evidence/03_symbols.md | 1037-1037 |
| ev.03_symbols_md.app_static_css_pico_admin_layout_css.admin_dashboard__ops.l1038 | evidence/03_symbols.md | 1038-1038 |
| ev.03_symbols_md.app_static_css_pico_admin_layout_css.admin_dashboard__summary.l1039 | evidence/03_symbols.md | 1039-1039 |
| ev.03_symbols_md.app_static_css_pico_admin_layout_css.admin_dashboard__summary_copy.l1040 | evidence/03_symbols.md | 1040-1040 |
| ev.03_symbols_md.app_static_css_pico_admin_layout_css.admin_dashboard__top.l1041 | evidence/03_symbols.md | 1041-1041 |
| ev.03_symbols_md.app_static_css_pico_admin_layout_css.admin_dashboard__analytics.l1042 | evidence/03_symbols.md | 1042-1042 |
| ev.03_symbols_md.app_static_css_pico_admin_layout_css.admin_dashboard__ops.l1043 | evidence/03_symbols.md | 1043-1043 |
| ev.03_symbols_md.app_static_css_pico_admin_layout_css.admin_main.l1044 | evidence/03_symbols.md | 1044-1044 |
| ev.03_symbols_md.app_static_css_pico_admin_layout_css.admin_main.l1045 | evidence/03_symbols.md | 1045-1045 |
| ev.03_symbols_md.app_static_css_pico_admin_layout_css.admin_content.l1046 | evidence/03_symbols.md | 1046-1046 |
| ev.03_symbols_md.app_static_css_pico_admin_layout_css.admin_grid.l1047 | evidence/03_symbols.md | 1047-1047 |
| ev.03_symbols_md.app_static_css_pico_admin_layout_css.admin_main.l1048 | evidence/03_symbols.md | 1048-1048 |
| ev.03_symbols_md.app_static_css_pico_admin_layout_css.admin_content.l1049 | evidence/03_symbols.md | 1049-1049 |
| ev.03_symbols_md.app_static_css_pico_admin_layout_css.admin_grid.l1050 | evidence/03_symbols.md | 1050-1050 |
| ev.03_symbols_md.app_static_css_pico_admin_layout_css.admin_grid__sidebar.l1051 | evidence/03_symbols.md | 1051-1051 |
| ev.03_symbols_md.app_static_css_pico_admin_layout_css.admin_dashboard__top.l1052 | evidence/03_symbols.md | 1052-1052 |
| ev.03_symbols_md.app_static_css_pico_admin_layout_css.admin_dashboard__analytics.l1053 | evidence/03_symbols.md | 1053-1053 |
| ev.03_symbols_md.app_static_css_pico_admin_layout_css.admin_dashboard__ops.l1054 | evidence/03_symbols.md | 1054-1054 |
| ev.03_symbols_md.app_static_css_pico_admin_layout_css.admin_shell.l1055 | evidence/03_symbols.md | 1055-1055 |
| ev.03_symbols_md.app_static_css_pico_admin_layout_css.admin_grid__6.l1056 | evidence/03_symbols.md | 1056-1056 |
| ev.03_symbols_md.app_static_css_pico_admin_layout_css.admin_grid__4.l1057 | evidence/03_symbols.md | 1057-1057 |
| ev.03_symbols_md.app_static_css_pico_admin_layout_css.admin_dashboard__top.l1058 | evidence/03_symbols.md | 1058-1058 |
| ev.03_symbols_md.app_static_css_pico_admin_layout_css.admin_dashboard__summary.l1059 | evidence/03_symbols.md | 1059-1059 |
| ev.03_symbols_md.app_static_css_pico_admin_layout_css.admin_dashboard__analytics.l1060 | evidence/03_symbols.md | 1060-1060 |
| ev.03_symbols_md.app_static_css_pico_admin_layout_css.admin_dashboard__ops.l1061 | evidence/03_symbols.md | 1061-1061 |
| ev.03_symbols_md.app_static_css_pico_admin_layout_css.admin_grid__sidebar.l1062 | evidence/03_symbols.md | 1062-1062 |
| ev.03_symbols_md.app_static_css_pico_admin_layout_css.admin_mobile_toggle.l1063 | evidence/03_symbols.md | 1063-1063 |
| ev.03_symbols_md.app_static_css_pico_admin_layout_css.admin_sidebar_backdrop.l1064 | evidence/03_symbols.md | 1064-1064 |
| ev.03_symbols_md.app_static_css_pico_admin_layout_css.admin_sidebar.l1065 | evidence/03_symbols.md | 1065-1065 |
| ev.03_symbols_md.app_static_css_pico_admin_layout_css.admin_shell.l1066 | evidence/03_symbols.md | 1066-1066 |
| ev.03_symbols_md.app_static_css_pico_admin_layout_css.admin_sidebar.l1067 | evidence/03_symbols.md | 1067-1067 |
| ev.03_symbols_md.app_static_css_pico_admin_layout_css.admin_main.l1068 | evidence/03_symbols.md | 1068-1068 |
| ev.03_symbols_md.app_static_css_pico_admin_layout_css.admin_mobile_toggle.l1069 | evidence/03_symbols.md | 1069-1069 |
| ev.03_symbols_md.app_static_css_pico_admin_layout_css.admin_sidebar_backdrop.l1070 | evidence/03_symbols.md | 1070-1070 |
| ev.03_symbols_md.app_static_css_pico_admin_layout_css.admin_sidebar.l1071 | evidence/03_symbols.md | 1071-1071 |
| ev.03_symbols_md.app_static_css_pico_admin_layout_css.admin_grid__3.l1072 | evidence/03_symbols.md | 1072-1072 |
| ev.03_symbols_md.app_static_css_pico_admin_layout_css.admin_grid__2.l1073 | evidence/03_symbols.md | 1073-1073 |
| ev.03_symbols_md.app_static_css_pico_admin_layout_css.admin_auth.l1074 | evidence/03_symbols.md | 1074-1074 |
| ev.03_symbols_md.app_static_css_pico_admin_layout_css.admin_auth__panel.l1075 | evidence/03_symbols.md | 1075-1075 |
| ev.03_symbols_md.app_static_css_pico_admin_layout_css.admin_auth__aside.l1076 | evidence/03_symbols.md | 1076-1076 |
| ev.03_symbols_md.app_static_css_pico_admin_layout_css.admin_header.l1077 | evidence/03_symbols.md | 1077-1077 |
| ev.03_symbols_md.app_static_css_pico_admin_layout_css.admin_header__actions.l1078 | evidence/03_symbols.md | 1078-1078 |
| ev.03_symbols_md.app_static_css_pico_admin_layout_css.admin_header__actions.l1079 | evidence/03_symbols.md | 1079-1079 |
| ev.03_symbols_md.app_static_css_pico_admin_layout_css.admin_content.l1080 | evidence/03_symbols.md | 1080-1080 |
| ev.03_symbols_md.app_static_css_pico_admin_layout_css.admin_grid.l1081 | evidence/03_symbols.md | 1081-1081 |
| ev.03_symbols_md.app_static_css_pico_admin_layout_css.admin_grid__4.l1082 | evidence/03_symbols.md | 1082-1082 |
| ev.03_symbols_md.app_static_css_pico_admin_theme_css.admin_bg_main.l1086 | evidence/03_symbols.md | 1086-1086 |
| ev.03_symbols_md.app_static_css_pico_admin_theme_css.admin_bg_sub.l1087 | evidence/03_symbols.md | 1087-1087 |
| ev.03_symbols_md.app_static_css_pico_admin_theme_css.admin_bg_elevated.l1088 | evidence/03_symbols.md | 1088-1088 |
| ev.03_symbols_md.app_static_css_pico_admin_theme_css.admin_bg_header.l1089 | evidence/03_symbols.md | 1089-1089 |
| ev.03_symbols_md.app_static_css_pico_admin_theme_css.admin_bg_hover.l1090 | evidence/03_symbols.md | 1090-1090 |
| ev.03_symbols_md.app_static_css_pico_admin_theme_css.admin_bg_active.l1091 | evidence/03_symbols.md | 1091-1091 |
| ev.03_symbols_md.app_static_css_pico_admin_theme_css.admin_bg_glass.l1092 | evidence/03_symbols.md | 1092-1092 |
| ev.03_symbols_md.app_static_css_pico_admin_theme_css.admin_border.l1093 | evidence/03_symbols.md | 1093-1093 |
| ev.03_symbols_md.app_static_css_pico_admin_theme_css.admin_border_strong.l1094 | evidence/03_symbols.md | 1094-1094 |
| ev.03_symbols_md.app_static_css_pico_admin_theme_css.admin_text_main.l1095 | evidence/03_symbols.md | 1095-1095 |
| ev.03_symbols_md.app_static_css_pico_admin_theme_css.admin_text_sub.l1096 | evidence/03_symbols.md | 1096-1096 |
| ev.03_symbols_md.app_static_css_pico_admin_theme_css.admin_text_muted.l1097 | evidence/03_symbols.md | 1097-1097 |
| ev.03_symbols_md.app_static_css_pico_admin_theme_css.admin_lime_main.l1098 | evidence/03_symbols.md | 1098-1098 |
| ev.03_symbols_md.app_static_css_pico_admin_theme_css.admin_lime_accent.l1099 | evidence/03_symbols.md | 1099-1099 |
| ev.03_symbols_md.app_static_css_pico_admin_theme_css.admin_lime_soft.l1100 | evidence/03_symbols.md | 1100-1100 |
| ev.03_symbols_md.app_static_css_pico_admin_theme_css.admin_lime_glow.l1101 | evidence/03_symbols.md | 1101-1101 |
| ev.03_symbols_md.app_static_css_pico_admin_theme_css.admin_pink_main.l1102 | evidence/03_symbols.md | 1102-1102 |
| ev.03_symbols_md.app_static_css_pico_admin_theme_css.admin_pink_soft.l1103 | evidence/03_symbols.md | 1103-1103 |
| ev.03_symbols_md.app_static_css_pico_admin_theme_css.admin_shadow.l1104 | evidence/03_symbols.md | 1104-1104 |
| ev.03_symbols_md.app_static_css_pico_admin_theme_css.admin_radius.l1105 | evidence/03_symbols.md | 1105-1105 |
| ev.03_symbols_md.app_static_css_pico_admin_theme_css.pico_background_color.l1106 | evidence/03_symbols.md | 1106-1106 |
| ev.03_symbols_md.app_static_css_pico_admin_theme_css.pico_color.l1107 | evidence/03_symbols.md | 1107-1107 |
| ev.03_symbols_md.app_static_css_pico_admin_theme_css.pico_muted_color.l1108 | evidence/03_symbols.md | 1108-1108 |
| ev.03_symbols_md.app_static_css_pico_admin_theme_css.pico_muted_border_color.l1109 | evidence/03_symbols.md | 1109-1109 |
| ev.03_symbols_md.app_static_css_pico_admin_theme_css.pico_primary.l1110 | evidence/03_symbols.md | 1110-1110 |
| ev.03_symbols_md.app_static_css_pico_admin_theme_css.pico_primary_hover.l1111 | evidence/03_symbols.md | 1111-1111 |
| ev.03_symbols_md.app_static_css_pico_admin_theme_css.pico_primary_focus.l1112 | evidence/03_symbols.md | 1112-1112 |
| ev.03_symbols_md.app_static_css_pico_admin_theme_css.pico_primary_inverse.l1113 | evidence/03_symbols.md | 1113-1113 |
| ev.03_symbols_md.app_static_css_pico_admin_theme_css.pico_secondary.l1114 | evidence/03_symbols.md | 1114-1114 |
| ev.03_symbols_md.app_static_css_pico_admin_theme_css.pico_secondary_hover.l1115 | evidence/03_symbols.md | 1115-1115 |
| ev.03_symbols_md.app_static_css_pico_admin_theme_css.pico_secondary_inverse.l1116 | evidence/03_symbols.md | 1116-1116 |
| ev.03_symbols_md.app_static_css_pico_admin_theme_css.pico_form_element_background_color.l1117 | evidence/03_symbols.md | 1117-1117 |
| ev.03_symbols_md.app_static_css_pico_admin_theme_css.pico_form_element_selected_background_color.l1118 | evidence/03_symbols.md | 1118-1118 |
| ev.03_symbols_md.app_static_css_pico_admin_theme_css.pico_form_element_border_color.l1119 | evidence/03_symbols.md | 1119-1119 |
| ev.03_symbols_md.app_static_css_pico_admin_theme_css.pico_form_element_active_border_color.l1120 | evidence/03_symbols.md | 1120-1120 |
| ev.03_symbols_md.app_static_css_pico_admin_theme_css.pico_form_element_focus_color.l1121 | evidence/03_symbols.md | 1121-1121 |
| ev.03_symbols_md.app_static_css_pico_admin_theme_css.pico_form_element_color.l1122 | evidence/03_symbols.md | 1122-1122 |
| ev.03_symbols_md.app_static_css_pico_admin_theme_css.pico_form_element_placeholder_color.l1123 | evidence/03_symbols.md | 1123-1123 |
| ev.03_symbols_md.app_static_css_pico_admin_theme_css.pico_card_background_color.l1124 | evidence/03_symbols.md | 1124-1124 |
| ev.03_symbols_md.app_static_css_pico_admin_theme_css.pico_card_border_color.l1125 | evidence/03_symbols.md | 1125-1125 |
| ev.03_symbols_md.app_static_css_pico_admin_theme_css.pico_card_sectioning_background_color.l1126 | evidence/03_symbols.md | 1126-1126 |
| ev.03_symbols_md.app_static_css_pico_admin_theme_css.pico_dropdown_background_color.l1127 | evidence/03_symbols.md | 1127-1127 |
| ev.03_symbols_md.app_static_css_pico_admin_theme_css.pico_dropdown_border_color.l1128 | evidence/03_symbols.md | 1128-1128 |
| ev.03_symbols_md.app_static_css_pico_admin_theme_css.pico_box_shadow.l1129 | evidence/03_symbols.md | 1129-1129 |
| ev.03_symbols_md.app_static_css_pico_admin_theme_css.pico_border_radius.l1130 | evidence/03_symbols.md | 1130-1130 |
| ev.03_symbols_md.app_static_css_pico_admin_theme_css.pico_spacing.l1131 | evidence/03_symbols.md | 1131-1131 |
| ev.03_symbols_md.app_static_css_pico_admin_theme_css.pico_font_family.l1132 | evidence/03_symbols.md | 1132-1132 |
| ev.03_symbols_md.app_static_css_pico_admin_theme_css.pico_line_height.l1133 | evidence/03_symbols.md | 1133-1133 |
| ev.03_symbols_md.app_static_js_search_ui_js.escapehtml.l1137 | evidence/03_symbols.md | 1137-1137 |
| ev.03_symbols_md.app_static_js_search_ui_js.yen.l1138 | evidence/03_symbols.md | 1138-1138 |
| ev.03_symbols_md.app_static_js_search_ui_js.boolbadge.l1139 | evidence/03_symbols.md | 1139-1139 |
| ev.03_symbols_md.app_static_js_search_ui_js.num.l1140 | evidence/03_symbols.md | 1140-1140 |
| ev.03_symbols_md.app_static_js_search_ui_js.assesscomponents.l1141 | evidence/03_symbols.md | 1141-1141 |
| ev.03_symbols_md.app_static_js_search_ui_js.renderpropertycard.l1142 | evidence/03_symbols.md | 1142-1142 |
| ev.03_symbols_md.app_static_js_search_ui_js.buildfilters.l1143 | evidence/03_symbols.md | 1143-1143 |
| ev.03_symbols_md.app_static_js_search_ui_js.rendercomponentstatus.l1144 | evidence/03_symbols.md | 1144-1144 |
| ev.03_symbols_md.app_static_js_search_ui_js.loadinfo.l1145 | evidence/03_symbols.md | 1145-1145 |
| ev.03_symbols_md.app_static_js_search_ui_js.init.l1146 | evidence/03_symbols.md | 1146-1146 |
| ev.03_symbols_md.app_static_js_search_ui_js.runsearch.l1147 | evidence/03_symbols.md | 1147-1147 |
| ev.03_symbols_md.app_static_js_search_ui_js.sendfeedback.l1148 | evidence/03_symbols.md | 1148-1148 |
| ev.03_symbols_md.app_templates__feedback_panel_html.panel_admin_card.l1152 | evidence/03_symbols.md | 1152-1152 |
| ev.03_symbols_md.app_templates__feedback_panel_html.admin_card__body.l1153 | evidence/03_symbols.md | 1153-1153 |
| ev.03_symbols_md.app_templates__feedback_panel_html.admin_section_heading.l1154 | evidence/03_symbols.md | 1154-1154 |
| ev.03_symbols_md.app_templates__feedback_panel_html.eyebrow.l1155 | evidence/03_symbols.md | 1155-1155 |
| ev.03_symbols_md.app_templates__feedback_panel_html.section_copy.l1156 | evidence/03_symbols.md | 1156-1156 |
| ev.03_symbols_md.app_templates__feedback_panel_html.feedback_form.l1157 | evidence/03_symbols.md | 1157-1157 |
| ev.03_symbols_md.app_templates__feedback_panel_html.grid.l1158 | evidence/03_symbols.md | 1158-1158 |
| ev.03_symbols_md.app_templates__feedback_panel_html.fb_pid.l1159 | evidence/03_symbols.md | 1159-1159 |
| ev.03_symbols_md.app_templates__feedback_panel_html.fb_action.l1160 | evidence/03_symbols.md | 1160-1160 |
| ev.03_symbols_md.app_templates__feedback_panel_html.action_row.l1161 | evidence/03_symbols.md | 1161-1161 |
| ev.03_symbols_md.app_templates__feedback_panel_html.feedback_btn.l1162 | evidence/03_symbols.md | 1162-1162 |
| ev.03_symbols_md.app_templates__feedback_panel_html.search_state.l1163 | evidence/03_symbols.md | 1163-1163 |
| ev.03_symbols_md.app_templates__feedback_panel_html.fb_result.l1164 | evidence/03_symbols.md | 1164-1164 |
| ev.03_symbols_md.app_templates__search_form_html.panel_admin_card.l1168 | evidence/03_symbols.md | 1168-1168 |
| ev.03_symbols_md.app_templates__search_form_html.admin_card__body.l1169 | evidence/03_symbols.md | 1169-1169 |
| ev.03_symbols_md.app_templates__search_form_html.admin_section_heading.l1170 | evidence/03_symbols.md | 1170-1170 |
| ev.03_symbols_md.app_templates__search_form_html.eyebrow.l1171 | evidence/03_symbols.md | 1171-1171 |
| ev.03_symbols_md.app_templates__search_form_html.section_copy.l1172 | evidence/03_symbols.md | 1172-1172 |
| ev.03_symbols_md.app_templates__search_form_html.search_form.l1173 | evidence/03_symbols.md | 1173-1173 |
| ev.03_symbols_md.app_templates__search_form_html.search_form.l1174 | evidence/03_symbols.md | 1174-1174 |
| ev.03_symbols_md.app_templates__search_form_html.q_query.l1175 | evidence/03_symbols.md | 1175-1175 |
| ev.03_symbols_md.app_templates__search_form_html.grid.l1176 | evidence/03_symbols.md | 1176-1176 |
| ev.03_symbols_md.app_templates__search_form_html.q_max_rent.l1177 | evidence/03_symbols.md | 1177-1177 |
| ev.03_symbols_md.app_templates__search_form_html.q_layout.l1178 | evidence/03_symbols.md | 1178-1178 |
| ev.03_symbols_md.app_templates__search_form_html.q_top_k.l1179 | evidence/03_symbols.md | 1179-1179 |
| ev.03_symbols_md.app_templates__search_form_html.grid.l1180 | evidence/03_symbols.md | 1180-1180 |
| ev.03_symbols_md.app_templates__search_form_html.q_max_walk_min.l1181 | evidence/03_symbols.md | 1181-1181 |
| ev.03_symbols_md.app_templates__search_form_html.q_max_age.l1182 | evidence/03_symbols.md | 1182-1182 |
| ev.03_symbols_md.app_templates__search_form_html.toggle_wrap.l1183 | evidence/03_symbols.md | 1183-1183 |
| ev.03_symbols_md.app_templates__search_form_html.q_pet_ok.l1184 | evidence/03_symbols.md | 1184-1184 |
| ev.03_symbols_md.app_templates__search_form_html.dev_controls.l1185 | evidence/03_symbols.md | 1185-1185 |
| ev.03_symbols_md.app_templates__search_form_html.toggle_wrap.l1186 | evidence/03_symbols.md | 1186-1186 |
| ev.03_symbols_md.app_templates__search_form_html.q_explain.l1187 | evidence/03_symbols.md | 1187-1187 |
| ev.03_symbols_md.app_templates__search_form_html.action_row.l1188 | evidence/03_symbols.md | 1188-1188 |
| ev.03_symbols_md.app_templates__search_form_html.search_btn.l1189 | evidence/03_symbols.md | 1189-1189 |
| ev.03_symbols_md.app_templates__search_form_html.search_state.l1190 | evidence/03_symbols.md | 1190-1190 |
| ev.03_symbols_md.app_templates__search_form_html.search_state.l1191 | evidence/03_symbols.md | 1191-1191 |
| ev.03_symbols_md.app_templates__search_results_html.result_card.l1195 | evidence/03_symbols.md | 1195-1195 |
| ev.03_symbols_md.app_templates__search_results_html.panel_admin_card_results_panel.l1196 | evidence/03_symbols.md | 1196-1196 |
| ev.03_symbols_md.app_templates__search_results_html.admin_card__body.l1197 | evidence/03_symbols.md | 1197-1197 |
| ev.03_symbols_md.app_templates__search_results_html.admin_section_heading.l1198 | evidence/03_symbols.md | 1198-1198 |
| ev.03_symbols_md.app_templates__search_results_html.eyebrow.l1199 | evidence/03_symbols.md | 1199-1199 |
| ev.03_symbols_md.app_templates__search_results_html.result_meta.l1200 | evidence/03_symbols.md | 1200-1200 |
| ev.03_symbols_md.app_templates__search_results_html.section_copy.l1201 | evidence/03_symbols.md | 1201-1201 |
| ev.03_symbols_md.app_templates__search_results_html.component_status_wrap_admin_grid_admin_grid__3.l1202 | evidence/03_symbols.md | 1202-1202 |
| ev.03_symbols_md.app_templates__search_results_html.status_card_admin_card_admin_card__compact_admin_card__dense.l1203 | evidence/03_symbols.md | 1203-1203 |
| ev.03_symbols_md.app_templates__search_results_html.status_label.l1204 | evidence/03_symbols.md | 1204-1204 |
| ev.03_symbols_md.app_templates__search_results_html.component_lexical_state.l1205 | evidence/03_symbols.md | 1205-1205 |
| ev.03_symbols_md.app_templates__search_results_html.component_lexical_note.l1206 | evidence/03_symbols.md | 1206-1206 |
| ev.03_symbols_md.app_templates__search_results_html.status_note.l1207 | evidence/03_symbols.md | 1207-1207 |
| ev.03_symbols_md.app_templates__search_results_html.status_card_admin_card_admin_card__compact_admin_card__dense.l1208 | evidence/03_symbols.md | 1208-1208 |
| ev.03_symbols_md.app_templates__search_results_html.status_label.l1209 | evidence/03_symbols.md | 1209-1209 |
| ev.03_symbols_md.app_templates__search_results_html.component_semantic_state.l1210 | evidence/03_symbols.md | 1210-1210 |
| ev.03_symbols_md.app_templates__search_results_html.component_semantic_note.l1211 | evidence/03_symbols.md | 1211-1211 |
| ev.03_symbols_md.app_templates__search_results_html.status_note.l1212 | evidence/03_symbols.md | 1212-1212 |
| ev.03_symbols_md.app_templates__search_results_html.status_card_admin_card_admin_card__compact_admin_card__dense.l1213 | evidence/03_symbols.md | 1213-1213 |
| ev.03_symbols_md.app_templates__search_results_html.status_label.l1214 | evidence/03_symbols.md | 1214-1214 |
| ev.03_symbols_md.app_templates__search_results_html.component_rerank_state.l1215 | evidence/03_symbols.md | 1215-1215 |
| ev.03_symbols_md.app_templates__search_results_html.component_rerank_note.l1216 | evidence/03_symbols.md | 1216-1216 |
| ev.03_symbols_md.app_templates__search_results_html.status_note.l1217 | evidence/03_symbols.md | 1217-1217 |
| ev.03_symbols_md.app_templates__search_results_html.result_rows.l1218 | evidence/03_symbols.md | 1218-1218 |
| ev.03_symbols_md.app_templates__search_results_html.result_grid.l1219 | evidence/03_symbols.md | 1219-1219 |
| ev.03_symbols_md.app_templates__search_results_html.admin_table_wrap_table_scroll.l1220 | evidence/03_symbols.md | 1220-1220 |
| ev.03_symbols_md.app_templates__search_results_html.admin_table.l1221 | evidence/03_symbols.md | 1221-1221 |
| ev.03_symbols_md.app_templates__search_results_html.debug_rows.l1222 | evidence/03_symbols.md | 1222-1222 |
| ev.03_symbols_md.app_templates__search_results_html.result_json.l1223 | evidence/03_symbols.md | 1223-1223 |
| ev.03_symbols_md.app_templates_base_html.admin_body.l1227 | evidence/03_symbols.md | 1227-1227 |
| ev.03_symbols_md.app_templates_base_html.admin_mobile_toggle_secondary.l1228 | evidence/03_symbols.md | 1228-1228 |
| ev.03_symbols_md.app_templates_base_html.admin_sidebar_backdrop.l1229 | evidence/03_symbols.md | 1229-1229 |
| ev.03_symbols_md.app_templates_base_html.admin_shell.l1230 | evidence/03_symbols.md | 1230-1230 |
| ev.03_symbols_md.app_templates_base_html.admin_sidebar.l1231 | evidence/03_symbols.md | 1231-1231 |
| ev.03_symbols_md.app_templates_base_html.admin_sidebar__inner.l1232 | evidence/03_symbols.md | 1232-1232 |
| ev.03_symbols_md.app_templates_base_html.admin_brand.l1233 | evidence/03_symbols.md | 1233-1233 |
| ev.03_symbols_md.app_templates_base_html.admin_brand__mark.l1234 | evidence/03_symbols.md | 1234-1234 |
| ev.03_symbols_md.app_templates_base_html.admin_brand__eyebrow.l1235 | evidence/03_symbols.md | 1235-1235 |
| ev.03_symbols_md.app_templates_base_html.secondary.l1236 | evidence/03_symbols.md | 1236-1236 |
| ev.03_symbols_md.app_templates_base_html.admin_nav.l1237 | evidence/03_symbols.md | 1237-1237 |
| ev.03_symbols_md.app_templates_base_html.admin_nav_item.l1238 | evidence/03_symbols.md | 1238-1238 |
| ev.03_symbols_md.app_templates_base_html.admin_nav_item.l1239 | evidence/03_symbols.md | 1239-1239 |
| ev.03_symbols_md.app_templates_base_html.admin_nav_item.l1240 | evidence/03_symbols.md | 1240-1240 |
| ev.03_symbols_md.app_templates_base_html.admin_nav_item.l1241 | evidence/03_symbols.md | 1241-1241 |
| ev.03_symbols_md.app_templates_base_html.admin_nav_item.l1242 | evidence/03_symbols.md | 1242-1242 |
| ev.03_symbols_md.app_templates_base_html.admin_nav_item_admin_nav_item__docs.l1243 | evidence/03_symbols.md | 1243-1243 |
| ev.03_symbols_md.app_templates_base_html.admin_main.l1244 | evidence/03_symbols.md | 1244-1244 |
| ev.03_symbols_md.app_templates_base_html.admin_header_app_header.l1245 | evidence/03_symbols.md | 1245-1245 |
| ev.03_symbols_md.app_templates_base_html.admin_eyebrow.l1246 | evidence/03_symbols.md | 1246-1246 |
| ev.03_symbols_md.app_templates_base_html.app_header__title.l1247 | evidence/03_symbols.md | 1247-1247 |
| ev.03_symbols_md.app_templates_base_html.app_header__copy.l1248 | evidence/03_symbols.md | 1248-1248 |
| ev.03_symbols_md.app_templates_base_html.admin_header__actions.l1249 | evidence/03_symbols.md | 1249-1249 |
| ev.03_symbols_md.app_templates_base_html.admin_segmented.l1250 | evidence/03_symbols.md | 1250-1250 |
| ev.03_symbols_md.app_templates_base_html.secondary_admin_user_chip.l1251 | evidence/03_symbols.md | 1251-1251 |
| ev.03_symbols_md.app_templates_base_html.admin_avatar.l1252 | evidence/03_symbols.md | 1252-1252 |
| ev.03_symbols_md.app_templates_base_html.admin_user__meta.l1253 | evidence/03_symbols.md | 1253-1253 |
| ev.03_symbols_md.app_templates_base_html.admin_user_chip__caret.l1254 | evidence/03_symbols.md | 1254-1254 |
| ev.03_symbols_md.app_templates_data_html.admin_content_admin_stack.l1258 | evidence/03_symbols.md | 1258-1258 |
| ev.03_symbols_md.app_templates_data_html.panel_admin_card.l1259 | evidence/03_symbols.md | 1259-1259 |
| ev.03_symbols_md.app_templates_data_html.admin_card__body_action_row.l1260 | evidence/03_symbols.md | 1260-1260 |
| ev.03_symbols_md.app_templates_data_html.data_btn.l1261 | evidence/03_symbols.md | 1261-1261 |
| ev.03_symbols_md.app_templates_data_html.data_meta.l1262 | evidence/03_symbols.md | 1262-1262 |
| ev.03_symbols_md.app_templates_data_html.search_state.l1263 | evidence/03_symbols.md | 1263-1263 |
| ev.03_symbols_md.app_templates_data_html.data_tables.l1264 | evidence/03_symbols.md | 1264-1264 |
| ev.03_symbols_md.app_templates_data_html.admin_stack.l1265 | evidence/03_symbols.md | 1265-1265 |
| ev.03_symbols_md.app_templates_data_html.search_state.l1266 | evidence/03_symbols.md | 1266-1266 |
| ev.03_symbols_md.app_templates_data_html.panel_admin_card.l1267 | evidence/03_symbols.md | 1267-1267 |
| ev.03_symbols_md.app_templates_data_html.admin_card__body.l1268 | evidence/03_symbols.md | 1268-1268 |
| ev.03_symbols_md.app_templates_data_html.admin_section_heading.l1269 | evidence/03_symbols.md | 1269-1269 |
| ev.03_symbols_md.app_templates_data_html.eyebrow.l1270 | evidence/03_symbols.md | 1270-1270 |
| ev.03_symbols_md.app_templates_data_html.section_copy.l1271 | evidence/03_symbols.md | 1271-1271 |
| ev.03_symbols_md.app_templates_data_html.section_copy.l1272 | evidence/03_symbols.md | 1272-1272 |
| ev.03_symbols_md.app_templates_data_html.admin_table_wrap_table_scroll.l1273 | evidence/03_symbols.md | 1273-1273 |
| ev.03_symbols_md.app_templates_data_html.admin_table.l1274 | evidence/03_symbols.md | 1274-1274 |
| ev.03_symbols_md.app_templates_data_html.panel.l1275 | evidence/03_symbols.md | 1275-1275 |
| ev.03_symbols_md.app_templates_index_html.search_app.l1279 | evidence/03_symbols.md | 1279-1279 |
| ev.03_symbols_md.app_templates_index_html.admin_content_search_shell.l1280 | evidence/03_symbols.md | 1280-1280 |
| ev.03_symbols_md.app_templates_model_metrics_html.admin_content_admin_stack.l1284 | evidence/03_symbols.md | 1284-1284 |
| ev.03_symbols_md.app_templates_model_metrics_html.admin_card.l1285 | evidence/03_symbols.md | 1285-1285 |
| ev.03_symbols_md.app_templates_model_metrics_html.admin_card__body.l1286 | evidence/03_symbols.md | 1286-1286 |
| ev.03_symbols_md.app_templates_model_metrics_html.acc_form.l1287 | evidence/03_symbols.md | 1287-1287 |
| ev.03_symbols_md.app_templates_model_metrics_html.q_k.l1288 | evidence/03_symbols.md | 1288-1288 |
| ev.03_symbols_md.app_templates_model_metrics_html.acc_btn.l1289 | evidence/03_symbols.md | 1289-1289 |
| ev.03_symbols_md.app_templates_model_metrics_html.acc_summary_card.l1290 | evidence/03_symbols.md | 1290-1290 |
| ev.03_symbols_md.app_templates_model_metrics_html.admin_card.l1291 | evidence/03_symbols.md | 1291-1291 |
| ev.03_symbols_md.app_templates_model_metrics_html.admin_card__body.l1292 | evidence/03_symbols.md | 1292-1292 |
| ev.03_symbols_md.app_templates_model_metrics_html.admin_section_heading.l1293 | evidence/03_symbols.md | 1293-1293 |
| ev.03_symbols_md.app_templates_model_metrics_html.admin_eyebrow.l1294 | evidence/03_symbols.md | 1294-1294 |
| ev.03_symbols_md.app_templates_model_metrics_html.acc_meta.l1295 | evidence/03_symbols.md | 1295-1295 |
| ev.03_symbols_md.app_templates_model_metrics_html.admin_grid_admin_grid__3.l1296 | evidence/03_symbols.md | 1296-1296 |
| ev.03_symbols_md.app_templates_model_metrics_html.acc_ndcg.l1297 | evidence/03_symbols.md | 1297-1297 |
| ev.03_symbols_md.app_templates_model_metrics_html.admin_card_admin_card__compact_admin_card__dense.l1298 | evidence/03_symbols.md | 1298-1298 |
| ev.03_symbols_md.app_templates_model_metrics_html.acc_hit.l1299 | evidence/03_symbols.md | 1299-1299 |
| ev.03_symbols_md.app_templates_model_metrics_html.admin_card_admin_card__compact_admin_card__dense.l1300 | evidence/03_symbols.md | 1300-1300 |
| ev.03_symbols_md.app_templates_model_metrics_html.acc_mrr.l1301 | evidence/03_symbols.md | 1301-1301 |
| ev.03_symbols_md.app_templates_model_metrics_html.admin_card_admin_card__compact_admin_card__dense.l1302 | evidence/03_symbols.md | 1302-1302 |
| ev.03_symbols_md.app_templates_model_metrics_html.acc_cases_card.l1303 | evidence/03_symbols.md | 1303-1303 |
| ev.03_symbols_md.app_templates_model_metrics_html.admin_card.l1304 | evidence/03_symbols.md | 1304-1304 |
| ev.03_symbols_md.app_templates_model_metrics_html.admin_card__body.l1305 | evidence/03_symbols.md | 1305-1305 |
| ev.03_symbols_md.app_templates_model_metrics_html.admin_section_heading.l1306 | evidence/03_symbols.md | 1306-1306 |
| ev.03_symbols_md.app_templates_model_metrics_html.admin_eyebrow.l1307 | evidence/03_symbols.md | 1307-1307 |
| ev.03_symbols_md.app_templates_model_metrics_html.admin_table_wrap_table_scroll.l1308 | evidence/03_symbols.md | 1308-1308 |
| ev.03_symbols_md.app_templates_model_metrics_html.admin_table.l1309 | evidence/03_symbols.md | 1309-1309 |
| ev.03_symbols_md.app_templates_model_metrics_html.acc_rows.l1310 | evidence/03_symbols.md | 1310-1310 |
| ev.03_symbols_md.app_templates_ops_html.admin_content_admin_stack.l1314 | evidence/03_symbols.md | 1314-1314 |
| ev.03_symbols_md.app_templates_ops_html.panel_admin_card.l1315 | evidence/03_symbols.md | 1315-1315 |
| ev.03_symbols_md.app_templates_ops_html.admin_card__body_action_row.l1316 | evidence/03_symbols.md | 1316-1316 |
| ev.03_symbols_md.app_templates_ops_html.ops_btn.l1317 | evidence/03_symbols.md | 1317-1317 |
| ev.03_symbols_md.app_templates_ops_html.ops_meta.l1318 | evidence/03_symbols.md | 1318-1318 |
| ev.03_symbols_md.app_templates_ops_html.search_state.l1319 | evidence/03_symbols.md | 1319-1319 |
| ev.03_symbols_md.app_templates_ops_html.admin_grid_admin_grid__3_status_grid.l1320 | evidence/03_symbols.md | 1320-1320 |
| ev.03_symbols_md.app_templates_ops_html.status_card_admin_card_admin_card__compact_admin_card__dense.l1321 | evidence/03_symbols.md | 1321-1321 |
| ev.03_symbols_md.app_templates_ops_html.status_label.l1322 | evidence/03_symbols.md | 1322-1322 |
| ev.03_symbols_md.app_templates_ops_html.ops_ok.l1323 | evidence/03_symbols.md | 1323-1323 |
| ev.03_symbols_md.app_templates_ops_html.status_card_admin_card_admin_card__compact_admin_card__dense.l1324 | evidence/03_symbols.md | 1324-1324 |
| ev.03_symbols_md.app_templates_ops_html.status_label.l1325 | evidence/03_symbols.md | 1325-1325 |
| ev.03_symbols_md.app_templates_ops_html.ops_warn.l1326 | evidence/03_symbols.md | 1326-1326 |
| ev.03_symbols_md.app_templates_ops_html.status_card_status_card_danger_admin_card_admin_card__compact_admin_card__dense.l1327 | evidence/03_symbols.md | 1327-1327 |
| ev.03_symbols_md.app_templates_ops_html.status_label.l1328 | evidence/03_symbols.md | 1328-1328 |
| ev.03_symbols_md.app_templates_ops_html.ops_bad.l1329 | evidence/03_symbols.md | 1329-1329 |
| ev.03_symbols_md.app_templates_ops_html.admin_grid_admin_grid__3_status_grid.l1330 | evidence/03_symbols.md | 1330-1330 |
| ev.03_symbols_md.app_templates_ops_html.status_card_admin_card_admin_card__compact_admin_card__dense.l1331 | evidence/03_symbols.md | 1331-1331 |
| ev.03_symbols_md.app_templates_ops_html.status_label.l1332 | evidence/03_symbols.md | 1332-1332 |
| ev.03_symbols_md.app_templates_ops_html.ops_search_volume.l1333 | evidence/03_symbols.md | 1333-1333 |
| ev.03_symbols_md.app_templates_ops_html.ops_search_window.l1334 | evidence/03_symbols.md | 1334-1334 |
| ev.03_symbols_md.app_templates_ops_html.status_note.l1335 | evidence/03_symbols.md | 1335-1335 |
| ev.03_symbols_md.app_templates_ops_html.status_card_status_card_wide_admin_card_admin_card__compact_admin_card__dense.l1336 | evidence/03_symbols.md | 1336-1336 |
| ev.03_symbols_md.app_templates_ops_html.status_label.l1337 | evidence/03_symbols.md | 1337-1337 |
| ev.03_symbols_md.app_templates_ops_html.ops_runs_count.l1338 | evidence/03_symbols.md | 1338-1338 |
| ev.03_symbols_md.app_templates_ops_html.status_note.l1339 | evidence/03_symbols.md | 1339-1339 |
| ev.03_symbols_md.app_templates_ops_html.panel_admin_card.l1340 | evidence/03_symbols.md | 1340-1340 |
| ev.03_symbols_md.app_templates_ops_html.admin_card__body.l1341 | evidence/03_symbols.md | 1341-1341 |
| ev.03_symbols_md.app_templates_ops_html.admin_section_heading.l1342 | evidence/03_symbols.md | 1342-1342 |
| ev.03_symbols_md.app_templates_ops_html.eyebrow.l1343 | evidence/03_symbols.md | 1343-1343 |
| ev.03_symbols_md.app_templates_ops_html.section_copy.l1344 | evidence/03_symbols.md | 1344-1344 |
| ev.03_symbols_md.app_templates_ops_html.admin_table_wrap_table_scroll.l1345 | evidence/03_symbols.md | 1345-1345 |
| ev.03_symbols_md.app_templates_ops_html.admin_table.l1346 | evidence/03_symbols.md | 1346-1346 |
| ev.03_symbols_md.app_templates_ops_html.ops_runs_rows.l1347 | evidence/03_symbols.md | 1347-1347 |
| ev.03_symbols_md.app_templates_ops_html.ops_findings.l1348 | evidence/03_symbols.md | 1348-1348 |
| ev.03_symbols_md.app_templates_ops_html.admin_grid_admin_grid__2.l1349 | evidence/03_symbols.md | 1349-1349 |
| ev.03_symbols_md.app_templates_ops_html.ops_item_list.l1350 | evidence/03_symbols.md | 1350-1350 |
| ev.03_symbols_md.app_templates_ops_html.section_copy.l1351 | evidence/03_symbols.md | 1351-1351 |
| ev.03_symbols_md.app_templates_ops_html.panel_admin_card_ops_panel_ops_panel___string_finding_severity.l1352 | evidence/03_symbols.md | 1352-1352 |
| ev.03_symbols_md.app_templates_ops_html.admin_card__body.l1353 | evidence/03_symbols.md | 1353-1353 |
| ev.03_symbols_md.app_templates_ops_html.admin_section_heading.l1354 | evidence/03_symbols.md | 1354-1354 |
| ev.03_symbols_md.app_templates_ops_html.eyebrow.l1355 | evidence/03_symbols.md | 1355-1355 |
| ev.03_symbols_md.app_templates_ops_html.search_state.l1356 | evidence/03_symbols.md | 1356-1356 |
| ev.03_symbols_md.app_templates_ops_html.panel.l1357 | evidence/03_symbols.md | 1357-1357 |
| ev.03_symbols_md.app_templates_property_detail_html.panel_admin_card.l1361 | evidence/03_symbols.md | 1361-1361 |
| ev.03_symbols_md.app_templates_property_detail_html.admin_card__body.l1362 | evidence/03_symbols.md | 1362-1362 |
| ev.03_symbols_md.app_templates_property_detail_html.admin_section_heading.l1363 | evidence/03_symbols.md | 1363-1363 |
| ev.03_symbols_md.app_templates_property_detail_html.eyebrow.l1364 | evidence/03_symbols.md | 1364-1364 |
| ev.03_symbols_md.app_templates_property_detail_html.property_title.l1365 | evidence/03_symbols.md | 1365-1365 |
| ev.03_symbols_md.app_templates_property_detail_html.request_id.l1366 | evidence/03_symbols.md | 1366-1366 |
| ev.03_symbols_md.app_templates_property_detail_html.section_copy.l1367 | evidence/03_symbols.md | 1367-1367 |
| ev.03_symbols_md.app_templates_property_detail_html.secondary.l1368 | evidence/03_symbols.md | 1368-1368 |
| ev.03_symbols_md.app_templates_property_detail_html.grid.l1369 | evidence/03_symbols.md | 1369-1369 |
| ev.03_symbols_md.app_templates_property_detail_html.section_copy.l1370 | evidence/03_symbols.md | 1370-1370 |
| ev.03_symbols_md.app_templates_property_detail_html.action_row.l1371 | evidence/03_symbols.md | 1371-1371 |
| ev.03_symbols_md.app_templates_property_detail_html.btn_favorite.l1372 | evidence/03_symbols.md | 1372-1372 |
| ev.03_symbols_md.app_templates_property_detail_html.secondary.l1373 | evidence/03_symbols.md | 1373-1373 |
| ev.03_symbols_md.app_templates_property_detail_html.btn_request_click.l1374 | evidence/03_symbols.md | 1374-1374 |
| ev.03_symbols_md.app_templates_property_detail_html.secondary.l1375 | evidence/03_symbols.md | 1375-1375 |
| ev.03_symbols_md.app_templates_property_detail_html.btn_request_complete.l1376 | evidence/03_symbols.md | 1376-1376 |
| ev.03_symbols_md.app_templates_property_detail_html.emit_result.l1377 | evidence/03_symbols.md | 1377-1377 |
| ev.03_symbols_md.app_templates_search_dev_html.search_app.l1381 | evidence/03_symbols.md | 1381-1381 |
| ev.03_symbols_md.app_templates_search_dev_html.admin_content_search_shell.l1382 | evidence/03_symbols.md | 1382-1382 |
| ev.03_symbols_md.app_templates_search_dev_html.panel_admin_card.l1383 | evidence/03_symbols.md | 1383-1383 |
| ev.03_symbols_md.app_templates_search_dev_html.admin_card__body.l1384 | evidence/03_symbols.md | 1384-1384 |
| ev.03_symbols_md.app_templates_search_dev_html.admin_section_heading.l1385 | evidence/03_symbols.md | 1385-1385 |
| ev.03_symbols_md.app_templates_search_dev_html.eyebrow.l1386 | evidence/03_symbols.md | 1386-1386 |
| ev.03_symbols_md.app_templates_search_dev_html.section_copy.l1387 | evidence/03_symbols.md | 1387-1387 |
| ev.03_symbols_md.app_templates_search_dev_html.action_row.l1388 | evidence/03_symbols.md | 1388-1388 |
| ev.03_symbols_md.app_templates_search_dev_html.data_btn.l1389 | evidence/03_symbols.md | 1389-1389 |
| ev.03_symbols_md.app_templates_search_dev_html.search_state.l1390 | evidence/03_symbols.md | 1390-1390 |
| ev.03_symbols_md.app_templates_search_dev_html.table_scroll.l1391 | evidence/03_symbols.md | 1391-1391 |
| ev.03_symbols_md.app_templates_search_dev_html.data_card.l1392 | evidence/03_symbols.md | 1392-1392 |
| ev.03_symbols_md.app_templates_search_dev_html.admin_table.l1393 | evidence/03_symbols.md | 1393-1393 |
| ev.03_symbols_md.app_templates_search_dev_html.data_rows.l1394 | evidence/03_symbols.md | 1394-1394 |
| ev.03_symbols_md.infra_run_services_composer_runner_dockerfile.ghcr_io_astral_sh_uv_0_5_4_python3_12_bookworm_slim.l1398 | evidence/03_symbols.md | 1398-1398 |
| ev.03_symbols_md.infra_run_services_composer_runner_dockerfile.python_3_12_slim_bookworm.l1399 | evidence/03_symbols.md | 1399-1399 |
| ev.03_symbols_md.infra_run_services_encoder_dockerfile.ml_builder_image.l1403 | evidence/03_symbols.md | 1403-1403 |
| ev.03_symbols_md.infra_run_services_encoder_dockerfile.python_3_12_slim_bookworm.l1404 | evidence/03_symbols.md | 1404-1404 |
| ev.03_symbols_md.infra_run_services_ml_base_dockerfile.ghcr_io_astral_sh_uv_0_5_4_python3_12_bookworm_slim.l1408 | evidence/03_symbols.md | 1408-1408 |
| ev.03_symbols_md.infra_run_services_reranker_dockerfile.ml_builder_image.l1412 | evidence/03_symbols.md | 1412-1412 |
| ev.03_symbols_md.infra_run_services_reranker_dockerfile.python_3_12_slim_bookworm.l1413 | evidence/03_symbols.md | 1413-1413 |
| ev.03_symbols_md.infra_run_services_search_api_dockerfile.ghcr_io_astral_sh_uv_0_5_4_python3_12_bookworm_slim.l1417 | evidence/03_symbols.md | 1417-1417 |
| ev.03_symbols_md.infra_run_services_search_api_dockerfile.python_3_12_slim_bookworm.l1418 | evidence/03_symbols.md | 1418-1418 |
| ev.03_symbols_md.infra_terraform_environments_dev_apis_tf.google_project_service_enabled.l1422 | evidence/03_symbols.md | 1422-1422 |
| ev.03_symbols_md.infra_terraform_modules_composer_main_tf.google_composer_environment_this.l1426 | evidence/03_symbols.md | 1426-1426 |
| ev.03_symbols_md.infra_terraform_modules_data_main_tf.google_bigquery_dataset_mlops.l1430 | evidence/03_symbols.md | 1430-1430 |
| ev.03_symbols_md.infra_terraform_modules_data_main_tf.google_bigquery_dataset_feature_mart.l1431 | evidence/03_symbols.md | 1431-1431 |
| ev.03_symbols_md.infra_terraform_modules_data_main_tf.google_bigquery_dataset_predictions.l1432 | evidence/03_symbols.md | 1432-1432 |
| ev.03_symbols_md.infra_terraform_modules_data_main_tf.google_bigquery_table_training_runs.l1433 | evidence/03_symbols.md | 1433-1433 |
| ev.03_symbols_md.infra_terraform_modules_data_main_tf.google_bigquery_table_property_features_daily.l1434 | evidence/03_symbols.md | 1434-1434 |
| ev.03_symbols_md.infra_terraform_modules_data_main_tf.google_bigquery_table_property_features_online_latest.l1435 | evidence/03_symbols.md | 1435-1435 |
| ev.03_symbols_md.infra_terraform_modules_data_main_tf.google_bigquery_table_property_embeddings.l1436 | evidence/03_symbols.md | 1436-1436 |
| ev.03_symbols_md.infra_terraform_modules_data_main_tf.google_bigquery_table_search_logs.l1437 | evidence/03_symbols.md | 1437-1437 |
| ev.03_symbols_md.infra_terraform_modules_data_main_tf.google_bigquery_table_ranking_log.l1438 | evidence/03_symbols.md | 1438-1438 |
| ev.03_symbols_md.infra_terraform_modules_data_main_tf.google_bigquery_table_feedback_events.l1439 | evidence/03_symbols.md | 1439-1439 |
| ev.03_symbols_md.infra_terraform_modules_data_main_tf.google_bigquery_table_search_events.l1440 | evidence/03_symbols.md | 1440-1440 |
| ev.03_symbols_md.infra_terraform_modules_data_main_tf.google_bigquery_table_search_impressions.l1441 | evidence/03_symbols.md | 1441-1441 |
| ev.03_symbols_md.infra_terraform_modules_data_main_tf.google_bigquery_table_user_actions.l1442 | evidence/03_symbols.md | 1442-1442 |
| ev.03_symbols_md.infra_terraform_modules_data_main_tf.google_bigquery_table_ranking_labels.l1443 | evidence/03_symbols.md | 1443-1443 |
| ev.03_symbols_md.infra_terraform_modules_data_main_tf.google_bigquery_table_evaluation_metrics.l1444 | evidence/03_symbols.md | 1444-1444 |
| ev.03_symbols_md.infra_terraform_modules_data_main_tf.google_bigquery_table_validation_results.l1445 | evidence/03_symbols.md | 1445-1445 |
| ev.03_symbols_md.infra_terraform_modules_data_main_tf.google_bigquery_table_model_monitoring_alerts.l1446 | evidence/03_symbols.md | 1446-1446 |
| ev.03_symbols_md.infra_terraform_modules_data_main_tf.google_bigquery_table_ranking_log_hourly_ctr.l1447 | evidence/03_symbols.md | 1447-1447 |
| ev.03_symbols_md.infra_terraform_modules_data_main_tf.google_storage_bucket_models.l1448 | evidence/03_symbols.md | 1448-1448 |
| ev.03_symbols_md.infra_terraform_modules_data_main_tf.google_storage_bucket_artifacts.l1449 | evidence/03_symbols.md | 1449-1449 |
| ev.03_symbols_md.infra_terraform_modules_data_main_tf.google_storage_bucket_pipeline_root.l1450 | evidence/03_symbols.md | 1450-1450 |
| ev.03_symbols_md.infra_terraform_modules_data_main_tf.google_artifact_registry_repository_mlops.l1451 | evidence/03_symbols.md | 1451-1451 |
| ev.03_symbols_md.infra_terraform_modules_data_main_tf.google_secret_manager_secret_search_api_iap_oauth_client_secret.l1452 | evidence/03_symbols.md | 1452-1452 |
| ev.03_symbols_md.infra_terraform_modules_data_main_tf.google_secret_manager_secret_version_search_api_iap_oauth_client_secret_dev_placeholder.l1453 | evidence/03_symbols.md | 1453-1453 |
| ev.03_symbols_md.infra_terraform_modules_data_main_tf.google_bigquery_dataset_iam_member_api_mlops_viewer.l1454 | evidence/03_symbols.md | 1454-1454 |
| ev.03_symbols_md.infra_terraform_modules_data_main_tf.google_bigquery_dataset_iam_member_api_feature_viewer.l1455 | evidence/03_symbols.md | 1455-1455 |
| ev.03_symbols_md.infra_terraform_modules_data_main_tf.google_storage_bucket_iam_member_api_models_read.l1456 | evidence/03_symbols.md | 1456-1456 |
| ev.03_symbols_md.infra_terraform_modules_data_main_tf.google_secret_manager_secret_iam_member_external_secrets_search_api_iap_oauth_client_secret_access.l1457 | evidence/03_symbols.md | 1457-1457 |
| ev.03_symbols_md.infra_terraform_modules_data_main_tf.google_bigquery_dataset_iam_member_train_feature_viewer.l1458 | evidence/03_symbols.md | 1458-1458 |
| ev.03_symbols_md.infra_terraform_modules_data_main_tf.google_bigquery_dataset_iam_member_train_mlops_editor.l1459 | evidence/03_symbols.md | 1459-1459 |
| ev.03_symbols_md.infra_terraform_modules_data_main_tf.google_storage_bucket_iam_member_train_models_admin.l1460 | evidence/03_symbols.md | 1460-1460 |
| ev.03_symbols_md.infra_terraform_modules_data_main_tf.google_storage_bucket_iam_member_train_pipeline_root_admin.l1461 | evidence/03_symbols.md | 1461-1461 |
| ev.03_symbols_md.infra_terraform_modules_data_main_tf.google_bigquery_dataset_iam_member_embed_feature_viewer.l1462 | evidence/03_symbols.md | 1462-1462 |
| ev.03_symbols_md.infra_terraform_modules_data_main_tf.google_bigquery_dataset_iam_member_embed_feature_editor.l1463 | evidence/03_symbols.md | 1463-1463 |
| ev.03_symbols_md.infra_terraform_modules_data_main_tf.google_storage_bucket_iam_member_embed_models_viewer.l1464 | evidence/03_symbols.md | 1464-1464 |
| ev.03_symbols_md.infra_terraform_modules_data_main_tf.google_bigquery_dataset_iam_member_pipeline_feature_viewer.l1465 | evidence/03_symbols.md | 1465-1465 |
| ev.03_symbols_md.infra_terraform_modules_data_main_tf.google_bigquery_dataset_iam_member_pipeline_mlops_editor.l1466 | evidence/03_symbols.md | 1466-1466 |
| ev.03_symbols_md.infra_terraform_modules_data_main_tf.google_storage_bucket_iam_member_pipeline_models_admin.l1467 | evidence/03_symbols.md | 1467-1467 |
| ev.03_symbols_md.infra_terraform_modules_data_main_tf.google_storage_bucket_iam_member_pipeline_root_pipeline_admin.l1468 | evidence/03_symbols.md | 1468-1468 |
| ev.03_symbols_md.infra_terraform_modules_data_main_tf.google_storage_bucket_iam_member_pipeline_root_composer_object_admin.l1469 | evidence/03_symbols.md | 1469-1469 |
| ev.03_symbols_md.infra_terraform_modules_data_main_tf.google_storage_bucket_iam_member_endpoint_encoder_models_viewer.l1470 | evidence/03_symbols.md | 1470-1470 |
| ev.03_symbols_md.infra_terraform_modules_data_main_tf.google_storage_bucket_iam_member_endpoint_reranker_models_viewer.l1471 | evidence/03_symbols.md | 1471-1471 |
| ev.03_symbols_md.infra_terraform_modules_data_main_tf.google_bigquery_dataset_iam_member_dataform_feature_editor.l1472 | evidence/03_symbols.md | 1472-1472 |
| ev.03_symbols_md.infra_terraform_modules_data_main_tf.google_bigquery_dataset_iam_member_dataform_mlops_editor.l1473 | evidence/03_symbols.md | 1473-1473 |
| ev.03_symbols_md.infra_terraform_modules_data_main_tf.google_dataform_repository_main.l1474 | evidence/03_symbols.md | 1474-1474 |
| ev.03_symbols_md.infra_terraform_modules_data_main_tf.google_dataform_repository_iam_member_admin_self.l1475 | evidence/03_symbols.md | 1475-1475 |
| ev.03_symbols_md.infra_terraform_modules_data_main_tf.google_dataform_repository_iam_member_deployer_editor.l1476 | evidence/03_symbols.md | 1476-1476 |
| ev.03_symbols_md.infra_terraform_modules_dns_main_tf.google_compute_global_address_search_api.l1480 | evidence/03_symbols.md | 1480-1480 |
| ev.03_symbols_md.infra_terraform_modules_dns_main_tf.google_dns_record_set_apex_a.l1481 | evidence/03_symbols.md | 1481-1481 |
| ev.03_symbols_md.infra_terraform_modules_dns_main_tf.google_certificate_manager_dns_authorization_search_api.l1482 | evidence/03_symbols.md | 1482-1482 |
| ev.03_symbols_md.infra_terraform_modules_dns_main_tf.google_dns_record_set_cert_auth_cname.l1483 | evidence/03_symbols.md | 1483-1483 |
| ev.03_symbols_md.infra_terraform_modules_dns_main_tf.google_certificate_manager_certificate_search_api.l1484 | evidence/03_symbols.md | 1484-1484 |
| ev.03_symbols_md.infra_terraform_modules_dns_main_tf.google_certificate_manager_certificate_map_search_api.l1485 | evidence/03_symbols.md | 1485-1485 |
| ev.03_symbols_md.infra_terraform_modules_dns_main_tf.google_certificate_manager_certificate_map_entry_search_api.l1486 | evidence/03_symbols.md | 1486-1486 |
| ev.03_symbols_md.infra_terraform_modules_elasticsearch_main_tf.kubernetes_namespace_elastic_system.l1490 | evidence/03_symbols.md | 1490-1490 |
| ev.03_symbols_md.infra_terraform_modules_elasticsearch_main_tf.helm_release_eck_operator.l1491 | evidence/03_symbols.md | 1491-1491 |
| ev.03_symbols_md.infra_terraform_modules_gke_main_tf.google_container_cluster_hybrid_search.l1495 | evidence/03_symbols.md | 1495-1495 |
| ev.03_symbols_md.infra_terraform_modules_gke_main_tf.google_service_account_iam_member_api_wi.l1496 | evidence/03_symbols.md | 1496-1496 |
| ev.03_symbols_md.infra_terraform_modules_gke_main_tf.google_service_account_iam_member_encoder_wi.l1497 | evidence/03_symbols.md | 1497-1497 |
| ev.03_symbols_md.infra_terraform_modules_gke_main_tf.google_service_account_iam_member_reranker_wi.l1498 | evidence/03_symbols.md | 1498-1498 |
| ev.03_symbols_md.infra_terraform_modules_gke_main_tf.google_service_account_iam_member_external_secrets_wi.l1499 | evidence/03_symbols.md | 1499-1499 |
| ev.03_symbols_md.infra_terraform_modules_iam_main_tf.google_service_account_api.l1503 | evidence/03_symbols.md | 1503-1503 |
| ev.03_symbols_md.infra_terraform_modules_iam_main_tf.google_service_account_job_train.l1504 | evidence/03_symbols.md | 1504-1504 |
| ev.03_symbols_md.infra_terraform_modules_iam_main_tf.google_service_account_job_embed.l1505 | evidence/03_symbols.md | 1505-1505 |
| ev.03_symbols_md.infra_terraform_modules_iam_main_tf.google_service_account_dataform.l1506 | evidence/03_symbols.md | 1506-1506 |
| ev.03_symbols_md.infra_terraform_modules_iam_main_tf.google_service_account_scheduler.l1507 | evidence/03_symbols.md | 1507-1507 |
| ev.03_symbols_md.infra_terraform_modules_iam_main_tf.google_service_account_pipeline.l1508 | evidence/03_symbols.md | 1508-1508 |
| ev.03_symbols_md.infra_terraform_modules_iam_main_tf.google_service_account_endpoint_encoder.l1509 | evidence/03_symbols.md | 1509-1509 |
| ev.03_symbols_md.infra_terraform_modules_iam_main_tf.google_service_account_endpoint_reranker.l1510 | evidence/03_symbols.md | 1510-1510 |
| ev.03_symbols_md.infra_terraform_modules_iam_main_tf.google_service_account_pipeline_trigger.l1511 | evidence/03_symbols.md | 1511-1511 |
| ev.03_symbols_md.infra_terraform_modules_iam_main_tf.google_service_account_external_secrets.l1512 | evidence/03_symbols.md | 1512-1512 |
| ev.03_symbols_md.infra_terraform_modules_iam_main_tf.google_iam_workload_identity_pool_github.l1513 | evidence/03_symbols.md | 1513-1513 |
| ev.03_symbols_md.infra_terraform_modules_iam_main_tf.google_iam_workload_identity_pool_provider_github.l1514 | evidence/03_symbols.md | 1514-1514 |
| ev.03_symbols_md.infra_terraform_modules_iam_main_tf.google_service_account_github_deployer.l1515 | evidence/03_symbols.md | 1515-1515 |
| ev.03_symbols_md.infra_terraform_modules_iam_main_tf.google_service_account_iam_member_github_wif_binding.l1516 | evidence/03_symbols.md | 1516-1516 |
| ev.03_symbols_md.infra_terraform_modules_iam_main_tf.google_service_account_iam_member_api_token_creator_for_admins.l1517 | evidence/03_symbols.md | 1517-1517 |
| ev.03_symbols_md.infra_terraform_modules_iam_main_tf.google_project_iam_member_github_deployer_editor.l1518 | evidence/03_symbols.md | 1518-1518 |
| ev.03_symbols_md.infra_terraform_modules_iam_main_tf.google_project_iam_member_github_deployer_sa_user.l1519 | evidence/03_symbols.md | 1519-1519 |
| ev.03_symbols_md.infra_terraform_modules_iam_main_tf.google_project_iam_member_api_bq_job_user.l1520 | evidence/03_symbols.md | 1520-1520 |
| ev.03_symbols_md.infra_terraform_modules_iam_main_tf.google_project_iam_member_gmp_compute_metric_writer.l1521 | evidence/03_symbols.md | 1521-1521 |
| ev.03_symbols_md.infra_terraform_modules_iam_main_tf.google_project_iam_member_api_aiplatform_user.l1522 | evidence/03_symbols.md | 1522-1522 |
| ev.03_symbols_md.infra_terraform_modules_iam_main_tf.google_project_iam_member_train_bq_job_user.l1523 | evidence/03_symbols.md | 1523-1523 |
| ev.03_symbols_md.infra_terraform_modules_iam_main_tf.google_project_iam_member_train_bq_read_session.l1524 | evidence/03_symbols.md | 1524-1524 |
| ev.03_symbols_md.infra_terraform_modules_iam_main_tf.google_project_iam_member_embed_bq_job_user.l1525 | evidence/03_symbols.md | 1525-1525 |
| ev.03_symbols_md.infra_terraform_modules_iam_main_tf.google_project_iam_member_embed_bq_read_session.l1526 | evidence/03_symbols.md | 1526-1526 |
| ev.03_symbols_md.infra_terraform_modules_iam_main_tf.google_project_iam_member_dataform_bq_job_user.l1527 | evidence/03_symbols.md | 1527-1527 |
| ev.03_symbols_md.infra_terraform_modules_iam_main_tf.google_project_iam_member_pipeline_bq_job_user.l1528 | evidence/03_symbols.md | 1528-1528 |
| ev.03_symbols_md.infra_terraform_modules_iam_main_tf.google_project_iam_member_pipeline_bq_read_session.l1529 | evidence/03_symbols.md | 1529-1529 |
| ev.03_symbols_md.infra_terraform_modules_iam_main_tf.google_project_iam_member_pipeline_aiplatform_user.l1530 | evidence/03_symbols.md | 1530-1530 |
| ev.03_symbols_md.infra_terraform_modules_iam_main_tf.google_project_iam_member_pipeline_trigger_aiplatform_user.l1531 | evidence/03_symbols.md | 1531-1531 |
| ev.03_symbols_md.infra_terraform_modules_iam_main_tf.google_project_iam_member_pipeline_trigger_eventarc_receiver.l1532 | evidence/03_symbols.md | 1532-1532 |
| ev.03_symbols_md.infra_terraform_modules_iam_main_tf.google_project_iam_member_pipeline_trigger_pubsub_subscriber.l1533 | evidence/03_symbols.md | 1533-1533 |
| ev.03_symbols_md.infra_terraform_modules_iam_main_tf.google_project_iam_member_pipeline_trigger_logging_writer.l1534 | evidence/03_symbols.md | 1534-1534 |
| ev.03_symbols_md.infra_terraform_modules_iam_main_tf.google_service_account_iam_member_pipeline_trigger_can_use_pipeline_sa.l1535 | evidence/03_symbols.md | 1535-1535 |
| ev.03_symbols_md.infra_terraform_modules_iam_main_tf.google_service_account_iam_member_composer_can_use_pipeline_sa.l1536 | evidence/03_symbols.md | 1536-1536 |
| ev.03_symbols_md.infra_terraform_modules_iam_main_tf.google_project_iam_member_endpoint_encoder_logging_writer.l1537 | evidence/03_symbols.md | 1537-1537 |
| ev.03_symbols_md.infra_terraform_modules_iam_main_tf.google_project_iam_member_endpoint_reranker_logging_writer.l1538 | evidence/03_symbols.md | 1538-1538 |
| ev.03_symbols_md.infra_terraform_modules_iam_main_tf.google_project_iam_member_endpoint_reranker_aiplatform_user.l1539 | evidence/03_symbols.md | 1539-1539 |
| ev.03_symbols_md.infra_terraform_modules_iam_main_tf.google_service_account_composer.l1540 | evidence/03_symbols.md | 1540-1540 |
| ev.03_symbols_md.infra_terraform_modules_iam_main_tf.google_project_iam_member_composer_worker.l1541 | evidence/03_symbols.md | 1541-1541 |
| ev.03_symbols_md.infra_terraform_modules_iam_main_tf.google_project_iam_member_composer_aiplatform_user.l1542 | evidence/03_symbols.md | 1542-1542 |
| ev.03_symbols_md.infra_terraform_modules_iam_main_tf.google_project_iam_member_composer_bq_job_user.l1543 | evidence/03_symbols.md | 1543-1543 |
| ev.03_symbols_md.infra_terraform_modules_iam_main_tf.google_project_iam_member_composer_bq_data_viewer.l1544 | evidence/03_symbols.md | 1544-1544 |
| ev.03_symbols_md.infra_terraform_modules_iam_main_tf.google_project_iam_member_composer_run_invoker.l1545 | evidence/03_symbols.md | 1545-1545 |
| ev.03_symbols_md.infra_terraform_modules_iam_main_tf.google_project_iam_member_composer_artifactregistry_reader.l1546 | evidence/03_symbols.md | 1546-1546 |
| ev.03_symbols_md.infra_terraform_modules_iam_main_tf.google_project_iam_member_composer_storage_object_viewer.l1547 | evidence/03_symbols.md | 1547-1547 |
| ev.03_symbols_md.infra_terraform_modules_iam_main_tf.google_project_iam_member_github_deployer_composer_admin.l1548 | evidence/03_symbols.md | 1548-1548 |
| ev.03_symbols_md.infra_terraform_modules_kserve_main_tf.kubernetes_namespace_search.l1552 | evidence/03_symbols.md | 1552-1552 |
| ev.03_symbols_md.infra_terraform_modules_kserve_main_tf.kubernetes_namespace_inference.l1553 | evidence/03_symbols.md | 1553-1553 |
| ev.03_symbols_md.infra_terraform_modules_kserve_main_tf.kubernetes_service_account_api.l1554 | evidence/03_symbols.md | 1554-1554 |
| ev.03_symbols_md.infra_terraform_modules_kserve_main_tf.kubernetes_service_account_encoder.l1555 | evidence/03_symbols.md | 1555-1555 |
| ev.03_symbols_md.infra_terraform_modules_kserve_main_tf.kubernetes_service_account_reranker.l1556 | evidence/03_symbols.md | 1556-1556 |
| ev.03_symbols_md.infra_terraform_modules_kserve_main_tf.helm_release_cert_manager.l1557 | evidence/03_symbols.md | 1557-1557 |
| ev.03_symbols_md.infra_terraform_modules_kserve_main_tf.helm_release_external_secrets.l1558 | evidence/03_symbols.md | 1558-1558 |
| ev.03_symbols_md.infra_terraform_modules_kserve_main_tf.helm_release_kserve_crd.l1559 | evidence/03_symbols.md | 1559-1559 |
| ev.03_symbols_md.infra_terraform_modules_kserve_main_tf.helm_release_kserve.l1560 | evidence/03_symbols.md | 1560-1560 |
| ev.03_symbols_md.infra_terraform_modules_kserve_tls_dev_tf.tls_private_key_search_api_dev.l1564 | evidence/03_symbols.md | 1564-1564 |
| ev.03_symbols_md.infra_terraform_modules_kserve_tls_dev_tf.tls_self_signed_cert_search_api_dev.l1565 | evidence/03_symbols.md | 1565-1565 |
| ev.03_symbols_md.infra_terraform_modules_kserve_tls_dev_tf.kubernetes_secret_search_api_tls.l1566 | evidence/03_symbols.md | 1566-1566 |
| ev.03_symbols_md.infra_terraform_modules_messaging_main_tf.google_pubsub_topic_ranking_log.l1570 | evidence/03_symbols.md | 1570-1570 |
| ev.03_symbols_md.infra_terraform_modules_messaging_main_tf.google_pubsub_topic_search_feedback.l1571 | evidence/03_symbols.md | 1571-1571 |
| ev.03_symbols_md.infra_terraform_modules_messaging_main_tf.google_pubsub_topic_retrain_trigger.l1572 | evidence/03_symbols.md | 1572-1572 |
| ev.03_symbols_md.infra_terraform_modules_messaging_main_tf.google_pubsub_topic_search_events.l1573 | evidence/03_symbols.md | 1573-1573 |
| ev.03_symbols_md.infra_terraform_modules_messaging_main_tf.google_pubsub_topic_search_impressions.l1574 | evidence/03_symbols.md | 1574-1574 |
| ev.03_symbols_md.infra_terraform_modules_messaging_main_tf.google_pubsub_topic_user_actions.l1575 | evidence/03_symbols.md | 1575-1575 |
| ev.03_symbols_md.infra_terraform_modules_messaging_main_tf.google_pubsub_topic_iam_member_api_publish_ranking_log.l1576 | evidence/03_symbols.md | 1576-1576 |
| ev.03_symbols_md.infra_terraform_modules_messaging_main_tf.google_pubsub_topic_iam_member_api_publish_feedback.l1577 | evidence/03_symbols.md | 1577-1577 |
| ev.03_symbols_md.infra_terraform_modules_messaging_main_tf.google_pubsub_topic_iam_member_api_publish_retrain.l1578 | evidence/03_symbols.md | 1578-1578 |
| ev.03_symbols_md.infra_terraform_modules_messaging_main_tf.google_pubsub_topic_iam_member_scheduler_publish_retrain.l1579 | evidence/03_symbols.md | 1579-1579 |
| ev.03_symbols_md.infra_terraform_modules_messaging_main_tf.google_pubsub_topic_iam_member_api_publish_search_events.l1580 | evidence/03_symbols.md | 1580-1580 |
| ev.03_symbols_md.infra_terraform_modules_messaging_main_tf.google_pubsub_topic_iam_member_api_publish_search_impressions.l1581 | evidence/03_symbols.md | 1581-1581 |
| ev.03_symbols_md.infra_terraform_modules_messaging_main_tf.google_pubsub_topic_iam_member_api_publish_user_actions.l1582 | evidence/03_symbols.md | 1582-1582 |
| ev.03_symbols_md.infra_terraform_modules_messaging_main_tf.google_pubsub_subscription_ranking_log_to_bq.l1583 | evidence/03_symbols.md | 1583-1583 |
| ev.03_symbols_md.infra_terraform_modules_messaging_main_tf.google_pubsub_subscription_search_feedback_to_bq.l1584 | evidence/03_symbols.md | 1584-1584 |
| ev.03_symbols_md.infra_terraform_modules_messaging_main_tf.google_pubsub_subscription_search_events_to_bq.l1585 | evidence/03_symbols.md | 1585-1585 |
| ev.03_symbols_md.infra_terraform_modules_messaging_main_tf.google_pubsub_subscription_search_impressions_to_bq.l1586 | evidence/03_symbols.md | 1586-1586 |
| ev.03_symbols_md.infra_terraform_modules_messaging_main_tf.google_pubsub_subscription_user_actions_to_bq.l1587 | evidence/03_symbols.md | 1587-1587 |
| ev.03_symbols_md.infra_terraform_modules_messaging_main_tf.google_project_iam_member_pubsub_bq_writer.l1588 | evidence/03_symbols.md | 1588-1588 |
| ev.03_symbols_md.infra_terraform_modules_messaging_main_tf.google_project_iam_member_pubsub_bq_metadata_viewer.l1589 | evidence/03_symbols.md | 1589-1589 |
| ev.03_symbols_md.infra_terraform_modules_messaging_main_tf.google_cloud_scheduler_job_check_retrain_daily.l1590 | evidence/03_symbols.md | 1590-1590 |
| ev.03_symbols_md.infra_terraform_modules_monitoring_main_tf.google_logging_metric_api_error_rate.l1594 | evidence/03_symbols.md | 1594-1594 |
| ev.03_symbols_md.infra_terraform_modules_monitoring_main_tf.google_logging_metric_api_p95_latency.l1595 | evidence/03_symbols.md | 1595-1595 |
| ev.03_symbols_md.infra_terraform_modules_monitoring_main_tf.google_monitoring_notification_channel_email.l1596 | evidence/03_symbols.md | 1596-1596 |
| ev.03_symbols_md.infra_terraform_modules_monitoring_main_tf.time_sleep_wait_for_log_metric_indexing.l1597 | evidence/03_symbols.md | 1597-1597 |
| ev.03_symbols_md.infra_terraform_modules_monitoring_main_tf.google_monitoring_alert_policy_api_error_rate.l1598 | evidence/03_symbols.md | 1598-1598 |
| ev.03_symbols_md.infra_terraform_modules_monitoring_main_tf.google_monitoring_alert_policy_api_p95_latency.l1599 | evidence/03_symbols.md | 1599-1599 |
| ev.03_symbols_md.infra_terraform_modules_monitoring_main_tf.google_bigquery_data_transfer_config_property_feature_skew_check.l1600 | evidence/03_symbols.md | 1600-1600 |
| ev.03_symbols_md.infra_terraform_modules_monitoring_main_tf.google_bigquery_data_transfer_config_model_output_drift_check.l1601 | evidence/03_symbols.md | 1601-1601 |
| ev.03_symbols_md.infra_terraform_modules_redis_synonym_main_tf.google_redis_instance_synonym.l1605 | evidence/03_symbols.md | 1605-1605 |
| ev.03_symbols_md.infra_terraform_modules_redis_synonym_main_tf.google_secret_manager_secret_redis_auth.l1606 | evidence/03_symbols.md | 1606-1606 |
| ev.03_symbols_md.infra_terraform_modules_redis_synonym_main_tf.google_secret_manager_secret_version_redis_auth.l1607 | evidence/03_symbols.md | 1607-1607 |
| ev.03_symbols_md.infra_terraform_modules_slo_main_tf.namespace___var_k8s_namespace.l1611 | evidence/03_symbols.md | 1611-1611 |
| ev.03_symbols_md.infra_terraform_modules_slo_main_tf.service_name___var_service_name.l1612 | evidence/03_symbols.md | 1612-1612 |
| ev.03_symbols_md.infra_terraform_modules_slo_main_tf.namespace___var_k8s_namespace.l1613 | evidence/03_symbols.md | 1613-1613 |
| ev.03_symbols_md.infra_terraform_modules_slo_main_tf.service_name___var_service_name.l1614 | evidence/03_symbols.md | 1614-1614 |
| ev.03_symbols_md.infra_terraform_modules_slo_main_tf.namespace___var_k8s_namespace.l1615 | evidence/03_symbols.md | 1615-1615 |
| ev.03_symbols_md.infra_terraform_modules_slo_main_tf.service_name___var_service_name.l1616 | evidence/03_symbols.md | 1616-1616 |
| ev.03_symbols_md.infra_terraform_modules_slo_main_tf.google_monitoring_custom_service_search_api.l1617 | evidence/03_symbols.md | 1617-1617 |
| ev.03_symbols_md.infra_terraform_modules_slo_main_tf.google_monitoring_slo_availability.l1618 | evidence/03_symbols.md | 1618-1618 |
| ev.03_symbols_md.infra_terraform_modules_slo_main_tf.google_monitoring_slo_latency.l1619 | evidence/03_symbols.md | 1619-1619 |
| ev.03_symbols_md.infra_terraform_modules_slo_main_tf.google_monitoring_alert_policy_availability_fast_burn.l1620 | evidence/03_symbols.md | 1620-1620 |
| ev.03_symbols_md.infra_terraform_modules_slo_main_tf.google_monitoring_alert_policy_availability_slow_burn.l1621 | evidence/03_symbols.md | 1621-1621 |
| ev.03_symbols_md.infra_terraform_modules_slo_main_tf.google_monitoring_alert_policy_latency_fast_burn.l1622 | evidence/03_symbols.md | 1622-1622 |
| ev.03_symbols_md.infra_terraform_modules_slo_main_tf.google_monitoring_alert_policy_latency_slow_burn.l1623 | evidence/03_symbols.md | 1623-1623 |
| ev.03_symbols_md.infra_terraform_modules_streaming_main_tf.google_service_account_dataflow.l1627 | evidence/03_symbols.md | 1627-1627 |
| ev.03_symbols_md.infra_terraform_modules_streaming_main_tf.google_project_iam_member_dataflow_pubsub_subscriber.l1628 | evidence/03_symbols.md | 1628-1628 |
| ev.03_symbols_md.infra_terraform_modules_streaming_main_tf.google_project_iam_member_dataflow_worker.l1629 | evidence/03_symbols.md | 1629-1629 |
| ev.03_symbols_md.infra_terraform_modules_streaming_main_tf.google_project_iam_member_dataflow_storage.l1630 | evidence/03_symbols.md | 1630-1630 |
| ev.03_symbols_md.infra_terraform_modules_streaming_main_tf.google_project_iam_member_dataflow_bq_data_editor.l1631 | evidence/03_symbols.md | 1631-1631 |
| ev.03_symbols_md.infra_terraform_modules_streaming_main_tf.google_project_iam_member_dataflow_bq_jobs.l1632 | evidence/03_symbols.md | 1632-1632 |
| ev.03_symbols_md.infra_terraform_modules_streaming_main_tf.google_dataflow_flex_template_job_ranking_log_hourly_ctr.l1633 | evidence/03_symbols.md | 1633-1633 |
| ev.03_symbols_md.infra_terraform_modules_vector_search_main_tf.google_vertex_ai_index_property_embeddings.l1637 | evidence/03_symbols.md | 1637-1637 |
| ev.03_symbols_md.infra_terraform_modules_vector_search_main_tf.google_vertex_ai_index_endpoint_property_embeddings.l1638 | evidence/03_symbols.md | 1638-1638 |
| ev.03_symbols_md.infra_terraform_modules_vector_search_main_tf.google_vertex_ai_index_endpoint_deployed_index_property_embeddings.l1639 | evidence/03_symbols.md | 1639-1639 |
| ev.03_symbols_md.infra_terraform_modules_vertex_main_tf.google_pubsub_topic_model_monitoring_alerts.l1643 | evidence/03_symbols.md | 1643-1643 |
| ev.03_symbols_md.infra_terraform_modules_vertex_main_tf.google_bigquery_dataset_iam_member_pubsub_mlops_editor.l1644 | evidence/03_symbols.md | 1644-1644 |
| ev.03_symbols_md.infra_terraform_modules_vertex_main_tf.google_bigquery_dataset_iam_member_pubsub_mlops_metadata_viewer.l1645 | evidence/03_symbols.md | 1645-1645 |
| ev.03_symbols_md.infra_terraform_modules_vertex_main_tf.google_pubsub_subscription_monitoring_alerts_to_bq.l1646 | evidence/03_symbols.md | 1646-1646 |
| ev.03_symbols_md.infra_terraform_modules_vertex_main_tf.google_storage_bucket_object_pipeline_trigger_zip.l1647 | evidence/03_symbols.md | 1647-1647 |
| ev.03_symbols_md.infra_terraform_modules_vertex_main_tf.google_cloudfunctions2_function_pipeline_trigger.l1648 | evidence/03_symbols.md | 1648-1648 |
| ev.03_symbols_md.infra_terraform_modules_vertex_main_tf.google_cloud_run_service_iam_member_pipeline_trigger_invoker.l1649 | evidence/03_symbols.md | 1649-1649 |
| ev.03_symbols_md.infra_terraform_modules_vertex_main_tf.google_eventarc_trigger_retrain_to_pipeline.l1650 | evidence/03_symbols.md | 1650-1650 |
| ev.03_symbols_md.infra_terraform_modules_vertex_main_tf.google_eventarc_trigger_monitoring_to_pipeline.l1651 | evidence/03_symbols.md | 1651-1651 |
| ev.03_symbols_md.infra_terraform_modules_vertex_main_tf.google_vertex_ai_feature_group_property_features.l1652 | evidence/03_symbols.md | 1652-1652 |
| ev.03_symbols_md.infra_terraform_modules_vertex_main_tf.google_vertex_ai_feature_group_feature_property_features.l1653 | evidence/03_symbols.md | 1653-1653 |
| ev.03_symbols_md.infra_terraform_modules_vertex_main_tf.google_vertex_ai_feature_online_store_property_features.l1654 | evidence/03_symbols.md | 1654-1654 |
| ev.03_symbols_md.infra_terraform_modules_vertex_main_tf.google_vertex_ai_feature_online_store_featureview_property_features.l1655 | evidence/03_symbols.md | 1655-1655 |
| ev.03_symbols_md.infra_terraform_modules_vertex_main_tf.google_vertex_ai_endpoint_encoder.l1656 | evidence/03_symbols.md | 1656-1656 |
| ev.03_symbols_md.infra_terraform_modules_vertex_main_tf.google_vertex_ai_endpoint_reranker.l1657 | evidence/03_symbols.md | 1657-1657 |
| ev.03_symbols_md.infra_terraform_modules_vertex_main_tf.google_storage_bucket_iam_member_endpoint_encoder_models_reader.l1658 | evidence/03_symbols.md | 1658-1658 |
| ev.03_symbols_md.infra_terraform_modules_vertex_main_tf.google_storage_bucket_iam_member_endpoint_reranker_models_reader.l1659 | evidence/03_symbols.md | 1659-1659 |
| ev.03_symbols_md.ml_common_config_base_py.baseappsettings.l1663 | evidence/03_symbols.md | 1663-1663 |
| ev.03_symbols_md.ml_common_config_base_py.settings_customise_sources.l1664 | evidence/03_symbols.md | 1664-1664 |
| ev.03_symbols_md.ml_common_config_embedding_py.embedsettings.l1668 | evidence/03_symbols.md | 1668-1668 |
| ev.03_symbols_md.ml_common_config_training_py.trainsettings.l1672 | evidence/03_symbols.md | 1672-1672 |
| ev.03_symbols_md.ml_common_logging_structured_logging_py.cloudloggingjsonformatter.l1676 | evidence/03_symbols.md | 1676-1676 |
| ev.03_symbols_md.ml_common_logging_structured_logging_py.format.l1677 | evidence/03_symbols.md | 1677-1677 |
| ev.03_symbols_md.ml_common_logging_structured_logging_py.configure_logging.l1678 | evidence/03_symbols.md | 1678-1678 |
| ev.03_symbols_md.ml_common_logging_structured_logging_py.get_logger.l1679 | evidence/03_symbols.md | 1679-1679 |
| ev.03_symbols_md.ml_common_utils_run_id_py.generate_run_id.l1683 | evidence/03_symbols.md | 1683-1683 |
| ev.03_symbols_md.ml_data_datasets_embedding_batch_py.logger.l1687 | evidence/03_symbols.md | 1687-1687 |
| ev.03_symbols_md.ml_data_datasets_embedding_batch_py.info.l1688 | evidence/03_symbols.md | 1688-1688 |
| ev.03_symbols_md.ml_data_datasets_embedding_batch_py.encoder.l1689 | evidence/03_symbols.md | 1689-1689 |
| ev.03_symbols_md.ml_data_datasets_embedding_batch_py.encode_passages.l1690 | evidence/03_symbols.md | 1690-1690 |
| ev.03_symbols_md.ml_data_datasets_embedding_batch_py.text_for_embedding.l1691 | evidence/03_symbols.md | 1691-1691 |
| ev.03_symbols_md.ml_data_datasets_embedding_batch_py.hash.l1692 | evidence/03_symbols.md | 1692-1692 |
| ev.03_symbols_md.ml_data_datasets_embedding_batch_py.run_embedding_batch.l1693 | evidence/03_symbols.md | 1693-1693 |
| ev.03_symbols_md.ml_data_feature_engineering_ranker_features_py.build_ranker_features.l1697 | evidence/03_symbols.md | 1697-1697 |
| ev.03_symbols_md.ml_data_loaders_embedding_store_py.propertytext.l1701 | evidence/03_symbols.md | 1701-1701 |
| ev.03_symbols_md.ml_data_loaders_embedding_store_py.embeddingrow.l1702 | evidence/03_symbols.md | 1702-1702 |
| ev.03_symbols_md.ml_data_loaders_embedding_store_py.propertytextrepository.l1703 | evidence/03_symbols.md | 1703-1703 |
| ev.03_symbols_md.ml_data_loaders_embedding_store_py.fetch_all.l1704 | evidence/03_symbols.md | 1704-1704 |
| ev.03_symbols_md.ml_data_loaders_embedding_store_py.embeddingstore.l1705 | evidence/03_symbols.md | 1705-1705 |
| ev.03_symbols_md.ml_data_loaders_embedding_store_py.existing_hashes.l1706 | evidence/03_symbols.md | 1706-1706 |
| ev.03_symbols_md.ml_data_loaders_embedding_store_py.upsert.l1707 | evidence/03_symbols.md | 1707-1707 |
| ev.03_symbols_md.ml_data_loaders_embedding_store_py.bigquerypropertytextrepository.l1708 | evidence/03_symbols.md | 1708-1708 |
| ev.03_symbols_md.ml_data_loaders_embedding_store_py.init.l1709 | evidence/03_symbols.md | 1709-1709 |
| ev.03_symbols_md.ml_data_loaders_embedding_store_py.fetch_all.l1710 | evidence/03_symbols.md | 1710-1710 |
| ev.03_symbols_md.ml_data_loaders_embedding_store_py.bigqueryembeddingstore.l1711 | evidence/03_symbols.md | 1711-1711 |
| ev.03_symbols_md.ml_data_loaders_embedding_store_py.init.l1712 | evidence/03_symbols.md | 1712-1712 |
| ev.03_symbols_md.ml_data_loaders_embedding_store_py.existing_hashes.l1713 | evidence/03_symbols.md | 1713-1713 |
| ev.03_symbols_md.ml_data_loaders_embedding_store_py.upsert.l1714 | evidence/03_symbols.md | 1714-1714 |
| ev.03_symbols_md.ml_data_loaders_ranker_repository_py.rankertrainingrepository.l1718 | evidence/03_symbols.md | 1718-1718 |
| ev.03_symbols_md.ml_data_loaders_ranker_repository_py.fetch_training_rows.l1719 | evidence/03_symbols.md | 1719-1719 |
| ev.03_symbols_md.ml_data_loaders_ranker_repository_py.save_run.l1720 | evidence/03_symbols.md | 1720-1720 |
| ev.03_symbols_md.ml_data_loaders_ranker_repository_py.latest_model_path.l1721 | evidence/03_symbols.md | 1721-1721 |
| ev.03_symbols_md.ml_data_loaders_ranker_repository_py.bigqueryrankerrepository.l1722 | evidence/03_symbols.md | 1722-1722 |
| ev.03_symbols_md.ml_data_loaders_ranker_repository_py.init.l1723 | evidence/03_symbols.md | 1723-1723 |
| ev.03_symbols_md.ml_data_loaders_ranker_repository_py.fetch_training_rows.l1724 | evidence/03_symbols.md | 1724-1724 |
| ev.03_symbols_md.ml_data_loaders_ranker_repository_py.save_run.l1725 | evidence/03_symbols.md | 1725-1725 |
| ev.03_symbols_md.ml_data_loaders_ranker_repository_py.log_vertex_experiment.l1726 | evidence/03_symbols.md | 1726-1726 |
| ev.03_symbols_md.ml_data_loaders_ranker_repository_py.latest_model_path.l1727 | evidence/03_symbols.md | 1727-1727 |
| ev.03_symbols_md.ml_data_loaders_ranker_repository_py.create_rank_repository.l1728 | evidence/03_symbols.md | 1728-1728 |
| ev.03_symbols_md.ml_evaluation_metrics_label_gain_py.assign_label.l1732 | evidence/03_symbols.md | 1732-1732 |
| ev.03_symbols_md.ml_evaluation_metrics_ranking_py.dcg.l1736 | evidence/03_symbols.md | 1736-1736 |
| ev.03_symbols_md.ml_evaluation_metrics_ranking_py.ndcg_at_k.l1737 | evidence/03_symbols.md | 1737-1737 |
| ev.03_symbols_md.ml_evaluation_metrics_ranking_py.mean_average_precision.l1738 | evidence/03_symbols.md | 1738-1738 |
| ev.03_symbols_md.ml_evaluation_metrics_ranking_py.recall_at_k.l1739 | evidence/03_symbols.md | 1739-1739 |
| ev.03_symbols_md.ml_evaluation_metrics_ranking_py.iter_groups.l1740 | evidence/03_symbols.md | 1740-1740 |
| ev.03_symbols_md.ml_evaluation_metrics_ranking_py.evaluate.l1741 | evidence/03_symbols.md | 1741-1741 |
| ev.03_symbols_md.ml_labeling_policy_py.synthetic_label_source.l1745 | evidence/03_symbols.md | 1745-1745 |
| ev.03_symbols_md.ml_labeling_policy_py.compute_label.l1746 | evidence/03_symbols.md | 1746-1746 |
| ev.03_symbols_md.ml_registry_adapters_vertex_model_registry_py.vertexmodelregistryadapter.l1750 | evidence/03_symbols.md | 1750-1750 |
| ev.03_symbols_md.ml_registry_adapters_vertex_model_registry_py.init.l1751 | evidence/03_symbols.md | 1751-1751 |
| ev.03_symbols_md.ml_registry_adapters_vertex_model_registry_py.init.l1752 | evidence/03_symbols.md | 1752-1752 |
| ev.03_symbols_md.ml_registry_adapters_vertex_model_registry_py.register.l1753 | evidence/03_symbols.md | 1753-1753 |
| ev.03_symbols_md.ml_registry_adapters_vertex_model_registry_py.promote.l1754 | evidence/03_symbols.md | 1754-1754 |
| ev.03_symbols_md.ml_registry_adapters_vertex_model_registry_py.resolve_alias.l1755 | evidence/03_symbols.md | 1755-1755 |
| ev.03_symbols_md.ml_registry_artifact_store_py.gcsprefix.l1759 | evidence/03_symbols.md | 1759-1759 |
| ev.03_symbols_md.ml_registry_artifact_store_py.parse.l1760 | evidence/03_symbols.md | 1760-1760 |
| ev.03_symbols_md.ml_registry_artifact_store_py.child.l1761 | evidence/03_symbols.md | 1761-1761 |
| ev.03_symbols_md.ml_registry_artifact_store_py.uri.l1762 | evidence/03_symbols.md | 1762-1762 |
| ev.03_symbols_md.ml_registry_artifact_store_py.model_prefix.l1763 | evidence/03_symbols.md | 1763-1763 |
| ev.03_symbols_md.ml_registry_artifact_store_py.upload_directory.l1764 | evidence/03_symbols.md | 1764-1764 |
| ev.03_symbols_md.ml_registry_artifact_store_py.download_file.l1765 | evidence/03_symbols.md | 1765-1765 |
| ev.03_symbols_md.ml_registry_artifact_store_py.artifactuploader.l1766 | evidence/03_symbols.md | 1766-1766 |
| ev.03_symbols_md.ml_registry_artifact_store_py.upload.l1767 | evidence/03_symbols.md | 1767-1767 |
| ev.03_symbols_md.ml_registry_artifact_store_py.gcsartifactuploader.l1768 | evidence/03_symbols.md | 1768-1768 |
| ev.03_symbols_md.ml_registry_artifact_store_py.init.l1769 | evidence/03_symbols.md | 1769-1769 |
| ev.03_symbols_md.ml_registry_artifact_store_py.upload.l1770 | evidence/03_symbols.md | 1770-1770 |
| ev.03_symbols_md.ml_registry_metadata_store_py.trainingrun.l1774 | evidence/03_symbols.md | 1774-1774 |
| ev.03_symbols_md.ml_registry_metadata_store_py.metadatastore.l1775 | evidence/03_symbols.md | 1775-1775 |
| ev.03_symbols_md.ml_registry_metadata_store_py.init.l1776 | evidence/03_symbols.md | 1776-1776 |
| ev.03_symbols_md.ml_registry_metadata_store_py.recent_runs.l1777 | evidence/03_symbols.md | 1777-1777 |
| ev.03_symbols_md.ml_registry_model_registry_py.registeredmodel.l1781 | evidence/03_symbols.md | 1781-1781 |
| ev.03_symbols_md.ml_registry_model_registry_py.modelregistry.l1782 | evidence/03_symbols.md | 1782-1782 |
| ev.03_symbols_md.ml_registry_model_registry_py.init.l1783 | evidence/03_symbols.md | 1783-1783 |
| ev.03_symbols_md.ml_registry_model_registry_py.promote.l1784 | evidence/03_symbols.md | 1784-1784 |
| ev.03_symbols_md.ml_registry_ports_model_registry_py.registeredmodelref.l1788 | evidence/03_symbols.md | 1788-1788 |
| ev.03_symbols_md.ml_registry_ports_model_registry_py.modelregistryport.l1789 | evidence/03_symbols.md | 1789-1789 |
| ev.03_symbols_md.ml_registry_ports_model_registry_py.register.l1790 | evidence/03_symbols.md | 1790-1790 |
| ev.03_symbols_md.ml_registry_ports_model_registry_py.promote.l1791 | evidence/03_symbols.md | 1791-1791 |
| ev.03_symbols_md.ml_registry_ports_model_registry_py.resolve_alias.l1792 | evidence/03_symbols.md | 1792-1792 |
| ev.03_symbols_md.ml_serving_adapters_kserve_predictor_py.kservepredictoradapter.l1796 | evidence/03_symbols.md | 1796-1796 |
| ev.03_symbols_md.ml_serving_adapters_kserve_predictor_py.init.l1797 | evidence/03_symbols.md | 1797-1797 |
| ev.03_symbols_md.ml_serving_adapters_kserve_predictor_py.predict.l1798 | evidence/03_symbols.md | 1798-1798 |
| ev.03_symbols_md.ml_serving_adapters_kserve_predictor_py.predict_with_explain.l1799 | evidence/03_symbols.md | 1799-1799 |
| ev.03_symbols_md.ml_serving_calibration_py.identity_calibrator.l1803 | evidence/03_symbols.md | 1803-1803 |
| ev.03_symbols_md.ml_serving_encoder_py.e5encoder.l1807 | evidence/03_symbols.md | 1807-1807 |
| ev.03_symbols_md.ml_serving_encoder_py.load.l1808 | evidence/03_symbols.md | 1808-1808 |
| ev.03_symbols_md.ml_serving_encoder_py.encode.l1809 | evidence/03_symbols.md | 1809-1809 |
| ev.03_symbols_md.ml_serving_encoder_py.encode_queries.l1810 | evidence/03_symbols.md | 1810-1810 |
| ev.03_symbols_md.ml_serving_encoder_py.encode_passages.l1811 | evidence/03_symbols.md | 1811-1811 |
| ev.03_symbols_md.ml_serving_encoder_py.encode_query.l1812 | evidence/03_symbols.md | 1812-1812 |
| ev.03_symbols_md.ml_serving_encoder_py.encode_passage.l1813 | evidence/03_symbols.md | 1813-1813 |
| ev.03_symbols_md.ml_serving_encoder_py.encoderinstance.l1814 | evidence/03_symbols.md | 1814-1814 |
| ev.03_symbols_md.ml_serving_encoder_py.encoderrequest.l1815 | evidence/03_symbols.md | 1815-1815 |
| ev.03_symbols_md.ml_serving_encoder_py.encoderresponse.l1816 | evidence/03_symbols.md | 1816-1816 |
| ev.03_symbols_md.ml_serving_encoder_py.download_artifact_dir.l1817 | evidence/03_symbols.md | 1817-1817 |
| ev.03_symbols_md.ml_serving_encoder_py.load_encoder.l1818 | evidence/03_symbols.md | 1818-1818 |
| ev.03_symbols_md.ml_serving_encoder_py.normalize_instance.l1819 | evidence/03_symbols.md | 1819-1819 |
| ev.03_symbols_md.ml_serving_encoder_py.lifespan.l1820 | evidence/03_symbols.md | 1820-1820 |
| ev.03_symbols_md.ml_serving_encoder_py.health.l1821 | evidence/03_symbols.md | 1821-1821 |
| ev.03_symbols_md.ml_serving_encoder_py.predict.l1822 | evidence/03_symbols.md | 1822-1822 |
| ev.03_symbols_md.ml_serving_encoder_py.main.l1823 | evidence/03_symbols.md | 1823-1823 |
| ev.03_symbols_md.ml_serving_ports_predictor_service_py.predictorservice.l1827 | evidence/03_symbols.md | 1827-1827 |
| ev.03_symbols_md.ml_serving_ports_predictor_service_py.predict.l1828 | evidence/03_symbols.md | 1828-1828 |
| ev.03_symbols_md.ml_serving_ports_predictor_service_py.predict_with_explain.l1829 | evidence/03_symbols.md | 1829-1829 |
| ev.03_symbols_md.ml_serving_predictor_py.predictor.l1833 | evidence/03_symbols.md | 1833-1833 |
| ev.03_symbols_md.ml_serving_predictor_py.predict.l1834 | evidence/03_symbols.md | 1834-1834 |
| ev.03_symbols_md.ml_serving_predictor_py.remotepredictorconfig.l1835 | evidence/03_symbols.md | 1835-1835 |
| ev.03_symbols_md.ml_serving_predictor_py.endpoint_name.l1836 | evidence/03_symbols.md | 1836-1836 |
| ev.03_symbols_md.ml_serving_reranker_py.rerankerparameters.l1840 | evidence/03_symbols.md | 1840-1840 |
| ev.03_symbols_md.ml_serving_reranker_py.rerankerrequest.l1841 | evidence/03_symbols.md | 1841-1841 |
| ev.03_symbols_md.ml_serving_reranker_py.rerankerresponse.l1842 | evidence/03_symbols.md | 1842-1842 |
| ev.03_symbols_md.ml_serving_reranker_py.explainrequest.l1843 | evidence/03_symbols.md | 1843-1843 |
| ev.03_symbols_md.ml_serving_reranker_py.explainresponse.l1844 | evidence/03_symbols.md | 1844-1844 |
| ev.03_symbols_md.ml_serving_reranker_py.load_booster.l1845 | evidence/03_symbols.md | 1845-1845 |
| ev.03_symbols_md.ml_serving_reranker_py.pred_contrib.l1846 | evidence/03_symbols.md | 1846-1846 |
| ev.03_symbols_md.ml_serving_reranker_py.lifespan.l1847 | evidence/03_symbols.md | 1847-1847 |
| ev.03_symbols_md.ml_serving_reranker_py.health.l1848 | evidence/03_symbols.md | 1848-1848 |
| ev.03_symbols_md.ml_serving_reranker_py.predict.l1849 | evidence/03_symbols.md | 1849-1849 |
| ev.03_symbols_md.ml_serving_reranker_py.explain.l1850 | evidence/03_symbols.md | 1850-1850 |
| ev.03_symbols_md.ml_serving_reranker_py.main.l1851 | evidence/03_symbols.md | 1851-1851 |
| ev.03_symbols_md.ml_streaming_adapters_dataflow_processor_py.dataflowstreamprocessor.l1855 | evidence/03_symbols.md | 1855-1855 |
| ev.03_symbols_md.ml_streaming_adapters_dataflow_processor_py.run.l1856 | evidence/03_symbols.md | 1856-1856 |
| ev.03_symbols_md.ml_streaming_container_dockerfile.gcr_io_dataflow_templates_base_python3_template_launcher_base_latest.l1860 | evidence/03_symbols.md | 1860-1860 |
| ev.03_symbols_md.ml_streaming_pipeline_py.parse_event.l1864 | evidence/03_symbols.md | 1864-1864 |
| ev.03_symbols_md.ml_streaming_pipeline_py.event_timestamp_seconds.l1865 | evidence/03_symbols.md | 1865-1865 |
| ev.03_symbols_md.ml_streaming_pipeline_py.to_kv.l1866 | evidence/03_symbols.md | 1866-1866 |
| ev.03_symbols_md.ml_streaming_pipeline_py.sum_pair.l1867 | evidence/03_symbols.md | 1867-1867 |
| ev.03_symbols_md.ml_streaming_pipeline_py.format_output_row.l1868 | evidence/03_symbols.md | 1868-1868 |
| ev.03_symbols_md.ml_streaming_pipeline_py.run.l1869 | evidence/03_symbols.md | 1869-1869 |
| ev.03_symbols_md.ml_streaming_pipeline_py.attachwindowtimestamps.l1870 | evidence/03_symbols.md | 1870-1870 |
| ev.03_symbols_md.ml_streaming_pipeline_py.process.l1871 | evidence/03_symbols.md | 1871-1871 |
| ev.03_symbols_md.ml_streaming_pipeline_py.combinecountsfn.l1872 | evidence/03_symbols.md | 1872-1872 |
| ev.03_symbols_md.ml_streaming_pipeline_py.create_accumulator.l1873 | evidence/03_symbols.md | 1873-1873 |
| ev.03_symbols_md.ml_streaming_pipeline_py.add_input.l1874 | evidence/03_symbols.md | 1874-1874 |
| ev.03_symbols_md.ml_streaming_pipeline_py.merge_accumulators.l1875 | evidence/03_symbols.md | 1875-1875 |
| ev.03_symbols_md.ml_streaming_pipeline_py.extract_output.l1876 | evidence/03_symbols.md | 1876-1876 |
| ev.03_symbols_md.ml_streaming_ports_stream_processor_py.streamconfig.l1880 | evidence/03_symbols.md | 1880-1880 |
| ev.03_symbols_md.ml_streaming_ports_stream_processor_py.streamprocessor.l1881 | evidence/03_symbols.md | 1881-1881 |
| ev.03_symbols_md.ml_streaming_ports_stream_processor_py.run.l1882 | evidence/03_symbols.md | 1882-1882 |
| ev.03_symbols_md.ml_training_adapters_lightgbm_trainer_py.lightgbmmodel.l1886 | evidence/03_symbols.md | 1886-1886 |
| ev.03_symbols_md.ml_training_adapters_lightgbm_trainer_py.init.l1887 | evidence/03_symbols.md | 1887-1887 |
| ev.03_symbols_md.ml_training_adapters_lightgbm_trainer_py.predict.l1888 | evidence/03_symbols.md | 1888-1888 |
| ev.03_symbols_md.ml_training_adapters_lightgbm_trainer_py.predict_with_explain.l1889 | evidence/03_symbols.md | 1889-1889 |
| ev.03_symbols_md.ml_training_adapters_lightgbm_trainer_py.save.l1890 | evidence/03_symbols.md | 1890-1890 |
| ev.03_symbols_md.ml_training_adapters_lightgbm_trainer_py.lightgbmrankertrainer.l1891 | evidence/03_symbols.md | 1891-1891 |
| ev.03_symbols_md.ml_training_adapters_lightgbm_trainer_py.init.l1892 | evidence/03_symbols.md | 1892-1892 |
| ev.03_symbols_md.ml_training_adapters_lightgbm_trainer_py.train.l1893 | evidence/03_symbols.md | 1893-1893 |
| ev.03_symbols_md.ml_training_experiments_adapters_null_tracker_py.nullexperimenttracker.l1897 | evidence/03_symbols.md | 1897-1897 |
| ev.03_symbols_md.ml_training_experiments_adapters_null_tracker_py.enter.l1898 | evidence/03_symbols.md | 1898-1898 |
| ev.03_symbols_md.ml_training_experiments_adapters_null_tracker_py.exit.l1899 | evidence/03_symbols.md | 1899-1899 |
| ev.03_symbols_md.ml_training_experiments_adapters_null_tracker_py.log_metrics.l1900 | evidence/03_symbols.md | 1900-1900 |
| ev.03_symbols_md.ml_training_experiments_adapters_null_tracker_py.log_params.l1901 | evidence/03_symbols.md | 1901-1901 |
| ev.03_symbols_md.ml_training_experiments_adapters_vertex_experiments_tracker_py.vertexexperimentstracker.l1905 | evidence/03_symbols.md | 1905-1905 |
| ev.03_symbols_md.ml_training_experiments_adapters_vertex_experiments_tracker_py.init.l1906 | evidence/03_symbols.md | 1906-1906 |
| ev.03_symbols_md.ml_training_experiments_adapters_vertex_experiments_tracker_py.enter.l1907 | evidence/03_symbols.md | 1907-1907 |
| ev.03_symbols_md.ml_training_experiments_adapters_vertex_experiments_tracker_py.exit.l1908 | evidence/03_symbols.md | 1908-1908 |
| ev.03_symbols_md.ml_training_experiments_adapters_vertex_experiments_tracker_py.log_metrics.l1909 | evidence/03_symbols.md | 1909-1909 |
| ev.03_symbols_md.ml_training_experiments_adapters_vertex_experiments_tracker_py.log_params.l1910 | evidence/03_symbols.md | 1910-1910 |
| ev.03_symbols_md.ml_training_experiments_ports_experiment_tracker_py.experimenttracker.l1914 | evidence/03_symbols.md | 1914-1914 |
| ev.03_symbols_md.ml_training_experiments_ports_experiment_tracker_py.enter.l1915 | evidence/03_symbols.md | 1915-1915 |
| ev.03_symbols_md.ml_training_experiments_ports_experiment_tracker_py.exit.l1916 | evidence/03_symbols.md | 1916-1916 |
| ev.03_symbols_md.ml_training_experiments_ports_experiment_tracker_py.log_metrics.l1917 | evidence/03_symbols.md | 1917-1917 |
| ev.03_symbols_md.ml_training_experiments_ports_experiment_tracker_py.log_params.l1918 | evidence/03_symbols.md | 1918-1918 |
| ev.03_symbols_md.ml_training_model_builder_py.synthetic_ranking_frames.l1922 | evidence/03_symbols.md | 1922-1922 |
| ev.03_symbols_md.ml_training_model_builder_py.split_by_request_id.l1923 | evidence/03_symbols.md | 1923-1923 |
| ev.03_symbols_md.ml_training_ports_ranker_model_py.rankermodel.l1927 | evidence/03_symbols.md | 1927-1927 |
| ev.03_symbols_md.ml_training_ports_ranker_model_py.predict.l1928 | evidence/03_symbols.md | 1928-1928 |
| ev.03_symbols_md.ml_training_ports_ranker_model_py.predict_with_explain.l1929 | evidence/03_symbols.md | 1929-1929 |
| ev.03_symbols_md.ml_training_ports_ranker_model_py.save.l1930 | evidence/03_symbols.md | 1930-1930 |
| ev.03_symbols_md.ml_training_ports_ranker_trainer_py.trainingresult.l1934 | evidence/03_symbols.md | 1934-1934 |
| ev.03_symbols_md.ml_training_ports_ranker_trainer_py.rankertrainer.l1935 | evidence/03_symbols.md | 1935-1935 |
| ev.03_symbols_md.ml_training_ports_ranker_trainer_py.train.l1936 | evidence/03_symbols.md | 1936-1936 |
| ev.03_symbols_md.ml_training_trainer_py.ranktrainresult.l1940 | evidence/03_symbols.md | 1940-1940 |
| ev.03_symbols_md.ml_training_trainer_py.ranktrainingartifacts.l1941 | evidence/03_symbols.md | 1941-1941 |
| ev.03_symbols_md.ml_training_trainer_py.build_rank_params.l1942 | evidence/03_symbols.md | 1942-1942 |
| ev.03_symbols_md.ml_training_trainer_py.group_sizes.l1943 | evidence/03_symbols.md | 1943-1943 |
| ev.03_symbols_md.ml_training_trainer_py.train.l1944 | evidence/03_symbols.md | 1944-1944 |
| ev.03_symbols_md.ml_training_trainer_py.write_artifacts.l1945 | evidence/03_symbols.md | 1945-1945 |
| ev.03_symbols_md.ml_training_trainer_py.copy_if_requested.l1946 | evidence/03_symbols.md | 1946-1946 |
| ev.03_symbols_md.ml_training_trainer_py.default_tracker_factory.l1947 | evidence/03_symbols.md | 1947-1947 |
| ev.03_symbols_md.ml_training_trainer_py.build.l1948 | evidence/03_symbols.md | 1948-1948 |
| ev.03_symbols_md.ml_training_trainer_py.run.l1949 | evidence/03_symbols.md | 1949-1949 |
| ev.03_symbols_md.ml_training_trainer_py.parse_args.l1950 | evidence/03_symbols.md | 1950-1950 |
| ev.03_symbols_md.ml_training_trainer_py.main.l1951 | evidence/03_symbols.md | 1951-1951 |
| ev.03_symbols_md.pipeline_batch_serving_job_main_py.property_search_batch_serve_pipeline.l1955 | evidence/03_symbols.md | 1955-1955 |
| ev.03_symbols_md.pipeline_batch_serving_job_main_py.get_pipeline.l1956 | evidence/03_symbols.md | 1956-1956 |
| ev.03_symbols_md.pipeline_batch_serving_job_main_py.main.l1957 | evidence/03_symbols.md | 1957-1957 |
| ev.03_symbols_md.pipeline_dags__common_py.env.l1961 | evidence/03_symbols.md | 1961-1961 |
| ev.03_symbols_md.pipeline_dags__common_py.project_id.l1962 | evidence/03_symbols.md | 1962-1962 |
| ev.03_symbols_md.pipeline_dags__common_py.region.l1963 | evidence/03_symbols.md | 1963-1963 |
| ev.03_symbols_md.pipeline_dags__common_py.vertex_location.l1964 | evidence/03_symbols.md | 1964-1964 |
| ev.03_symbols_md.pipeline_dags__common_py.fixed_start_date.l1965 | evidence/03_symbols.md | 1965-1965 |
| ev.03_symbols_md.pipeline_dags__pod_py.composer_runner_image.l1969 | evidence/03_symbols.md | 1969-1969 |
| ev.03_symbols_md.pipeline_dags__pod_py.propagated_env_vars.l1970 | evidence/03_symbols.md | 1970-1970 |
| ev.03_symbols_md.pipeline_dags__pod_py.python_pod.l1971 | evidence/03_symbols.md | 1971-1971 |
| ev.03_symbols_md.pipeline_dags__pod_py.gcloud_pod.l1972 | evidence/03_symbols.md | 1972-1972 |
| ev.03_symbols_md.pipeline_dags_daily_feature_refresh_py.gate_daily_vvs_refresh.l1976 | evidence/03_symbols.md | 1976-1976 |
| ev.03_symbols_md.pipeline_dags_monitoring_validation_py.resolve_sql_path.l1980 | evidence/03_symbols.md | 1980-1980 |
| ev.03_symbols_md.pipeline_dags_retrain_orchestration_py.gate_auto_promote.l1984 | evidence/03_symbols.md | 1984-1984 |
| ev.03_symbols_md.pipeline_data_job_adapters_in_memory_vector_search_writer_py.inmemoryvectorsearchwriter.l1988 | evidence/03_symbols.md | 1988-1988 |
| ev.03_symbols_md.pipeline_data_job_adapters_in_memory_vector_search_writer_py.init.l1989 | evidence/03_symbols.md | 1989-1989 |
| ev.03_symbols_md.pipeline_data_job_adapters_in_memory_vector_search_writer_py.upsert.l1990 | evidence/03_symbols.md | 1990-1990 |
| ev.03_symbols_md.pipeline_data_job_adapters_vertex_vector_search_writer_py.vertexvectorsearchwriter.l1994 | evidence/03_symbols.md | 1994-1994 |
| ev.03_symbols_md.pipeline_data_job_adapters_vertex_vector_search_writer_py.init.l1995 | evidence/03_symbols.md | 1995-1995 |
| ev.03_symbols_md.pipeline_data_job_adapters_vertex_vector_search_writer_py.resolve_index.l1996 | evidence/03_symbols.md | 1996-1996 |
| ev.03_symbols_md.pipeline_data_job_adapters_vertex_vector_search_writer_py.upsert.l1997 | evidence/03_symbols.md | 1997-1997 |
| ev.03_symbols_md.pipeline_data_job_adapters_vertex_vector_search_writer_py.to_sdk_datapoint.l1998 | evidence/03_symbols.md | 1998-1998 |
| ev.03_symbols_md.pipeline_data_job_adapters_vertex_vector_search_writer_py.chunked.l1999 | evidence/03_symbols.md | 1999-1999 |
| ev.03_symbols_md.pipeline_data_job_components_batch_predict_embeddings_py.batch_predict_embeddings.l2003 | evidence/03_symbols.md | 2003-2003 |
| ev.03_symbols_md.pipeline_data_job_components_load_properties_py.load_properties.l2007 | evidence/03_symbols.md | 2007-2007 |
| ev.03_symbols_md.pipeline_data_job_components_upsert_vector_search_py.upsert_vector_search.l2011 | evidence/03_symbols.md | 2011-2011 |
| ev.03_symbols_md.pipeline_data_job_components_write_embeddings_py.write_embeddings.l2015 | evidence/03_symbols.md | 2015-2015 |
| ev.03_symbols_md.pipeline_data_job_main_py.property_search_embed_pipeline.l2019 | evidence/03_symbols.md | 2019-2019 |
| ev.03_symbols_md.pipeline_data_job_main_py.build_pipeline_spec.l2020 | evidence/03_symbols.md | 2020-2020 |
| ev.03_symbols_md.pipeline_data_job_main_py.get_pipeline.l2021 | evidence/03_symbols.md | 2021-2021 |
| ev.03_symbols_md.pipeline_data_job_main_py.main.l2022 | evidence/03_symbols.md | 2022-2022 |
| ev.03_symbols_md.pipeline_data_job_ports_vector_search_writer_py.embeddingdatapoint.l2026 | evidence/03_symbols.md | 2026-2026 |
| ev.03_symbols_md.pipeline_data_job_ports_vector_search_writer_py.vectorsearchwriter.l2027 | evidence/03_symbols.md | 2027-2027 |
| ev.03_symbols_md.pipeline_data_job_ports_vector_search_writer_py.upsert.l2028 | evidence/03_symbols.md | 2028-2028 |
| ev.03_symbols_md.pipeline_evaluation_job_main_py.property_search_evaluate_pipeline.l2032 | evidence/03_symbols.md | 2032-2032 |
| ev.03_symbols_md.pipeline_evaluation_job_main_py.get_pipeline.l2033 | evidence/03_symbols.md | 2033-2033 |
| ev.03_symbols_md.pipeline_evaluation_job_main_py.main.l2034 | evidence/03_symbols.md | 2034-2034 |
| ev.03_symbols_md.pipeline_labeling_job_main_py.run.l2038 | evidence/03_symbols.md | 2038-2038 |
| ev.03_symbols_md.pipeline_labeling_job_main_py.main.l2039 | evidence/03_symbols.md | 2039-2039 |
| ev.03_symbols_md.pipeline_training_dataset_job_main_py.run.l2043 | evidence/03_symbols.md | 2043-2043 |
| ev.03_symbols_md.pipeline_training_dataset_job_main_py.main.l2044 | evidence/03_symbols.md | 2044-2044 |
| ev.03_symbols_md.pipeline_training_job_adapters_kfp_orchestrator_py.ref.l2048 | evidence/03_symbols.md | 2048-2048 |
| ev.03_symbols_md.pipeline_training_job_adapters_kfp_orchestrator_py.init.l2049 | evidence/03_symbols.md | 2049-2049 |
| ev.03_symbols_md.pipeline_training_job_adapters_kfp_orchestrator_py.name.l2050 | evidence/03_symbols.md | 2050-2050 |
| ev.03_symbols_md.pipeline_training_job_adapters_kfp_orchestrator_py.task.l2051 | evidence/03_symbols.md | 2051-2051 |
| ev.03_symbols_md.pipeline_training_job_adapters_kfp_orchestrator_py.kfporchestrator.l2052 | evidence/03_symbols.md | 2052-2052 |
| ev.03_symbols_md.pipeline_training_job_adapters_kfp_orchestrator_py.init.l2053 | evidence/03_symbols.md | 2053-2053 |
| ev.03_symbols_md.pipeline_training_job_adapters_kfp_orchestrator_py.add_component.l2054 | evidence/03_symbols.md | 2054-2054 |
| ev.03_symbols_md.pipeline_training_job_adapters_kfp_orchestrator_py.add_dependency.l2055 | evidence/03_symbols.md | 2055-2055 |
| ev.03_symbols_md.pipeline_training_job_adapters_kfp_orchestrator_py.compile.l2056 | evidence/03_symbols.md | 2056-2056 |
| ev.03_symbols_md.pipeline_training_job_adapters_kfp_orchestrator_py.pipeline_fn.l2057 | evidence/03_symbols.md | 2057-2057 |
| ev.03_symbols_md.pipeline_training_job_adapters_kfp_orchestrator_py.submit.l2058 | evidence/03_symbols.md | 2058-2058 |
| ev.03_symbols_md.pipeline_training_job_components_evaluate_py.evaluate_reranker.l2062 | evidence/03_symbols.md | 2062-2062 |
| ev.03_symbols_md.pipeline_training_job_components_evaluate_py.log.l2063 | evidence/03_symbols.md | 2063-2063 |
| ev.03_symbols_md.pipeline_training_job_components_load_features_py.load_features.l2067 | evidence/03_symbols.md | 2067-2067 |
| ev.03_symbols_md.pipeline_training_job_components_load_features_py.log.l2068 | evidence/03_symbols.md | 2068-2068 |
| ev.03_symbols_md.pipeline_training_job_components_register_reranker_py.register_reranker.l2072 | evidence/03_symbols.md | 2072-2072 |
| ev.03_symbols_md.pipeline_training_job_components_register_reranker_py.log.l2073 | evidence/03_symbols.md | 2073-2073 |
| ev.03_symbols_md.pipeline_training_job_components_train_reranker_py.train_reranker.l2077 | evidence/03_symbols.md | 2077-2077 |
| ev.03_symbols_md.pipeline_training_job_components_train_reranker_py.log.l2078 | evidence/03_symbols.md | 2078-2078 |
| ev.03_symbols_md.pipeline_training_job_main_py.property_search_train_pipeline.l2082 | evidence/03_symbols.md | 2082-2082 |
| ev.03_symbols_md.pipeline_training_job_main_py.build_pipeline_spec.l2083 | evidence/03_symbols.md | 2083-2083 |
| ev.03_symbols_md.pipeline_training_job_main_py.get_pipeline.l2084 | evidence/03_symbols.md | 2084-2084 |
| ev.03_symbols_md.pipeline_training_job_main_py.main.l2085 | evidence/03_symbols.md | 2085-2085 |
| ev.03_symbols_md.pipeline_training_job_ports_pipeline_component_py.pipelinecomponent.l2089 | evidence/03_symbols.md | 2089-2089 |
| ev.03_symbols_md.pipeline_training_job_ports_pipeline_component_py.name.l2090 | evidence/03_symbols.md | 2090-2090 |
| ev.03_symbols_md.pipeline_training_job_ports_pipeline_component_py.to_runtime_task.l2091 | evidence/03_symbols.md | 2091-2091 |
| ev.03_symbols_md.pipeline_training_job_ports_pipeline_component_py.pipelinecomponentref.l2092 | evidence/03_symbols.md | 2092-2092 |
| ev.03_symbols_md.pipeline_training_job_ports_pipeline_component_py.name.l2093 | evidence/03_symbols.md | 2093-2093 |
| ev.03_symbols_md.pipeline_training_job_ports_pipeline_orchestrator_py.pipelineconfig.l2097 | evidence/03_symbols.md | 2097-2097 |
| ev.03_symbols_md.pipeline_training_job_ports_pipeline_orchestrator_py.pipelineorchestrator.l2098 | evidence/03_symbols.md | 2098-2098 |
| ev.03_symbols_md.pipeline_training_job_ports_pipeline_orchestrator_py.add_component.l2099 | evidence/03_symbols.md | 2099-2099 |
| ev.03_symbols_md.pipeline_training_job_ports_pipeline_orchestrator_py.add_dependency.l2100 | evidence/03_symbols.md | 2100-2100 |
| ev.03_symbols_md.pipeline_training_job_ports_pipeline_orchestrator_py.compile.l2101 | evidence/03_symbols.md | 2101-2101 |
| ev.03_symbols_md.pipeline_training_job_ports_pipeline_orchestrator_py.submit.l2102 | evidence/03_symbols.md | 2102-2102 |
| ev.03_symbols_md.pipeline_workflow_compile_py.compile_pipeline.l2106 | evidence/03_symbols.md | 2106-2106 |
| ev.03_symbols_md.pipeline_workflow_compile_py.target_path.l2107 | evidence/03_symbols.md | 2107-2107 |
| ev.03_symbols_md.pipeline_workflow_compile_py.spec.l2108 | evidence/03_symbols.md | 2108-2108 |
| ev.03_symbols_md.pipeline_workflow_compile_py.pipeline.l2109 | evidence/03_symbols.md | 2109-2109 |
| ev.03_symbols_md.pipeline_workflow_compile_py.coerce_parameter_value.l2110 | evidence/03_symbols.md | 2110-2110 |
| ev.03_symbols_md.pipeline_workflow_compile_py.merge_parameter_values.l2111 | evidence/03_symbols.md | 2111-2111 |
| ev.03_symbols_md.pipeline_workflow_compile_py.submit_pipeline.l2112 | evidence/03_symbols.md | 2112-2112 |
| ev.03_symbols_md.pipeline_workflow_compile_py.submit_pipeline_yaml.l2113 | evidence/03_symbols.md | 2113-2113 |
| ev.03_symbols_md.pipeline_workflow_compile_py.main.l2114 | evidence/03_symbols.md | 2114-2114 |
| ev.03_symbols_md.pipeline_workflow_trigger_py.env.l2118 | evidence/03_symbols.md | 2118-2118 |
| ev.03_symbols_md.pipeline_workflow_trigger_py.optional_json_env.l2119 | evidence/03_symbols.md | 2119-2119 |
| ev.03_symbols_md.pipeline_workflow_trigger_py.decode_pubsub_message.l2120 | evidence/03_symbols.md | 2120-2120 |
| ev.03_symbols_md.pipeline_workflow_trigger_py.merge_parameters.l2121 | evidence/03_symbols.md | 2121-2121 |
| ev.03_symbols_md.pipeline_workflow_trigger_py.build_job_id.l2122 | evidence/03_symbols.md | 2122-2122 |
| ev.03_symbols_md.pipeline_workflow_trigger_py.trigger_pipeline.l2123 | evidence/03_symbols.md | 2123-2123 |
| ev.03_symbols_md.pipeline_workflow_trigger_py.submit_pipeline.l2124 | evidence/03_symbols.md | 2124-2124 |
| ev.03_symbols_md.pipeline_workflow_trigger_zip_main_py.env.l2128 | evidence/03_symbols.md | 2128-2128 |
| ev.03_symbols_md.pipeline_workflow_trigger_zip_main_py.optional_json_env.l2129 | evidence/03_symbols.md | 2129-2129 |
| ev.03_symbols_md.pipeline_workflow_trigger_zip_main_py.decode_pubsub_message.l2130 | evidence/03_symbols.md | 2130-2130 |
| ev.03_symbols_md.pipeline_workflow_trigger_zip_main_py.merge_parameters.l2131 | evidence/03_symbols.md | 2131-2131 |
| ev.03_symbols_md.pipeline_workflow_trigger_zip_main_py.build_job_id.l2132 | evidence/03_symbols.md | 2132-2132 |
| ev.03_symbols_md.pipeline_workflow_trigger_zip_main_py.trigger_pipeline.l2133 | evidence/03_symbols.md | 2133-2133 |
| ev.03_symbols_md.pipeline_workflow_trigger_zip_main_py.submit_pipeline.l2134 | evidence/03_symbols.md | 2134-2134 |
| ev.03_symbols_md.scripts__common_py.load_flat_yaml.l2138 | evidence/03_symbols.md | 2138-2138 |
| ev.03_symbols_md.scripts__common_py.load_list_setting.l2139 | evidence/03_symbols.md | 2139-2139 |
| ev.03_symbols_md.scripts__common_py.resolve_project_id.l2140 | evidence/03_symbols.md | 2140-2140 |
| ev.03_symbols_md.scripts__common_py.env.l2141 | evidence/03_symbols.md | 2141-2141 |
| ev.03_symbols_md.scripts__common_py.secret.l2142 | evidence/03_symbols.md | 2142-2142 |
| ev.03_symbols_md.scripts__common_py.terraform_var_args.l2143 | evidence/03_symbols.md | 2143-2143 |
| ev.03_symbols_md.scripts__common_py.gcs_bucket_name.l2144 | evidence/03_symbols.md | 2144-2144 |
| ev.03_symbols_md.scripts__common_py.run.l2145 | evidence/03_symbols.md | 2145-2145 |
| ev.03_symbols_md.scripts__common_py.gcloud.l2146 | evidence/03_symbols.md | 2146-2146 |
| ev.03_symbols_md.scripts__common_py.resolve_git_sha.l2147 | evidence/03_symbols.md | 2147-2147 |
| ev.03_symbols_md.scripts__common_py.cloud_run_url.l2148 | evidence/03_symbols.md | 2148-2148 |
| ev.03_symbols_md.scripts__common_py.gateway_url.l2149 | evidence/03_symbols.md | 2149-2149 |
| ev.03_symbols_md.scripts__common_py.identity_token.l2150 | evidence/03_symbols.md | 2150-2150 |
| ev.03_symbols_md.scripts__common_py.resolvedapitarget.l2151 | evidence/03_symbols.md | 2151-2151 |
| ev.03_symbols_md.scripts__common_py.call.l2152 | evidence/03_symbols.md | 2152-2152 |
| ev.03_symbols_md.scripts__common_py.env_flag.l2153 | evidence/03_symbols.md | 2153-2153 |
| ev.03_symbols_md.scripts__common_py.resolve_api_target.l2154 | evidence/03_symbols.md | 2154-2154 |
| ev.03_symbols_md.scripts__common_py.http_json.l2155 | evidence/03_symbols.md | 2155-2155 |
| ev.03_symbols_md.scripts__common_py.fail.l2156 | evidence/03_symbols.md | 2156-2156 |
| ev.03_symbols_md.scripts__common_py.print_pretty.l2157 | evidence/03_symbols.md | 2157-2157 |
| ev.03_symbols_md.scripts__common_py.submit_cloud_build_async.l2158 | evidence/03_symbols.md | 2158-2158 |
| ev.03_symbols_md.scripts__common_py.wait_cloud_build.l2159 | evidence/03_symbols.md | 2159-2159 |
| ev.03_symbols_md.scripts__common_py.print_build_diagnostics.l2160 | evidence/03_symbols.md | 2160-2160 |
| ev.03_symbols_md.scripts_adapters_gcloud_py.gcloud_run.l2164 | evidence/03_symbols.md | 2164-2164 |
| ev.03_symbols_md.scripts_adapters_kubectl_py.kubectl_run.l2168 | evidence/03_symbols.md | 2168-2168 |
| ev.03_symbols_md.scripts_adapters_terraform_py.terraform_run.l2172 | evidence/03_symbols.md | 2172-2172 |
| ev.03_symbols_md.scripts_bqml_train_popularity_py.main.l2176 | evidence/03_symbols.md | 2176-2176 |
| ev.03_symbols_md.scripts_ci_layers_py.violation.l2180 | evidence/03_symbols.md | 2180-2180 |
| ev.03_symbols_md.scripts_ci_layers_py.str.l2181 | evidence/03_symbols.md | 2181-2181 |
| ev.03_symbols_md.scripts_ci_layers_py.imports_with_lines.l2182 | evidence/03_symbols.md | 2182-2182 |
| ev.03_symbols_md.scripts_ci_layers_py.matches.l2183 | evidence/03_symbols.md | 2183-2183 |
| ev.03_symbols_md.scripts_ci_layers_py.is_excluded.l2184 | evidence/03_symbols.md | 2184-2184 |
| ev.03_symbols_md.scripts_ci_layers_py.find_rules_for_file.l2185 | evidence/03_symbols.md | 2185-2185 |
| ev.03_symbols_md.scripts_ci_layers_py.find_violations.l2186 | evidence/03_symbols.md | 2186-2186 |
| ev.03_symbols_md.scripts_ci_layers_py.discover_files.l2187 | evidence/03_symbols.md | 2187-2187 |
| ev.03_symbols_md.scripts_ci_layers_py.main.l2188 | evidence/03_symbols.md | 2188-2188 |
| ev.03_symbols_md.scripts_ci_sync_configmap_py.render.l2192 | evidence/03_symbols.md | 2192-2192 |
| ev.03_symbols_md.scripts_ci_sync_configmap_py.main.l2193 | evidence/03_symbols.md | 2193-2193 |
| ev.03_symbols_md.scripts_ci_sync_dataform_py.render.l2197 | evidence/03_symbols.md | 2197-2197 |
| ev.03_symbols_md.scripts_ci_sync_dataform_py.main.l2198 | evidence/03_symbols.md | 2198-2198 |
| ev.03_symbols_md.scripts_deploy_api_gke_py.step.l2202 | evidence/03_symbols.md | 2202-2202 |
| ev.03_symbols_md.scripts_deploy_api_gke_py.info.l2203 | evidence/03_symbols.md | 2203-2203 |
| ev.03_symbols_md.scripts_deploy_api_gke_py.error.l2204 | evidence/03_symbols.md | 2204-2204 |
| ev.03_symbols_md.scripts_deploy_api_gke_py.diag.l2205 | evidence/03_symbols.md | 2205-2205 |
| ev.03_symbols_md.scripts_deploy_api_gke_py.require.l2206 | evidence/03_symbols.md | 2206-2206 |
| ev.03_symbols_md.scripts_deploy_api_gke_py.ensure_kubectl_context.l2207 | evidence/03_symbols.md | 2207-2207 |
| ev.03_symbols_md.scripts_deploy_api_gke_py.dump_rollout_diagnostics.l2208 | evidence/03_symbols.md | 2208-2208 |
| ev.03_symbols_md.scripts_deploy_api_gke_py.main.l2209 | evidence/03_symbols.md | 2209-2209 |
| ev.03_symbols_md.scripts_deploy_api_gke_local_py.step.l2213 | evidence/03_symbols.md | 2213-2213 |
| ev.03_symbols_md.scripts_deploy_api_gke_local_py.info.l2214 | evidence/03_symbols.md | 2214-2214 |
| ev.03_symbols_md.scripts_deploy_api_gke_local_py.error.l2215 | evidence/03_symbols.md | 2215-2215 |
| ev.03_symbols_md.scripts_deploy_api_gke_local_py.diag.l2216 | evidence/03_symbols.md | 2216-2216 |
| ev.03_symbols_md.scripts_deploy_api_gke_local_py.require.l2217 | evidence/03_symbols.md | 2217-2217 |
| ev.03_symbols_md.scripts_deploy_api_gke_local_py.ensure_docker_buildx.l2218 | evidence/03_symbols.md | 2218-2218 |
| ev.03_symbols_md.scripts_deploy_api_gke_local_py.ensure_ar_auth.l2219 | evidence/03_symbols.md | 2219-2219 |
| ev.03_symbols_md.scripts_deploy_api_gke_local_py.ensure_kubectl_context.l2220 | evidence/03_symbols.md | 2220-2220 |
| ev.03_symbols_md.scripts_deploy_api_gke_local_py.main.l2221 | evidence/03_symbols.md | 2221-2221 |
| ev.03_symbols_md.scripts_deploy_build_all_local_py.step.l2225 | evidence/03_symbols.md | 2225-2225 |
| ev.03_symbols_md.scripts_deploy_build_all_local_py.build.l2226 | evidence/03_symbols.md | 2226-2226 |
| ev.03_symbols_md.scripts_deploy_build_all_local_py.main.l2227 | evidence/03_symbols.md | 2227-2227 |
| ev.03_symbols_md.scripts_deploy_build_kserve_images_py.step.l2231 | evidence/03_symbols.md | 2231-2231 |
| ev.03_symbols_md.scripts_deploy_build_kserve_images_py.info.l2232 | evidence/03_symbols.md | 2232-2232 |
| ev.03_symbols_md.scripts_deploy_build_kserve_images_py.error.l2233 | evidence/03_symbols.md | 2233-2233 |
| ev.03_symbols_md.scripts_deploy_build_kserve_images_py.build_image.l2234 | evidence/03_symbols.md | 2234-2234 |
| ev.03_symbols_md.scripts_deploy_build_kserve_images_py.patch_inference_service_image.l2235 | evidence/03_symbols.md | 2235-2235 |
| ev.03_symbols_md.scripts_deploy_build_kserve_images_py.set_deployment_image.l2236 | evidence/03_symbols.md | 2236-2236 |
| ev.03_symbols_md.scripts_deploy_build_kserve_images_py.main.l2237 | evidence/03_symbols.md | 2237-2237 |
| ev.03_symbols_md.scripts_deploy_build_kserve_images_local_py.step.l2241 | evidence/03_symbols.md | 2241-2241 |
| ev.03_symbols_md.scripts_deploy_build_kserve_images_local_py.info.l2242 | evidence/03_symbols.md | 2242-2242 |
| ev.03_symbols_md.scripts_deploy_build_kserve_images_local_py.error.l2243 | evidence/03_symbols.md | 2243-2243 |
| ev.03_symbols_md.scripts_deploy_build_kserve_images_local_py.require.l2244 | evidence/03_symbols.md | 2244-2244 |
| ev.03_symbols_md.scripts_deploy_build_kserve_images_local_py.diag.l2245 | evidence/03_symbols.md | 2245-2245 |
| ev.03_symbols_md.scripts_deploy_build_kserve_images_local_py.ensure_docker_buildx.l2246 | evidence/03_symbols.md | 2246-2246 |
| ev.03_symbols_md.scripts_deploy_build_kserve_images_local_py.ensure_ar_auth.l2247 | evidence/03_symbols.md | 2247-2247 |
| ev.03_symbols_md.scripts_deploy_build_kserve_images_local_py.ensure_kubectl_context.l2248 | evidence/03_symbols.md | 2248-2248 |
| ev.03_symbols_md.scripts_deploy_build_kserve_images_local_py.build_local_image.l2249 | evidence/03_symbols.md | 2249-2249 |
| ev.03_symbols_md.scripts_deploy_build_kserve_images_local_py.patch_inference_service_image.l2250 | evidence/03_symbols.md | 2250-2250 |
| ev.03_symbols_md.scripts_deploy_build_kserve_images_local_py.set_deployment_image.l2251 | evidence/03_symbols.md | 2251-2251 |
| ev.03_symbols_md.scripts_deploy_build_kserve_images_local_py.main.l2252 | evidence/03_symbols.md | 2252-2252 |
| ev.03_symbols_md.scripts_deploy_composer_deploy_dags_py.terraform_output.l2256 | evidence/03_symbols.md | 2256-2256 |
| ev.03_symbols_md.scripts_deploy_composer_deploy_dags_py.list_top_level_dag_files.l2257 | evidence/03_symbols.md | 2257-2257 |
| ev.03_symbols_md.scripts_deploy_composer_deploy_dags_py.list_pipeline_pkg_files.l2258 | evidence/03_symbols.md | 2258-2258 |
| ev.03_symbols_md.scripts_deploy_composer_deploy_dags_py.list_data_files.l2259 | evidence/03_symbols.md | 2259-2259 |
| ev.03_symbols_md.scripts_deploy_composer_deploy_dags_py.main.l2260 | evidence/03_symbols.md | 2260-2260 |
| ev.03_symbols_md.scripts_deploy_composer_runner_py.step.l2264 | evidence/03_symbols.md | 2264-2264 |
| ev.03_symbols_md.scripts_deploy_composer_runner_py.info.l2265 | evidence/03_symbols.md | 2265-2265 |
| ev.03_symbols_md.scripts_deploy_composer_runner_py.error.l2266 | evidence/03_symbols.md | 2266-2266 |
| ev.03_symbols_md.scripts_deploy_composer_runner_py.require.l2267 | evidence/03_symbols.md | 2267-2267 |
| ev.03_symbols_md.scripts_deploy_composer_runner_py.main.l2268 | evidence/03_symbols.md | 2268-2268 |
| ev.03_symbols_md.scripts_deploy_configmap_overlay_py.terraform_output_map.l2272 | evidence/03_symbols.md | 2272-2272 |
| ev.03_symbols_md.scripts_deploy_configmap_overlay_py.feature_online_store_public_domain_from_api.l2273 | evidence/03_symbols.md | 2273-2273 |
| ev.03_symbols_md.scripts_deploy_configmap_overlay_py.main.l2274 | evidence/03_symbols.md | 2274-2274 |
| ev.03_symbols_md.scripts_deploy_kserve_models_py.step.l2278 | evidence/03_symbols.md | 2278-2278 |
| ev.03_symbols_md.scripts_deploy_kserve_models_py.info.l2279 | evidence/03_symbols.md | 2279-2279 |
| ev.03_symbols_md.scripts_deploy_kserve_models_py.error.l2280 | evidence/03_symbols.md | 2280-2280 |
| ev.03_symbols_md.scripts_deploy_kserve_models_py.modelversion.l2281 | evidence/03_symbols.md | 2281-2281 |
| ev.03_symbols_md.scripts_deploy_kserve_models_py.require.l2282 | evidence/03_symbols.md | 2282-2282 |
| ev.03_symbols_md.scripts_deploy_kserve_models_py.resolve_latest.l2283 | evidence/03_symbols.md | 2283-2283 |
| ev.03_symbols_md.scripts_deploy_kserve_models_py.kubectl_patch.l2284 | evidence/03_symbols.md | 2284-2284 |
| ev.03_symbols_md.scripts_deploy_kserve_models_py.patch_reranker_storage_uri.l2285 | evidence/03_symbols.md | 2285-2285 |
| ev.03_symbols_md.scripts_deploy_kserve_models_py.patch_encoder_storage_uri.l2286 | evidence/03_symbols.md | 2286-2286 |
| ev.03_symbols_md.scripts_deploy_kserve_models_py.dump_diagnostics.l2287 | evidence/03_symbols.md | 2287-2287 |
| ev.03_symbols_md.scripts_deploy_kserve_models_py.wait_ready.l2288 | evidence/03_symbols.md | 2288-2288 |
| ev.03_symbols_md.scripts_deploy_kserve_models_py.main.l2289 | evidence/03_symbols.md | 2289-2289 |
| ev.03_symbols_md.scripts_deploy_monitor_py.parse_args.l2293 | evidence/03_symbols.md | 2293-2293 |
| ev.03_symbols_md.scripts_deploy_monitor_py.resolve_log_dir.l2294 | evidence/03_symbols.md | 2294-2294 |
| ev.03_symbols_md.scripts_deploy_monitor_py.utc_stamp.l2295 | evidence/03_symbols.md | 2295-2295 |
| ev.03_symbols_md.scripts_deploy_monitor_py.open_log_sink.l2296 | evidence/03_symbols.md | 2296-2296 |
| ev.03_symbols_md.scripts_deploy_monitor_py.resolve_command.l2297 | evidence/03_symbols.md | 2297-2297 |
| ev.03_symbols_md.scripts_deploy_monitor_py.build_describe.l2298 | evidence/03_symbols.md | 2298-2298 |
| ev.03_symbols_md.scripts_deploy_monitor_py.monitorstate.l2299 | evidence/03_symbols.md | 2299-2299 |
| ev.03_symbols_md.scripts_deploy_monitor_py.now_utc.l2300 | evidence/03_symbols.md | 2300-2300 |
| ev.03_symbols_md.scripts_deploy_monitor_py.maybe_parse_step.l2301 | evidence/03_symbols.md | 2301-2301 |
| ev.03_symbols_md.scripts_deploy_monitor_py.maybe_parse_build_wait.l2302 | evidence/03_symbols.md | 2302-2302 |
| ev.03_symbols_md.scripts_deploy_monitor_py.print_heartbeat.l2303 | evidence/03_symbols.md | 2303-2303 |
| ev.03_symbols_md.scripts_deploy_monitor_py.main.l2304 | evidence/03_symbols.md | 2304-2304 |
| ev.03_symbols_md.scripts_deploy_seed_lgbm_model_py.step.l2308 | evidence/03_symbols.md | 2308-2308 |
| ev.03_symbols_md.scripts_deploy_seed_lgbm_model_py.info.l2309 | evidence/03_symbols.md | 2309-2309 |
| ev.03_symbols_md.scripts_deploy_seed_lgbm_model_py.resolve_bucket.l2310 | evidence/03_symbols.md | 2310-2310 |
| ev.03_symbols_md.scripts_deploy_seed_lgbm_model_py.existing_object_size.l2311 | evidence/03_symbols.md | 2311-2311 |
| ev.03_symbols_md.scripts_deploy_seed_lgbm_model_py.train_synthetic_model.l2312 | evidence/03_symbols.md | 2312-2312 |
| ev.03_symbols_md.scripts_deploy_seed_lgbm_model_py.upload.l2313 | evidence/03_symbols.md | 2313-2313 |
| ev.03_symbols_md.scripts_deploy_seed_lgbm_model_py.main.l2314 | evidence/03_symbols.md | 2314-2314 |
| ev.03_symbols_md.scripts_domain_gcp_feature_view_sync_py.terraform_output_map.l2318 | evidence/03_symbols.md | 2318-2318 |
| ev.03_symbols_md.scripts_domain_gcp_feature_view_sync_py.access_token.l2319 | evidence/03_symbols.md | 2319-2319 |
| ev.03_symbols_md.scripts_domain_gcp_feature_view_sync_py.request_json.l2320 | evidence/03_symbols.md | 2320-2320 |
| ev.03_symbols_md.scripts_domain_gcp_feature_view_sync_py.feature_view_resource.l2321 | evidence/03_symbols.md | 2321-2321 |
| ev.03_symbols_md.scripts_domain_gcp_feature_view_sync_py.latest_sync_name.l2322 | evidence/03_symbols.md | 2322-2322 |
| ev.03_symbols_md.scripts_domain_gcp_feature_view_sync_py.list_syncs.l2323 | evidence/03_symbols.md | 2323-2323 |
| ev.03_symbols_md.scripts_domain_gcp_feature_view_sync_py.trigger_and_wait.l2324 | evidence/03_symbols.md | 2324-2324 |
| ev.03_symbols_md.scripts_domain_gcp_feature_view_sync_py.main.l2325 | evidence/03_symbols.md | 2325-2325 |
| ev.03_symbols_md.scripts_domain_gcp_gcs_cleanup_py.wipe_bucket.l2329 | evidence/03_symbols.md | 2329-2329 |
| ev.03_symbols_md.scripts_domain_gcp_gcs_cleanup_py.wipe_all_terraform_managed_buckets.l2330 | evidence/03_symbols.md | 2330-2330 |
| ev.03_symbols_md.scripts_domain_gcp_state_recovery_py.state_has.l2334 | evidence/03_symbols.md | 2334-2334 |
| ev.03_symbols_md.scripts_domain_gcp_state_recovery_py.terraform_import.l2335 | evidence/03_symbols.md | 2335-2335 |
| ev.03_symbols_md.scripts_domain_gcp_state_recovery_py.gcloud_json.l2336 | evidence/03_symbols.md | 2336-2336 |
| ev.03_symbols_md.scripts_domain_gcp_state_recovery_py.recover_iam_sas.l2337 | evidence/03_symbols.md | 2337-2337 |
| ev.03_symbols_md.scripts_domain_gcp_state_recovery_py.bq_exists.l2338 | evidence/03_symbols.md | 2338-2338 |
| ev.03_symbols_md.scripts_domain_gcp_state_recovery_py.recover_bq.l2339 | evidence/03_symbols.md | 2339-2339 |
| ev.03_symbols_md.scripts_domain_gcp_state_recovery_py.recover_pubsub.l2340 | evidence/03_symbols.md | 2340-2340 |
| ev.03_symbols_md.scripts_domain_gcp_state_recovery_py.recover_cloudfunctions.l2341 | evidence/03_symbols.md | 2341-2341 |
| ev.03_symbols_md.scripts_domain_gcp_state_recovery_py.recover_eventarc.l2342 | evidence/03_symbols.md | 2342-2342 |
| ev.03_symbols_md.scripts_domain_gcp_state_recovery_py.recover_cloud_run.l2343 | evidence/03_symbols.md | 2343-2343 |
| ev.03_symbols_md.scripts_domain_gcp_state_recovery_py.recover_artifact_registry.l2344 | evidence/03_symbols.md | 2344-2344 |
| ev.03_symbols_md.scripts_domain_gcp_state_recovery_py.recover_secret_manager.l2345 | evidence/03_symbols.md | 2345-2345 |
| ev.03_symbols_md.scripts_domain_gcp_state_recovery_py.recover_gcs_buckets.l2346 | evidence/03_symbols.md | 2346-2346 |
| ev.03_symbols_md.scripts_domain_gcp_state_recovery_py.aiplatform_get.l2347 | evidence/03_symbols.md | 2347-2347 |
| ev.03_symbols_md.scripts_domain_gcp_state_recovery_py.recover_feature_store.l2348 | evidence/03_symbols.md | 2348-2348 |
| ev.03_symbols_md.scripts_domain_gcp_state_recovery_py.recover_dataform.l2349 | evidence/03_symbols.md | 2349-2349 |
| ev.03_symbols_md.scripts_domain_gcp_state_recovery_py.recover_orphan_gcp_resources.l2350 | evidence/03_symbols.md | 2350-2350 |
| ev.03_symbols_md.scripts_domain_gcp_state_recovery_py.main.l2351 | evidence/03_symbols.md | 2351-2351 |
| ev.03_symbols_md.scripts_domain_gcp_vertex_cleanup_py.undeploy_endpoint_models.l2355 | evidence/03_symbols.md | 2355-2355 |
| ev.03_symbols_md.scripts_domain_gcp_vertex_cleanup_py.undeploy_all_endpoint_shells.l2356 | evidence/03_symbols.md | 2356-2356 |
| ev.03_symbols_md.scripts_domain_gcp_vertex_cleanup_py.deployed_index_exists.l2357 | evidence/03_symbols.md | 2357-2357 |
| ev.03_symbols_md.scripts_domain_gcp_vertex_cleanup_py.deployed_index_state.l2358 | evidence/03_symbols.md | 2358-2358 |
| ev.03_symbols_md.scripts_domain_gcp_vertex_cleanup_py.undeploy_all_vvs_deployed_indexes.l2359 | evidence/03_symbols.md | 2359-2359 |
| ev.03_symbols_md.scripts_domain_gcp_vertex_cleanup_py.wait_for_deployed_index_absent.l2360 | evidence/03_symbols.md | 2360-2360 |
| ev.03_symbols_md.scripts_domain_gcp_vertex_feature_store_wait_py.access_token.l2364 | evidence/03_symbols.md | 2364-2364 |
| ev.03_symbols_md.scripts_domain_gcp_vertex_feature_store_wait_py.rest_get.l2365 | evidence/03_symbols.md | 2365-2365 |
| ev.03_symbols_md.scripts_domain_gcp_vertex_feature_store_wait_py.feature_group_ids.l2366 | evidence/03_symbols.md | 2366-2366 |
| ev.03_symbols_md.scripts_domain_gcp_vertex_feature_store_wait_py.feature_online_store_ids.l2367 | evidence/03_symbols.md | 2367-2367 |
| ev.03_symbols_md.scripts_domain_gcp_vertex_feature_store_wait_py.wait_until_feature_store_names_released.l2368 | evidence/03_symbols.md | 2368-2368 |
| ev.03_symbols_md.scripts_domain_gcp_vertex_feature_store_wait_py.wait_until_feature_store_names_released_from_env.l2369 | evidence/03_symbols.md | 2369-2369 |
| ev.03_symbols_md.scripts_domain_gcp_vertex_import_py.state_has.l2373 | evidence/03_symbols.md | 2373-2373 |
| ev.03_symbols_md.scripts_domain_gcp_vertex_import_py.gcloud_first.l2374 | evidence/03_symbols.md | 2374-2374 |
| ev.03_symbols_md.scripts_domain_gcp_vertex_import_py.terraform_import.l2375 | evidence/03_symbols.md | 2375-2375 |
| ev.03_symbols_md.scripts_domain_gcp_vertex_import_py.import_persistent_vvs_resources.l2376 | evidence/03_symbols.md | 2376-2376 |
| ev.03_symbols_md.scripts_domain_k8s_elasticsearch_wait_py.read_health.l2380 | evidence/03_symbols.md | 2380-2380 |
| ev.03_symbols_md.scripts_domain_k8s_elasticsearch_wait_py.read_phase.l2381 | evidence/03_symbols.md | 2381-2381 |
| ev.03_symbols_md.scripts_domain_k8s_elasticsearch_wait_py.wait_until_es_healthy.l2382 | evidence/03_symbols.md | 2382-2382 |
| ev.03_symbols_md.scripts_domain_k8s_kube_cleanup_py.delete_orphan_workloads.l2386 | evidence/03_symbols.md | 2386-2386 |
| ev.03_symbols_md.scripts_domain_k8s_kubectl_context_py.ensure.l2390 | evidence/03_symbols.md | 2390-2390 |
| ev.03_symbols_md.scripts_domain_k8s_kubectl_context_py.wait_until_api_ready.l2391 | evidence/03_symbols.md | 2391-2391 |
| ev.03_symbols_md.scripts_domain_terraform_lock_py.should_auto_force_unlock.l2395 | evidence/03_symbols.md | 2395-2395 |
| ev.03_symbols_md.scripts_domain_terraform_lock_py.parse_terraform_lock_id.l2396 | evidence/03_symbols.md | 2396-2396 |
| ev.03_symbols_md.scripts_domain_terraform_lock_py.is_state_lock_error.l2397 | evidence/03_symbols.md | 2397-2397 |
| ev.03_symbols_md.scripts_domain_terraform_lock_py.run_terraform_streaming_with_lock_retry.l2398 | evidence/03_symbols.md | 2398-2398 |
| ev.03_symbols_md.scripts_domain_terraform_lock_py.run_stream_capture.l2399 | evidence/03_symbols.md | 2399-2399 |
| ev.03_symbols_md.scripts_domain_terraform_stage_apply_py.terraform_apply_stage1_with_retries.l2403 | evidence/03_symbols.md | 2403-2403 |
| ev.03_symbols_md.scripts_domain_terraform_state_py.state_list.l2407 | evidence/03_symbols.md | 2407-2407 |
| ev.03_symbols_md.scripts_domain_terraform_state_py.state_size.l2408 | evidence/03_symbols.md | 2408-2408 |
| ev.03_symbols_md.scripts_domain_terraform_state_py.addresses_starting_with.l2409 | evidence/03_symbols.md | 2409-2409 |
| ev.03_symbols_md.scripts_domain_terraform_state_py.is_in_state.l2410 | evidence/03_symbols.md | 2410-2410 |
| ev.03_symbols_md.scripts_domain_terraform_state_py.filter_targets_in_state.l2411 | evidence/03_symbols.md | 2411-2411 |
| ev.03_symbols_md.scripts_domain_terraform_state_py.state_rm.l2412 | evidence/03_symbols.md | 2412-2412 |
| ev.03_symbols_md.scripts_lib_bq_property_rows_py.load_properties_cleaned_rows.l2416 | evidence/03_symbols.md | 2416-2416 |
| ev.03_symbols_md.scripts_lib_config_py.generate_configmap_data.l2420 | evidence/03_symbols.md | 2420-2420 |
| ev.03_symbols_md.scripts_lib_config_py.render_configmap_yaml.l2421 | evidence/03_symbols.md | 2421-2421 |
| ev.03_symbols_md.scripts_lib_makefile_help_py.format.l2425 | evidence/03_symbols.md | 2425-2425 |
| ev.03_symbols_md.scripts_lib_makefile_help_py.main.l2426 | evidence/03_symbols.md | 2426-2426 |
| ev.03_symbols_md.scripts_lib_step_timing_py.fmt_duration.l2430 | evidence/03_symbols.md | 2430-2430 |
| ev.03_symbols_md.scripts_lib_step_timing_py.record.l2431 | evidence/03_symbols.md | 2431-2431 |
| ev.03_symbols_md.scripts_lib_step_timing_py.trim.l2432 | evidence/03_symbols.md | 2432-2432 |
| ev.03_symbols_md.scripts_lib_step_timing_py.baselines.l2433 | evidence/03_symbols.md | 2433-2433 |
| ev.03_symbols_md.scripts_lib_step_timing_py.print_eta.l2434 | evidence/03_symbols.md | 2434-2434 |
| ev.03_symbols_md.scripts_ops_accuracy_report_py.evalcase.l2438 | evidence/03_symbols.md | 2438-2438 |
| ev.03_symbols_md.scripts_ops_accuracy_report_py.default_cases_path.l2439 | evidence/03_symbols.md | 2439-2439 |
| ev.03_symbols_md.scripts_ops_accuracy_report_py.load_cases.l2440 | evidence/03_symbols.md | 2440-2440 |
| ev.03_symbols_md.scripts_ops_accuracy_report_py.dcg_binary.l2441 | evidence/03_symbols.md | 2441-2441 |
| ev.03_symbols_md.scripts_ops_accuracy_report_py.ndcg_at_k_binary.l2442 | evidence/03_symbols.md | 2442-2442 |
| ev.03_symbols_md.scripts_ops_accuracy_report_py.hit_rate_at_k_binary.l2443 | evidence/03_symbols.md | 2443-2443 |
| ev.03_symbols_md.scripts_ops_accuracy_report_py.mrr_at_k_binary.l2444 | evidence/03_symbols.md | 2444-2444 |
| ev.03_symbols_md.scripts_ops_accuracy_report_py.main.l2445 | evidence/03_symbols.md | 2445-2445 |
| ev.03_symbols_md.scripts_ops_check_retrain_py.diag.l2449 | evidence/03_symbols.md | 2449-2449 |
| ev.03_symbols_md.scripts_ops_check_retrain_py.main.l2450 | evidence/03_symbols.md | 2450-2450 |
| ev.03_symbols_md.scripts_ops_composer_dag_py.resolve.l2454 | evidence/03_symbols.md | 2454-2454 |
| ev.03_symbols_md.scripts_ops_composer_dag_py.build_gcloud_cmd.l2455 | evidence/03_symbols.md | 2455-2455 |
| ev.03_symbols_md.scripts_ops_composer_dag_py.parse_args.l2456 | evidence/03_symbols.md | 2456-2456 |
| ev.03_symbols_md.scripts_ops_composer_dag_py.main.l2457 | evidence/03_symbols.md | 2457-2457 |
| ev.03_symbols_md.scripts_ops_composer_task_states_py.balanced_array_from.l2461 | evidence/03_symbols.md | 2461-2461 |
| ev.03_symbols_md.scripts_ops_composer_task_states_py.extract_json_array.l2462 | evidence/03_symbols.md | 2462-2462 |
| ev.03_symbols_md.scripts_ops_composer_task_states_py.gcloud_composer.l2463 | evidence/03_symbols.md | 2463-2463 |
| ev.03_symbols_md.scripts_ops_composer_task_states_py.latest_run_id_from_list_runs.l2464 | evidence/03_symbols.md | 2464-2464 |
| ev.03_symbols_md.scripts_ops_composer_task_states_py.fetch_task_states_json.l2465 | evidence/03_symbols.md | 2465-2465 |
| ev.03_symbols_md.scripts_ops_composer_task_states_py.main.l2466 | evidence/03_symbols.md | 2466-2466 |
| ev.03_symbols_md.scripts_ops_destroy_check_py.finding.l2470 | evidence/03_symbols.md | 2470-2470 |
| ev.03_symbols_md.scripts_ops_destroy_check_py.parse_args.l2471 | evidence/03_symbols.md | 2471-2471 |
| ev.03_symbols_md.scripts_ops_destroy_check_py.looks_like_api_disabled.l2472 | evidence/03_symbols.md | 2472-2472 |
| ev.03_symbols_md.scripts_ops_destroy_check_py.run_json.l2473 | evidence/03_symbols.md | 2473-2473 |
| ev.03_symbols_md.scripts_ops_destroy_check_py.run_bq_json.l2474 | evidence/03_symbols.md | 2474-2474 |
| ev.03_symbols_md.scripts_ops_destroy_check_py.pluck.l2475 | evidence/03_symbols.md | 2475-2475 |
| ev.03_symbols_md.scripts_ops_destroy_check_py.collect_gke_clusters.l2476 | evidence/03_symbols.md | 2476-2476 |
| ev.03_symbols_md.scripts_ops_destroy_check_py.collect_cloud_run_services.l2477 | evidence/03_symbols.md | 2477-2477 |
| ev.03_symbols_md.scripts_ops_destroy_check_py.collect_dataflow_jobs.l2478 | evidence/03_symbols.md | 2478-2478 |
| ev.03_symbols_md.scripts_ops_destroy_check_py.collect_vertex_endpoints.l2479 | evidence/03_symbols.md | 2479-2479 |
| ev.03_symbols_md.scripts_ops_destroy_check_py.collect_cloud_functions.l2480 | evidence/03_symbols.md | 2480-2480 |
| ev.03_symbols_md.scripts_ops_destroy_check_py.collect_eventarc_triggers.l2481 | evidence/03_symbols.md | 2481-2481 |
| ev.03_symbols_md.scripts_ops_destroy_check_py.collect_pubsub_topics.l2482 | evidence/03_symbols.md | 2482-2482 |
| ev.03_symbols_md.scripts_ops_destroy_check_py.collect_pubsub_subscriptions.l2483 | evidence/03_symbols.md | 2483-2483 |
| ev.03_symbols_md.scripts_ops_destroy_check_py.collect_buckets.l2484 | evidence/03_symbols.md | 2484-2484 |
| ev.03_symbols_md.scripts_ops_destroy_check_py.collect_artifact_repos.l2485 | evidence/03_symbols.md | 2485-2485 |
| ev.03_symbols_md.scripts_ops_destroy_check_py.collect_bq_datasets.l2486 | evidence/03_symbols.md | 2486-2486 |
| ev.03_symbols_md.scripts_ops_destroy_check_py.classify_bucket_names.l2487 | evidence/03_symbols.md | 2487-2487 |
| ev.03_symbols_md.scripts_ops_destroy_check_py.classify_artifact_repos.l2488 | evidence/03_symbols.md | 2488-2488 |
| ev.03_symbols_md.scripts_ops_destroy_check_py.filter_high_cost_datasets.l2489 | evidence/03_symbols.md | 2489-2489 |
| ev.03_symbols_md.scripts_ops_destroy_check_py.evaluate.l2490 | evidence/03_symbols.md | 2490-2490 |
| ev.03_symbols_md.scripts_ops_destroy_check_py.render_text.l2491 | evidence/03_symbols.md | 2491-2491 |
| ev.03_symbols_md.scripts_ops_destroy_check_py.render_json.l2492 | evidence/03_symbols.md | 2492-2492 |
| ev.03_symbols_md.scripts_ops_destroy_check_py.collect_findings.l2493 | evidence/03_symbols.md | 2493-2493 |
| ev.03_symbols_md.scripts_ops_destroy_check_py.main.l2494 | evidence/03_symbols.md | 2494-2494 |
| ev.03_symbols_md.scripts_ops_feedback_py.main.l2498 | evidence/03_symbols.md | 2498-2498 |
| ev.03_symbols_md.scripts_ops_label_seed_py.main.l2502 | evidence/03_symbols.md | 2502-2502 |
| ev.03_symbols_md.scripts_ops_livez_py.main.l2506 | evidence/03_symbols.md | 2506-2506 |
| ev.03_symbols_md.scripts_ops_promote_py.log.l2510 | evidence/03_symbols.md | 2510-2510 |
| ev.03_symbols_md.scripts_ops_promote_py.resolve_display_name.l2511 | evidence/03_symbols.md | 2511-2511 |
| ev.03_symbols_md.scripts_ops_promote_py.list_versions.l2512 | evidence/03_symbols.md | 2512-2512 |
| ev.03_symbols_md.scripts_ops_promote_py.model_id_of.l2513 | evidence/03_symbols.md | 2513-2513 |
| ev.03_symbols_md.scripts_ops_promote_py.select_version.l2514 | evidence/03_symbols.md | 2514-2514 |
| ev.03_symbols_md.scripts_ops_promote_py.gsutil_ls.l2515 | evidence/03_symbols.md | 2515-2515 |
| ev.03_symbols_md.scripts_ops_promote_py.bst_rename_if_needed.l2516 | evidence/03_symbols.md | 2516-2516 |
| ev.03_symbols_md.scripts_ops_promote_py.set_production_alias.l2517 | evidence/03_symbols.md | 2517-2517 |
| ev.03_symbols_md.scripts_ops_promote_py.run_alias.l2518 | evidence/03_symbols.md | 2518-2518 |
| ev.03_symbols_md.scripts_ops_promote_py.env_fallback.l2519 | evidence/03_symbols.md | 2519-2519 |
| ev.03_symbols_md.scripts_ops_promote_py.env_flag.l2520 | evidence/03_symbols.md | 2520-2520 |
| ev.03_symbols_md.scripts_ops_promote_py.main.l2521 | evidence/03_symbols.md | 2521-2521 |
| ev.03_symbols_md.scripts_ops_ranking_py.main.l2525 | evidence/03_symbols.md | 2525-2525 |
| ev.03_symbols_md.scripts_ops_register_model_py.latest_pipeline_run.l2529 | evidence/03_symbols.md | 2529-2529 |
| ev.03_symbols_md.scripts_ops_register_model_py.resolve_model_uri_from_gcs.l2530 | evidence/03_symbols.md | 2530-2530 |
| ev.03_symbols_md.scripts_ops_register_model_py.upload_model.l2531 | evidence/03_symbols.md | 2531-2531 |
| ev.03_symbols_md.scripts_ops_register_model_py.main.l2532 | evidence/03_symbols.md | 2532-2532 |
| ev.03_symbols_md.scripts_ops_run_all_py.run_make.l2536 | evidence/03_symbols.md | 2536-2536 |
| ev.03_symbols_md.scripts_ops_run_all_py.main.l2537 | evidence/03_symbols.md | 2537-2537 |
| ev.03_symbols_md.scripts_ops_search_py.search_once.l2541 | evidence/03_symbols.md | 2541-2541 |
| ev.03_symbols_md.scripts_ops_search_py.main.l2542 | evidence/03_symbols.md | 2542-2542 |
| ev.03_symbols_md.scripts_ops_search_components_py.diagnose_semantic_zero.l2546 | evidence/03_symbols.md | 2546-2546 |
| ev.03_symbols_md.scripts_ops_search_components_py.main.l2547 | evidence/03_symbols.md | 2547-2547 |
| ev.03_symbols_md.scripts_ops_slo_status_py.terraform_output.l2551 | evidence/03_symbols.md | 2551-2551 |
| ev.03_symbols_md.scripts_ops_slo_status_py.default_service_id.l2552 | evidence/03_symbols.md | 2552-2552 |
| ev.03_symbols_md.scripts_ops_slo_status_py.describe_slo.l2553 | evidence/03_symbols.md | 2553-2553 |
| ev.03_symbols_md.scripts_ops_slo_status_py.burn_rate.l2554 | evidence/03_symbols.md | 2554-2554 |
| ev.03_symbols_md.scripts_ops_slo_status_py.main.l2555 | evidence/03_symbols.md | 2555-2555 |
| ev.03_symbols_md.scripts_ops_submit_train_pipeline_py.main.l2559 | evidence/03_symbols.md | 2559-2559 |
| ev.03_symbols_md.scripts_ops_sync_elasticsearch_py.log.l2563 | evidence/03_symbols.md | 2563-2563 |
| ev.03_symbols_md.scripts_ops_sync_elasticsearch_py.headers.l2564 | evidence/03_symbols.md | 2564-2564 |
| ev.03_symbols_md.scripts_ops_sync_elasticsearch_py.ensure_index.l2565 | evidence/03_symbols.md | 2565-2565 |
| ev.03_symbols_md.scripts_ops_sync_elasticsearch_py.bulk_upsert.l2566 | evidence/03_symbols.md | 2566-2566 |
| ev.03_symbols_md.scripts_ops_sync_elasticsearch_py.parse_args.l2567 | evidence/03_symbols.md | 2567-2567 |
| ev.03_symbols_md.scripts_ops_sync_elasticsearch_py.maybe_port_forward_for_cluster_dns.l2568 | evidence/03_symbols.md | 2568-2568 |
| ev.03_symbols_md.scripts_ops_sync_elasticsearch_py.run_sync_with_count.l2569 | evidence/03_symbols.md | 2569-2569 |
| ev.03_symbols_md.scripts_ops_sync_elasticsearch_py.run.l2570 | evidence/03_symbols.md | 2570-2570 |
| ev.03_symbols_md.scripts_ops_sync_elasticsearch_py.main.l2571 | evidence/03_symbols.md | 2571-2571 |
| ev.03_symbols_md.scripts_ops_sync_synonyms_py.log.l2575 | evidence/03_symbols.md | 2575-2575 |
| ev.03_symbols_md.scripts_ops_sync_synonyms_py.gcloud.l2576 | evidence/03_symbols.md | 2576-2576 |
| ev.03_symbols_md.scripts_ops_sync_synonyms_py.resolve_redis_url.l2577 | evidence/03_symbols.md | 2577-2577 |
| ev.03_symbols_md.scripts_ops_sync_synonyms_py.resolve_redis_auth.l2578 | evidence/03_symbols.md | 2578-2578 |
| ev.03_symbols_md.scripts_ops_sync_synonyms_py.parse_args.l2579 | evidence/03_symbols.md | 2579-2579 |
| ev.03_symbols_md.scripts_ops_sync_synonyms_py.load_dictionary.l2580 | evidence/03_symbols.md | 2580-2580 |
| ev.03_symbols_md.scripts_ops_sync_synonyms_py.main.l2581 | evidence/03_symbols.md | 2581-2581 |
| ev.03_symbols_md.scripts_ops_vertex_explain_py.main.l2585 | evidence/03_symbols.md | 2585-2585 |
| ev.03_symbols_md.scripts_ops_vertex_feature_group_py.access_token.l2589 | evidence/03_symbols.md | 2589-2589 |
| ev.03_symbols_md.scripts_ops_vertex_feature_group_py.request_json.l2590 | evidence/03_symbols.md | 2590-2590 |
| ev.03_symbols_md.scripts_ops_vertex_feature_group_py.emit_404_diagnostics.l2591 | evidence/03_symbols.md | 2591-2591 |
| ev.03_symbols_md.scripts_ops_vertex_feature_group_py.canonical_feature_view_name.l2592 | evidence/03_symbols.md | 2592-2592 |
| ev.03_symbols_md.scripts_ops_vertex_feature_group_py.main.l2593 | evidence/03_symbols.md | 2593-2593 |
| ev.03_symbols_md.scripts_ops_vertex_models_list_py.main.l2597 | evidence/03_symbols.md | 2597-2597 |
| ev.03_symbols_md.scripts_ops_vertex_monitoring_py.main.l2601 | evidence/03_symbols.md | 2601-2601 |
| ev.03_symbols_md.scripts_ops_vertex_pipeline_status_py.main.l2605 | evidence/03_symbols.md | 2605-2605 |
| ev.03_symbols_md.scripts_ops_vertex_pipeline_wait_py.state_name.l2609 | evidence/03_symbols.md | 2609-2609 |
| ev.03_symbols_md.scripts_ops_vertex_pipeline_wait_py.latest_job.l2610 | evidence/03_symbols.md | 2610-2610 |
| ev.03_symbols_md.scripts_ops_vertex_pipeline_wait_py.main.l2611 | evidence/03_symbols.md | 2611-2611 |
| ev.03_symbols_md.scripts_ops_vertex_vector_search_py.terraform_output_map.l2615 | evidence/03_symbols.md | 2615-2615 |
| ev.03_symbols_md.scripts_ops_vertex_vector_search_py.build_probe_vector.l2616 | evidence/03_symbols.md | 2616-2616 |
| ev.03_symbols_md.scripts_ops_vertex_vector_search_py.main.l2617 | evidence/03_symbols.md | 2617-2617 |
| ev.03_symbols_md.scripts_setup_backfill_vector_search_index_py.backfillspec.l2621 | evidence/03_symbols.md | 2621-2621 |
| ev.03_symbols_md.scripts_setup_backfill_vector_search_index_py.terraform_output_map.l2622 | evidence/03_symbols.md | 2622-2622 |
| ev.03_symbols_md.scripts_setup_backfill_vector_search_index_py.build_spec.l2623 | evidence/03_symbols.md | 2623-2623 |
| ev.03_symbols_md.scripts_setup_backfill_vector_search_index_py.bq_iter_rows.l2624 | evidence/03_symbols.md | 2624-2624 |
| ev.03_symbols_md.scripts_setup_backfill_vector_search_index_py.to_datapoints.l2625 | evidence/03_symbols.md | 2625-2625 |
| ev.03_symbols_md.scripts_setup_backfill_vector_search_index_py.build_writer.l2626 | evidence/03_symbols.md | 2626-2626 |
| ev.03_symbols_md.scripts_setup_backfill_vector_search_index_py.main.l2627 | evidence/03_symbols.md | 2627-2627 |
| ev.03_symbols_md.scripts_setup_create_schedule_py.build_schedule_specs.l2631 | evidence/03_symbols.md | 2631-2631 |
| ev.03_symbols_md.scripts_setup_create_schedule_py.main.l2632 | evidence/03_symbols.md | 2632-2632 |
| ev.03_symbols_md.scripts_setup_deploy_all_py.deploystep.l2636 | evidence/03_symbols.md | 2636-2636 |
| ev.03_symbols_md.scripts_setup_deploy_all_py.step.l2637 | evidence/03_symbols.md | 2637-2637 |
| ev.03_symbols_md.scripts_setup_deploy_all_py.elapsed_since_step_start.l2638 | evidence/03_symbols.md | 2638-2638 |
| ev.03_symbols_md.scripts_setup_deploy_all_py.step_done.l2639 | evidence/03_symbols.md | 2639-2639 |
| ev.03_symbols_md.scripts_setup_deploy_all_py.run_tf_bootstrap.l2640 | evidence/03_symbols.md | 2640-2640 |
| ev.03_symbols_md.scripts_setup_deploy_all_py.run_tf_init.l2641 | evidence/03_symbols.md | 2641-2641 |
| ev.03_symbols_md.scripts_setup_deploy_all_py.run_recover_wif.l2642 | evidence/03_symbols.md | 2642-2642 |
| ev.03_symbols_md.scripts_setup_deploy_all_py.run_sync_dataform.l2643 | evidence/03_symbols.md | 2643-2643 |
| ev.03_symbols_md.scripts_setup_deploy_all_py.run_tf_plan.l2644 | evidence/03_symbols.md | 2644-2644 |
| ev.03_symbols_md.scripts_setup_deploy_all_py.run_tf_apply.l2645 | evidence/03_symbols.md | 2645-2645 |
| ev.03_symbols_md.scripts_setup_deploy_all_py.run_seed_lgbm_model.l2646 | evidence/03_symbols.md | 2646-2646 |
| ev.03_symbols_md.scripts_setup_deploy_all_py.run_seed_test.l2647 | evidence/03_symbols.md | 2647-2647 |
| ev.03_symbols_md.scripts_setup_deploy_all_py.run_sync_elasticsearch.l2648 | evidence/03_symbols.md | 2648-2648 |
| ev.03_symbols_md.scripts_setup_deploy_all_py.run_trigger_feature_view_sync.l2649 | evidence/03_symbols.md | 2649-2649 |
| ev.03_symbols_md.scripts_setup_deploy_all_py.run_backfill_vvs.l2650 | evidence/03_symbols.md | 2650-2650 |
| ev.03_symbols_md.scripts_setup_deploy_all_py.run_apply_manifests.l2651 | evidence/03_symbols.md | 2651-2651 |
| ev.03_symbols_md.scripts_setup_deploy_all_py.run_overlay_configmap.l2652 | evidence/03_symbols.md | 2652-2652 |
| ev.03_symbols_md.scripts_setup_deploy_all_py.run_composer_deploy_dags.l2653 | evidence/03_symbols.md | 2653-2653 |
| ev.03_symbols_md.scripts_setup_deploy_all_py.run_deploy_api.l2654 | evidence/03_symbols.md | 2654-2654 |
| ev.03_symbols_md.scripts_setup_deploy_all_py.steps.l2655 | evidence/03_symbols.md | 2655-2655 |
| ev.03_symbols_md.scripts_setup_deploy_all_py.parse_args.l2656 | evidence/03_symbols.md | 2656-2656 |
| ev.03_symbols_md.scripts_setup_deploy_all_py.resolve_step_ref.l2657 | evidence/03_symbols.md | 2657-2657 |
| ev.03_symbols_md.scripts_setup_deploy_all_py.main.l2658 | evidence/03_symbols.md | 2658-2658 |
| ev.03_symbols_md.scripts_setup_destroy_all_py.destroystep.l2662 | evidence/03_symbols.md | 2662-2662 |
| ev.03_symbols_md.scripts_setup_destroy_all_py.step.l2663 | evidence/03_symbols.md | 2663-2663 |
| ev.03_symbols_md.scripts_setup_destroy_all_py.elapsed_since_step_start.l2664 | evidence/03_symbols.md | 2664-2664 |
| ev.03_symbols_md.scripts_setup_destroy_all_py.step_done.l2665 | evidence/03_symbols.md | 2665-2665 |
| ev.03_symbols_md.scripts_setup_destroy_all_py.common_vars.l2666 | evidence/03_symbols.md | 2666-2666 |
| ev.03_symbols_md.scripts_setup_destroy_all_py.run_seed_clean.l2667 | evidence/03_symbols.md | 2667-2667 |
| ev.03_symbols_md.scripts_setup_destroy_all_py.run_undeploy_vertex_endpoints.l2668 | evidence/03_symbols.md | 2668-2668 |
| ev.03_symbols_md.scripts_setup_destroy_all_py.run_undeploy_vvs_deployed_indexes.l2669 | evidence/03_symbols.md | 2669-2669 |
| ev.03_symbols_md.scripts_setup_destroy_all_py.run_state_rm_persistent_vvs.l2670 | evidence/03_symbols.md | 2670-2670 |
| ev.03_symbols_md.scripts_setup_destroy_all_py.run_wipe_gcs_buckets.l2671 | evidence/03_symbols.md | 2671-2671 |
| ev.03_symbols_md.scripts_setup_destroy_all_py.run_flip_deletion_protection.l2672 | evidence/03_symbols.md | 2672-2672 |
| ev.03_symbols_md.scripts_setup_destroy_all_py.run_destroy_kserve.l2673 | evidence/03_symbols.md | 2673-2673 |
| ev.03_symbols_md.scripts_setup_destroy_all_py.run_destroy_main.l2674 | evidence/03_symbols.md | 2674-2674 |
| ev.03_symbols_md.scripts_setup_destroy_all_py.steps.l2675 | evidence/03_symbols.md | 2675-2675 |
| ev.03_symbols_md.scripts_setup_destroy_all_py.parse_args.l2676 | evidence/03_symbols.md | 2676-2676 |
| ev.03_symbols_md.scripts_setup_destroy_all_py.resolve_step_ref.l2677 | evidence/03_symbols.md | 2677-2677 |
| ev.03_symbols_md.scripts_setup_destroy_all_py.main.l2678 | evidence/03_symbols.md | 2678-2678 |
| ev.03_symbols_md.scripts_setup_doctor_py.version.l2682 | evidence/03_symbols.md | 2682-2682 |
| ev.03_symbols_md.scripts_setup_doctor_py.main.l2683 | evidence/03_symbols.md | 2683-2683 |
| ev.03_symbols_md.scripts_setup_local_hybrid_py.log.l2687 | evidence/03_symbols.md | 2687-2687 |
| ev.03_symbols_md.scripts_setup_local_hybrid_py.http_available.l2688 | evidence/03_symbols.md | 2688-2688 |
| ev.03_symbols_md.scripts_setup_local_hybrid_py.resolve_elasticsearch_url.l2689 | evidence/03_symbols.md | 2689-2689 |
| ev.03_symbols_md.scripts_setup_local_hybrid_py.resolve_elasticsearch_api_key.l2690 | evidence/03_symbols.md | 2690-2690 |
| ev.03_symbols_md.scripts_setup_local_hybrid_py.ensure_local_reranker_model.l2691 | evidence/03_symbols.md | 2691-2691 |
| ev.03_symbols_md.scripts_setup_local_hybrid_py.wait_http.l2692 | evidence/03_symbols.md | 2692-2692 |
| ev.03_symbols_md.scripts_setup_local_hybrid_py.port_in_use.l2693 | evidence/03_symbols.md | 2693-2693 |
| ev.03_symbols_md.scripts_setup_local_hybrid_py.spawn.l2694 | evidence/03_symbols.md | 2694-2694 |
| ev.03_symbols_md.scripts_setup_local_hybrid_py.main.l2695 | evidence/03_symbols.md | 2695-2695 |
| ev.03_symbols_md.scripts_setup_print_github_variables_py.build_variable_rows.l2699 | evidence/03_symbols.md | 2699-2699 |
| ev.03_symbols_md.scripts_setup_print_github_variables_py.build_gh_commands.l2700 | evidence/03_symbols.md | 2700-2700 |
| ev.03_symbols_md.scripts_setup_print_github_variables_py.main.l2701 | evidence/03_symbols.md | 2701-2701 |
| ev.03_symbols_md.scripts_setup_recover_wif_py.gcloud_capture.l2705 | evidence/03_symbols.md | 2705-2705 |
| ev.03_symbols_md.scripts_setup_recover_wif_py.recover.l2706 | evidence/03_symbols.md | 2706-2706 |
| ev.03_symbols_md.scripts_setup_recover_wif_py.main.l2707 | evidence/03_symbols.md | 2707-2707 |
| ev.03_symbols_md.scripts_setup_seed_minimal_py.store_and_load_properties.l2711 | evidence/03_symbols.md | 2711-2711 |
| ev.03_symbols_md.scripts_setup_seed_minimal_py.vec_literal.l2712 | evidence/03_symbols.md | 2712-2712 |
| ev.03_symbols_md.scripts_setup_seed_minimal_py.bq.l2713 | evidence/03_symbols.md | 2713-2713 |
| ev.03_symbols_md.scripts_setup_seed_minimal_py.main.l2714 | evidence/03_symbols.md | 2714-2714 |
| ev.03_symbols_md.scripts_setup_seed_minimal_clean_py.main.l2718 | evidence/03_symbols.md | 2718-2718 |
| ev.03_symbols_md.scripts_setup_setup_model_monitoring_py.build_monitoring_spec.l2722 | evidence/03_symbols.md | 2722-2722 |
| ev.03_symbols_md.scripts_setup_setup_model_monitoring_py.main.l2723 | evidence/03_symbols.md | 2723-2723 |
| ev.03_symbols_md.scripts_setup_tf_apply_py.main.l2727 | evidence/03_symbols.md | 2727-2727 |
| ev.03_symbols_md.scripts_setup_tf_bootstrap_py.main.l2731 | evidence/03_symbols.md | 2731-2731 |
| ev.03_symbols_md.scripts_setup_tf_init_py.main.l2735 | evidence/03_symbols.md | 2735-2735 |
| ev.03_symbols_md.scripts_setup_tf_plan_py.main.l2739 | evidence/03_symbols.md | 2739-2739 |
| ev.03_symbols_md.scripts_setup_upload_encoder_assets_py.build_upload_spec.l2743 | evidence/03_symbols.md | 2743-2743 |
| ev.03_symbols_md.scripts_setup_upload_encoder_assets_py.download_model.l2744 | evidence/03_symbols.md | 2744-2744 |
| ev.03_symbols_md.scripts_setup_upload_encoder_assets_py.iter_local_files.l2745 | evidence/03_symbols.md | 2745-2745 |
| ev.03_symbols_md.scripts_setup_upload_encoder_assets_py.upload_directory.l2746 | evidence/03_symbols.md | 2746-2746 |
| ev.03_symbols_md.scripts_setup_upload_encoder_assets_py.apply.l2747 | evidence/03_symbols.md | 2747-2747 |
| ev.03_symbols_md.scripts_setup_upload_encoder_assets_py.main.l2748 | evidence/03_symbols.md | 2748-2748 |
| ev.03_symbols_md.scripts_verify__runner_py.resolve_log_dir.l2752 | evidence/03_symbols.md | 2752-2752 |
| ev.03_symbols_md.scripts_verify__runner_py.utc_stamp.l2753 | evidence/03_symbols.md | 2753-2753 |
| ev.03_symbols_md.scripts_verify__runner_py.update_symlink.l2754 | evidence/03_symbols.md | 2754-2754 |
| ev.03_symbols_md.scripts_verify__runner_py.run.l2755 | evidence/03_symbols.md | 2755-2755 |
| ev.03_symbols_md.scripts_verify_deploy_all_py.main.l2759 | evidence/03_symbols.md | 2759-2759 |
| ev.03_symbols_md.scripts_verify_destroy_all_py.main.l2763 | evidence/03_symbols.md | 2763-2763 |
| ev.03_symbols_md.scripts_verify_full_recreate_py.main.l2767 | evidence/03_symbols.md | 2767-2767 |
| ev.03_symbols_md.scripts_verify_live_acceptance_py.main.l2771 | evidence/03_symbols.md | 2771-2771 |
| ev.03_symbols_md.system_map_html.wrap.l2775 | evidence/03_symbols.md | 2775-2775 |
| ev.03_symbols_md.system_map_html.subtitle.l2776 | evidence/03_symbols.md | 2776-2776 |
| ev.03_symbols_md.system_map_html.panel.l2777 | evidence/03_symbols.md | 2777-2777 |
| ev.03_symbols_md.system_map_html.stack_chip.l2778 | evidence/03_symbols.md | 2778-2778 |
| ev.03_symbols_md.system_map_html.stack_chip.l2779 | evidence/03_symbols.md | 2779-2779 |
| ev.03_symbols_md.system_map_html.stack_chip.l2780 | evidence/03_symbols.md | 2780-2780 |
| ev.03_symbols_md.system_map_html.stack_chip.l2781 | evidence/03_symbols.md | 2781-2781 |
| ev.03_symbols_md.system_map_html.stack_chip.l2782 | evidence/03_symbols.md | 2782-2782 |
| ev.03_symbols_md.system_map_html.stack_chip.l2783 | evidence/03_symbols.md | 2783-2783 |
| ev.03_symbols_md.system_map_html.stack_chip.l2784 | evidence/03_symbols.md | 2784-2784 |
| ev.03_symbols_md.system_map_html.stack_chip.l2785 | evidence/03_symbols.md | 2785-2785 |
| ev.03_symbols_md.system_map_html.tag_web.l2786 | evidence/03_symbols.md | 2786-2786 |
| ev.03_symbols_md.system_map_html.tag_web.l2787 | evidence/03_symbols.md | 2787-2787 |
| ev.03_symbols_md.system_map_html.tag_web.l2788 | evidence/03_symbols.md | 2788-2788 |
| ev.03_symbols_md.system_map_html.tag_pipeline.l2789 | evidence/03_symbols.md | 2789-2789 |
| ev.03_symbols_md.system_map_html.tag_pipeline.l2790 | evidence/03_symbols.md | 2790-2790 |
| ev.03_symbols_md.system_map_html.tag_pipeline.l2791 | evidence/03_symbols.md | 2791-2791 |
| ev.03_symbols_md.system_map_html.tag_pipeline.l2792 | evidence/03_symbols.md | 2792-2792 |
| ev.03_symbols_md.system_map_html.tag_cli.l2793 | evidence/03_symbols.md | 2793-2793 |
| ev.03_symbols_md.system_map_html.tag_cli.l2794 | evidence/03_symbols.md | 2794-2794 |
| ev.03_symbols_md.system_map_html.tag_cli.l2795 | evidence/03_symbols.md | 2795-2795 |
| ev.03_symbols_md.system_map_html.tag_pipeline.l2796 | evidence/03_symbols.md | 2796-2796 |
| ev.03_symbols_md.system_map_html.tag_pipeline.l2797 | evidence/03_symbols.md | 2797-2797 |
| ev.03_symbols_md.system_map_html.tag_pipeline.l2798 | evidence/03_symbols.md | 2798-2798 |
| ev.03_symbols_md.system_map_html.tag_pipeline.l2799 | evidence/03_symbols.md | 2799-2799 |
| ev.03_symbols_md.system_map_html.tag_cli.l2800 | evidence/03_symbols.md | 2800-2800 |
| ev.03_symbols_md.system_map_html.tag_cli.l2801 | evidence/03_symbols.md | 2801-2801 |
| ev.03_symbols_md.system_map_html.tag_cli.l2802 | evidence/03_symbols.md | 2802-2802 |
| ev.03_symbols_md.system_map_html.tag_cli.l2803 | evidence/03_symbols.md | 2803-2803 |
| ev.03_symbols_md.system_map_html.module.l2804 | evidence/03_symbols.md | 2804-2804 |
| ev.03_symbols_md.system_map_html.tag_domain.l2805 | evidence/03_symbols.md | 2805-2805 |
| ev.03_symbols_md.system_map_html.resp.l2806 | evidence/03_symbols.md | 2806-2806 |
| ev.03_symbols_md.system_map_html.deps.l2807 | evidence/03_symbols.md | 2807-2807 |
| ev.03_symbols_md.system_map_html.deps.l2808 | evidence/03_symbols.md | 2808-2808 |
| ev.03_symbols_md.system_map_html.module.l2809 | evidence/03_symbols.md | 2809-2809 |
| ev.03_symbols_md.system_map_html.tag_domain.l2810 | evidence/03_symbols.md | 2810-2810 |
| ev.03_symbols_md.system_map_html.resp.l2811 | evidence/03_symbols.md | 2811-2811 |
| ev.03_symbols_md.system_map_html.deps.l2812 | evidence/03_symbols.md | 2812-2812 |
| ev.03_symbols_md.system_map_html.module.l2813 | evidence/03_symbols.md | 2813-2813 |
| ev.03_symbols_md.system_map_html.tag_domain.l2814 | evidence/03_symbols.md | 2814-2814 |
| ev.03_symbols_md.system_map_html.resp.l2815 | evidence/03_symbols.md | 2815-2815 |
| ev.03_symbols_md.system_map_html.module.l2816 | evidence/03_symbols.md | 2816-2816 |
| ev.03_symbols_md.system_map_html.tag_domain.l2817 | evidence/03_symbols.md | 2817-2817 |
| ev.03_symbols_md.system_map_html.resp.l2818 | evidence/03_symbols.md | 2818-2818 |
| ev.03_symbols_md.system_map_html.module.l2819 | evidence/03_symbols.md | 2819-2819 |
| ev.03_symbols_md.system_map_html.tag_domain.l2820 | evidence/03_symbols.md | 2820-2820 |
| ev.03_symbols_md.system_map_html.resp.l2821 | evidence/03_symbols.md | 2821-2821 |
| ev.03_symbols_md.system_map_html.module.l2822 | evidence/03_symbols.md | 2822-2822 |
| ev.03_symbols_md.system_map_html.tag_domain.l2823 | evidence/03_symbols.md | 2823-2823 |
| ev.03_symbols_md.system_map_html.resp.l2824 | evidence/03_symbols.md | 2824-2824 |
| ev.03_symbols_md.system_map_html.module.l2825 | evidence/03_symbols.md | 2825-2825 |
| ev.03_symbols_md.system_map_html.tag_domain.l2826 | evidence/03_symbols.md | 2826-2826 |
| ev.03_symbols_md.system_map_html.resp.l2827 | evidence/03_symbols.md | 2827-2827 |
| ev.03_symbols_md.system_map_html.module.l2828 | evidence/03_symbols.md | 2828-2828 |
| ev.03_symbols_md.system_map_html.tag_usecase.l2829 | evidence/03_symbols.md | 2829-2829 |
| ev.03_symbols_md.system_map_html.resp.l2830 | evidence/03_symbols.md | 2830-2830 |
| ev.03_symbols_md.system_map_html.deps.l2831 | evidence/03_symbols.md | 2831-2831 |
| ev.03_symbols_md.system_map_html.module.l2832 | evidence/03_symbols.md | 2832-2832 |
| ev.03_symbols_md.system_map_html.tag_usecase.l2833 | evidence/03_symbols.md | 2833-2833 |
| ev.03_symbols_md.system_map_html.resp.l2834 | evidence/03_symbols.md | 2834-2834 |
| ev.03_symbols_md.system_map_html.module.l2835 | evidence/03_symbols.md | 2835-2835 |
| ev.03_symbols_md.system_map_html.tag_usecase.l2836 | evidence/03_symbols.md | 2836-2836 |
| ev.03_symbols_md.system_map_html.resp.l2837 | evidence/03_symbols.md | 2837-2837 |
| ev.03_symbols_md.system_map_html.module.l2838 | evidence/03_symbols.md | 2838-2838 |
| ev.03_symbols_md.system_map_html.tag_usecase.l2839 | evidence/03_symbols.md | 2839-2839 |
| ev.03_symbols_md.system_map_html.resp.l2840 | evidence/03_symbols.md | 2840-2840 |
| ev.03_symbols_md.system_map_html.module.l2841 | evidence/03_symbols.md | 2841-2841 |
| ev.03_symbols_md.system_map_html.tag_usecase.l2842 | evidence/03_symbols.md | 2842-2842 |
| ev.03_symbols_md.system_map_html.resp.l2843 | evidence/03_symbols.md | 2843-2843 |
| ev.03_symbols_md.system_map_html.module.l2844 | evidence/03_symbols.md | 2844-2844 |
| ev.03_symbols_md.system_map_html.tag_port.l2845 | evidence/03_symbols.md | 2845-2845 |
| ev.03_symbols_md.system_map_html.resp.l2846 | evidence/03_symbols.md | 2846-2846 |
| ev.03_symbols_md.system_map_html.module.l2847 | evidence/03_symbols.md | 2847-2847 |
| ev.03_symbols_md.system_map_html.tag_port.l2848 | evidence/03_symbols.md | 2848-2848 |
| ev.03_symbols_md.system_map_html.resp.l2849 | evidence/03_symbols.md | 2849-2849 |
| ev.03_symbols_md.system_map_html.grid_2.l2850 | evidence/03_symbols.md | 2850-2850 |
| ev.03_symbols_md.system_map_html.module.l2851 | evidence/03_symbols.md | 2851-2851 |
| ev.03_symbols_md.system_map_html.module.l2852 | evidence/03_symbols.md | 2852-2852 |
| ev.03_symbols_md.system_map_html.module.l2853 | evidence/03_symbols.md | 2853-2853 |
| ev.03_symbols_md.system_map_html.module.l2854 | evidence/03_symbols.md | 2854-2854 |
| ev.03_symbols_md.system_map_html.module.l2855 | evidence/03_symbols.md | 2855-2855 |
| ev.03_symbols_md.system_map_html.module.l2856 | evidence/03_symbols.md | 2856-2856 |
| ev.03_symbols_md.system_map_html.module.l2857 | evidence/03_symbols.md | 2857-2857 |
| ev.03_symbols_md.system_map_html.module.l2858 | evidence/03_symbols.md | 2858-2858 |
| ev.03_symbols_md.system_map_html.module.l2859 | evidence/03_symbols.md | 2859-2859 |
| ev.03_symbols_md.system_map_html.module.l2860 | evidence/03_symbols.md | 2860-2860 |
| ev.03_symbols_md.system_map_html.module.l2861 | evidence/03_symbols.md | 2861-2861 |
| ev.03_symbols_md.system_map_html.module.l2862 | evidence/03_symbols.md | 2862-2862 |
| ev.03_symbols_md.system_map_html.module.l2863 | evidence/03_symbols.md | 2863-2863 |
| ev.03_symbols_md.system_map_html.module.l2864 | evidence/03_symbols.md | 2864-2864 |
| ev.03_symbols_md.system_map_html.module.l2865 | evidence/03_symbols.md | 2865-2865 |
| ev.03_symbols_md.system_map_html.module.l2866 | evidence/03_symbols.md | 2866-2866 |
| ev.03_symbols_md.system_map_html.module.l2867 | evidence/03_symbols.md | 2867-2867 |
| ev.03_symbols_md.system_map_html.module.l2868 | evidence/03_symbols.md | 2868-2868 |
| ev.03_symbols_md.system_map_html.module.l2869 | evidence/03_symbols.md | 2869-2869 |
| ev.03_symbols_md.system_map_html.module.l2870 | evidence/03_symbols.md | 2870-2870 |
| ev.03_symbols_md.system_map_html.module.l2871 | evidence/03_symbols.md | 2871-2871 |
| ev.03_symbols_md.system_map_html.tag_composition_root.l2872 | evidence/03_symbols.md | 2872-2872 |
| ev.03_symbols_md.system_map_html.resp.l2873 | evidence/03_symbols.md | 2873-2873 |
| ev.03_symbols_md.system_map_html.deps.l2874 | evidence/03_symbols.md | 2874-2874 |
| ev.03_symbols_md.system_map_html.module.l2875 | evidence/03_symbols.md | 2875-2875 |
| ev.03_symbols_md.system_map_html.tag_composition_root.l2876 | evidence/03_symbols.md | 2876-2876 |
| ev.03_symbols_md.system_map_html.resp.l2877 | evidence/03_symbols.md | 2877-2877 |
| ev.03_symbols_md.system_map_html.module.l2878 | evidence/03_symbols.md | 2878-2878 |
| ev.03_symbols_md.system_map_html.tag_composition_root.l2879 | evidence/03_symbols.md | 2879-2879 |
| ev.03_symbols_md.system_map_html.resp.l2880 | evidence/03_symbols.md | 2880-2880 |
| ev.03_symbols_md.system_map_html.module.l2881 | evidence/03_symbols.md | 2881-2881 |
| ev.03_symbols_md.system_map_html.tag_composition_root.l2882 | evidence/03_symbols.md | 2882-2882 |
| ev.03_symbols_md.system_map_html.resp.l2883 | evidence/03_symbols.md | 2883-2883 |
| ev.03_symbols_md.system_map_html.module.l2884 | evidence/03_symbols.md | 2884-2884 |
| ev.03_symbols_md.system_map_html.tag_web.l2885 | evidence/03_symbols.md | 2885-2885 |
| ev.03_symbols_md.system_map_html.resp.l2886 | evidence/03_symbols.md | 2886-2886 |
| ev.03_symbols_md.system_map_html.row.l2887 | evidence/03_symbols.md | 2887-2887 |
| ev.03_symbols_md.system_map_html.tag_web.l2888 | evidence/03_symbols.md | 2888-2888 |
| ev.03_symbols_md.system_map_html.tag_web.l2889 | evidence/03_symbols.md | 2889-2889 |
| ev.03_symbols_md.system_map_html.module.l2890 | evidence/03_symbols.md | 2890-2890 |
| ev.03_symbols_md.system_map_html.tag_web.l2891 | evidence/03_symbols.md | 2891-2891 |
| ev.03_symbols_md.system_map_html.resp.l2892 | evidence/03_symbols.md | 2892-2892 |
| ev.03_symbols_md.system_map_html.module.l2893 | evidence/03_symbols.md | 2893-2893 |
| ev.03_symbols_md.system_map_html.tag_web.l2894 | evidence/03_symbols.md | 2894-2894 |
| ev.03_symbols_md.system_map_html.resp.l2895 | evidence/03_symbols.md | 2895-2895 |
| ev.03_symbols_md.system_map_html.module.l2896 | evidence/03_symbols.md | 2896-2896 |
| ev.03_symbols_md.system_map_html.tag_cli.l2897 | evidence/03_symbols.md | 2897-2897 |
| ev.03_symbols_md.system_map_html.resp.l2898 | evidence/03_symbols.md | 2898-2898 |
| ev.03_symbols_md.system_map_html.module.l2899 | evidence/03_symbols.md | 2899-2899 |
| ev.03_symbols_md.system_map_html.tag_cli.l2900 | evidence/03_symbols.md | 2900-2900 |
| ev.03_symbols_md.system_map_html.resp.l2901 | evidence/03_symbols.md | 2901-2901 |
| ev.03_symbols_md.system_map_html.module.l2902 | evidence/03_symbols.md | 2902-2902 |
| ev.03_symbols_md.system_map_html.tag_cli.l2903 | evidence/03_symbols.md | 2903-2903 |
| ev.03_symbols_md.system_map_html.resp.l2904 | evidence/03_symbols.md | 2904-2904 |
| ev.03_symbols_md.system_map_html.module.l2905 | evidence/03_symbols.md | 2905-2905 |
| ev.03_symbols_md.system_map_html.tag_cli.l2906 | evidence/03_symbols.md | 2906-2906 |
| ev.03_symbols_md.system_map_html.resp.l2907 | evidence/03_symbols.md | 2907-2907 |
| ev.03_symbols_md.system_map_html.module.l2908 | evidence/03_symbols.md | 2908-2908 |
| ev.03_symbols_md.system_map_html.module.l2909 | evidence/03_symbols.md | 2909-2909 |
| ev.03_symbols_md.system_map_html.module.l2910 | evidence/03_symbols.md | 2910-2910 |
| ev.03_symbols_md.system_map_html.module.l2911 | evidence/03_symbols.md | 2911-2911 |
| ev.03_symbols_md.system_map_html.module.l2912 | evidence/03_symbols.md | 2912-2912 |
| ev.03_symbols_md.system_map_html.module.l2913 | evidence/03_symbols.md | 2913-2913 |
| ev.03_symbols_md.system_map_html.module.l2914 | evidence/03_symbols.md | 2914-2914 |
| ev.03_symbols_md.system_map_html.module.l2915 | evidence/03_symbols.md | 2915-2915 |
| ev.03_symbols_md.system_map_html.module.l2916 | evidence/03_symbols.md | 2916-2916 |
| ev.03_symbols_md.system_map_html.module.l2917 | evidence/03_symbols.md | 2917-2917 |
| ev.03_symbols_md.system_map_html.external.l2918 | evidence/03_symbols.md | 2918-2918 |
| ev.03_symbols_md.system_map_html.flow_steps.l2919 | evidence/03_symbols.md | 2919-2919 |
| ev.03_symbols_md.system_map_html.external.l2920 | evidence/03_symbols.md | 2920-2920 |
| ev.03_symbols_md.system_map_html.external.l2921 | evidence/03_symbols.md | 2921-2921 |
| ev.03_symbols_md.system_map_html.flow_steps.l2922 | evidence/03_symbols.md | 2922-2922 |
| ev.03_symbols_md.system_map_html.external.l2923 | evidence/03_symbols.md | 2923-2923 |
| ev.03_symbols_md.system_map_html.external.l2924 | evidence/03_symbols.md | 2924-2924 |
| ev.03_symbols_md.system_map_html.flow_steps.l2925 | evidence/03_symbols.md | 2925-2925 |
| ev.03_symbols_md.system_map_html.external.l2926 | evidence/03_symbols.md | 2926-2926 |
| ev.03_symbols_md.system_map_html.external.l2927 | evidence/03_symbols.md | 2927-2927 |
| ev.03_symbols_md.system_map_html.flow_steps.l2928 | evidence/03_symbols.md | 2928-2928 |
| ev.03_symbols_md.system_map_html.external.l2929 | evidence/03_symbols.md | 2929-2929 |
| ev.03_symbols_md.system_map_html.external.l2930 | evidence/03_symbols.md | 2930-2930 |
| ev.03_symbols_md.system_map_html.flow_steps.l2931 | evidence/03_symbols.md | 2931-2931 |
| ev.03_symbols_md.system_map_html.external.l2932 | evidence/03_symbols.md | 2932-2932 |
| ev.03_symbols_md.system_map_html.external.l2933 | evidence/03_symbols.md | 2933-2933 |
| ev.03_symbols_md.system_map_html.flow_steps.l2934 | evidence/03_symbols.md | 2934-2934 |
| ev.03_symbols_md.system_map_html.external.l2935 | evidence/03_symbols.md | 2935-2935 |
| ev.03_symbols_md.system_map_html.external.l2936 | evidence/03_symbols.md | 2936-2936 |
| ev.03_symbols_md.system_map_html.flow_steps.l2937 | evidence/03_symbols.md | 2937-2937 |
| ev.03_symbols_md.system_map_html.external.l2938 | evidence/03_symbols.md | 2938-2938 |
| ev.03_symbols_md.system_map_html.external.l2939 | evidence/03_symbols.md | 2939-2939 |
| ev.03_symbols_md.system_map_html.flow_steps.l2940 | evidence/03_symbols.md | 2940-2940 |
| ev.03_symbols_md.system_map_html.external.l2941 | evidence/03_symbols.md | 2941-2941 |
| ev.03_symbols_md.system_map_html.external.l2942 | evidence/03_symbols.md | 2942-2942 |
| ev.03_symbols_md.system_map_html.flow_steps.l2943 | evidence/03_symbols.md | 2943-2943 |
| ev.03_symbols_md.system_map_html.external.l2944 | evidence/03_symbols.md | 2944-2944 |
| ev.03_symbols_md.system_map_html.external.l2945 | evidence/03_symbols.md | 2945-2945 |
| ev.03_symbols_md.system_map_html.flow_steps.l2946 | evidence/03_symbols.md | 2946-2946 |
| ev.03_symbols_md.system_map_html.external.l2947 | evidence/03_symbols.md | 2947-2947 |
| ev.03_symbols_md.system_map_html.panel.l2948 | evidence/03_symbols.md | 2948-2948 |
| ev.03_symbols_md.system_map_html.small.l2949 | evidence/03_symbols.md | 2949-2949 |
| ev.03_symbols_md.system_map_html.small.l2950 | evidence/03_symbols.md | 2950-2950 |
| ev.03_symbols_md.system_map_html.small.l2951 | evidence/03_symbols.md | 2951-2951 |
| ev.03_symbols_md.system_map_html.small.l2952 | evidence/03_symbols.md | 2952-2952 |
| ev.03_symbols_md.system_map_html.panel.l2953 | evidence/03_symbols.md | 2953-2953 |
| ev.03_symbols_md.system_map_html.risk_row.l2954 | evidence/03_symbols.md | 2954-2954 |
| ev.03_symbols_md.system_map_html.risk_row.l2955 | evidence/03_symbols.md | 2955-2955 |
| ev.03_symbols_md.system_map_html.risk_row.l2956 | evidence/03_symbols.md | 2956-2956 |
| ev.03_symbols_md.system_map_html.risk_row.l2957 | evidence/03_symbols.md | 2957-2957 |
| ev.03_symbols_md.system_map_html.risk_row.l2958 | evidence/03_symbols.md | 2958-2958 |
| ev.03_symbols_md.system_map_html.risk_row.l2959 | evidence/03_symbols.md | 2959-2959 |
| ev.03_symbols_md.system_map_html.risk_row.l2960 | evidence/03_symbols.md | 2960-2960 |
| ev.03_symbols_md.system_map_html.risk_row.l2961 | evidence/03_symbols.md | 2961-2961 |
| ev.03_symbols_md.system_map_html.risk_row.l2962 | evidence/03_symbols.md | 2962-2962 |
| ev.03_symbols_md.system_map_html.risk_row.l2963 | evidence/03_symbols.md | 2963-2963 |
| ev.03_symbols_md.system_map_html.risk_row.l2964 | evidence/03_symbols.md | 2964-2964 |
| ev.03_symbols_md.system_map_html.risk_row.l2965 | evidence/03_symbols.md | 2965-2965 |
| ev.03_symbols_md.system_map_html.panel.l2966 | evidence/03_symbols.md | 2966-2966 |
| ev.03_symbols_md.system_map_html.spacer.l2967 | evidence/03_symbols.md | 2967-2967 |
| ev.03_symbols_md.system_map_html.small.l2968 | evidence/03_symbols.md | 2968-2968 |
| ev.03_symbols_md.tests__fakes_in_memory_candidate_retriever_py.inmemorycandidateretriever.l2972 | evidence/03_symbols.md | 2972-2972 |
| ev.03_symbols_md.tests__fakes_in_memory_candidate_retriever_py.init.l2973 | evidence/03_symbols.md | 2973-2973 |
| ev.03_symbols_md.tests__fakes_in_memory_candidate_retriever_py.retrieve.l2974 | evidence/03_symbols.md | 2974-2974 |
| ev.03_symbols_md.tests__fakes_in_memory_candidate_retriever_py.retrievecall.l2975 | evidence/03_symbols.md | 2975-2975 |
| ev.03_symbols_md.tests__fakes_in_memory_candidate_retriever_py.init.l2976 | evidence/03_symbols.md | 2976-2976 |
| ev.03_symbols_md.tests__fakes_in_memory_event_writer_py.inmemoryeventwriter.l2980 | evidence/03_symbols.md | 2980-2980 |
| ev.03_symbols_md.tests__fakes_in_memory_event_writer_py.init.l2981 | evidence/03_symbols.md | 2981-2981 |
| ev.03_symbols_md.tests__fakes_in_memory_event_writer_py.emit_search_event.l2982 | evidence/03_symbols.md | 2982-2982 |
| ev.03_symbols_md.tests__fakes_in_memory_event_writer_py.emit_impression.l2983 | evidence/03_symbols.md | 2983-2983 |
| ev.03_symbols_md.tests__fakes_in_memory_event_writer_py.emit_user_action.l2984 | evidence/03_symbols.md | 2984-2984 |
| ev.03_symbols_md.tests__fakes_in_memory_event_writer_py.raise_if_needed.l2985 | evidence/03_symbols.md | 2985-2985 |
| ev.03_symbols_md.tests__fakes_in_memory_feature_fetcher_py.inmemoryfeaturefetcher.l2989 | evidence/03_symbols.md | 2989-2989 |
| ev.03_symbols_md.tests__fakes_in_memory_feature_fetcher_py.init.l2990 | evidence/03_symbols.md | 2990-2990 |
| ev.03_symbols_md.tests__fakes_in_memory_feature_fetcher_py.fetch.l2991 | evidence/03_symbols.md | 2991-2991 |
| ev.03_symbols_md.tests__fakes_in_memory_feedback_recorder_py.feedbackevent.l2995 | evidence/03_symbols.md | 2995-2995 |
| ev.03_symbols_md.tests__fakes_in_memory_feedback_recorder_py.inmemoryfeedbackrecorder.l2996 | evidence/03_symbols.md | 2996-2996 |
| ev.03_symbols_md.tests__fakes_in_memory_feedback_recorder_py.init.l2997 | evidence/03_symbols.md | 2997-2997 |
| ev.03_symbols_md.tests__fakes_in_memory_feedback_recorder_py.record.l2998 | evidence/03_symbols.md | 2998-2998 |
| ev.03_symbols_md.tests__fakes_in_memory_lexical_search_py.inmemorylexicalsearch.l3002 | evidence/03_symbols.md | 3002-3002 |
| ev.03_symbols_md.tests__fakes_in_memory_lexical_search_py.init.l3003 | evidence/03_symbols.md | 3003-3003 |
| ev.03_symbols_md.tests__fakes_in_memory_lexical_search_py.search.l3004 | evidence/03_symbols.md | 3004-3004 |
| ev.03_symbols_md.tests__fakes_in_memory_lexical_search_py.lexicalcall.l3005 | evidence/03_symbols.md | 3005-3005 |
| ev.03_symbols_md.tests__fakes_in_memory_lexical_search_py.init.l3006 | evidence/03_symbols.md | 3006-3006 |
| ev.03_symbols_md.tests__fakes_in_memory_metrics_repository_py.inmemorymetricsrepository.l3010 | evidence/03_symbols.md | 3010-3010 |
| ev.03_symbols_md.tests__fakes_in_memory_metrics_repository_py.init.l3011 | evidence/03_symbols.md | 3011-3011 |
| ev.03_symbols_md.tests__fakes_in_memory_metrics_repository_py.write_evaluation_metrics.l3012 | evidence/03_symbols.md | 3012-3012 |
| ev.03_symbols_md.tests__fakes_in_memory_metrics_repository_py.read_evaluation_metrics.l3013 | evidence/03_symbols.md | 3013-3013 |
| ev.03_symbols_md.tests__fakes_in_memory_metrics_repository_py.latest_metrics.l3014 | evidence/03_symbols.md | 3014-3014 |
| ev.03_symbols_md.tests__fakes_in_memory_metrics_repository_py.metrics.l3015 | evidence/03_symbols.md | 3015-3015 |
| ev.03_symbols_md.tests__fakes_in_memory_ranking_log_publisher_py.rankinglogcall.l3019 | evidence/03_symbols.md | 3019-3019 |
| ev.03_symbols_md.tests__fakes_in_memory_ranking_log_publisher_py.inmemoryrankinglogpublisher.l3020 | evidence/03_symbols.md | 3020-3020 |
| ev.03_symbols_md.tests__fakes_in_memory_ranking_log_publisher_py.init.l3021 | evidence/03_symbols.md | 3021-3021 |
| ev.03_symbols_md.tests__fakes_in_memory_ranking_log_publisher_py.publish_candidates.l3022 | evidence/03_symbols.md | 3022-3022 |
| ev.03_symbols_md.tests__fakes_in_memory_semantic_search_py.inmemorysemanticsearch.l3026 | evidence/03_symbols.md | 3026-3026 |
| ev.03_symbols_md.tests__fakes_in_memory_semantic_search_py.init.l3027 | evidence/03_symbols.md | 3027-3027 |
| ev.03_symbols_md.tests__fakes_in_memory_semantic_search_py.search.l3028 | evidence/03_symbols.md | 3028-3028 |
| ev.03_symbols_md.tests__fakes_in_memory_semantic_search_py.semanticcall.l3029 | evidence/03_symbols.md | 3029-3029 |
| ev.03_symbols_md.tests__fakes_in_memory_semantic_search_py.init.l3030 | evidence/03_symbols.md | 3030-3030 |
| ev.03_symbols_md.tests__fakes_in_memory_training_dataset_repository_py.inmemorytrainingdatasetrepository.l3034 | evidence/03_symbols.md | 3034-3034 |
| ev.03_symbols_md.tests__fakes_in_memory_training_dataset_repository_py.init.l3035 | evidence/03_symbols.md | 3035-3035 |
| ev.03_symbols_md.tests__fakes_in_memory_training_dataset_repository_py.write_training_dataset.l3036 | evidence/03_symbols.md | 3036-3036 |
| ev.03_symbols_md.tests__fakes_in_memory_training_dataset_repository_py.read_training_dataset.l3037 | evidence/03_symbols.md | 3037-3037 |
| ev.03_symbols_md.tests__fakes_in_memory_training_dataset_repository_py.latest_training_dataset.l3038 | evidence/03_symbols.md | 3038-3038 |
| ev.03_symbols_md.tests__fakes_in_memory_training_dataset_repository_py.refs.l3039 | evidence/03_symbols.md | 3039-3039 |
| ev.03_symbols_md.tests__fakes_mock_prediction_publisher_py.mockpredictionpublisher.l3043 | evidence/03_symbols.md | 3043-3043 |
| ev.03_symbols_md.tests__fakes_mock_prediction_publisher_py.init.l3044 | evidence/03_symbols.md | 3044-3044 |
| ev.03_symbols_md.tests__fakes_mock_prediction_publisher_py.publish.l3045 | evidence/03_symbols.md | 3045-3045 |
| ev.03_symbols_md.tests__fakes_mock_reranker_client_py.mockrerankerclient.l3049 | evidence/03_symbols.md | 3049-3049 |
| ev.03_symbols_md.tests__fakes_mock_reranker_client_py.init.l3050 | evidence/03_symbols.md | 3050-3050 |
| ev.03_symbols_md.tests__fakes_mock_reranker_client_py.scores.l3051 | evidence/03_symbols.md | 3051-3051 |
| ev.03_symbols_md.tests__fakes_mock_reranker_client_py.predict.l3052 | evidence/03_symbols.md | 3052-3052 |
| ev.03_symbols_md.tests__fakes_mock_reranker_client_py.predict_with_explain.l3053 | evidence/03_symbols.md | 3053-3053 |
| ev.03_symbols_md.tests__fakes_stub_encoder_client_py.stubencoderclient.l3057 | evidence/03_symbols.md | 3057-3057 |
| ev.03_symbols_md.tests__fakes_stub_encoder_client_py.init.l3058 | evidence/03_symbols.md | 3058-3058 |
| ev.03_symbols_md.tests__fakes_stub_encoder_client_py.embed.l3059 | evidence/03_symbols.md | 3059-3059 |
| ev.03_symbols_md.tests__fakes_stub_encoder_client_py.encodercall.l3060 | evidence/03_symbols.md | 3060-3060 |
| ev.03_symbols_md.tests__fakes_stub_encoder_client_py.init.l3061 | evidence/03_symbols.md | 3061-3061 |
| ev.03_symbols_md.tests__fakes_stub_encoder_client_py.repr.l3062 | evidence/03_symbols.md | 3062-3062 |
| ev.03_symbols_md.tests__fakes_stub_popularity_scorer_py.stubpopularityscorer.l3066 | evidence/03_symbols.md | 3066-3066 |
| ev.03_symbols_md.tests__fakes_stub_popularity_scorer_py.init.l3067 | evidence/03_symbols.md | 3067-3067 |
| ev.03_symbols_md.tests__fakes_stub_popularity_scorer_py.score.l3068 | evidence/03_symbols.md | 3068-3068 |
| ev.03_symbols_md.tests__fakes_stub_retrain_queries_py.stubretrainqueries.l3072 | evidence/03_symbols.md | 3072-3072 |
| ev.03_symbols_md.tests__fakes_stub_retrain_queries_py.init.l3073 | evidence/03_symbols.md | 3073-3073 |
| ev.03_symbols_md.tests__fakes_stub_retrain_queries_py.last_run_finished_at.l3074 | evidence/03_symbols.md | 3074-3074 |
| ev.03_symbols_md.tests__fakes_stub_retrain_queries_py.feedback_rows_since.l3075 | evidence/03_symbols.md | 3075-3075 |
| ev.03_symbols_md.tests__fakes_stub_retrain_queries_py.ndcg_in_window.l3076 | evidence/03_symbols.md | 3076-3076 |
| ev.03_symbols_md.tests_conftest_py.stubdatacatalogreader.l3080 | evidence/03_symbols.md | 3080-3080 |
| ev.03_symbols_md.tests_conftest_py.read_snapshot.l3081 | evidence/03_symbols.md | 3081-3081 |
| ev.03_symbols_md.tests_conftest_py.fake_settings.l3082 | evidence/03_symbols.md | 3082-3082 |
| ev.03_symbols_md.tests_conftest_py.fake_encoder.l3083 | evidence/03_symbols.md | 3083-3083 |
| ev.03_symbols_md.tests_conftest_py.fake_reranker.l3084 | evidence/03_symbols.md | 3084-3084 |
| ev.03_symbols_md.tests_conftest_py.fake_candidate_retriever.l3085 | evidence/03_symbols.md | 3085-3085 |
| ev.03_symbols_md.tests_conftest_py.fake_ranking_log_publisher.l3086 | evidence/03_symbols.md | 3086-3086 |
| ev.03_symbols_md.tests_conftest_py.fake_feedback_recorder.l3087 | evidence/03_symbols.md | 3087-3087 |
| ev.03_symbols_md.tests_conftest_py.fake_event_writer.l3088 | evidence/03_symbols.md | 3088-3088 |
| ev.03_symbols_md.tests_conftest_py.fake_retrain_queries.l3089 | evidence/03_symbols.md | 3089-3089 |
| ev.03_symbols_md.tests_conftest_py.fake_retrain_publisher.l3090 | evidence/03_symbols.md | 3090-3090 |
| ev.03_symbols_md.tests_conftest_py.fake_feature_fetcher.l3091 | evidence/03_symbols.md | 3091-3091 |
| ev.03_symbols_md.tests_conftest_py.fake_container_factory.l3092 | evidence/03_symbols.md | 3092-3092 |
| ev.03_symbols_md.tests_conftest_py.test_x.l3093 | evidence/03_symbols.md | 3093-3093 |
| ev.03_symbols_md.tests_conftest_py.build.l3094 | evidence/03_symbols.md | 3094-3094 |
| ev.03_symbols_md.tests_conftest_py.fake_container.l3095 | evidence/03_symbols.md | 3095-3095 |
| ev.03_symbols_md.tests_conftest_py.fake_app.l3096 | evidence/03_symbols.md | 3096-3096 |
| ev.03_symbols_md.tests_conftest_py.fake_client.l3097 | evidence/03_symbols.md | 3097-3097 |
| ev.03_symbols_md.tests_e2e_live_acceptance_checks_py.run_live_acceptance_checks.l3101 | evidence/03_symbols.md | 3101-3101 |
| ev.03_symbols_md.tests_e2e_live_acceptance_checks_py.run.l3102 | evidence/03_symbols.md | 3102-3102 |
| ev.03_symbols_md.tests_e2e_test_full_recreate_gate_py.require_full_recreate.l3106 | evidence/03_symbols.md | 3106-3106 |
| ev.03_symbols_md.tests_e2e_test_full_recreate_gate_py.run.l3107 | evidence/03_symbols.md | 3107-3107 |
| ev.03_symbols_md.tests_e2e_test_full_recreate_gate_py.test_full_recreate_acceptance_live.l3108 | evidence/03_symbols.md | 3108-3108 |
| ev.03_symbols_md.tests_e2e_test_live_acceptance_gate_py.require_acceptance_env.l3112 | evidence/03_symbols.md | 3112-3112 |
| ev.03_symbols_md.tests_e2e_test_live_acceptance_gate_py.test_live_acceptance_on_existing_env.l3113 | evidence/03_symbols.md | 3113-3113 |
| ev.03_symbols_md.tests_integration_infra_test_destroy_all_table_parity_py.resources_with_deletion_protection.l3117 | evidence/03_symbols.md | 3117-3117 |
| ev.03_symbols_md.tests_integration_infra_test_destroy_all_table_parity_py.destroy_all_targets.l3118 | evidence/03_symbols.md | 3118-3118 |
| ev.03_symbols_md.tests_integration_infra_test_destroy_all_table_parity_py.destroy_bq_table_names.l3119 | evidence/03_symbols.md | 3119-3119 |
| ev.03_symbols_md.tests_integration_infra_test_destroy_all_table_parity_py.destroy_gke_cluster_names.l3120 | evidence/03_symbols.md | 3120-3120 |
| ev.03_symbols_md.tests_integration_infra_test_destroy_all_table_parity_py.test_every_protected_bq_table_is_in_destroy_all_targets.l3121 | evidence/03_symbols.md | 3121-3121 |
| ev.03_symbols_md.tests_integration_infra_test_destroy_all_table_parity_py.test_destroy_all_bq_targets_do_not_reference_removed_tables.l3122 | evidence/03_symbols.md | 3122-3122 |
| ev.03_symbols_md.tests_integration_infra_test_destroy_all_table_parity_py.test_protected_gke_cluster_is_in_destroy_all_targets.l3123 | evidence/03_symbols.md | 3123-3123 |
| ev.03_symbols_md.tests_integration_infra_test_destroy_all_table_parity_py.test_protected_targets_baseline.l3124 | evidence/03_symbols.md | 3124-3124 |
| ev.03_symbols_md.tests_integration_infra_test_infra_ranker_tables_py.read.l3128 | evidence/03_symbols.md | 3128-3128 |
| ev.03_symbols_md.tests_integration_infra_test_infra_ranker_tables_py.extract_resource_block.l3129 | evidence/03_symbols.md | 3129-3129 |
| ev.03_symbols_md.tests_integration_infra_test_infra_ranker_tables_py.test_property_features_daily_declared.l3130 | evidence/03_symbols.md | 3130-3130 |
| ev.03_symbols_md.tests_integration_infra_test_infra_ranker_tables_py.test_property_embeddings_declared_with_repeated_float64.l3131 | evidence/03_symbols.md | 3131-3131 |
| ev.03_symbols_md.tests_integration_infra_test_infra_ranker_tables_py.test_search_logs_declared.l3132 | evidence/03_symbols.md | 3132-3132 |
| ev.03_symbols_md.tests_integration_infra_test_infra_ranker_tables_py.test_ranking_log_declared_with_dual_cluster.l3133 | evidence/03_symbols.md | 3133-3133 |
| ev.03_symbols_md.tests_integration_infra_test_infra_ranker_tables_py.test_feedback_events_declared.l3134 | evidence/03_symbols.md | 3134-3134 |
| ev.03_symbols_md.tests_integration_infra_test_infra_ranker_tables_py.test_search_events_declared.l3135 | evidence/03_symbols.md | 3135-3135 |
| ev.03_symbols_md.tests_integration_infra_test_infra_ranker_tables_py.test_search_impressions_declared.l3136 | evidence/03_symbols.md | 3136-3136 |
| ev.03_symbols_md.tests_integration_infra_test_infra_ranker_tables_py.test_user_actions_declared.l3137 | evidence/03_symbols.md | 3137-3137 |
| ev.03_symbols_md.tests_integration_infra_test_infra_ranker_tables_py.test_ranking_labels_declared.l3138 | evidence/03_symbols.md | 3138-3138 |
| ev.03_symbols_md.tests_integration_infra_test_infra_ranker_tables_py.test_training_runs_metrics_has_ranker_columns.l3139 | evidence/03_symbols.md | 3139-3139 |
| ev.03_symbols_md.tests_integration_infra_test_infra_ranker_tables_py.test_training_runs_hyperparams_has_lambdarank_fields.l3140 | evidence/03_symbols.md | 3140-3140 |
| ev.03_symbols_md.tests_integration_infra_test_infra_ranker_tables_py.test_legacy_predictions_log_removed.l3141 | evidence/03_symbols.md | 3141-3141 |
| ev.03_symbols_md.tests_integration_infra_test_makefile_py.test_makefile_declares_destroy_coast_down_target.l3145 | evidence/03_symbols.md | 3145-3145 |
| ev.03_symbols_md.tests_integration_infra_test_manifests_structure_py.load.l3149 | evidence/03_symbols.md | 3149-3149 |
| ev.03_symbols_md.tests_integration_infra_test_manifests_structure_py.test_kustomization_lists_every_yaml_under_manifests.l3150 | evidence/03_symbols.md | 3150-3150 |
| ev.03_symbols_md.tests_integration_infra_test_manifests_structure_py.test_search_api_deployment_resource_limits_match_nonnegotiable.l3151 | evidence/03_symbols.md | 3151-3151 |
| ev.03_symbols_md.tests_integration_infra_test_manifests_structure_py.test_search_api_deployment_exposes_kserve_env_vars.l3152 | evidence/03_symbols.md | 3152-3152 |
| ev.03_symbols_md.tests_integration_infra_test_manifests_structure_py.test_search_api_secretstore_uses_gcpsm_provider.l3153 | evidence/03_symbols.md | 3153-3153 |
| ev.03_symbols_md.tests_integration_infra_test_manifests_structure_py.test_search_api_external_secret_syncs_iap_client_secret.l3154 | evidence/03_symbols.md | 3154-3154 |
| ev.03_symbols_md.tests_integration_infra_test_manifests_structure_py.test_search_api_deployment_probes_have_canonical_paths.l3155 | evidence/03_symbols.md | 3155-3155 |
| ev.03_symbols_md.tests_integration_infra_test_manifests_structure_py.test_search_api_hpa_bounds_and_thresholds.l3156 | evidence/03_symbols.md | 3156-3156 |
| ev.03_symbols_md.tests_integration_infra_test_manifests_structure_py.test_search_api_networkpolicy_allows_egress_to_kserve_inference.l3157 | evidence/03_symbols.md | 3157-3157 |
| ev.03_symbols_md.tests_integration_infra_test_manifests_structure_py.test_kserve_inferenceservice_has_correct_shape.l3158 | evidence/03_symbols.md | 3158-3158 |
| ev.03_symbols_md.tests_integration_infra_test_manifests_structure_py.test_kserve_reranker_uses_lightgbm_model_format.l3159 | evidence/03_symbols.md | 3159-3159 |
| ev.03_symbols_md.tests_integration_infra_test_manifests_structure_py.test_kserve_networkpolicy_restricts_ingress_to_search_namespace.l3160 | evidence/03_symbols.md | 3160-3160 |
| ev.03_symbols_md.tests_integration_infra_test_manifests_structure_py.test_search_api_iap_policy_targets_gateway_service_with_gcp_backend_policy.l3161 | evidence/03_symbols.md | 3161-3161 |
| ev.03_symbols_md.tests_integration_infra_test_manifests_structure_py.test_configmap_example_covers_expected_keys.l3162 | evidence/03_symbols.md | 3162-3162 |
| ev.03_symbols_md.tests_integration_infra_test_public_domain_consistency_py.read.l3166 | evidence/03_symbols.md | 3166-3166 |
| ev.03_symbols_md.tests_integration_infra_test_public_domain_consistency_py.setting_value.l3167 | evidence/03_symbols.md | 3167-3167 |
| ev.03_symbols_md.tests_integration_infra_test_public_domain_consistency_py.test_setting_yaml_holds_canonical_domain_and_zone.l3168 | evidence/03_symbols.md | 3168-3168 |
| ev.03_symbols_md.tests_integration_infra_test_public_domain_consistency_py.test_gateway_manifest_uses_setting_public_domain_and_certmap.l3169 | evidence/03_symbols.md | 3169-3169 |
| ev.03_symbols_md.tests_integration_infra_test_public_domain_consistency_py.test_dns_module_has_static_ip_apex_a_and_cert_manager_chain.l3170 | evidence/03_symbols.md | 3170-3170 |
| ev.03_symbols_md.tests_integration_infra_test_public_domain_consistency_py.test_dns_module_defaults_match_gateway_annotation.l3171 | evidence/03_symbols.md | 3171-3171 |
| ev.03_symbols_md.tests_integration_infra_test_public_domain_consistency_py.test_dev_main_wires_dns_module_and_passes_public_domain_everywhere.l3172 | evidence/03_symbols.md | 3172-3172 |
| ev.03_symbols_md.tests_integration_infra_test_public_domain_consistency_py.test_apis_tf_enables_cloud_dns.l3173 | evidence/03_symbols.md | 3173-3173 |
| ev.03_symbols_md.tests_integration_infra_test_public_domain_consistency_py.test_variables_tf_declares_public_domain_and_zone_without_default.l3174 | evidence/03_symbols.md | 3174-3174 |
| ev.03_symbols_md.tests_integration_infra_test_public_domain_consistency_py.test_canonical_tf_var_names_includes_public_domain_and_zone.l3175 | evidence/03_symbols.md | 3175-3175 |
| ev.03_symbols_md.tests_integration_infra_test_public_domain_consistency_py.test_makefile_exports_public_domain_and_zone.l3176 | evidence/03_symbols.md | 3176-3176 |
| ev.03_symbols_md.tests_integration_infra_test_public_domain_consistency_py.test_tf_plan_feeds_terraform_the_canonical_var_set.l3177 | evidence/03_symbols.md | 3177-3177 |
| ev.03_symbols_md.tests_integration_infra_test_public_domain_consistency_py.test_tf_apply_stage1_targets_includes_module_dns.l3178 | evidence/03_symbols.md | 3178-3178 |
| ev.03_symbols_md.tests_integration_infra_test_public_domain_consistency_py.test_build_all_local_is_single_line_script_call.l3179 | evidence/03_symbols.md | 3179-3179 |
| ev.03_symbols_md.tests_integration_infra_test_terraform_module_structure_py.modules.l3183 | evidence/03_symbols.md | 3183-3183 |
| ev.03_symbols_md.tests_integration_infra_test_terraform_module_structure_py.test_module_has_required_file.l3184 | evidence/03_symbols.md | 3184-3184 |
| ev.03_symbols_md.tests_integration_infra_test_terraform_module_structure_py.test_every_variable_has_description.l3185 | evidence/03_symbols.md | 3185-3185 |
| ev.03_symbols_md.tests_integration_infra_test_workflows_structure_py.test_workflow_file_exists.l3189 | evidence/03_symbols.md | 3189-3189 |
| ev.03_symbols_md.tests_integration_infra_test_workflows_structure_py.test_retired_workflows_are_absent.l3190 | evidence/03_symbols.md | 3190-3190 |
| ev.03_symbols_md.tests_integration_infra_test_workflows_structure_py.test_deploy_workflows_request_oidc_token.l3191 | evidence/03_symbols.md | 3191-3191 |
| ev.03_symbols_md.tests_integration_infra_test_workflows_structure_py.test_encoder_image_workflow_paths.l3192 | evidence/03_symbols.md | 3192-3192 |
| ev.03_symbols_md.tests_integration_infra_test_workflows_structure_py.test_reranker_image_workflow_paths.l3193 | evidence/03_symbols.md | 3193-3193 |
| ev.03_symbols_md.tests_integration_infra_test_workflows_structure_py.test_trainer_image_workflow_paths.l3194 | evidence/03_symbols.md | 3194-3194 |
| ev.03_symbols_md.tests_integration_infra_test_workflows_structure_py.test_pipeline_workflow_paths.l3195 | evidence/03_symbols.md | 3195-3195 |
| ev.03_symbols_md.tests_integration_infra_test_workflows_structure_py.test_api_workflow_keeps_broad_filter_and_rolls_out_via_kubectl.l3196 | evidence/03_symbols.md | 3196-3196 |
| ev.03_symbols_md.tests_integration_parity_parity_invariant_py.read_text.l3200 | evidence/03_symbols.md | 3200-3200 |
| ev.03_symbols_md.tests_integration_parity_parity_invariant_py.flat_yaml.l3201 | evidence/03_symbols.md | 3201-3201 |
| ev.03_symbols_md.tests_integration_parity_parity_invariant_py.extract_terraform_block.l3202 | evidence/03_symbols.md | 3202-3202 |
| ev.03_symbols_md.tests_integration_parity_test_api_route_prefixes_py.app_no_lifespan.l3206 | evidence/03_symbols.md | 3206-3206 |
| ev.03_symbols_md.tests_integration_parity_test_api_route_prefixes_py.noopcontainer.l3207 | evidence/03_symbols.md | 3207-3207 |
| ev.03_symbols_md.tests_integration_parity_test_api_route_prefixes_py.build.l3208 | evidence/03_symbols.md | 3208-3208 |
| ev.03_symbols_md.tests_integration_parity_test_api_route_prefixes_py.all_paths.l3209 | evidence/03_symbols.md | 3209-3209 |
| ev.03_symbols_md.tests_integration_parity_test_api_route_prefixes_py.classify.l3210 | evidence/03_symbols.md | 3210-3210 |
| ev.03_symbols_md.tests_integration_parity_test_api_route_prefixes_py.test_all_routes_belong_to_a_known_axis.l3211 | evidence/03_symbols.md | 3211-3211 |
| ev.03_symbols_md.tests_integration_parity_test_api_route_prefixes_py.test_canonical_public_endpoints_exist.l3212 | evidence/03_symbols.md | 3212-3212 |
| ev.03_symbols_md.tests_integration_parity_test_api_route_prefixes_py.test_canonical_ops_endpoints_exist.l3213 | evidence/03_symbols.md | 3213-3213 |
| ev.03_symbols_md.tests_integration_parity_test_api_route_prefixes_py.test_legacy_paths_redirect_to_new_prefix.l3214 | evidence/03_symbols.md | 3214-3214 |
| ev.03_symbols_md.tests_integration_parity_test_api_route_prefixes_py.test_probes_are_not_namespaced.l3215 | evidence/03_symbols.md | 3215-3215 |
| ev.03_symbols_md.tests_integration_parity_test_api_route_prefixes_py.test_metrics_endpoint_at_root.l3216 | evidence/03_symbols.md | 3216-3216 |
| ev.03_symbols_md.tests_integration_parity_test_api_route_prefixes_py.test_legacy_redirects_excluded_from_openapi_schema.l3217 | evidence/03_symbols.md | 3217-3217 |
| ev.03_symbols_md.tests_integration_parity_test_api_route_prefixes_py.test_canonical_paths_appear_in_openapi_schema.l3218 | evidence/03_symbols.md | 3218-3218 |
| ev.03_symbols_md.tests_integration_parity_test_api_route_prefixes_py.test_route_iap_policy_documents_prefix_axes.l3219 | evidence/03_symbols.md | 3219-3219 |
| ev.03_symbols_md.tests_integration_parity_test_codebase_invariants_py.walk_files.l3223 | evidence/03_symbols.md | 3223-3223 |
| ev.03_symbols_md.tests_integration_parity_test_codebase_invariants_py.find_substring_hits.l3224 | evidence/03_symbols.md | 3224-3224 |
| ev.03_symbols_md.tests_integration_parity_test_codebase_invariants_py.test_w2_8_legacy_tokens_absent_in_python_trees.l3225 | evidence/03_symbols.md | 3225-3225 |
| ev.03_symbols_md.tests_integration_parity_test_codebase_invariants_py.test_w2_8_legacy_tokens_absent_in_manifests_yaml.l3226 | evidence/03_symbols.md | 3226-3226 |
| ev.03_symbols_md.tests_integration_parity_test_codebase_invariants_py.test_lexical_es_canonical_no_meilisearch_in_app.l3227 | evidence/03_symbols.md | 3227-3227 |
| ev.03_symbols_md.tests_integration_parity_test_codebase_invariants_py.test_makefile_has_no_removed_sync_meili_target.l3228 | evidence/03_symbols.md | 3228-3228 |
| ev.03_symbols_md.tests_integration_parity_test_codebase_invariants_py.test_pyproject_has_no_sync_meili_console_script.l3229 | evidence/03_symbols.md | 3229-3229 |
| ev.03_symbols_md.tests_integration_parity_test_codebase_invariants_py.test_search_api_deployment_has_no_meili_env_refs.l3230 | evidence/03_symbols.md | 3230-3230 |
| ev.03_symbols_md.tests_integration_parity_test_codebase_invariants_py.test_es_networkpolicy_allows_eck_operator_namespace.l3231 | evidence/03_symbols.md | 3231-3231 |
| ev.03_symbols_md.tests_integration_parity_test_codebase_invariants_py.test_es_manifest_pins_http_and_anonymous_auth.l3232 | evidence/03_symbols.md | 3232-3232 |
| ev.03_symbols_md.tests_integration_parity_test_configmap_drift_py.test_committed_configmap_matches_generator_output.l3236 | evidence/03_symbols.md | 3236-3236 |
| ev.03_symbols_md.tests_integration_parity_test_configmap_drift_py.test_configmap_keys_cover_every_deployment_reference.l3237 | evidence/03_symbols.md | 3237-3237 |
| ev.03_symbols_md.tests_integration_parity_test_configmap_drift_py.test_generated_configmap_keeps_deployment_referenced_keys.l3238 | evidence/03_symbols.md | 3238-3238 |
| ev.03_symbols_md.tests_integration_parity_test_dataform_workflow_settings_py.test_generator_includes_every_required_dataform_key.l3242 | evidence/03_symbols.md | 3242-3242 |
| ev.03_symbols_md.tests_integration_parity_test_dataform_workflow_settings_py.test_generator_values_match_setting_yaml.l3243 | evidence/03_symbols.md | 3243-3243 |
| ev.03_symbols_md.tests_integration_parity_test_dataform_workflow_settings_py.test_setting_yaml_has_all_required_keys.l3244 | evidence/03_symbols.md | 3244-3244 |
| ev.03_symbols_md.tests_integration_parity_test_event_schema_parity_py.test_app_emit_keys_match_domain_action_type.l3248 | evidence/03_symbols.md | 3248-3248 |
| ev.03_symbols_md.tests_integration_parity_test_event_schema_parity_py.test_app_emit_keys_match_pydantic_feedback_request.l3249 | evidence/03_symbols.md | 3249-3249 |
| ev.03_symbols_md.tests_integration_parity_test_event_schema_parity_py.test_app_emit_keys_match_terraform_user_actions_description.l3250 | evidence/03_symbols.md | 3250-3250 |
| ev.03_symbols_md.tests_integration_parity_test_event_schema_parity_py.test_terraform_user_actions_description_excludes_synthetic.l3251 | evidence/03_symbols.md | 3251-3251 |
| ev.03_symbols_md.tests_integration_parity_test_event_schema_parity_py.load_synthetic_yaml.l3252 | evidence/03_symbols.md | 3252-3252 |
| ev.03_symbols_md.tests_integration_parity_test_event_schema_parity_py.test_synthetic_yaml_action_types_match_policy.l3253 | evidence/03_symbols.md | 3253-3253 |
| ev.03_symbols_md.tests_integration_parity_test_event_schema_parity_py.test_synthetic_yaml_weights_match_policy.l3254 | evidence/03_symbols.md | 3254-3254 |
| ev.03_symbols_md.tests_integration_parity_test_event_schema_parity_py.test_synthetic_yaml_label_source_format.l3255 | evidence/03_symbols.md | 3255-3255 |
| ev.03_symbols_md.tests_integration_parity_test_event_schema_parity_py.test_action_weights_is_app_emit_union_synthetic_no_overlap.l3256 | evidence/03_symbols.md | 3256-3256 |
| ev.03_symbols_md.tests_integration_parity_test_event_schema_parity_py.test_canonical_weight_values_pinned.l3257 | evidence/03_symbols.md | 3257-3257 |
| ev.03_symbols_md.tests_integration_parity_test_event_schema_parity_py.test_evaluation_metrics_table_declared.l3258 | evidence/03_symbols.md | 3258-3258 |
| ev.03_symbols_md.tests_integration_parity_test_event_schema_parity_py.test_ranking_labels_description_documents_label_source_canonical.l3259 | evidence/03_symbols.md | 3259-3259 |
| ev.03_symbols_md.tests_integration_parity_test_feature_parity_feature_group_py.extract_feature_group_block.l3263 | evidence/03_symbols.md | 3263-3263 |
| ev.03_symbols_md.tests_integration_parity_test_feature_parity_feature_group_py.extract_feature_group_names.l3264 | evidence/03_symbols.md | 3264-3264 |
| ev.03_symbols_md.tests_integration_parity_test_feature_parity_feature_group_py.extract_feature_group_value_types.l3265 | evidence/03_symbols.md | 3265-3265 |
| ev.03_symbols_md.tests_integration_parity_test_feature_parity_feature_group_py.test_vertex_feature_group_order_matches_property_side_cols.l3266 | evidence/03_symbols.md | 3266-3266 |
| ev.03_symbols_md.tests_integration_parity_test_feature_parity_feature_group_py.test_vertex_feature_group_uses_double_features.l3267 | evidence/03_symbols.md | 3267-3267 |
| ev.03_symbols_md.tests_integration_parity_test_feature_parity_ranking_py.extract_ranking_log_fields.l3271 | evidence/03_symbols.md | 3271-3271 |
| ev.03_symbols_md.tests_integration_parity_test_feature_parity_ranking_py.test_feature_cols_ranker_has_ten_columns.l3272 | evidence/03_symbols.md | 3272-3272 |
| ev.03_symbols_md.tests_integration_parity_test_feature_parity_ranking_py.test_feature_cols_ranker_no_duplicates.l3273 | evidence/03_symbols.md | 3273-3273 |
| ev.03_symbols_md.tests_integration_parity_test_feature_parity_ranking_py.test_build_ranker_features_keys_match_schema_exactly.l3274 | evidence/03_symbols.md | 3274-3274 |
| ev.03_symbols_md.tests_integration_parity_test_feature_parity_ranking_py.test_infra_ranking_log_features_order_matches_schema.l3275 | evidence/03_symbols.md | 3275-3275 |
| ev.03_symbols_md.tests_integration_parity_test_feature_parity_ranking_py.test_infra_ranking_log_features_are_float64_nullable.l3276 | evidence/03_symbols.md | 3276-3276 |
| ev.03_symbols_md.tests_integration_parity_test_feature_parity_ranking_py.test_dataform_property_features_has_behavioral_cols.l3277 | evidence/03_symbols.md | 3277-3277 |
| ev.03_symbols_md.tests_integration_parity_test_feature_parity_sql_ranker_py.extract_unpivot_feature_lists.l3281 | evidence/03_symbols.md | 3281-3281 |
| ev.03_symbols_md.tests_integration_parity_test_feature_parity_sql_ranker_py.test_ranker_sql_file_exists.l3282 | evidence/03_symbols.md | 3282-3282 |
| ev.03_symbols_md.tests_integration_parity_test_feature_parity_sql_ranker_py.test_ranker_sql_has_both_unpivots.l3283 | evidence/03_symbols.md | 3283-3283 |
| ev.03_symbols_md.tests_integration_parity_test_feature_parity_sql_ranker_py.test_ranker_unpivot_matches_property_side_cols.l3284 | evidence/03_symbols.md | 3284-3284 |
| ev.03_symbols_md.tests_integration_parity_test_feature_parity_sql_ranker_py.test_ranker_sql_reads_ranking_log_not_predictions_log.l3285 | evidence/03_symbols.md | 3285-3285 |
| ev.03_symbols_md.tests_integration_pipeline_test_pipeline_compile_py.test_build_embed_pipeline_spec_contains_expected_steps.l3289 | evidence/03_symbols.md | 3289-3289 |
| ev.03_symbols_md.tests_integration_pipeline_test_pipeline_compile_py.test_build_train_pipeline_spec_contains_expected_steps.l3290 | evidence/03_symbols.md | 3290-3290 |
| ev.03_symbols_md.tests_integration_pipeline_test_pipeline_compile_py.test_coerce_parameter_value_handles_primitives_and_json.l3291 | evidence/03_symbols.md | 3291-3291 |
| ev.03_symbols_md.tests_integration_pipeline_test_pipeline_compile_py.test_merge_parameter_values_overrides_defaults.l3292 | evidence/03_symbols.md | 3292-3292 |
| ev.03_symbols_md.tests_integration_workflow_conftest_py.read_repo_file.l3296 | evidence/03_symbols.md | 3296-3296 |
| ev.03_symbols_md.tests_integration_workflow_test_composer_dags_contract_py.test_dag_files_have_valid_python_syntax.l3300 | evidence/03_symbols.md | 3300-3300 |
| ev.03_symbols_md.tests_integration_workflow_test_composer_dags_contract_py.test_dag_files_pin_canonical_schedule_and_dag_id.l3301 | evidence/03_symbols.md | 3301-3301 |
| ev.03_symbols_md.tests_integration_workflow_test_composer_dags_contract_py.test_dag_schedules_are_valid_5_field_cron.l3302 | evidence/03_symbols.md | 3302-3302 |
| ev.03_symbols_md.tests_integration_workflow_test_composer_dags_contract_py.test_dag_schedules_avoid_simultaneous_run.l3303 | evidence/03_symbols.md | 3303-3303 |
| ev.03_symbols_md.tests_integration_workflow_test_composer_dags_contract_py.test_dag_files_avoid_kfp_2_16_module_level_compile_import.l3304 | evidence/03_symbols.md | 3304-3304 |
| ev.03_symbols_md.tests_integration_workflow_test_composer_dags_contract_py.test_retrain_dag_is_canonical_retrain_trigger.l3305 | evidence/03_symbols.md | 3305-3305 |
| ev.03_symbols_md.tests_integration_workflow_test_composer_dags_contract_py.test_dag_files_call_only_existing_scripts.l3306 | evidence/03_symbols.md | 3306-3306 |
| ev.03_symbols_md.tests_integration_workflow_test_composer_dags_contract_py.test_layers_rules_isolate_pipeline_dags_from_app_imports.l3307 | evidence/03_symbols.md | 3307-3307 |
| ev.03_symbols_md.tests_integration_workflow_test_composer_gcloud_json_contract_py.test_extract_json_array_skips_executing_command_prologue.l3311 | evidence/03_symbols.md | 3311-3311 |
| ev.03_symbols_md.tests_integration_workflow_test_composer_gcloud_json_contract_py.test_extract_json_array_prefers_array_of_objects_over_inner_brackets.l3312 | evidence/03_symbols.md | 3312-3312 |
| ev.03_symbols_md.tests_integration_workflow_test_composer_gcloud_json_contract_py.test_extract_json_array_handles_empty_array.l3313 | evidence/03_symbols.md | 3313-3313 |
| ev.03_symbols_md.tests_integration_workflow_test_composer_gcloud_json_contract_py.test_latest_run_id_from_list_runs_finds_manual_run_id.l3314 | evidence/03_symbols.md | 3314-3314 |
| ev.03_symbols_md.tests_integration_workflow_test_composer_gcloud_json_contract_py.test_balanced_array_respects_string_literals_with_brackets.l3315 | evidence/03_symbols.md | 3315-3315 |
| ev.03_symbols_md.tests_integration_workflow_test_composer_gcloud_json_contract_py.test_extract_json_array_missing_array_raises.l3316 | evidence/03_symbols.md | 3316-3316 |
| ev.03_symbols_md.tests_integration_workflow_test_composer_module_contract_py.test_composer_module_exists_with_required_files.l3320 | evidence/03_symbols.md | 3320-3320 |
| ev.03_symbols_md.tests_integration_workflow_test_composer_module_contract_py.test_composer_module_uses_gen3_image_with_enable_flag_gate.l3321 | evidence/03_symbols.md | 3321-3321 |
| ev.03_symbols_md.tests_integration_workflow_test_composer_module_contract_py.test_composer_env_variables_avoid_reserved_names.l3322 | evidence/03_symbols.md | 3322-3322 |
| ev.03_symbols_md.tests_integration_workflow_test_composer_module_contract_py.test_composer_image_version_is_known_supported_form.l3323 | evidence/03_symbols.md | 3323-3323 |
| ev.03_symbols_md.tests_integration_workflow_test_composer_module_contract_py.test_composer_environment_uses_correct_region_var.l3324 | evidence/03_symbols.md | 3324-3324 |
| ev.03_symbols_md.tests_integration_workflow_test_composer_module_contract_py.test_composer_environment_has_proper_create_destroy_timeouts.l3325 | evidence/03_symbols.md | 3325-3325 |
| ev.03_symbols_md.tests_integration_workflow_test_composer_module_contract_py.test_composer_workloads_have_max_count_to_bound_cost.l3326 | evidence/03_symbols.md | 3326-3326 |
| ev.03_symbols_md.tests_integration_workflow_test_composer_module_contract_py.test_composer_module_workloads_config_has_scheduler_web_worker.l3327 | evidence/03_symbols.md | 3327-3327 |
| ev.03_symbols_md.tests_integration_workflow_test_composer_module_contract_py.test_composer_module_outputs_dag_bucket_and_airflow_uri.l3328 | evidence/03_symbols.md | 3328-3328 |
| ev.03_symbols_md.tests_integration_workflow_test_composer_module_contract_py.test_composer_module_wired_into_dev_environment_with_correct_depends_on.l3329 | evidence/03_symbols.md | 3329-3329 |
| ev.03_symbols_md.tests_integration_workflow_test_composer_module_contract_py.test_composer_module_passes_required_terraform_inputs.l3330 | evidence/03_symbols.md | 3330-3330 |
| ev.03_symbols_md.tests_integration_workflow_test_composer_module_contract_py.test_dev_environment_has_composer_variables_and_outputs.l3331 | evidence/03_symbols.md | 3331-3331 |
| ev.03_symbols_md.tests_integration_workflow_test_composer_module_contract_py.test_enable_composer_default_is_flipped_to_true.l3332 | evidence/03_symbols.md | 3332-3332 |
| ev.03_symbols_md.tests_integration_workflow_test_composer_module_contract_py.test_iam_module_provisions_sa_composer_with_required_roles.l3333 | evidence/03_symbols.md | 3333-3333 |
| ev.03_symbols_md.tests_integration_workflow_test_composer_module_contract_py.test_composer_sa_used_in_workload_identity_binding_chain.l3334 | evidence/03_symbols.md | 3334-3334 |
| ev.03_symbols_md.tests_integration_workflow_test_composer_module_contract_py.test_composer_sa_email_consumed_by_module.l3335 | evidence/03_symbols.md | 3335-3335 |
| ev.03_symbols_md.tests_integration_workflow_test_composer_module_contract_py.test_tf_apply_stage1_targets_includes_module_composer.l3336 | evidence/03_symbols.md | 3336-3336 |
| ev.03_symbols_md.tests_integration_workflow_test_composer_module_contract_py.test_composer_deploy_dags_step_inserted_between_overlay_and_deploy_api.l3337 | evidence/03_symbols.md | 3337-3337 |
| ev.03_symbols_md.tests_integration_workflow_test_composer_module_contract_py.test_deploy_all_step_runner_imports_composer_deploy_dags.l3338 | evidence/03_symbols.md | 3338-3338 |
| ev.03_symbols_md.tests_integration_workflow_test_composer_module_contract_py.test_composer_deploy_dags_early_returns_when_disabled.l3339 | evidence/03_symbols.md | 3339-3339 |
| ev.03_symbols_md.tests_integration_workflow_test_composer_module_contract_py.fake_run.l3340 | evidence/03_symbols.md | 3340-3340 |
| ev.03_symbols_md.tests_integration_workflow_test_composer_module_contract_py.test_composer_deploy_dags_uses_gsutil_m_for_parallel_upload.l3341 | evidence/03_symbols.md | 3341-3341 |
| ev.03_symbols_md.tests_integration_workflow_test_composer_module_contract_py.test_composer_dag_bucket_terraform_output_consumed_by_deploy_script.l3342 | evidence/03_symbols.md | 3342-3342 |
| ev.03_symbols_md.tests_integration_workflow_test_composer_module_contract_py.test_makefile_exposes_composer_deploy_dags_and_smoke_targets.l3343 | evidence/03_symbols.md | 3343-3343 |
| ev.03_symbols_md.tests_integration_workflow_test_composer_module_contract_py.test_composer_runner_dockerfile_does_not_bake_setting_yaml.l3344 | evidence/03_symbols.md | 3344-3344 |
| ev.03_symbols_md.tests_integration_workflow_test_composer_module_contract_py.test_make_composer_env_default_matches_terraform_default.l3345 | evidence/03_symbols.md | 3345-3345 |
| ev.03_symbols_md.tests_integration_workflow_test_composer_module_contract_py.test_pyproject_does_not_pull_apache_airflow_into_runtime.l3346 | evidence/03_symbols.md | 3346-3346 |
| ev.03_symbols_md.tests_integration_workflow_test_deploy_all_contract_py.test_deploy_all_step_sequence_pins_one_shot_pdca_contract.l3350 | evidence/03_symbols.md | 3350-3350 |
| ev.03_symbols_md.tests_integration_workflow_test_deploy_all_contract_py.test_deploy_all_seed_test_runs_before_feature_view_sync.l3351 | evidence/03_symbols.md | 3351-3351 |
| ev.03_symbols_md.tests_integration_workflow_test_deploy_all_contract_py.test_deploy_all_overlay_configmap_runs_before_deploy_api.l3352 | evidence/03_symbols.md | 3352-3352 |
| ev.03_symbols_md.tests_integration_workflow_test_deploy_all_contract_py.test_configmap_overlay_injects_live_vertex_outputs.l3353 | evidence/03_symbols.md | 3353-3353 |
| ev.03_symbols_md.tests_integration_workflow_test_deploy_all_contract_py.fake_generate.l3354 | evidence/03_symbols.md | 3354-3354 |
| ev.03_symbols_md.tests_integration_workflow_test_deploy_all_contract_py.test_configmap_overlay_fills_fos_endpoint_from_api_when_terraform_empty.l3355 | evidence/03_symbols.md | 3355-3355 |
| ev.03_symbols_md.tests_integration_workflow_test_deploy_all_contract_py.fake_generate.l3356 | evidence/03_symbols.md | 3356-3356 |
| ev.03_symbols_md.tests_integration_workflow_test_deploy_all_contract_py.test_local_boot_contract_does_not_require_adc_when_search_disabled.l3357 | evidence/03_symbols.md | 3357-3357 |
| ev.03_symbols_md.tests_integration_workflow_test_deploy_all_contract_py.forbidden.l3358 | evidence/03_symbols.md | 3358-3358 |
| ev.03_symbols_md.tests_integration_workflow_test_deploy_all_contract_py.test_run_all_core_pins_canonical_validation_path.l3359 | evidence/03_symbols.md | 3359-3359 |
| ev.03_symbols_md.tests_integration_workflow_test_deploy_all_contract_py.test_wait_for_deployed_index_absent_is_idempotent_on_resume.l3360 | evidence/03_symbols.md | 3360-3360 |
| ev.03_symbols_md.tests_integration_workflow_test_deploy_all_contract_py.test_deploy_all_waits_vertex_feature_store_and_retries_stage1_on_409.l3361 | evidence/03_symbols.md | 3361-3361 |
| ev.03_symbols_md.tests_integration_workflow_test_deploy_all_contract_py.test_run_all_core_steps_all_have_makefile_targets.l3362 | evidence/03_symbols.md | 3362-3362 |
| ev.03_symbols_md.tests_integration_workflow_test_destroy_all_contract_py.test_destroy_all_keeps_pdca_reproducibility_guards.l3366 | evidence/03_symbols.md | 3366-3366 |
| ev.03_symbols_md.tests_integration_workflow_test_destroy_all_contract_py.test_destroy_all_destroy_apply_symmetry.l3367 | evidence/03_symbols.md | 3367-3367 |
| ev.03_symbols_md.tests_integration_workflow_test_destroy_all_contract_py.test_destroy_all_undeploys_vertex_endpoint_models_before_destroy.l3368 | evidence/03_symbols.md | 3368-3368 |
| ev.03_symbols_md.tests_integration_workflow_test_destroy_all_contract_py.test_destroy_all_proactively_undeploys_stale_vvs_indexes.l3369 | evidence/03_symbols.md | 3369-3369 |
| ev.03_symbols_md.tests_integration_workflow_test_destroy_all_contract_py.test_destroy_all_flips_bq_deletion_protection_before_destroy.l3370 | evidence/03_symbols.md | 3370-3370 |
| ev.03_symbols_md.tests_integration_workflow_test_destroy_all_contract_py.test_destroy_all_force_destroys_blocking_gcs_buckets.l3371 | evidence/03_symbols.md | 3371-3371 |
| ev.03_symbols_md.tests_integration_workflow_test_destroy_all_contract_py.test_recover_wif_handles_soft_delete_undelete.l3372 | evidence/03_symbols.md | 3372-3372 |
| ev.03_symbols_md.tests_integration_workflow_test_destroy_all_contract_py.test_sync_elasticsearch_step_waits_for_es_health_first.l3373 | evidence/03_symbols.md | 3373-3373 |
| ev.03_symbols_md.tests_integration_workflow_test_destroy_all_contract_py.test_destroy_all_provides_step_slicing_symmetric_with_deploy_all.l3374 | evidence/03_symbols.md | 3374-3374 |
| ev.03_symbols_md.tests_integration_workflow_test_destroy_all_contract_py.test_tf_apply_invokes_recover_wif_as_pre_step.l3375 | evidence/03_symbols.md | 3375-3375 |
| ev.03_symbols_md.tests_integration_workflow_test_destroy_all_contract_py.test_destroy_all_persists_vvs_index_and_endpoint.l3376 | evidence/03_symbols.md | 3376-3376 |
| ev.03_symbols_md.tests_integration_workflow_test_destroy_all_contract_py.test_no_vertex_pipeline_job_schedule_resource_in_terraform.l3377 | evidence/03_symbols.md | 3377-3377 |
| ev.03_symbols_md.tests_integration_workflow_test_destroy_all_contract_py.test_runbook_documents_emergency_kill_switch_for_composer_gke_cloudrun.l3378 | evidence/03_symbols.md | 3378-3378 |
| ev.03_symbols_md.tests_integration_workflow_test_destroy_all_contract_py.test_runbook_documents_orphan_state_cleanup_after_emergency_delete.l3379 | evidence/03_symbols.md | 3379-3379 |
| ev.03_symbols_md.tests_integration_workflow_test_destroy_all_contract_py.test_deploy_all_invokes_state_recovery_before_tf_apply.l3380 | evidence/03_symbols.md | 3380-3380 |
| ev.03_symbols_md.tests_integration_workflow_test_destroy_all_contract_py.test_state_recovery_iam_sa_mapping_matches_terraform.l3381 | evidence/03_symbols.md | 3381-3381 |
| ev.03_symbols_md.tests_integration_workflow_test_destroy_all_contract_py.test_runbook_warns_against_bare_state_rm_without_state_recovery.l3382 | evidence/03_symbols.md | 3382-3382 |
| ev.03_symbols_md.tests_integration_workflow_test_destroy_all_contract_py.test_destroy_all_lessons_learned_documented_in_roadmap.l3383 | evidence/03_symbols.md | 3383-3383 |
| ev.03_symbols_md.tests_integration_workflow_test_docs_canonical_contract_py.test_canonical_docs_describe_workflow_contract_goals.l3387 | evidence/03_symbols.md | 3387-3387 |
| ev.03_symbols_md.tests_integration_workflow_test_docs_canonical_contract_py.test_composer_canonical_doc_section_exists.l3388 | evidence/03_symbols.md | 3388-3388 |
| ev.03_symbols_md.tests_integration_workflow_test_docs_canonical_contract_py.test_cost_estimate_documented_in_runbook.l3389 | evidence/03_symbols.md | 3389-3389 |
| ev.03_symbols_md.tests_integration_workflow_test_elasticsearch_workflow_contract_py.test_makefile_exposes_sync_elasticsearch_canonical_target.l3393 | evidence/03_symbols.md | 3393-3393 |
| ev.03_symbols_md.tests_integration_workflow_test_elasticsearch_workflow_contract_py.test_run_all_core_keeps_sync_elasticsearch_before_search_smokes.l3394 | evidence/03_symbols.md | 3394-3394 |
| ev.03_symbols_md.tests_integration_workflow_test_elasticsearch_workflow_contract_py.test_deploy_all_sync_elasticsearch_step_wiring_stays_canonical.l3395 | evidence/03_symbols.md | 3395-3395 |
| ev.03_symbols_md.tests_integration_workflow_test_elasticsearch_workflow_contract_py.test_docs_runbook_and_catalog_pin_elasticsearch_workflow.l3396 | evidence/03_symbols.md | 3396-3396 |
| ev.03_symbols_md.tests_integration_workflow_test_ground_truth_contract_py.test_makefile_exposes_ground_truth_targets.l3400 | evidence/03_symbols.md | 3400-3400 |
| ev.03_symbols_md.tests_integration_workflow_test_ground_truth_contract_py.test_kserve_dockerfiles_use_split_ml_extras.l3401 | evidence/03_symbols.md | 3401-3401 |
| ev.03_symbols_md.tests_integration_workflow_test_ground_truth_contract_py.test_training_pipeline_contract_uses_ranking_labels_not_feedback_events.l3402 | evidence/03_symbols.md | 3402-3402 |
| ev.03_symbols_md.tests_integration_workflow_test_ground_truth_contract_py.test_dataform_and_app_contract_use_canonical_event_schema.l3403 | evidence/03_symbols.md | 3403-3403 |
| ev.03_symbols_md.tests_integration_workflow_test_infra_apis_contract_py.test_required_apis_cover_all_modules_actually_used.l3407 | evidence/03_symbols.md | 3407-3407 |
| ev.03_symbols_md.tests_integration_workflow_test_infra_apis_contract_py.test_all_modules_use_consistent_region_var.l3408 | evidence/03_symbols.md | 3408-3408 |
| ev.03_symbols_md.tests_integration_workflow_test_infra_apis_contract_py.test_gke_two_stage_apply_pattern_preserved.l3409 | evidence/03_symbols.md | 3409-3409 |
| ev.03_symbols_md.tests_integration_workflow_test_infra_apis_contract_py.test_search_api_image_lifecycle_ignore_changes_pinned.l3410 | evidence/03_symbols.md | 3410-3410 |
| ev.03_symbols_md.tests_integration_workflow_test_infra_apis_contract_py.test_ops_vertex_all_includes_vvs_and_feature_view_checks.l3411 | evidence/03_symbols.md | 3411-3411 |
| ev.03_symbols_md.tests_integration_workflow_test_local_workflow_contract_py.test_verify_local_hybrid_recipe_pins_fast_local_order.l3415 | evidence/03_symbols.md | 3415-3415 |
| ev.03_symbols_md.tests_integration_workflow_test_local_workflow_contract_py.test_verify_local_app_contract_pins_local_only_scope.l3416 | evidence/03_symbols.md | 3416-3416 |
| ev.03_symbols_md.tests_integration_workflow_test_local_workflow_contract_py.test_verify_local_ml_contract_pins_local_only_scope.l3417 | evidence/03_symbols.md | 3417-3417 |
| ev.03_symbols_md.tests_integration_workflow_test_local_workflow_contract_py.test_ui_templates_fetch_canonical_api_v1_and_ops_paths.l3418 | evidence/03_symbols.md | 3418-3418 |
| ev.03_symbols_md.tests_integration_workflow_test_local_workflow_contract_py.test_ops_scripts_use_canonical_api_v1_and_ops_paths.l3419 | evidence/03_symbols.md | 3419-3419 |
| ev.03_symbols_md.tests_integration_workflow_test_local_workflow_contract_py.test_readme_documents_local_verification_entrypoints.l3420 | evidence/03_symbols.md | 3420-3420 |
| ev.03_symbols_md.tests_integration_workflow_test_local_workflow_contract_py.test_runbook_pins_local_hybrid_required_env_exports.l3421 | evidence/03_symbols.md | 3421-3421 |
| ev.03_symbols_md.tests_integration_workflow_test_vertex_pipeline_submit_contract_py.test_pipeline_wait_resolves_project_via_common_helper.l3425 | evidence/03_symbols.md | 3425-3425 |
| ev.03_symbols_md.tests_integration_workflow_test_vertex_pipeline_submit_contract_py.test_submit_train_pipeline_resolves_project_via_common_helper.l3426 | evidence/03_symbols.md | 3426-3426 |
| ev.03_symbols_md.tests_integration_workflow_test_vertex_pipeline_submit_contract_py.test_common_documents_gcp_project_precedence_in_resolve_project_id.l3427 | evidence/03_symbols.md | 3427-3427 |
| ev.03_symbols_md.tests_integration_workflow_test_vertex_resources_contract_py.test_vvs_module_lifecycle_protects_against_stale_id_recreation.l3431 | evidence/03_symbols.md | 3431-3431 |
| ev.03_symbols_md.tests_integration_workflow_test_vertex_resources_contract_py.test_vvs_module_min_max_replica_pinned_to_one_for_dev.l3432 | evidence/03_symbols.md | 3432-3432 |
| ev.03_symbols_md.tests_integration_workflow_test_vertex_resources_contract_py.test_feature_view_online_serving_source_is_direct_bigquery.l3433 | evidence/03_symbols.md | 3433-3433 |
| ev.03_symbols_md.tests_integration_workflow_test_vertex_resources_contract_py.test_legacy_cloud_scheduler_demoted_to_monthly_smoke.l3434 | evidence/03_symbols.md | 3434-3434 |
| ev.03_symbols_md.tests_integration_workflow_test_vertex_resources_contract_py.test_legacy_cloud_function_eventarc_marked_as_smoke.l3435 | evidence/03_symbols.md | 3435-3435 |
| ev.03_symbols_md.tests_integration_workflow_test_vertex_resources_contract_py.test_retrain_router_marked_as_smoke_endpoint.l3436 | evidence/03_symbols.md | 3436-3436 |
| ev.03_symbols_md.tests_unit_app_conftest_py.app_with_search_stub.l3440 | evidence/03_symbols.md | 3440-3440 |
| ev.03_symbols_md.tests_unit_app_conftest_py.search_client.l3441 | evidence/03_symbols.md | 3441-3441 |
| ev.03_symbols_md.tests_unit_app_test_adapters_py.fake_httpx_client.l3445 | evidence/03_symbols.md | 3445-3445 |
| ev.03_symbols_md.tests_unit_app_test_adapters_py.test_create_retrain_queries_wires_bigquery_client.l3446 | evidence/03_symbols.md | 3446-3446 |
| ev.03_symbols_md.tests_unit_app_test_adapters_py.test_pubsub_publisher_publishes_json_bytes.l3447 | evidence/03_symbols.md | 3447-3447 |
| ev.03_symbols_md.tests_unit_app_test_adapters_py.test_kserve_encoder_parses_embedding_dict_response_v1.l3448 | evidence/03_symbols.md | 3448-3448 |
| ev.03_symbols_md.tests_unit_app_test_adapters_py.test_kserve_reranker_parses_scalar_scores_v1.l3449 | evidence/03_symbols.md | 3449-3449 |
| ev.03_symbols_md.tests_unit_app_test_adapters_py.test_kserve_encoder_parses_v2_open_inference_response.l3450 | evidence/03_symbols.md | 3450-3450 |
| ev.03_symbols_md.tests_unit_app_test_adapters_py.test_kserve_reranker_predict_with_explain_via_predict_route.l3451 | evidence/03_symbols.md | 3451-3451 |
| ev.03_symbols_md.tests_unit_app_test_adapters_py.test_kserve_reranker_predict_with_explain_via_dedicated_url.l3452 | evidence/03_symbols.md | 3452-3452 |
| ev.03_symbols_md.tests_unit_app_test_adapters_py.test_kserve_reranker_predict_with_explain_degrades_when_attrs_missing.l3453 | evidence/03_symbols.md | 3453-3453 |
| ev.03_symbols_md.tests_unit_app_test_adapters_py.test_kserve_reranker_predict_with_explain_empty_instances_short_circuits.l3454 | evidence/03_symbols.md | 3454-3454 |
| ev.03_symbols_md.tests_unit_app_test_adapters_py.test_kserve_reranker_predict_with_explain_v2_degrades_to_predict_only.l3455 | evidence/03_symbols.md | 3455-3455 |
| ev.03_symbols_md.tests_unit_app_test_adapters_py.test_kserve_reranker_satisfies_reranker_explainer_protocol.l3456 | evidence/03_symbols.md | 3456-3456 |
| ev.03_symbols_md.tests_unit_app_test_adapters_py.test_kserve_encoder_rejects_html_error_page_as_non_json.l3457 | evidence/03_symbols.md | 3457-3457 |
| ev.03_symbols_md.tests_unit_app_test_adapters_py.test_kserve_encoder_rejects_empty_embedding_vector.l3458 | evidence/03_symbols.md | 3458-3458 |
| ev.03_symbols_md.tests_unit_app_test_adapters_py.test_kserve_encoder_enforces_768d_by_default.l3459 | evidence/03_symbols.md | 3459-3459 |
| ev.03_symbols_md.tests_unit_app_test_adapters_py.test_kserve_encoder_rejects_nan_in_embedding.l3460 | evidence/03_symbols.md | 3460-3460 |
| ev.03_symbols_md.tests_unit_app_test_adapters_py.test_kserve_encoder_rejects_inf_in_embedding.l3461 | evidence/03_symbols.md | 3461-3461 |
| ev.03_symbols_md.tests_unit_app_test_adapters_py.test_kserve_reranker_rejects_score_count_mismatch.l3462 | evidence/03_symbols.md | 3462-3462 |
| ev.03_symbols_md.tests_unit_app_test_adapters_py.test_kserve_reranker_predict_with_explain_logs_count_mismatch_and_degrades.l3463 | evidence/03_symbols.md | 3463-3463 |
| ev.03_symbols_md.tests_unit_app_test_adapters_py.test_kserve_reranker_parses_v2_attributions_output.l3464 | evidence/03_symbols.md | 3464-3464 |
| ev.03_symbols_md.tests_unit_app_test_api_contract_template_py.search_payload.l3468 | evidence/03_symbols.md | 3468-3468 |
| ev.03_symbols_md.tests_unit_app_test_api_contract_template_py.assert_search_shape.l3469 | evidence/03_symbols.md | 3469-3469 |
| ev.03_symbols_md.tests_unit_app_test_api_contract_template_py.assert_trace_identifier.l3470 | evidence/03_symbols.md | 3470-3470 |
| ev.03_symbols_md.tests_unit_app_test_api_contract_template_py.assert_result_item_required_fields.l3471 | evidence/03_symbols.md | 3471-3471 |
| ev.03_symbols_md.tests_unit_app_test_api_contract_template_py.assert_feedback_shape.l3472 | evidence/03_symbols.md | 3472-3472 |
| ev.03_symbols_md.tests_unit_app_test_api_contract_template_py.replace_search_container.l3473 | evidence/03_symbols.md | 3473-3473 |
| ev.03_symbols_md.tests_unit_app_test_api_contract_template_py.test_api_contract_readyz_returns_ok.l3474 | evidence/03_symbols.md | 3474-3474 |
| ev.03_symbols_md.tests_unit_app_test_api_contract_template_py.test_api_contract_search_success_shape.l3475 | evidence/03_symbols.md | 3475-3475 |
| ev.03_symbols_md.tests_unit_app_test_api_contract_template_py.test_api_contract_search_has_trace_identifier.l3476 | evidence/03_symbols.md | 3476-3476 |
| ev.03_symbols_md.tests_unit_app_test_api_contract_template_py.test_api_contract_search_result_item_required_fields.l3477 | evidence/03_symbols.md | 3477-3477 |
| ev.03_symbols_md.tests_unit_app_test_api_contract_template_py.test_api_contract_feedback_accepts_click.l3478 | evidence/03_symbols.md | 3478-3478 |
| ev.03_symbols_md.tests_unit_app_test_api_contract_template_py.test_api_contract_search_validation_error.l3479 | evidence/03_symbols.md | 3479-3479 |
| ev.03_symbols_md.tests_unit_app_test_api_contract_template_py.test_api_contract_feedback_rejects_unknown_action.l3480 | evidence/03_symbols.md | 3480-3480 |
| ev.03_symbols_md.tests_unit_app_test_api_contract_template_py.test_api_contract_feedback_validation_error.l3481 | evidence/03_symbols.md | 3481-3481 |
| ev.03_symbols_md.tests_unit_app_test_api_contract_template_py.test_api_contract_search_unavailable_behavior.l3482 | evidence/03_symbols.md | 3482-3482 |
| ev.03_symbols_md.tests_unit_app_test_bq_retrain_queries_py.client_with_rows.l3486 | evidence/03_symbols.md | 3486-3486 |
| ev.03_symbols_md.tests_unit_app_test_bq_retrain_queries_py.make_q.l3487 | evidence/03_symbols.md | 3487-3487 |
| ev.03_symbols_md.tests_unit_app_test_bq_retrain_queries_py.test_last_run_finished_at_returns_timestamp.l3488 | evidence/03_symbols.md | 3488-3488 |
| ev.03_symbols_md.tests_unit_app_test_bq_retrain_queries_py.test_last_run_finished_at_returns_none_when_null.l3489 | evidence/03_symbols.md | 3489-3489 |
| ev.03_symbols_md.tests_unit_app_test_bq_retrain_queries_py.test_last_run_finished_at_returns_none_when_empty_result.l3490 | evidence/03_symbols.md | 3490-3490 |
| ev.03_symbols_md.tests_unit_app_test_bq_retrain_queries_py.test_feedback_rows_since_casts_to_int.l3491 | evidence/03_symbols.md | 3491-3491 |
| ev.03_symbols_md.tests_unit_app_test_bq_retrain_queries_py.test_feedback_rows_since_returns_none_on_exception.l3492 | evidence/03_symbols.md | 3492-3492 |
| ev.03_symbols_md.tests_unit_app_test_bq_retrain_queries_py.test_ndcg_in_window_returns_float.l3493 | evidence/03_symbols.md | 3493-3493 |
| ev.03_symbols_md.tests_unit_app_test_bq_retrain_queries_py.test_ndcg_in_window_returns_none_when_no_runs.l3494 | evidence/03_symbols.md | 3494-3494 |
| ev.03_symbols_md.tests_unit_app_test_check_retrain_endpoint_py.fakequeries.l3498 | evidence/03_symbols.md | 3498-3498 |
| ev.03_symbols_md.tests_unit_app_test_check_retrain_endpoint_py.init.l3499 | evidence/03_symbols.md | 3499-3499 |
| ev.03_symbols_md.tests_unit_app_test_check_retrain_endpoint_py.last_run_finished_at.l3500 | evidence/03_symbols.md | 3500-3500 |
| ev.03_symbols_md.tests_unit_app_test_check_retrain_endpoint_py.feedback_rows_since.l3501 | evidence/03_symbols.md | 3501-3501 |
| ev.03_symbols_md.tests_unit_app_test_check_retrain_endpoint_py.ndcg_in_window.l3502 | evidence/03_symbols.md | 3502-3502 |
| ev.03_symbols_md.tests_unit_app_test_check_retrain_endpoint_py.recordingtrigger.l3503 | evidence/03_symbols.md | 3503-3503 |
| ev.03_symbols_md.tests_unit_app_test_check_retrain_endpoint_py.init.l3504 | evidence/03_symbols.md | 3504-3504 |
| ev.03_symbols_md.tests_unit_app_test_check_retrain_endpoint_py.publish.l3505 | evidence/03_symbols.md | 3505-3505 |
| ev.03_symbols_md.tests_unit_app_test_check_retrain_endpoint_py.test_check_retrain_does_nothing_when_fresh.l3506 | evidence/03_symbols.md | 3506-3506 |
| ev.03_symbols_md.tests_unit_app_test_check_retrain_endpoint_py.test_check_retrain_publishes_when_feedback_threshold_exceeded.l3507 | evidence/03_symbols.md | 3507-3507 |
| ev.03_symbols_md.tests_unit_app_test_check_retrain_endpoint_py.test_check_retrain_publishes_when_ndcg_drops.l3508 | evidence/03_symbols.md | 3508-3508 |
| ev.03_symbols_md.tests_unit_app_test_elasticsearch_lexical_py.test_elasticsearch_lexical_maps_hits_to_lexical_result.l3512 | evidence/03_symbols.md | 3512-3512 |
| ev.03_symbols_md.tests_unit_app_test_elasticsearch_lexical_py.test_elasticsearch_lexical_returns_empty_on_exception.l3513 | evidence/03_symbols.md | 3513-3513 |
| ev.03_symbols_md.tests_unit_app_test_event_repositories_py.result_with_rows.l3517 | evidence/03_symbols.md | 3517-3517 |
| ev.03_symbols_md.tests_unit_app_test_event_repositories_py.test_bigquery_event_repository_reads_search_events_with_since_param.l3518 | evidence/03_symbols.md | 3518-3518 |
| ev.03_symbols_md.tests_unit_app_test_event_repositories_py.test_bigquery_event_repository_reads_impressions_and_user_actions.l3519 | evidence/03_symbols.md | 3519-3519 |
| ev.03_symbols_md.tests_unit_app_test_event_repositories_py.test_bigquery_label_repository_write_ranking_labels_merges_rows.l3520 | evidence/03_symbols.md | 3520-3520 |
| ev.03_symbols_md.tests_unit_app_test_event_repositories_py.test_bigquery_label_repository_reads_labels.l3521 | evidence/03_symbols.md | 3521-3521 |
| ev.03_symbols_md.tests_unit_app_test_explain_py.fakeretriever.l3525 | evidence/03_symbols.md | 3525-3525 |
| ev.03_symbols_md.tests_unit_app_test_explain_py.retrieve.l3526 | evidence/03_symbols.md | 3526-3526 |
| ev.03_symbols_md.tests_unit_app_test_explain_py.fakepublisher.l3527 | evidence/03_symbols.md | 3527-3527 |
| ev.03_symbols_md.tests_unit_app_test_explain_py.publish_candidates.l3528 | evidence/03_symbols.md | 3528-3528 |
| ev.03_symbols_md.tests_unit_app_test_explain_py.plainreranker.l3529 | evidence/03_symbols.md | 3529-3529 |
| ev.03_symbols_md.tests_unit_app_test_explain_py.predict.l3530 | evidence/03_symbols.md | 3530-3530 |
| ev.03_symbols_md.tests_unit_app_test_explain_py.explainreranker.l3531 | evidence/03_symbols.md | 3531-3531 |
| ev.03_symbols_md.tests_unit_app_test_explain_py.predict.l3532 | evidence/03_symbols.md | 3532-3532 |
| ev.03_symbols_md.tests_unit_app_test_explain_py.predict_with_explain.l3533 | evidence/03_symbols.md | 3533-3533 |
| ev.03_symbols_md.tests_unit_app_test_explain_py.candidate.l3534 | evidence/03_symbols.md | 3534-3534 |
| ev.03_symbols_md.tests_unit_app_test_explain_py.test_run_search_returns_attributions_when_reranker_supports_explain.l3535 | evidence/03_symbols.md | 3535-3535 |
| ev.03_symbols_md.tests_unit_app_test_explain_py.test_run_search_falls_back_to_no_attributions_when_reranker_lacks_explain.l3536 | evidence/03_symbols.md | 3536-3536 |
| ev.03_symbols_md.tests_unit_app_test_feature_fetcher_adapters_py.make_feature_value.l3540 | evidence/03_symbols.md | 3540-3540 |
| ev.03_symbols_md.tests_unit_app_test_feature_fetcher_adapters_py.make_feature.l3541 | evidence/03_symbols.md | 3541-3541 |
| ev.03_symbols_md.tests_unit_app_test_feature_fetcher_adapters_py.fos_client_returning.l3542 | evidence/03_symbols.md | 3542-3542 |
| ev.03_symbols_md.tests_unit_app_test_feature_fetcher_adapters_py.fetch.l3543 | evidence/03_symbols.md | 3543-3543 |
| ev.03_symbols_md.tests_unit_app_test_feature_fetcher_adapters_py.test_fos_fetcher_extracts_three_known_features.l3544 | evidence/03_symbols.md | 3544-3544 |
| ev.03_symbols_md.tests_unit_app_test_feature_fetcher_adapters_py.test_fos_fetcher_ignores_unknown_feature_names.l3545 | evidence/03_symbols.md | 3545-3545 |
| ev.03_symbols_md.tests_unit_app_test_feature_fetcher_adapters_py.test_fos_fetcher_returns_all_none_when_per_id_call_raises.l3546 | evidence/03_symbols.md | 3546-3546 |
| ev.03_symbols_md.tests_unit_app_test_feature_fetcher_adapters_py.fetch.l3547 | evidence/03_symbols.md | 3547-3547 |
| ev.03_symbols_md.tests_unit_app_test_feature_fetcher_adapters_py.test_fos_fetcher_returns_empty_for_empty_input.l3548 | evidence/03_symbols.md | 3548-3548 |
| ev.03_symbols_md.tests_unit_app_test_feature_fetcher_adapters_py.test_fos_fetcher_raises_when_endpoint_resolver_returns_empty.l3549 | evidence/03_symbols.md | 3549-3549 |
| ev.03_symbols_md.tests_unit_app_test_feature_fetcher_adapters_py.test_fos_fetcher_rejects_empty_feature_view.l3550 | evidence/03_symbols.md | 3550-3550 |
| ev.03_symbols_md.tests_unit_app_test_feature_fetcher_adapters_py.test_fos_fetcher_canonicalizes_feature_view_name_via_admin_lookup.l3551 | evidence/03_symbols.md | 3551-3551 |
| ev.03_symbols_md.tests_unit_app_test_feature_fetcher_adapters_py.adminclient.l3552 | evidence/03_symbols.md | 3552-3552 |
| ev.03_symbols_md.tests_unit_app_test_feature_fetcher_adapters_py.init.l3553 | evidence/03_symbols.md | 3553-3553 |
| ev.03_symbols_md.tests_unit_app_test_feature_fetcher_adapters_py.get_feature_view.l3554 | evidence/03_symbols.md | 3554-3554 |
| ev.03_symbols_md.tests_unit_app_test_feature_fetcher_adapters_py.datakey.l3555 | evidence/03_symbols.md | 3555-3555 |
| ev.03_symbols_md.tests_unit_app_test_feature_fetcher_adapters_py.init.l3556 | evidence/03_symbols.md | 3556-3556 |
| ev.03_symbols_md.tests_unit_app_test_feature_fetcher_adapters_py.request.l3557 | evidence/03_symbols.md | 3557-3557 |
| ev.03_symbols_md.tests_unit_app_test_feature_fetcher_adapters_py.init.l3558 | evidence/03_symbols.md | 3558-3558 |
| ev.03_symbols_md.tests_unit_app_test_feature_fetcher_adapters_py.servingclient.l3559 | evidence/03_symbols.md | 3559-3559 |
| ev.03_symbols_md.tests_unit_app_test_feature_fetcher_adapters_py.init.l3560 | evidence/03_symbols.md | 3560-3560 |
| ev.03_symbols_md.tests_unit_app_test_feature_fetcher_adapters_py.fetch_feature_values.l3561 | evidence/03_symbols.md | 3561-3561 |
| ev.03_symbols_md.tests_unit_app_test_feedback_handler_http_py.test_feedback_endpoint_records_event.l3565 | evidence/03_symbols.md | 3565-3565 |
| ev.03_symbols_md.tests_unit_app_test_feedback_handler_http_py.test_feedback_endpoint_rejects_invalid_action.l3566 | evidence/03_symbols.md | 3566-3566 |
| ev.03_symbols_md.tests_unit_app_test_feedback_handler_http_py.test_feedback_endpoint_accepts_all_canonical_actions.l3567 | evidence/03_symbols.md | 3567-3567 |
| ev.03_symbols_md.tests_unit_app_test_feedback_service_py.test_record_returns_true_on_success.l3571 | evidence/03_symbols.md | 3571-3571 |
| ev.03_symbols_md.tests_unit_app_test_feedback_service_py.test_record_returns_false_on_publish_failure.l3572 | evidence/03_symbols.md | 3572-3572 |
| ev.03_symbols_md.tests_unit_app_test_feedback_service_py.test_record_emits_new_user_action_contract.l3573 | evidence/03_symbols.md | 3573-3573 |
| ev.03_symbols_md.tests_unit_app_test_health_handler_py.test_livez_returns_ok.l3577 | evidence/03_symbols.md | 3577-3577 |
| ev.03_symbols_md.tests_unit_app_test_health_handler_py.test_healthz_returns_ok.l3578 | evidence/03_symbols.md | 3578-3578 |
| ev.03_symbols_md.tests_unit_app_test_health_handler_py.test_readyz_returns_ready_when_search_wired.l3579 | evidence/03_symbols.md | 3579-3579 |
| ev.03_symbols_md.tests_unit_app_test_health_handler_py.test_readyz_returns_loading_when_retriever_missing.l3580 | evidence/03_symbols.md | 3580-3580 |
| ev.03_symbols_md.tests_unit_app_test_kserve_wiring_py.settings.l3584 | evidence/03_symbols.md | 3584-3584 |
| ev.03_symbols_md.tests_unit_app_test_kserve_wiring_py.build_encoder_client.l3585 | evidence/03_symbols.md | 3585-3585 |
| ev.03_symbols_md.tests_unit_app_test_kserve_wiring_py.build_reranker_client.l3586 | evidence/03_symbols.md | 3586-3586 |
| ev.03_symbols_md.tests_unit_app_test_kserve_wiring_py.test_apisettings_kserve_fields_default_to_empty_string.l3587 | evidence/03_symbols.md | 3587-3587 |
| ev.03_symbols_md.tests_unit_app_test_kserve_wiring_py.test_apisettings_kserve_fields_populated_from_env.l3588 | evidence/03_symbols.md | 3588-3588 |
| ev.03_symbols_md.tests_unit_app_test_kserve_wiring_py.test_apisettings_exposes_grouped_views_for_flags_messaging_and_popularity.l3589 | evidence/03_symbols.md | 3589-3589 |
| ev.03_symbols_md.tests_unit_app_test_kserve_wiring_py.test_build_encoder_client_returns_none_when_url_empty.l3590 | evidence/03_symbols.md | 3590-3590 |
| ev.03_symbols_md.tests_unit_app_test_kserve_wiring_py.test_build_encoder_client_instantiates_kserve_encoder_when_url_set.l3591 | evidence/03_symbols.md | 3591-3591 |
| ev.03_symbols_md.tests_unit_app_test_kserve_wiring_py.test_build_reranker_client_returns_none_when_enable_rerank_false.l3592 | evidence/03_symbols.md | 3592-3592 |
| ev.03_symbols_md.tests_unit_app_test_kserve_wiring_py.test_build_reranker_client_returns_none_when_url_empty.l3593 | evidence/03_symbols.md | 3593-3593 |
| ev.03_symbols_md.tests_unit_app_test_kserve_wiring_py.test_build_reranker_client_instantiates_with_explain_url_when_set.l3594 | evidence/03_symbols.md | 3594-3594 |
| ev.03_symbols_md.tests_unit_app_test_kserve_wiring_py.test_build_reranker_client_passes_none_when_explain_url_is_empty_string.l3595 | evidence/03_symbols.md | 3595-3595 |
| ev.03_symbols_md.tests_unit_app_test_kserve_wiring_py.test_build_reranker_client_handles_whitespace_explain_url.l3596 | evidence/03_symbols.md | 3596-3596 |
| ev.03_symbols_md.tests_unit_app_test_kserve_wiring_py.test_build_reranker_client_has_predict_with_explain_for_ranking_gate.l3597 | evidence/03_symbols.md | 3597-3597 |
| ev.03_symbols_md.tests_unit_app_test_local_boot_contract_py.test_container_builder_avoids_gcp_clients_when_search_disabled.l3601 | evidence/03_symbols.md | 3601-3601 |
| ev.03_symbols_md.tests_unit_app_test_local_boot_contract_py.forbidden.l3602 | evidence/03_symbols.md | 3602-3602 |
| ev.03_symbols_md.tests_unit_app_test_logging_middleware_py.test_middleware_generates_request_id_when_absent.l3606 | evidence/03_symbols.md | 3606-3606 |
| ev.03_symbols_md.tests_unit_app_test_logging_middleware_py.test_middleware_preserves_client_supplied_request_id.l3607 | evidence/03_symbols.md | 3607-3607 |
| ev.03_symbols_md.tests_unit_app_test_logging_middleware_py.test_middleware_request_id_matches_search_response.l3608 | evidence/03_symbols.md | 3608-3608 |
| ev.03_symbols_md.tests_unit_app_test_main_routing_py.app_no_lifespan.l3612 | evidence/03_symbols.md | 3612-3612 |
| ev.03_symbols_md.tests_unit_app_test_main_routing_py.noopcontainer.l3613 | evidence/03_symbols.md | 3613-3613 |
| ev.03_symbols_md.tests_unit_app_test_main_routing_py.build.l3614 | evidence/03_symbols.md | 3614-3614 |
| ev.03_symbols_md.tests_unit_app_test_main_routing_py.test_root_redirects_to_ui.l3615 | evidence/03_symbols.md | 3615-3615 |
| ev.03_symbols_md.tests_unit_app_test_main_routing_py.test_ui_home_returns_html.l3616 | evidence/03_symbols.md | 3616-3616 |
| ev.03_symbols_md.tests_unit_app_test_main_routing_py.test_ui_dev_returns_html.l3617 | evidence/03_symbols.md | 3617-3617 |
| ev.03_symbols_md.tests_unit_app_test_main_routing_py.test_ui_model_metrics_returns_html.l3618 | evidence/03_symbols.md | 3618-3618 |
| ev.03_symbols_md.tests_unit_app_test_main_routing_py.test_ui_data_returns_html.l3619 | evidence/03_symbols.md | 3619-3619 |
| ev.03_symbols_md.tests_unit_app_test_main_routing_py.test_ui_ops_returns_html.l3620 | evidence/03_symbols.md | 3620-3620 |
| ev.03_symbols_md.tests_unit_app_test_main_routing_py.test_metrics_serves_prometheus_exposition.l3621 | evidence/03_symbols.md | 3621-3621 |
| ev.03_symbols_md.tests_unit_app_test_main_routing_py.test_metrics_emits_slo_compatible_labels.l3622 | evidence/03_symbols.md | 3622-3622 |
| ev.03_symbols_md.tests_unit_app_test_main_routing_py.test_livez_unconditional.l3623 | evidence/03_symbols.md | 3623-3623 |
| ev.03_symbols_md.tests_unit_app_test_model_handler_py.build_client.l3627 | evidence/03_symbols.md | 3627-3627 |
| ev.03_symbols_md.tests_unit_app_test_model_handler_py.wire_candidates.l3628 | evidence/03_symbols.md | 3628-3628 |
| ev.03_symbols_md.tests_unit_app_test_model_handler_py.test_model_metrics_returns_summary_and_per_case.l3629 | evidence/03_symbols.md | 3629-3629 |
| ev.03_symbols_md.tests_unit_app_test_model_handler_py.test_model_metrics_503_when_service_missing.l3630 | evidence/03_symbols.md | 3630-3630 |
| ev.03_symbols_md.tests_unit_app_test_model_handler_py.test_model_metrics_rejects_invalid_k.l3631 | evidence/03_symbols.md | 3631-3631 |
| ev.03_symbols_md.tests_unit_app_test_model_handler_py.test_model_info_reports_container_state.l3632 | evidence/03_symbols.md | 3632-3632 |
| ev.03_symbols_md.tests_unit_app_test_model_handler_py.test_model_data_returns_preview_tables.l3633 | evidence/03_symbols.md | 3633-3633 |
| ev.03_symbols_md.tests_unit_app_test_model_handler_py.test_load_cases_rejects_empty_file.l3634 | evidence/03_symbols.md | 3634-3634 |
| ev.03_symbols_md.tests_unit_app_test_model_handler_py.test_evaluate_default_cases_returns_report.l3635 | evidence/03_symbols.md | 3635-3635 |
| ev.03_symbols_md.tests_unit_app_test_observability_py.test_for_test_uses_stdlib_logger_and_default_service.l3639 | evidence/03_symbols.md | 3639-3639 |
| ev.03_symbols_md.tests_unit_app_test_observability_py.test_for_test_accepts_custom_service_name.l3640 | evidence/03_symbols.md | 3640-3640 |
| ev.03_symbols_md.tests_unit_app_test_observability_py.test_from_env_reads_otel_service_name.l3641 | evidence/03_symbols.md | 3641-3641 |
| ev.03_symbols_md.tests_unit_app_test_observability_py.test_from_env_default_matches_slo_label_contract.l3642 | evidence/03_symbols.md | 3642-3642 |
| ev.03_symbols_md.tests_unit_app_test_ops_handler_py.build_test_app.l3646 | evidence/03_symbols.md | 3646-3646 |
| ev.03_symbols_md.tests_unit_app_test_ops_handler_py.test_destroy_check_returns_summary.l3647 | evidence/03_symbols.md | 3647-3647 |
| ev.03_symbols_md.tests_unit_app_test_ops_handler_py.test_search_volume_returns_summary.l3648 | evidence/03_symbols.md | 3648-3648 |
| ev.03_symbols_md.tests_unit_app_test_ops_handler_py.test_runs_recent_returns_rows.l3649 | evidence/03_symbols.md | 3649-3649 |
| ev.03_symbols_md.tests_unit_app_test_ops_handler_py.test_search_volume_returns_503_with_json_detail_on_bq_error.l3650 | evidence/03_symbols.md | 3650-3650 |
| ev.03_symbols_md.tests_unit_app_test_ops_handler_py.test_runs_recent_returns_503_with_json_detail_on_bq_error.l3651 | evidence/03_symbols.md | 3651-3651 |
| ev.03_symbols_md.tests_unit_app_test_optional_adapter_helper_py.test_returns_none_when_disabled_without_calling_factory.l3655 | evidence/03_symbols.md | 3655-3655 |
| ev.03_symbols_md.tests_unit_app_test_optional_adapter_helper_py.factory.l3656 | evidence/03_symbols.md | 3656-3656 |
| ev.03_symbols_md.tests_unit_app_test_optional_adapter_helper_py.test_returns_factory_result_when_enabled.l3657 | evidence/03_symbols.md | 3657-3657 |
| ev.03_symbols_md.tests_unit_app_test_optional_adapter_helper_py.test_swallows_factory_exception_and_logs_with_name.l3658 | evidence/03_symbols.md | 3658-3658 |
| ev.03_symbols_md.tests_unit_app_test_optional_adapter_helper_py.factory.l3659 | evidence/03_symbols.md | 3659-3659 |
| ev.03_symbols_md.tests_unit_app_test_publisher_py.test_noop_publisher_accepts_any_payload.l3663 | evidence/03_symbols.md | 3663-3663 |
| ev.03_symbols_md.tests_unit_app_test_pubsub_event_writer_py.client_for.l3667 | evidence/03_symbols.md | 3667-3667 |
| ev.03_symbols_md.tests_unit_app_test_pubsub_event_writer_py.topic_path.l3668 | evidence/03_symbols.md | 3668-3668 |
| ev.03_symbols_md.tests_unit_app_test_pubsub_event_writer_py.build.l3669 | evidence/03_symbols.md | 3669-3669 |
| ev.03_symbols_md.tests_unit_app_test_pubsub_event_writer_py.test_emit_search_event_publishes_to_search_events_topic.l3670 | evidence/03_symbols.md | 3670-3670 |
| ev.03_symbols_md.tests_unit_app_test_pubsub_event_writer_py.test_emit_impression_publishes_to_search_impressions_topic.l3671 | evidence/03_symbols.md | 3671-3671 |
| ev.03_symbols_md.tests_unit_app_test_pubsub_event_writer_py.test_emit_user_action_publishes_to_user_actions_topic.l3672 | evidence/03_symbols.md | 3672-3672 |
| ev.03_symbols_md.tests_unit_app_test_pubsub_event_writer_py.test_publish_failure_is_logged_and_reraised.l3673 | evidence/03_symbols.md | 3673-3673 |
| ev.03_symbols_md.tests_unit_app_test_pubsub_event_writer_py.api_settings.l3674 | evidence/03_symbols.md | 3674-3674 |
| ev.03_symbols_md.tests_unit_app_test_pubsub_event_writer_py.test_build_event_writer_selects_pubsub_when_topics_set.l3675 | evidence/03_symbols.md | 3675-3675 |
| ev.03_symbols_md.tests_unit_app_test_pubsub_event_writer_py.test_build_event_writer_falls_back_to_cloud_logging_when_topic_missing.l3676 | evidence/03_symbols.md | 3676-3676 |
| ev.03_symbols_md.tests_unit_app_test_ranking_service_py.fakeretriever.l3680 | evidence/03_symbols.md | 3680-3680 |
| ev.03_symbols_md.tests_unit_app_test_ranking_service_py.retrieve.l3681 | evidence/03_symbols.md | 3681-3681 |
| ev.03_symbols_md.tests_unit_app_test_ranking_service_py.fakepublisher.l3682 | evidence/03_symbols.md | 3682-3682 |
| ev.03_symbols_md.tests_unit_app_test_ranking_service_py.publish_candidates.l3683 | evidence/03_symbols.md | 3683-3683 |
| ev.03_symbols_md.tests_unit_app_test_ranking_service_py.stubreranker.l3684 | evidence/03_symbols.md | 3684-3684 |
| ev.03_symbols_md.tests_unit_app_test_ranking_service_py.predict.l3685 | evidence/03_symbols.md | 3685-3685 |
| ev.03_symbols_md.tests_unit_app_test_ranking_service_py.candidate.l3686 | evidence/03_symbols.md | 3686-3686 |
| ev.03_symbols_md.tests_unit_app_test_ranking_service_py.test_run_search_preserves_lexical_order.l3687 | evidence/03_symbols.md | 3687-3687 |
| ev.03_symbols_md.tests_unit_app_test_ranking_service_py.test_run_search_final_rank_equals_lexical_rank_without_reranker.l3688 | evidence/03_symbols.md | 3688-3688 |
| ev.03_symbols_md.tests_unit_app_test_ranking_service_py.test_run_search_continues_when_publisher_raises.l3689 | evidence/03_symbols.md | 3689-3689 |
| ev.03_symbols_md.tests_unit_app_test_ranking_service_py.failingpublisher.l3690 | evidence/03_symbols.md | 3690-3690 |
| ev.03_symbols_md.tests_unit_app_test_ranking_service_py.init.l3691 | evidence/03_symbols.md | 3691-3691 |
| ev.03_symbols_md.tests_unit_app_test_ranking_service_py.publish_candidates.l3692 | evidence/03_symbols.md | 3692-3692 |
| ev.03_symbols_md.tests_unit_app_test_ranking_service_py.test_run_search_publishes_full_pool_not_just_top_k.l3693 | evidence/03_symbols.md | 3693-3693 |
| ev.03_symbols_md.tests_unit_app_test_ranking_service_py.test_run_search_forwards_filters_to_retriever.l3694 | evidence/03_symbols.md | 3694-3694 |
| ev.03_symbols_md.tests_unit_app_test_ranking_service_py.test_run_search_empty_result.l3695 | evidence/03_symbols.md | 3695-3695 |
| ev.03_symbols_md.tests_unit_app_test_ranking_service_py.test_run_search_rerank_reverses_order_when_reranker_says_so.l3696 | evidence/03_symbols.md | 3696-3696 |
| ev.03_symbols_md.tests_unit_app_test_ranking_service_py.test_run_search_rerank_truncates_to_top_k.l3697 | evidence/03_symbols.md | 3697-3697 |
| ev.03_symbols_md.tests_unit_app_test_ranking_service_py.test_run_search_rerank_with_higher_score_wins.l3698 | evidence/03_symbols.md | 3698-3698 |
| ev.03_symbols_md.tests_unit_app_test_ranking_service_py.forcewinreranker.l3699 | evidence/03_symbols.md | 3699-3699 |
| ev.03_symbols_md.tests_unit_app_test_ranking_service_py.predict.l3700 | evidence/03_symbols.md | 3700-3700 |
| ev.03_symbols_md.tests_unit_app_test_ranking_service_py.test_run_search_rerank_tie_breaks_by_lexical_then_semantic_rank.l3701 | evidence/03_symbols.md | 3701-3701 |
| ev.03_symbols_md.tests_unit_app_test_ranking_service_py.tiereranker.l3702 | evidence/03_symbols.md | 3702-3702 |
| ev.03_symbols_md.tests_unit_app_test_ranking_service_py.predict.l3703 | evidence/03_symbols.md | 3703-3703 |
| ev.03_symbols_md.tests_unit_app_test_retrain_py.fakequeries.l3707 | evidence/03_symbols.md | 3707-3707 |
| ev.03_symbols_md.tests_unit_app_test_retrain_py.init.l3708 | evidence/03_symbols.md | 3708-3708 |
| ev.03_symbols_md.tests_unit_app_test_retrain_py.last_run_finished_at.l3709 | evidence/03_symbols.md | 3709-3709 |
| ev.03_symbols_md.tests_unit_app_test_retrain_py.feedback_rows_since.l3710 | evidence/03_symbols.md | 3710-3710 |
| ev.03_symbols_md.tests_unit_app_test_retrain_py.ndcg_in_window.l3711 | evidence/03_symbols.md | 3711-3711 |
| ev.03_symbols_md.tests_unit_app_test_retrain_py.test_no_reason_no_retrain.l3712 | evidence/03_symbols.md | 3712-3712 |
| ev.03_symbols_md.tests_unit_app_test_retrain_py.test_feedback_rows_trigger.l3713 | evidence/03_symbols.md | 3713-3713 |
| ev.03_symbols_md.tests_unit_app_test_retrain_py.test_feedback_rows_below_threshold_does_not_trigger.l3714 | evidence/03_symbols.md | 3714-3714 |
| ev.03_symbols_md.tests_unit_app_test_retrain_py.test_ndcg_drop_triggers_retrain.l3715 | evidence/03_symbols.md | 3715-3715 |
| ev.03_symbols_md.tests_unit_app_test_retrain_py.test_ndcg_improvement_does_not_trigger.l3716 | evidence/03_symbols.md | 3716-3716 |
| ev.03_symbols_md.tests_unit_app_test_retrain_py.test_ndcg_missing_does_not_trigger.l3717 | evidence/03_symbols.md | 3717-3717 |
| ev.03_symbols_md.tests_unit_app_test_retrain_py.test_ndcg_small_drop_below_threshold.l3718 | evidence/03_symbols.md | 3718-3718 |
| ev.03_symbols_md.tests_unit_app_test_retrain_py.test_custom_ndcg_threshold_flips_decision.l3719 | evidence/03_symbols.md | 3719-3719 |
| ev.03_symbols_md.tests_unit_app_test_retrain_py.test_staleness_trigger.l3720 | evidence/03_symbols.md | 3720-3720 |
| ev.03_symbols_md.tests_unit_app_test_retrain_py.test_no_prior_run_triggers.l3721 | evidence/03_symbols.md | 3721-3721 |
| ev.03_symbols_md.tests_unit_app_test_retrain_py.test_custom_feedback_threshold.l3722 | evidence/03_symbols.md | 3722-3722 |
| ev.03_symbols_md.tests_unit_app_test_retrain_py.test_custom_stale_days_triggers_on_shorter_window.l3723 | evidence/03_symbols.md | 3723-3723 |
| ev.03_symbols_md.tests_unit_app_test_retrain_py.test_decision_exposes_ranker_fields.l3724 | evidence/03_symbols.md | 3724-3724 |
| ev.03_symbols_md.tests_unit_app_test_run_search_feature_fetcher_py.candidate.l3728 | evidence/03_symbols.md | 3728-3728 |
| ev.03_symbols_md.tests_unit_app_test_run_search_feature_fetcher_py.test_augment_overwrites_three_dynamic_features.l3729 | evidence/03_symbols.md | 3729-3729 |
| ev.03_symbols_md.tests_unit_app_test_run_search_feature_fetcher_py.test_augment_preserves_bq_value_when_fos_field_is_none.l3730 | evidence/03_symbols.md | 3730-3730 |
| ev.03_symbols_md.tests_unit_app_test_run_search_feature_fetcher_py.test_augment_keeps_candidate_unchanged_when_id_not_in_fos.l3731 | evidence/03_symbols.md | 3731-3731 |
| ev.03_symbols_md.tests_unit_app_test_run_search_feature_fetcher_py.test_augment_returns_empty_list_for_empty_input.l3732 | evidence/03_symbols.md | 3732-3732 |
| ev.03_symbols_md.tests_unit_app_test_run_search_feature_fetcher_py.test_augment_calls_fetch_once_with_all_property_ids.l3733 | evidence/03_symbols.md | 3733-3733 |
| ev.03_symbols_md.tests_unit_app_test_run_search_feature_fetcher_py.test_run_search_default_feature_fetcher_is_none_no_fetch_happens.l3734 | evidence/03_symbols.md | 3734-3734 |
| ev.03_symbols_md.tests_unit_app_test_run_search_feature_fetcher_py.test_run_search_with_feature_fetcher_merges_before_reranker_predict.l3735 | evidence/03_symbols.md | 3735-3735 |
| ev.03_symbols_md.tests_unit_app_test_run_search_feature_fetcher_py.test_run_search_swallows_feature_fetcher_failure_and_continues.l3736 | evidence/03_symbols.md | 3736-3736 |
| ev.03_symbols_md.tests_unit_app_test_run_search_feature_fetcher_py.explodingfetcher.l3737 | evidence/03_symbols.md | 3737-3737 |
| ev.03_symbols_md.tests_unit_app_test_run_search_feature_fetcher_py.fetch.l3738 | evidence/03_symbols.md | 3738-3738 |
| ev.03_symbols_md.tests_unit_app_test_run_search_feature_fetcher_py.test_container_dataclass_has_feature_fetcher_field.l3739 | evidence/03_symbols.md | 3739-3739 |
| ev.03_symbols_md.tests_unit_app_test_run_search_feature_fetcher_py.test_search_service_accepts_feature_fetcher_kwarg.l3740 | evidence/03_symbols.md | 3740-3740 |
| ev.03_symbols_md.tests_unit_app_test_run_search_feature_fetcher_py.test_run_search_signature_lists_feature_fetcher_with_default_none.l3741 | evidence/03_symbols.md | 3741-3741 |
| ev.03_symbols_md.tests_unit_app_test_search_api_py.search_payload.l3745 | evidence/03_symbols.md | 3745-3745 |
| ev.03_symbols_md.tests_unit_app_test_search_api_py.replace_search_container.l3746 | evidence/03_symbols.md | 3746-3746 |
| ev.03_symbols_md.tests_unit_app_test_search_api_py.test_search_returns_200_with_results.l3747 | evidence/03_symbols.md | 3747-3747 |
| ev.03_symbols_md.tests_unit_app_test_search_api_py.test_search_results_preserve_lexical_rank_when_rerank_disabled.l3748 | evidence/03_symbols.md | 3748-3748 |
| ev.03_symbols_md.tests_unit_app_test_search_api_py.test_search_emits_ranking_log.l3749 | evidence/03_symbols.md | 3749-3749 |
| ev.03_symbols_md.tests_unit_app_test_search_api_py.test_search_top_k_truncates_response.l3750 | evidence/03_symbols.md | 3750-3750 |
| ev.03_symbols_md.tests_unit_app_test_search_api_py.test_search_rejects_empty_query.l3751 | evidence/03_symbols.md | 3751-3751 |
| ev.03_symbols_md.tests_unit_app_test_search_api_py.test_search_503_when_disabled.l3752 | evidence/03_symbols.md | 3752-3752 |
| ev.03_symbols_md.tests_unit_app_test_search_api_py.test_feedback_accepts_click.l3753 | evidence/03_symbols.md | 3753-3753 |
| ev.03_symbols_md.tests_unit_app_test_search_api_py.test_feedback_rejects_unknown_action.l3754 | evidence/03_symbols.md | 3754-3754 |
| ev.03_symbols_md.tests_unit_app_test_search_api_py.test_readyz_ok_when_search_enabled.l3755 | evidence/03_symbols.md | 3755-3755 |
| ev.03_symbols_md.tests_unit_app_test_search_api_py.test_readyz_503_when_retriever_missing.l3756 | evidence/03_symbols.md | 3756-3756 |
| ev.03_symbols_md.tests_unit_app_test_search_api_py.test_readyz_503_when_encoder_missing.l3757 | evidence/03_symbols.md | 3757-3757 |
| ev.03_symbols_md.tests_unit_app_test_search_api_py.test_healthz_unconditional.l3758 | evidence/03_symbols.md | 3758-3758 |
| ev.03_symbols_md.tests_unit_app_test_search_api_py.test_readyz_reports_rerank_disabled_when_client_missing.l3759 | evidence/03_symbols.md | 3759-3759 |
| ev.03_symbols_md.tests_unit_app_test_search_api_py.test_readyz_reports_rerank_enabled_when_client_set.l3760 | evidence/03_symbols.md | 3760-3760 |
| ev.03_symbols_md.tests_unit_app_test_search_api_py.stubreranker.l3761 | evidence/03_symbols.md | 3761-3761 |
| ev.03_symbols_md.tests_unit_app_test_search_api_py.predict.l3762 | evidence/03_symbols.md | 3762-3762 |
| ev.03_symbols_md.tests_unit_app_test_search_api_py.test_search_returns_scores_when_reranker_loaded.l3763 | evidence/03_symbols.md | 3763-3763 |
| ev.03_symbols_md.tests_unit_app_test_search_api_py.stubreranker.l3764 | evidence/03_symbols.md | 3764-3764 |
| ev.03_symbols_md.tests_unit_app_test_search_api_py.predict.l3765 | evidence/03_symbols.md | 3765-3765 |
| ev.03_symbols_md.tests_unit_app_test_search_api_py.test_ranking_log_receives_scores_when_reranker_loaded.l3766 | evidence/03_symbols.md | 3766-3766 |
| ev.03_symbols_md.tests_unit_app_test_search_api_py.stubreranker.l3767 | evidence/03_symbols.md | 3767-3767 |
| ev.03_symbols_md.tests_unit_app_test_search_api_py.predict.l3768 | evidence/03_symbols.md | 3768-3768 |
| ev.03_symbols_md.tests_unit_app_test_search_builder_canonical_py.fakecontext.l3772 | evidence/03_symbols.md | 3772-3772 |
| ev.03_symbols_md.tests_unit_app_test_search_builder_canonical_py.init.l3773 | evidence/03_symbols.md | 3773-3773 |
| ev.03_symbols_md.tests_unit_app_test_search_builder_canonical_py.bigquery.l3774 | evidence/03_symbols.md | 3774-3774 |
| ev.03_symbols_md.tests_unit_app_test_search_builder_canonical_py.settings.l3775 | evidence/03_symbols.md | 3775-3775 |
| ev.03_symbols_md.tests_unit_app_test_search_builder_canonical_py.builder.l3776 | evidence/03_symbols.md | 3776-3776 |
| ev.03_symbols_md.tests_unit_app_test_search_builder_canonical_py.test_build_vertex_vector_search_assembles_endpoint_resource_name.l3777 | evidence/03_symbols.md | 3777-3777 |
| ev.03_symbols_md.tests_unit_app_test_search_builder_canonical_py.test_build_vertex_vector_search_accepts_fully_qualified_endpoint_name.l3778 | evidence/03_symbols.md | 3778-3778 |
| ev.03_symbols_md.tests_unit_app_test_search_builder_canonical_py.test_build_vertex_vector_search_fails_loud_when_endpoint_missing.l3779 | evidence/03_symbols.md | 3779-3779 |
| ev.03_symbols_md.tests_unit_app_test_search_builder_canonical_py.test_build_vertex_vector_search_fails_loud_when_deployed_id_missing.l3780 | evidence/03_symbols.md | 3780-3780 |
| ev.03_symbols_md.tests_unit_app_test_search_builder_canonical_py.test_resolve_feature_fetcher_returns_fos_when_fully_configured.l3781 | evidence/03_symbols.md | 3781-3781 |
| ev.03_symbols_md.tests_unit_app_test_search_builder_canonical_py.test_resolve_feature_fetcher_fails_loud_when_store_missing.l3782 | evidence/03_symbols.md | 3782-3782 |
| ev.03_symbols_md.tests_unit_app_test_search_builder_canonical_py.test_resolve_feature_fetcher_fails_loud_when_view_missing.l3783 | evidence/03_symbols.md | 3783-3783 |
| ev.03_symbols_md.tests_unit_app_test_search_builder_canonical_py.test_resolve_feature_fetcher_fails_loud_when_endpoint_missing.l3784 | evidence/03_symbols.md | 3784-3784 |
| ev.03_symbols_md.tests_unit_app_test_search_builder_canonical_py.test_resolve_lexical_returns_elasticsearch_when_url_configured.l3785 | evidence/03_symbols.md | 3785-3785 |
| ev.03_symbols_md.tests_unit_app_test_search_builder_canonical_py.test_resolve_lexical_fails_loud_when_es_backend_enable_search_no_lexical_url.l3786 | evidence/03_symbols.md | 3786-3786 |
| ev.03_symbols_md.tests_unit_app_test_search_builder_canonical_py.test_resolve_lexical_noop_when_search_disabled_and_no_lexical_urls.l3787 | evidence/03_symbols.md | 3787-3787 |
| ev.03_symbols_md.tests_unit_app_test_search_handler_http_py.candidate.l3791 | evidence/03_symbols.md | 3791-3791 |
| ev.03_symbols_md.tests_unit_app_test_search_handler_http_py.test_search_endpoint_returns_results.l3792 | evidence/03_symbols.md | 3792-3792 |
| ev.03_symbols_md.tests_unit_app_test_search_handler_http_py.test_search_endpoint_503_when_retriever_unavailable.l3793 | evidence/03_symbols.md | 3793-3793 |
| ev.03_symbols_md.tests_unit_app_test_search_handler_http_py.test_search_endpoint_explain_returns_attributions.l3794 | evidence/03_symbols.md | 3794-3794 |
| ev.03_symbols_md.tests_unit_app_test_search_handler_http_py.test_search_endpoint_emits_canonical_event_logs.l3795 | evidence/03_symbols.md | 3795-3795 |
| ev.03_symbols_md.tests_unit_app_test_search_mapper_py.test_search_request_to_input_propagates_filters_and_flags.l3799 | evidence/03_symbols.md | 3799-3799 |
| ev.03_symbols_md.tests_unit_app_test_search_mapper_py.test_to_search_response_maps_items.l3800 | evidence/03_symbols.md | 3800-3800 |
| ev.03_symbols_md.tests_unit_app_test_search_service_py.make_candidate.l3804 | evidence/03_symbols.md | 3804-3804 |
| ev.03_symbols_md.tests_unit_app_test_search_service_py.build_service.l3805 | evidence/03_symbols.md | 3805-3805 |
| ev.03_symbols_md.tests_unit_app_test_search_service_py.test_search_returns_items_sorted_by_final_rank.l3806 | evidence/03_symbols.md | 3806-3806 |
| ev.03_symbols_md.tests_unit_app_test_search_service_py.test_search_calls_publisher_once_with_full_pool.l3807 | evidence/03_symbols.md | 3807-3807 |
| ev.03_symbols_md.tests_unit_app_test_search_service_py.test_search_uses_reranker_scores_when_available.l3808 | evidence/03_symbols.md | 3808-3808 |
| ev.03_symbols_md.tests_unit_app_test_search_service_py.test_search_raises_unavailable_when_retriever_missing.l3809 | evidence/03_symbols.md | 3809-3809 |
| ev.03_symbols_md.tests_unit_app_test_search_service_py.test_search_raises_unavailable_when_encoder_missing.l3810 | evidence/03_symbols.md | 3810-3810 |
| ev.03_symbols_md.tests_unit_app_test_search_service_py.test_search_populates_popularity_score_when_scorer_present.l3811 | evidence/03_symbols.md | 3811-3811 |
| ev.03_symbols_md.tests_unit_app_test_search_service_py.test_search_emits_search_event_and_impressions.l3812 | evidence/03_symbols.md | 3812-3812 |
| ev.03_symbols_md.tests_unit_app_test_settings_sources_py.test_apisettings_loads_non_secret_values_from_setting_yaml.l3816 | evidence/03_symbols.md | 3816-3816 |
| ev.03_symbols_md.tests_unit_app_test_settings_sources_py.test_env_vars_override_yaml_sources.l3817 | evidence/03_symbols.md | 3817-3817 |
| ev.03_symbols_md.tests_unit_app_test_synonym_expander_py.b.l3821 | evidence/03_symbols.md | 3821-3821 |
| ev.03_symbols_md.tests_unit_app_test_synonym_expander_py.fakeredis.l3822 | evidence/03_symbols.md | 3822-3822 |
| ev.03_symbols_md.tests_unit_app_test_synonym_expander_py.init.l3823 | evidence/03_symbols.md | 3823-3823 |
| ev.03_symbols_md.tests_unit_app_test_synonym_expander_py.smembers.l3824 | evidence/03_symbols.md | 3824-3824 |
| ev.03_symbols_md.tests_unit_app_test_synonym_expander_py.flakyredis.l3825 | evidence/03_symbols.md | 3825-3825 |
| ev.03_symbols_md.tests_unit_app_test_synonym_expander_py.smembers.l3826 | evidence/03_symbols.md | 3826-3826 |
| ev.03_symbols_md.tests_unit_app_test_synonym_expander_py.test_noop_returns_query_unchanged.l3827 | evidence/03_symbols.md | 3827-3827 |
| ev.03_symbols_md.tests_unit_app_test_synonym_expander_py.test_redis_expands_known_tokens_with_synonyms.l3828 | evidence/03_symbols.md | 3828-3828 |
| ev.03_symbols_md.tests_unit_app_test_synonym_expander_py.test_redis_keeps_query_when_no_synonyms_known.l3829 | evidence/03_symbols.md | 3829-3829 |
| ev.03_symbols_md.tests_unit_app_test_synonym_expander_py.test_redis_returns_original_on_backend_failure.l3830 | evidence/03_symbols.md | 3830-3830 |
| ev.03_symbols_md.tests_unit_app_test_synonym_expander_py.test_redis_caps_synonyms_per_token.l3831 | evidence/03_symbols.md | 3831-3831 |
| ev.03_symbols_md.tests_unit_app_test_synonym_expander_py.test_redis_dedupes_across_tokens.l3832 | evidence/03_symbols.md | 3832-3832 |
| ev.03_symbols_md.tests_unit_app_test_synonym_expander_py.test_redis_handles_string_decoded_values.l3833 | evidence/03_symbols.md | 3833-3833 |
| ev.03_symbols_md.tests_unit_app_test_synonym_expander_py.strredis.l3834 | evidence/03_symbols.md | 3834-3834 |
| ev.03_symbols_md.tests_unit_app_test_synonym_expander_py.smembers.l3835 | evidence/03_symbols.md | 3835-3835 |
| ev.03_symbols_md.tests_unit_app_test_vertex_vector_search_semantic_search_py.make_neighbor.l3839 | evidence/03_symbols.md | 3839-3839 |
| ev.03_symbols_md.tests_unit_app_test_vertex_vector_search_semantic_search_py.factory_returning.l3840 | evidence/03_symbols.md | 3840-3840 |
| ev.03_symbols_md.tests_unit_app_test_vertex_vector_search_semantic_search_py.adapter.l3841 | evidence/03_symbols.md | 3841-3841 |
| ev.03_symbols_md.tests_unit_app_test_vertex_vector_search_semantic_search_py.test_search_converts_neighbors_to_semantic_results_in_distance_order.l3842 | evidence/03_symbols.md | 3842-3842 |
| ev.03_symbols_md.tests_unit_app_test_vertex_vector_search_semantic_search_py.test_search_returns_empty_when_no_neighbors.l3843 | evidence/03_symbols.md | 3843-3843 |
| ev.03_symbols_md.tests_unit_app_test_vertex_vector_search_semantic_search_py.test_search_returns_empty_when_response_is_empty.l3844 | evidence/03_symbols.md | 3844-3844 |
| ev.03_symbols_md.tests_unit_app_test_vertex_vector_search_semantic_search_py.test_search_passes_top_k_and_query_vector_and_deployed_index_id.l3845 | evidence/03_symbols.md | 3845-3845 |
| ev.03_symbols_md.tests_unit_app_test_vertex_vector_search_semantic_search_py.test_search_ignores_filters_in_pr1_known_limitation.l3846 | evidence/03_symbols.md | 3846-3846 |
| ev.03_symbols_md.tests_unit_app_test_vertex_vector_search_semantic_search_py.test_endpoint_factory_called_with_resource_name_once.l3847 | evidence/03_symbols.md | 3847-3847 |
| ev.03_symbols_md.tests_unit_app_test_vertex_vector_search_semantic_search_py.factory.l3848 | evidence/03_symbols.md | 3848-3848 |
| ev.03_symbols_md.tests_unit_app_test_vertex_vector_search_semantic_search_py.test_search_handles_missing_distance_attribute_as_max_distance.l3849 | evidence/03_symbols.md | 3849-3849 |
| ev.03_symbols_md.tests_unit_app_test_vertex_vector_search_semantic_search_py.test_constructor_rejects_empty_required_args.l3850 | evidence/03_symbols.md | 3850-3850 |
| ev.03_symbols_md.tests_unit_arch_test_import_boundaries_py.test_no_forbidden_imports.l3854 | evidence/03_symbols.md | 3854-3854 |
| ev.03_symbols_md.tests_unit_ml_common_test_gcs_py.test_parse_round_trip.l3858 | evidence/03_symbols.md | 3858-3858 |
| ev.03_symbols_md.tests_unit_ml_common_test_gcs_py.test_parse_bucket_only.l3859 | evidence/03_symbols.md | 3859-3859 |
| ev.03_symbols_md.tests_unit_ml_common_test_gcs_py.test_parse_trailing_slash.l3860 | evidence/03_symbols.md | 3860-3860 |
| ev.03_symbols_md.tests_unit_ml_common_test_gcs_py.test_child_and_uri.l3861 | evidence/03_symbols.md | 3861-3861 |
| ev.03_symbols_md.tests_unit_ml_common_test_gcs_py.test_model_prefix_layout.l3862 | evidence/03_symbols.md | 3862-3862 |
| ev.03_symbols_md.tests_unit_ml_common_test_gcs_py.test_parse_rejects_non_gcs.l3863 | evidence/03_symbols.md | 3863-3863 |
| ev.03_symbols_md.tests_unit_ml_common_test_gcs_io_py.test_upload_directory_recurses_and_returns_uris.l3867 | evidence/03_symbols.md | 3867-3867 |
| ev.03_symbols_md.tests_unit_ml_common_test_gcs_io_py.test_upload_directory_handles_empty_prefix.l3868 | evidence/03_symbols.md | 3868-3868 |
| ev.03_symbols_md.tests_unit_ml_common_test_gcs_io_py.test_download_file_writes_to_local_path.l3869 | evidence/03_symbols.md | 3869-3869 |
| ev.03_symbols_md.tests_unit_ml_common_test_logging_py.test_json_formatter_basic.l3873 | evidence/03_symbols.md | 3873-3873 |
| ev.03_symbols_md.tests_unit_ml_common_test_logging_py.test_json_formatter_extras.l3874 | evidence/03_symbols.md | 3874-3874 |
| ev.03_symbols_md.tests_unit_ml_common_test_run_id_py.test_generate_run_id_format.l3878 | evidence/03_symbols.md | 3878-3878 |
| ev.03_symbols_md.tests_unit_ml_common_test_run_id_py.test_generate_run_id_uniqueness.l3879 | evidence/03_symbols.md | 3879-3879 |
| ev.03_symbols_md.tests_unit_ml_data_test_bigquery_ranker_repository_py.make_repo.l3883 | evidence/03_symbols.md | 3883-3883 |
| ev.03_symbols_md.tests_unit_ml_data_test_bigquery_ranker_repository_py.test_fetch_training_rows_builds_parameterized_query.l3884 | evidence/03_symbols.md | 3884-3884 |
| ev.03_symbols_md.tests_unit_ml_data_test_bigquery_ranker_repository_py.test_save_run_records_ranker_metrics.l3885 | evidence/03_symbols.md | 3885-3885 |
| ev.03_symbols_md.tests_unit_ml_data_test_bigquery_ranker_repository_py.test_save_run_raises_on_insert_errors.l3886 | evidence/03_symbols.md | 3886-3886 |
| ev.03_symbols_md.tests_unit_ml_data_test_bigquery_ranker_repository_py.test_latest_model_path_returns_none_when_empty.l3887 | evidence/03_symbols.md | 3887-3887 |
| ev.03_symbols_md.tests_unit_ml_data_test_bigquery_ranker_repository_py.test_latest_model_path_returns_model_path.l3888 | evidence/03_symbols.md | 3888-3888 |
| ev.03_symbols_md.tests_unit_ml_data_test_bigquery_ranker_repository_py.test_save_run_dual_writes_to_vertex_experiments.l3889 | evidence/03_symbols.md | 3889-3889 |
| ev.03_symbols_md.tests_unit_ml_data_test_bigquery_ranker_repository_py.test_save_run_skips_vertex_experiments_without_env.l3890 | evidence/03_symbols.md | 3890-3890 |
| ev.03_symbols_md.tests_unit_ml_data_test_embedding_batch_py.fakeencoder.l3894 | evidence/03_symbols.md | 3894-3894 |
| ev.03_symbols_md.tests_unit_ml_data_test_embedding_batch_py.encode_passages.l3895 | evidence/03_symbols.md | 3895-3895 |
| ev.03_symbols_md.tests_unit_ml_data_test_embedding_batch_py.encode_queries.l3896 | evidence/03_symbols.md | 3896-3896 |
| ev.03_symbols_md.tests_unit_ml_data_test_embedding_batch_py.fakerepo.l3897 | evidence/03_symbols.md | 3897-3897 |
| ev.03_symbols_md.tests_unit_ml_data_test_embedding_batch_py.fetch_all.l3898 | evidence/03_symbols.md | 3898-3898 |
| ev.03_symbols_md.tests_unit_ml_data_test_embedding_batch_py.fakestore.l3899 | evidence/03_symbols.md | 3899-3899 |
| ev.03_symbols_md.tests_unit_ml_data_test_embedding_batch_py.existing_hashes.l3900 | evidence/03_symbols.md | 3900-3900 |
| ev.03_symbols_md.tests_unit_ml_data_test_embedding_batch_py.upsert.l3901 | evidence/03_symbols.md | 3901-3901 |
| ev.03_symbols_md.tests_unit_ml_data_test_embedding_batch_py.capturelogger.l3902 | evidence/03_symbols.md | 3902-3902 |
| ev.03_symbols_md.tests_unit_ml_data_test_embedding_batch_py.init.l3903 | evidence/03_symbols.md | 3903-3903 |
| ev.03_symbols_md.tests_unit_ml_data_test_embedding_batch_py.info.l3904 | evidence/03_symbols.md | 3904-3904 |
| ev.03_symbols_md.tests_unit_ml_data_test_embedding_batch_py.test_encodes_all_on_empty_store.l3905 | evidence/03_symbols.md | 3905-3905 |
| ev.03_symbols_md.tests_unit_ml_data_test_embedding_batch_py.test_skips_unchanged_rows_on_rerun.l3906 | evidence/03_symbols.md | 3906-3906 |
| ev.03_symbols_md.tests_unit_ml_data_test_embedding_batch_py.test_re_encodes_when_text_changes.l3907 | evidence/03_symbols.md | 3907-3907 |
| ev.03_symbols_md.tests_unit_ml_data_test_feature_engineering_ranker_py.test_build_ranker_features_keys_match_feature_cols_ranker.l3911 | evidence/03_symbols.md | 3911-3911 |
| ev.03_symbols_md.tests_unit_ml_data_test_feature_engineering_ranker_py.test_build_ranker_features_numeric_coercion.l3912 | evidence/03_symbols.md | 3912-3912 |
| ev.03_symbols_md.tests_unit_ml_data_test_feature_engineering_ranker_py.test_build_ranker_features_handles_missing_behavior.l3913 | evidence/03_symbols.md | 3913-3913 |
| ev.03_symbols_md.tests_unit_ml_evaluation_test_label_gain_py.test_request_complete_beats_favorite_beats_click.l3917 | evidence/03_symbols.md | 3917-3917 |
| ev.03_symbols_md.tests_unit_ml_evaluation_test_label_gain_py.test_empty_or_unknown_returns_zero.l3918 | evidence/03_symbols.md | 3918-3918 |
| ev.03_symbols_md.tests_unit_ml_evaluation_test_ranking_metrics_py.test_ndcg_perfect_ranking_is_one.l3922 | evidence/03_symbols.md | 3922-3922 |
| ev.03_symbols_md.tests_unit_ml_evaluation_test_ranking_metrics_py.test_ndcg_reversed_is_below_one.l3923 | evidence/03_symbols.md | 3923-3923 |
| ev.03_symbols_md.tests_unit_ml_evaluation_test_ranking_metrics_py.test_ndcg_all_zero_labels_is_zero.l3924 | evidence/03_symbols.md | 3924-3924 |
| ev.03_symbols_md.tests_unit_ml_evaluation_test_ranking_metrics_py.test_map_relevant_at_top_is_one.l3925 | evidence/03_symbols.md | 3925-3925 |
| ev.03_symbols_md.tests_unit_ml_evaluation_test_ranking_metrics_py.test_map_no_relevance_is_zero.l3926 | evidence/03_symbols.md | 3926-3926 |
| ev.03_symbols_md.tests_unit_ml_evaluation_test_ranking_metrics_py.test_recall_at_k_basic.l3927 | evidence/03_symbols.md | 3927-3927 |
| ev.03_symbols_md.tests_unit_ml_evaluation_test_ranking_metrics_py.test_evaluate_over_groups_returns_all_three_keys.l3928 | evidence/03_symbols.md | 3928-3928 |
| ev.03_symbols_md.tests_unit_ml_evaluation_test_ranking_metrics_py.test_evaluate_empty_input.l3929 | evidence/03_symbols.md | 3929-3929 |
| ev.03_symbols_md.tests_unit_ml_test_encoder_server_py.fakeencoder.l3933 | evidence/03_symbols.md | 3933-3933 |
| ev.03_symbols_md.tests_unit_ml_test_encoder_server_py.encode.l3934 | evidence/03_symbols.md | 3934-3934 |
| ev.03_symbols_md.tests_unit_ml_test_encoder_server_py.test_normalize_instance_accepts_prefixed_string.l3935 | evidence/03_symbols.md | 3935-3935 |
| ev.03_symbols_md.tests_unit_ml_test_encoder_server_py.test_normalize_instance_accepts_legacy_object_payload.l3936 | evidence/03_symbols.md | 3936-3936 |
| ev.03_symbols_md.tests_unit_ml_test_encoder_server_py.test_predict_accepts_mixed_request_shapes.l3937 | evidence/03_symbols.md | 3937-3937 |
| ev.03_symbols_md.tests_unit_ml_test_lightgbm_trainer_adapter_py.test_lightgbm_trainer_satisfies_ranker_trainer_protocol.l3941 | evidence/03_symbols.md | 3941-3941 |
| ev.03_symbols_md.tests_unit_ml_training_test_cli_run_py.inmemoryrepo.l3945 | evidence/03_symbols.md | 3945-3945 |
| ev.03_symbols_md.tests_unit_ml_training_test_cli_run_py.init.l3946 | evidence/03_symbols.md | 3946-3946 |
| ev.03_symbols_md.tests_unit_ml_training_test_cli_run_py.fetch_training_rows.l3947 | evidence/03_symbols.md | 3947-3947 |
| ev.03_symbols_md.tests_unit_ml_training_test_cli_run_py.save_run.l3948 | evidence/03_symbols.md | 3948-3948 |
| ev.03_symbols_md.tests_unit_ml_training_test_cli_run_py.latest_model_path.l3949 | evidence/03_symbols.md | 3949-3949 |
| ev.03_symbols_md.tests_unit_ml_training_test_cli_run_py.stubuploader.l3950 | evidence/03_symbols.md | 3950-3950 |
| ev.03_symbols_md.tests_unit_ml_training_test_cli_run_py.init.l3951 | evidence/03_symbols.md | 3951-3951 |
| ev.03_symbols_md.tests_unit_ml_training_test_cli_run_py.upload.l3952 | evidence/03_symbols.md | 3952-3952 |
| ev.03_symbols_md.tests_unit_ml_training_test_cli_run_py.stubtracker.l3953 | evidence/03_symbols.md | 3953-3953 |
| ev.03_symbols_md.tests_unit_ml_training_test_cli_run_py.init.l3954 | evidence/03_symbols.md | 3954-3954 |
| ev.03_symbols_md.tests_unit_ml_training_test_cli_run_py.enter.l3955 | evidence/03_symbols.md | 3955-3955 |
| ev.03_symbols_md.tests_unit_ml_training_test_cli_run_py.exit.l3956 | evidence/03_symbols.md | 3956-3956 |
| ev.03_symbols_md.tests_unit_ml_training_test_cli_run_py.log_metrics.l3957 | evidence/03_symbols.md | 3957-3957 |
| ev.03_symbols_md.tests_unit_ml_training_test_cli_run_py.tracker_factory.l3958 | evidence/03_symbols.md | 3958-3958 |
| ev.03_symbols_md.tests_unit_ml_training_test_cli_run_py.test_split_by_request_id_keeps_groups_intact.l3959 | evidence/03_symbols.md | 3959-3959 |
| ev.03_symbols_md.tests_unit_ml_training_test_cli_run_py.test_split_by_request_id_empty.l3960 | evidence/03_symbols.md | 3960-3960 |
| ev.03_symbols_md.tests_unit_ml_training_test_cli_run_py.test_run_non_dry_run_happy_path.l3961 | evidence/03_symbols.md | 3961-3961 |
| ev.03_symbols_md.tests_unit_ml_training_test_cli_run_py.test_run_non_dry_run_raises_on_empty_dataset.l3962 | evidence/03_symbols.md | 3962-3962 |
| ev.03_symbols_md.tests_unit_ml_training_test_cli_run_py.test_run_dry_run_skips_upload_and_save.l3963 | evidence/03_symbols.md | 3963-3963 |
| ev.03_symbols_md.tests_unit_ml_training_test_cli_run_py.frozen_time.l3964 | evidence/03_symbols.md | 3964-3964 |
| ev.03_symbols_md.tests_unit_ml_training_test_trainer_py.synthetic_frame.l3968 | evidence/03_symbols.md | 3968-3968 |
| ev.03_symbols_md.tests_unit_ml_training_test_trainer_py.test_group_sizes_contiguous.l3969 | evidence/03_symbols.md | 3969-3969 |
| ev.03_symbols_md.tests_unit_ml_training_test_trainer_py.test_group_sizes_empty.l3970 | evidence/03_symbols.md | 3970-3970 |
| ev.03_symbols_md.tests_unit_ml_training_test_trainer_py.test_rank_train_produces_booster.l3971 | evidence/03_symbols.md | 3971-3971 |
| ev.03_symbols_md.tests_unit_ml_training_test_trainer_py.test_rank_train_missing_columns_raises.l3972 | evidence/03_symbols.md | 3972-3972 |
| ev.03_symbols_md.tests_unit_ml_training_test_vertex_experiments_tracker_py.fake_aiplatform.l3976 | evidence/03_symbols.md | 3976-3976 |
| ev.03_symbols_md.tests_unit_ml_training_test_vertex_experiments_tracker_py.test_enter_initializes_aiplatform_and_starts_run.l3977 | evidence/03_symbols.md | 3977-3977 |
| ev.03_symbols_md.tests_unit_ml_training_test_vertex_experiments_tracker_py.test_log_metrics_filters_non_numeric.l3978 | evidence/03_symbols.md | 3978-3978 |
| ev.03_symbols_md.tests_unit_ml_training_test_vertex_experiments_tracker_py.test_log_params_filters_non_scalar_and_none.l3979 | evidence/03_symbols.md | 3979-3979 |
| ev.03_symbols_md.tests_unit_ml_training_test_vertex_experiments_tracker_py.test_exit_propagates_aiplatform_exit_then_clears_handle.l3980 | evidence/03_symbols.md | 3980-3980 |
| ev.03_symbols_md.tests_unit_ml_training_test_vertex_experiments_tracker_py.test_satisfies_experiment_tracker_protocol.l3981 | evidence/03_symbols.md | 3981-3981 |
| ev.03_symbols_md.tests_unit_pipeline_dags_test_dag_files_py.test_dag_file_is_syntactically_valid.l3985 | evidence/03_symbols.md | 3985-3985 |
| ev.03_symbols_md.tests_unit_pipeline_dags_test_dag_files_py.test_dag_id_matches_filename_stem.l3986 | evidence/03_symbols.md | 3986-3986 |
| ev.03_symbols_md.tests_unit_pipeline_dags_test_dag_files_py.test_dag_has_schedule_and_catchup_false.l3987 | evidence/03_symbols.md | 3987-3987 |
| ev.03_symbols_md.tests_unit_pipeline_dags_test_dag_files_py.test_dag_does_not_use_bash_operator.l3988 | evidence/03_symbols.md | 3988-3988 |
| ev.03_symbols_md.tests_unit_pipeline_dags_test_dag_files_py.test_retrain_orchestration_invokes_compile_via_pod_runner_not_import.l3989 | evidence/03_symbols.md | 3989-3989 |
| ev.03_symbols_md.tests_unit_pipeline_dags_test_dag_files_py.test_dag_uses_pod_or_provider_operator.l3990 | evidence/03_symbols.md | 3990-3990 |
| ev.03_symbols_md.tests_unit_pipeline_dags_test_dag_files_py.test_monitoring_validation_sql_paths_resolve_to_real_files.l3991 | evidence/03_symbols.md | 3991-3991 |
| ev.03_symbols_md.tests_unit_pipeline_dags_test_dag_files_py.test_all_dag_files_present.l3992 | evidence/03_symbols.md | 3992-3992 |
| ev.03_symbols_md.tests_unit_pipeline_test_data_job_dag_wiring_py.main_source.l3996 | evidence/03_symbols.md | 3996-3996 |
| ev.03_symbols_md.tests_unit_pipeline_test_data_job_dag_wiring_py.test_pipeline_signature_declares_strangler_off_defaults.l3997 | evidence/03_symbols.md | 3997-3997 |
| ev.03_symbols_md.tests_unit_pipeline_test_data_job_dag_wiring_py.test_build_pipeline_spec_lists_vector_search_params_with_strangler_defaults.l3998 | evidence/03_symbols.md | 3998-3998 |
| ev.03_symbols_md.tests_unit_pipeline_test_data_job_dag_wiring_py.test_build_pipeline_spec_steps_include_upsert_vector_search.l3999 | evidence/03_symbols.md | 3999-3999 |
| ev.03_symbols_md.tests_unit_pipeline_test_data_job_dag_wiring_py.test_pipeline_body_invokes_upsert_vector_search.l4000 | evidence/03_symbols.md | 4000-4000 |
| ev.03_symbols_md.tests_unit_pipeline_test_data_job_dag_wiring_py.test_pipeline_imports_upsert_component.l4001 | evidence/03_symbols.md | 4001-4001 |
| ev.03_symbols_md.tests_unit_pipeline_test_ground_truth_jobs_py.test_labeling_job_builds_labels_from_impressions_and_actions.l4005 | evidence/03_symbols.md | 4005-4005 |
| ev.03_symbols_md.tests_unit_pipeline_test_ground_truth_jobs_py.fakeeventrepository.l4006 | evidence/03_symbols.md | 4006-4006 |
| ev.03_symbols_md.tests_unit_pipeline_test_ground_truth_jobs_py.read_impressions.l4007 | evidence/03_symbols.md | 4007-4007 |
| ev.03_symbols_md.tests_unit_pipeline_test_ground_truth_jobs_py.read_user_actions.l4008 | evidence/03_symbols.md | 4008-4008 |
| ev.03_symbols_md.tests_unit_pipeline_test_ground_truth_jobs_py.fakelabelrepository.l4009 | evidence/03_symbols.md | 4009-4009 |
| ev.03_symbols_md.tests_unit_pipeline_test_ground_truth_jobs_py.write_ranking_labels.l4010 | evidence/03_symbols.md | 4010-4010 |
| ev.03_symbols_md.tests_unit_pipeline_test_ground_truth_jobs_py.test_training_dataset_job_exports_relevance_label_csv.l4011 | evidence/03_symbols.md | 4011-4011 |
| ev.03_symbols_md.tests_unit_pipeline_test_ground_truth_jobs_py.fakerepository.l4012 | evidence/03_symbols.md | 4012-4012 |
| ev.03_symbols_md.tests_unit_pipeline_test_ground_truth_jobs_py.fetch_training_rows.l4013 | evidence/03_symbols.md | 4013-4013 |
| ev.03_symbols_md.tests_unit_pipeline_test_kfp_orchestrator_py.stubcomponent.l4017 | evidence/03_symbols.md | 4017-4017 |
| ev.03_symbols_md.tests_unit_pipeline_test_kfp_orchestrator_py.init.l4018 | evidence/03_symbols.md | 4018-4018 |
| ev.03_symbols_md.tests_unit_pipeline_test_kfp_orchestrator_py.name.l4019 | evidence/03_symbols.md | 4019-4019 |
| ev.03_symbols_md.tests_unit_pipeline_test_kfp_orchestrator_py.to_runtime_task.l4020 | evidence/03_symbols.md | 4020-4020 |
| ev.03_symbols_md.tests_unit_pipeline_test_kfp_orchestrator_py.test_kfp_orchestrator_satisfies_protocol.l4021 | evidence/03_symbols.md | 4021-4021 |
| ev.03_symbols_md.tests_unit_pipeline_test_pipeline_trigger_py.test_decode_pubsub_message_reads_json_payload.l4025 | evidence/03_symbols.md | 4025-4025 |
| ev.03_symbols_md.tests_unit_pipeline_test_pipeline_trigger_py.test_decode_pubsub_message_returns_empty_when_payload_missing.l4026 | evidence/03_symbols.md | 4026-4026 |
| ev.03_symbols_md.tests_unit_pipeline_test_pipeline_trigger_py.test_merge_parameters_promotes_reasons.l4027 | evidence/03_symbols.md | 4027-4027 |
| ev.03_symbols_md.tests_unit_pipeline_test_pipeline_trigger_py.test_merge_parameters_overrides_defaults_with_event_payload.l4028 | evidence/03_symbols.md | 4028-4028 |
| ev.03_symbols_md.tests_unit_pipeline_test_pipeline_trigger_py.test_build_job_id_uses_prefix.l4029 | evidence/03_symbols.md | 4029-4029 |
| ev.03_symbols_md.tests_unit_pipeline_test_vector_search_writer_py.datapoint.l4033 | evidence/03_symbols.md | 4033-4033 |
| ev.03_symbols_md.tests_unit_pipeline_test_vector_search_writer_py.test_in_memory_writer_records_datapoints.l4034 | evidence/03_symbols.md | 4034-4034 |
| ev.03_symbols_md.tests_unit_pipeline_test_vector_search_writer_py.test_in_memory_writer_is_idempotent.l4035 | evidence/03_symbols.md | 4035-4035 |
| ev.03_symbols_md.tests_unit_pipeline_test_vector_search_writer_py.test_in_memory_writer_skips_empty_batch.l4036 | evidence/03_symbols.md | 4036-4036 |
| ev.03_symbols_md.tests_unit_pipeline_test_vector_search_writer_py.index_with_recorder.l4037 | evidence/03_symbols.md | 4037-4037 |
| ev.03_symbols_md.tests_unit_pipeline_test_vector_search_writer_py.upsert.l4038 | evidence/03_symbols.md | 4038-4038 |
| ev.03_symbols_md.tests_unit_pipeline_test_vector_search_writer_py.test_vertex_writer_calls_upsert_datapoints_with_payload.l4039 | evidence/03_symbols.md | 4039-4039 |
| ev.03_symbols_md.tests_unit_pipeline_test_vector_search_writer_py.test_vertex_writer_chunks_large_batches.l4040 | evidence/03_symbols.md | 4040-4040 |
| ev.03_symbols_md.tests_unit_pipeline_test_vector_search_writer_py.test_vertex_writer_skips_empty_batch.l4041 | evidence/03_symbols.md | 4041-4041 |
| ev.03_symbols_md.tests_unit_pipeline_test_vector_search_writer_py.test_vertex_writer_resolves_index_once.l4042 | evidence/03_symbols.md | 4042-4042 |
| ev.03_symbols_md.tests_unit_pipeline_test_vector_search_writer_py.factory.l4043 | evidence/03_symbols.md | 4043-4043 |
| ev.03_symbols_md.tests_unit_pipeline_test_vector_search_writer_py.test_vertex_writer_rejects_invalid_args.l4044 | evidence/03_symbols.md | 4044-4044 |
| ev.03_symbols_md.tests_unit_scripts_test_adapters_py.fakeproc.l4048 | evidence/03_symbols.md | 4048-4048 |
| ev.03_symbols_md.tests_unit_scripts_test_adapters_py.init.l4049 | evidence/03_symbols.md | 4049-4049 |
| ev.03_symbols_md.tests_unit_scripts_test_adapters_py.test_kubectl_run_prefixes_kubectl_to_args.l4050 | evidence/03_symbols.md | 4050-4050 |
| ev.03_symbols_md.tests_unit_scripts_test_adapters_py.test_kubectl_run_forwards_capture_check_timeout.l4051 | evidence/03_symbols.md | 4051-4051 |
| ev.03_symbols_md.tests_unit_scripts_test_adapters_py.test_kubectl_run_forwards_input_for_stdin_apply.l4052 | evidence/03_symbols.md | 4052-4052 |
| ev.03_symbols_md.tests_unit_scripts_test_adapters_py.test_terraform_run_inserts_chdir_flag.l4053 | evidence/03_symbols.md | 4053-4053 |
| ev.03_symbols_md.tests_unit_scripts_test_adapters_py.test_terraform_run_omits_chdir_when_none.l4054 | evidence/03_symbols.md | 4054-4054 |
| ev.03_symbols_md.tests_unit_scripts_test_adapters_py.test_gcloud_run_prefixes_gcloud_to_args.l4055 | evidence/03_symbols.md | 4055-4055 |
| ev.03_symbols_md.tests_unit_scripts_test_adapters_py.test_gcloud_run_forwards_capture_check_timeout.l4056 | evidence/03_symbols.md | 4056-4056 |
| ev.03_symbols_md.tests_unit_scripts_test_common_resolve_project_py.test_resolve_project_id_prefers_gcp_project.l4060 | evidence/03_symbols.md | 4060-4060 |
| ev.03_symbols_md.tests_unit_scripts_test_common_resolve_project_py.test_resolve_project_id_falls_back_to_project_id.l4061 | evidence/03_symbols.md | 4061-4061 |
| ev.03_symbols_md.tests_unit_scripts_test_common_resolve_project_py.test_resolve_project_id_falls_back_to_defaults.l4062 | evidence/03_symbols.md | 4062-4062 |
| ev.03_symbols_md.tests_unit_scripts_test_common_resolve_project_py.test_env_project_id_reads_gcp_project_when_project_id_empty.l4063 | evidence/03_symbols.md | 4063-4063 |
| ev.03_symbols_md.tests_unit_scripts_test_common_resolve_project_py.test_env_gcp_project_reads_project_id_when_gcp_empty.l4064 | evidence/03_symbols.md | 4064-4064 |
| ev.03_symbols_md.tests_unit_scripts_test_composer_deploy_dags_py.fake_run_factory.l4068 | evidence/03_symbols.md | 4068-4068 |
| ev.03_symbols_md.tests_unit_scripts_test_composer_deploy_dags_py.fake_run.l4069 | evidence/03_symbols.md | 4069-4069 |
| ev.03_symbols_md.tests_unit_scripts_test_composer_deploy_dags_py.test_main_early_returns_when_dag_bucket_empty.l4070 | evidence/03_symbols.md | 4070-4070 |
| ev.03_symbols_md.tests_unit_scripts_test_composer_deploy_dags_py.test_main_uploads_dags_when_bucket_set.l4071 | evidence/03_symbols.md | 4071-4071 |
| ev.03_symbols_md.tests_unit_scripts_test_composer_deploy_dags_py.fake_terraform_run.l4072 | evidence/03_symbols.md | 4072-4072 |
| ev.03_symbols_md.tests_unit_scripts_test_composer_deploy_dags_py.fake_run.l4073 | evidence/03_symbols.md | 4073-4073 |
| ev.03_symbols_md.tests_unit_scripts_test_composer_deploy_dags_py.test_main_raises_when_terraform_output_fails.l4074 | evidence/03_symbols.md | 4074-4074 |
| ev.03_symbols_md.tests_unit_scripts_test_composer_deploy_dags_py.test_main_raises_on_invalid_json.l4075 | evidence/03_symbols.md | 4075-4075 |
| ev.03_symbols_md.tests_unit_scripts_test_composer_deploy_dags_py.test_top_level_dag_listing_excludes_underscore_files.l4076 | evidence/03_symbols.md | 4076-4076 |
| ev.03_symbols_md.tests_unit_scripts_test_composer_deploy_dags_py.test_pipeline_pkg_files_listed_with_gcs_relative_paths.l4077 | evidence/03_symbols.md | 4077-4077 |
| ev.03_symbols_md.tests_unit_scripts_test_composer_deploy_dags_py.test_data_files_listed_for_sql_assets.l4078 | evidence/03_symbols.md | 4078-4078 |
| ev.03_symbols_md.tests_unit_scripts_test_composer_task_states_py.test_extract_json_array_strips_prologue.l4082 | evidence/03_symbols.md | 4082-4082 |
| ev.03_symbols_md.tests_unit_scripts_test_composer_task_states_py.test_latest_run_id_first_row.l4083 | evidence/03_symbols.md | 4083-4083 |
| ev.03_symbols_md.tests_unit_scripts_test_configmap_overlay_py.test_feature_online_store_public_domain_from_api_parses_rest_shape.l4087 | evidence/03_symbols.md | 4087-4087 |
| ev.03_symbols_md.tests_unit_scripts_test_configmap_overlay_py.test_feature_online_store_public_domain_from_api_returns_empty_on_missing_domain.l4088 | evidence/03_symbols.md | 4088-4088 |
| ev.03_symbols_md.tests_unit_scripts_test_deploy_all_step_timing_py.reset_globals.l4092 | evidence/03_symbols.md | 4092-4092 |
| ev.03_symbols_md.tests_unit_scripts_test_deploy_all_step_timing_py.test_step_first_call_emits_header_without_elapsed_anchor.l4093 | evidence/03_symbols.md | 4093-4093 |
| ev.03_symbols_md.tests_unit_scripts_test_deploy_all_step_timing_py.test_step_subsequent_calls_emit_elapsed_anchor.l4094 | evidence/03_symbols.md | 4094-4094 |
| ev.03_symbols_md.tests_unit_scripts_test_deploy_all_step_timing_py.test_step_done_emits_elapsed_line_matching_monitor_contract.l4095 | evidence/03_symbols.md | 4095-4095 |
| ev.03_symbols_md.tests_unit_scripts_test_deploy_all_step_timing_py.test_step_done_noop_before_any_step.l4096 | evidence/03_symbols.md | 4096-4096 |
| ev.03_symbols_md.tests_unit_scripts_test_deploy_all_step_timing_py.test_resolve_step_ref_accepts_number_and_name.l4097 | evidence/03_symbols.md | 4097-4097 |
| ev.03_symbols_md.tests_unit_scripts_test_deploy_all_step_timing_py.test_main_honors_from_step_and_to_step.l4098 | evidence/03_symbols.md | 4098-4098 |
| ev.03_symbols_md.tests_unit_scripts_test_deploy_all_step_timing_py.runner.l4099 | evidence/03_symbols.md | 4099-4099 |
| ev.03_symbols_md.tests_unit_scripts_test_deploy_all_step_timing_py.run.l4100 | evidence/03_symbols.md | 4100-4100 |
| ev.03_symbols_md.tests_unit_scripts_test_deploy_all_step_timing_py.test_main_prints_failure_summary_for_nonzero_step.l4101 | evidence/03_symbols.md | 4101-4101 |
| ev.03_symbols_md.tests_unit_scripts_test_deploy_all_step_timing_py.test_run_tf_apply_uses_staged_apply_and_waits_for_readiness.l4102 | evidence/03_symbols.md | 4102-4102 |
| ev.03_symbols_md.tests_unit_scripts_test_deploy_all_step_timing_py.fake_stage1.l4103 | evidence/03_symbols.md | 4103-4103 |
| ev.03_symbols_md.tests_unit_scripts_test_deploy_all_step_timing_py.fake_stream.l4104 | evidence/03_symbols.md | 4104-4104 |
| ev.03_symbols_md.tests_unit_scripts_test_deploy_all_step_timing_py.test_run_sync_elasticsearch_uses_project_and_default_cluster_url.l4105 | evidence/03_symbols.md | 4105-4105 |
| ev.03_symbols_md.tests_unit_scripts_test_deploy_all_step_timing_py.test_run_sync_elasticsearch_propagates_nonzero_exit.l4106 | evidence/03_symbols.md | 4106-4106 |
| ev.03_symbols_md.tests_unit_scripts_test_deploy_all_step_timing_py.test_main_invokes_precondition_before_run.l4107 | evidence/03_symbols.md | 4107-4107 |
| ev.03_symbols_md.tests_unit_scripts_test_deploy_all_step_timing_py.fake_pre.l4108 | evidence/03_symbols.md | 4108-4108 |
| ev.03_symbols_md.tests_unit_scripts_test_deploy_all_step_timing_py.fake_run.l4109 | evidence/03_symbols.md | 4109-4109 |
| ev.03_symbols_md.tests_unit_scripts_test_deploy_all_step_timing_py.test_main_skips_precondition_when_none.l4110 | evidence/03_symbols.md | 4110-4110 |
| ev.03_symbols_md.tests_unit_scripts_test_deploy_all_step_timing_py.fake_run.l4111 | evidence/03_symbols.md | 4111-4111 |
| ev.03_symbols_md.tests_unit_scripts_test_deploy_all_step_timing_py.test_main_propagates_precondition_exception_as_step_failure.l4112 | evidence/03_symbols.md | 4112-4112 |
| ev.03_symbols_md.tests_unit_scripts_test_deploy_all_step_timing_py.fake_pre.l4113 | evidence/03_symbols.md | 4113-4113 |
| ev.03_symbols_md.tests_unit_scripts_test_deploy_all_step_timing_py.fake_run.l4114 | evidence/03_symbols.md | 4114-4114 |
| ev.03_symbols_md.tests_unit_scripts_test_destroy_check_py.test_classify_bucket_names_splits_fail_and_warn.l4118 | evidence/03_symbols.md | 4118-4118 |
| ev.03_symbols_md.tests_unit_scripts_test_destroy_check_py.test_classify_artifact_repos_splits_google_managed_repo.l4119 | evidence/03_symbols.md | 4119-4119 |
| ev.03_symbols_md.tests_unit_scripts_test_destroy_check_py.test_filter_high_cost_datasets_ignores_unrelated_datasets.l4120 | evidence/03_symbols.md | 4120-4120 |
| ev.03_symbols_md.tests_unit_scripts_test_destroy_check_py.test_looks_like_api_disabled_detects_disabled_service_errors.l4121 | evidence/03_symbols.md | 4121-4121 |
| ev.03_symbols_md.tests_unit_scripts_test_elasticsearch_wait_py.fakeproc.l4125 | evidence/03_symbols.md | 4125-4125 |
| ev.03_symbols_md.tests_unit_scripts_test_elasticsearch_wait_py.init.l4126 | evidence/03_symbols.md | 4126-4126 |
| ev.03_symbols_md.tests_unit_scripts_test_elasticsearch_wait_py.test_wait_returns_immediately_on_green.l4127 | evidence/03_symbols.md | 4127-4127 |
| ev.03_symbols_md.tests_unit_scripts_test_elasticsearch_wait_py.test_wait_accepts_yellow_for_single_node_cluster.l4128 | evidence/03_symbols.md | 4128-4128 |
| ev.03_symbols_md.tests_unit_scripts_test_elasticsearch_wait_py.test_wait_polls_until_health_becomes_green.l4129 | evidence/03_symbols.md | 4129-4129 |
| ev.03_symbols_md.tests_unit_scripts_test_elasticsearch_wait_py.fake_kubectl_run.l4130 | evidence/03_symbols.md | 4130-4130 |
| ev.03_symbols_md.tests_unit_scripts_test_elasticsearch_wait_py.test_wait_raises_timeout_on_stuck_unknown.l4131 | evidence/03_symbols.md | 4131-4131 |
| ev.03_symbols_md.tests_unit_scripts_test_elasticsearch_wait_py.test_healthy_states_pin_green_and_yellow.l4132 | evidence/03_symbols.md | 4132-4132 |
| ev.03_symbols_md.tests_unit_scripts_test_infra_cleanup_py.completed.l4136 | evidence/03_symbols.md | 4136-4136 |
| ev.03_symbols_md.tests_unit_scripts_test_infra_cleanup_py.test_delete_orphan_workloads_invokes_two_kubectl_deletes.l4137 | evidence/03_symbols.md | 4137-4137 |
| ev.03_symbols_md.tests_unit_scripts_test_infra_cleanup_py.fake_run.l4138 | evidence/03_symbols.md | 4138-4138 |
| ev.03_symbols_md.tests_unit_scripts_test_infra_cleanup_py.test_delete_orphan_workloads_swallows_kubectl_failure.l4139 | evidence/03_symbols.md | 4139-4139 |
| ev.03_symbols_md.tests_unit_scripts_test_infra_cleanup_py.fake_run.l4140 | evidence/03_symbols.md | 4140-4140 |
| ev.03_symbols_md.tests_unit_scripts_test_infra_cleanup_py.test_wipe_bucket_passes_recursive_glob.l4141 | evidence/03_symbols.md | 4141-4141 |
| ev.03_symbols_md.tests_unit_scripts_test_infra_cleanup_py.fake_run.l4142 | evidence/03_symbols.md | 4142-4142 |
| ev.03_symbols_md.tests_unit_scripts_test_infra_cleanup_py.test_wipe_all_iterates_bucket_suffixes.l4143 | evidence/03_symbols.md | 4143-4143 |
| ev.03_symbols_md.tests_unit_scripts_test_infra_cleanup_py.fake_run.l4144 | evidence/03_symbols.md | 4144-4144 |
| ev.03_symbols_md.tests_unit_scripts_test_infra_cleanup_py.test_undeploy_endpoint_models_skips_when_endpoint_absent.l4145 | evidence/03_symbols.md | 4145-4145 |
| ev.03_symbols_md.tests_unit_scripts_test_infra_cleanup_py.test_undeploy_endpoint_models_skips_when_no_deployed.l4146 | evidence/03_symbols.md | 4146-4146 |
| ev.03_symbols_md.tests_unit_scripts_test_infra_cleanup_py.test_undeploy_endpoint_models_iterates_deployed_models.l4147 | evidence/03_symbols.md | 4147-4147 |
| ev.03_symbols_md.tests_unit_scripts_test_infra_cleanup_py.fake_run.l4148 | evidence/03_symbols.md | 4148-4148 |
| ev.03_symbols_md.tests_unit_scripts_test_infra_cleanup_py.test_deployed_index_exists_reads_index_endpoint_payload.l4149 | evidence/03_symbols.md | 4149-4149 |
| ev.03_symbols_md.tests_unit_scripts_test_infra_cleanup_py.test_wait_for_deployed_index_absent_polls_until_stale_index_disappears.l4150 | evidence/03_symbols.md | 4150-4150 |
| ev.03_symbols_md.tests_unit_scripts_test_infra_cleanup_py.test_wait_for_deployed_index_absent_early_exits_on_ready_state.l4151 | evidence/03_symbols.md | 4151-4151 |
| ev.03_symbols_md.tests_unit_scripts_test_infra_cleanup_py.test_deployed_index_state_classifies_ready_vs_transitional.l4152 | evidence/03_symbols.md | 4152-4152 |
| ev.03_symbols_md.tests_unit_scripts_test_infra_feature_view_sync_py.fakeresponse.l4156 | evidence/03_symbols.md | 4156-4156 |
| ev.03_symbols_md.tests_unit_scripts_test_infra_feature_view_sync_py.init.l4157 | evidence/03_symbols.md | 4157-4157 |
| ev.03_symbols_md.tests_unit_scripts_test_infra_feature_view_sync_py.read.l4158 | evidence/03_symbols.md | 4158-4158 |
| ev.03_symbols_md.tests_unit_scripts_test_infra_feature_view_sync_py.enter.l4159 | evidence/03_symbols.md | 4159-4159 |
| ev.03_symbols_md.tests_unit_scripts_test_infra_feature_view_sync_py.exit.l4160 | evidence/03_symbols.md | 4160-4160 |
| ev.03_symbols_md.tests_unit_scripts_test_infra_feature_view_sync_py.test_main_skips_when_fos_outputs_are_empty.l4161 | evidence/03_symbols.md | 4161-4161 |
| ev.03_symbols_md.tests_unit_scripts_test_infra_feature_view_sync_py.test_trigger_and_wait_posts_sync_then_polls_until_complete.l4162 | evidence/03_symbols.md | 4162-4162 |
| ev.03_symbols_md.tests_unit_scripts_test_infra_feature_view_sync_py.fake_urlopen.l4163 | evidence/03_symbols.md | 4163-4163 |
| ev.03_symbols_md.tests_unit_scripts_test_infra_terraform_state_py.completed.l4167 | evidence/03_symbols.md | 4167-4167 |
| ev.03_symbols_md.tests_unit_scripts_test_infra_terraform_state_py.test_state_list_returns_empty_on_cli_failure.l4168 | evidence/03_symbols.md | 4168-4168 |
| ev.03_symbols_md.tests_unit_scripts_test_infra_terraform_state_py.test_state_list_returns_lines_when_present.l4169 | evidence/03_symbols.md | 4169-4169 |
| ev.03_symbols_md.tests_unit_scripts_test_infra_terraform_state_py.test_state_size_counts_addresses.l4170 | evidence/03_symbols.md | 4170-4170 |
| ev.03_symbols_md.tests_unit_scripts_test_infra_terraform_state_py.test_state_size_zero_on_cli_failure.l4171 | evidence/03_symbols.md | 4171-4171 |
| ev.03_symbols_md.tests_unit_scripts_test_infra_terraform_state_py.test_addresses_starting_with_filters_by_prefix.l4172 | evidence/03_symbols.md | 4172-4172 |
| ev.03_symbols_md.tests_unit_scripts_test_infra_terraform_state_py.test_is_in_state_true_when_address_present.l4173 | evidence/03_symbols.md | 4173-4173 |
| ev.03_symbols_md.tests_unit_scripts_test_infra_terraform_state_py.test_filter_targets_keeps_only_in_state.l4174 | evidence/03_symbols.md | 4174-4174 |
| ev.03_symbols_md.tests_unit_scripts_test_infra_terraform_state_py.test_state_rm_returns_true_on_success.l4175 | evidence/03_symbols.md | 4175-4175 |
| ev.03_symbols_md.tests_unit_scripts_test_infra_terraform_state_py.test_state_rm_returns_false_on_failure.l4176 | evidence/03_symbols.md | 4176-4176 |
| ev.03_symbols_md.tests_unit_scripts_test_infra_terraform_state_py.test_state_list_passes_env_when_supplied.l4177 | evidence/03_symbols.md | 4177-4177 |
| ev.03_symbols_md.tests_unit_scripts_test_infra_terraform_state_py.fake_run.l4178 | evidence/03_symbols.md | 4178-4178 |
| ev.03_symbols_md.tests_unit_scripts_test_kserve_models_deploy_py.fakemodel.l4182 | evidence/03_symbols.md | 4182-4182 |
| ev.03_symbols_md.tests_unit_scripts_test_kserve_models_deploy_py.init.l4183 | evidence/03_symbols.md | 4183-4183 |
| ev.03_symbols_md.tests_unit_scripts_test_kserve_models_deploy_py.install_fake_aiplatform.l4184 | evidence/03_symbols.md | 4184-4184 |
| ev.03_symbols_md.tests_unit_scripts_test_kserve_models_deploy_py.test_resolve_latest_prefers_model_with_production_alias.l4185 | evidence/03_symbols.md | 4185-4185 |
| ev.03_symbols_md.tests_unit_scripts_test_kserve_models_deploy_py.test_resolve_latest_falls_back_to_first_when_no_production_alias.l4186 | evidence/03_symbols.md | 4186-4186 |
| ev.03_symbols_md.tests_unit_scripts_test_kserve_models_deploy_py.test_resolve_latest_raises_when_no_models.l4187 | evidence/03_symbols.md | 4187-4187 |
| ev.03_symbols_md.tests_unit_scripts_test_kserve_models_deploy_py.test_resolve_latest_raises_when_artifact_uri_missing.l4188 | evidence/03_symbols.md | 4188-4188 |
| ev.03_symbols_md.tests_unit_scripts_test_kserve_models_deploy_py.capture_kubectl_patch_call.l4189 | evidence/03_symbols.md | 4189-4189 |
| ev.03_symbols_md.tests_unit_scripts_test_kserve_models_deploy_py.fake_run.l4190 | evidence/03_symbols.md | 4190-4190 |
| ev.03_symbols_md.tests_unit_scripts_test_kserve_models_deploy_py.capture_kubectl_run_call.l4191 | evidence/03_symbols.md | 4191-4191 |
| ev.03_symbols_md.tests_unit_scripts_test_kserve_models_deploy_py.fake_kubectl_run.l4192 | evidence/03_symbols.md | 4192-4192 |
| ev.03_symbols_md.tests_unit_scripts_test_kserve_models_deploy_py.test_patch_reranker_storage_uri_emits_expected_kubectl_shape.l4193 | evidence/03_symbols.md | 4193-4193 |
| ev.03_symbols_md.tests_unit_scripts_test_kserve_models_deploy_py.test_patch_encoder_storage_uri_is_noop_under_hf_runtime.l4194 | evidence/03_symbols.md | 4194-4194 |
| ev.03_symbols_md.tests_unit_scripts_test_kserve_models_deploy_py.test_resolve_latest_warns_on_production_alias_fallback.l4195 | evidence/03_symbols.md | 4195-4195 |
| ev.03_symbols_md.tests_unit_scripts_test_lib_config_py.test_configmap_keys_pin.l4199 | evidence/03_symbols.md | 4199-4199 |
| ev.03_symbols_md.tests_unit_scripts_test_lib_config_py.test_generate_configmap_data_returns_all_keys_strings.l4200 | evidence/03_symbols.md | 4200-4200 |
| ev.03_symbols_md.tests_unit_scripts_test_lib_config_py.test_committed_example_defaults_are_empty_for_vertex_resources.l4201 | evidence/03_symbols.md | 4201-4201 |
| ev.03_symbols_md.tests_unit_scripts_test_lib_config_py.test_generate_configmap_data_passes_through_live_vertex_outputs.l4202 | evidence/03_symbols.md | 4202-4202 |
| ev.03_symbols_md.tests_unit_scripts_test_lib_config_py.test_render_committed_form_matches_example_yaml.l4203 | evidence/03_symbols.md | 4203-4203 |
| ev.03_symbols_md.tests_unit_scripts_test_lib_config_py.test_render_runtime_form_omits_header.l4204 | evidence/03_symbols.md | 4204-4204 |
| ev.03_symbols_md.tests_unit_scripts_test_lib_config_py.test_render_values_are_double_quoted.l4205 | evidence/03_symbols.md | 4205-4205 |
| ev.03_symbols_md.tests_unit_scripts_test_lib_gcp_resources_py.test_vertex_endpoints_pin.l4209 | evidence/03_symbols.md | 4209-4209 |
| ev.03_symbols_md.tests_unit_scripts_test_lib_gcp_resources_py.test_bucket_suffixes_pin.l4210 | evidence/03_symbols.md | 4210-4210 |
| ev.03_symbols_md.tests_unit_scripts_test_lib_gcp_resources_py.test_default_names_pin.l4211 | evidence/03_symbols.md | 4211-4211 |
| ev.03_symbols_md.tests_unit_scripts_test_lib_gcp_resources_py.test_vertex_model_names_pin.l4212 | evidence/03_symbols.md | 4212-4212 |
| ev.03_symbols_md.tests_unit_scripts_test_lib_gcp_resources_py.test_endpoint_names_have_endpoint_suffix.l4213 | evidence/03_symbols.md | 4213-4213 |
| ev.03_symbols_md.tests_unit_scripts_test_lib_gcp_resources_py.test_model_names_no_endpoint_suffix.l4214 | evidence/03_symbols.md | 4214-4214 |
| ev.03_symbols_md.tests_unit_scripts_test_local_hybrid_py.test_resolve_elasticsearch_api_key_prefers_local_secret.l4218 | evidence/03_symbols.md | 4218-4218 |
| ev.03_symbols_md.tests_unit_scripts_test_local_hybrid_py.test_resolve_elasticsearch_api_key_empty_when_no_url.l4219 | evidence/03_symbols.md | 4219-4219 |
| ev.03_symbols_md.tests_unit_scripts_test_local_hybrid_py.test_resolve_elasticsearch_url_prefers_explicit_env.l4220 | evidence/03_symbols.md | 4220-4220 |
| ev.03_symbols_md.tests_unit_scripts_test_local_hybrid_py.test_resolve_elasticsearch_url_uses_local_when_http_available.l4221 | evidence/03_symbols.md | 4221-4221 |
| ev.03_symbols_md.tests_unit_scripts_test_local_hybrid_py.test_resolve_elasticsearch_url_returns_empty_when_unreachable.l4222 | evidence/03_symbols.md | 4222-4222 |
| ev.03_symbols_md.tests_unit_scripts_test_local_hybrid_py.test_ensure_local_reranker_model_skips_existing_file.l4223 | evidence/03_symbols.md | 4223-4223 |
| ev.03_symbols_md.tests_unit_scripts_test_monitor_py.test_step_regex_matches_deploy_all_step_log_format.l4227 | evidence/03_symbols.md | 4227-4227 |
| ev.03_symbols_md.tests_unit_scripts_test_monitor_py.test_step_regex_matches_single_space.l4228 | evidence/03_symbols.md | 4228-4228 |
| ev.03_symbols_md.tests_unit_scripts_test_monitor_py.test_step_regex_ignores_unrelated_lines.l4229 | evidence/03_symbols.md | 4229-4229 |
| ev.03_symbols_md.tests_unit_scripts_test_monitor_py.test_build_wait_regex_extracts_build_id_and_timeout.l4230 | evidence/03_symbols.md | 4230-4230 |
| ev.03_symbols_md.tests_unit_scripts_test_monitor_py.test_build_wait_regex_requires_numeric_timeout.l4231 | evidence/03_symbols.md | 4231-4231 |
| ev.03_symbols_md.tests_unit_scripts_test_monitor_py.test_maybe_parse_step_updates_state_and_clears_build_tracking.l4232 | evidence/03_symbols.md | 4232-4232 |
| ev.03_symbols_md.tests_unit_scripts_test_monitor_py.test_maybe_parse_step_noop_for_unrelated_line.l4233 | evidence/03_symbols.md | 4233-4233 |
| ev.03_symbols_md.tests_unit_scripts_test_monitor_py.test_maybe_parse_build_wait_records_build_id_and_start_time.l4234 | evidence/03_symbols.md | 4234-4234 |
| ev.03_symbols_md.tests_unit_scripts_test_monitor_py.test_maybe_parse_build_wait_noop_for_unrelated_line.l4235 | evidence/03_symbols.md | 4235-4235 |
| ev.03_symbols_md.tests_unit_scripts_test_promote_py.fakeregistry.l4239 | evidence/03_symbols.md | 4239-4239 |
| ev.03_symbols_md.tests_unit_scripts_test_promote_py.init.l4240 | evidence/03_symbols.md | 4240-4240 |
| ev.03_symbols_md.tests_unit_scripts_test_promote_py.add_version_aliases.l4241 | evidence/03_symbols.md | 4241-4241 |
| ev.03_symbols_md.tests_unit_scripts_test_promote_py.remove_version_aliases.l4242 | evidence/03_symbols.md | 4242-4242 |
| ev.03_symbols_md.tests_unit_scripts_test_promote_py.fakemodel.l4243 | evidence/03_symbols.md | 4243-4243 |
| ev.03_symbols_md.tests_unit_scripts_test_promote_py.init.l4244 | evidence/03_symbols.md | 4244-4244 |
| ev.03_symbols_md.tests_unit_scripts_test_promote_py.args.l4245 | evidence/03_symbols.md | 4245-4245 |
| ev.03_symbols_md.tests_unit_scripts_test_promote_py.test_resolve_display_name_uses_model_not_endpoint.l4246 | evidence/03_symbols.md | 4246-4246 |
| ev.03_symbols_md.tests_unit_scripts_test_promote_py.test_resolve_display_name_env_override_uses_model_named_var.l4247 | evidence/03_symbols.md | 4247-4247 |
| ev.03_symbols_md.tests_unit_scripts_test_promote_py.test_select_version_picks_explicit_version_id.l4248 | evidence/03_symbols.md | 4248-4248 |
| ev.03_symbols_md.tests_unit_scripts_test_promote_py.test_select_version_picks_alias.l4249 | evidence/03_symbols.md | 4249-4249 |
| ev.03_symbols_md.tests_unit_scripts_test_promote_py.test_select_version_errors_when_no_selector_matches.l4250 | evidence/03_symbols.md | 4250-4250 |
| ev.03_symbols_md.tests_unit_scripts_test_promote_py.test_set_production_alias_moves_alias_between_versions.l4251 | evidence/03_symbols.md | 4251-4251 |
| ev.03_symbols_md.tests_unit_scripts_test_promote_py.test_set_production_alias_dry_run_does_not_call_registry.l4252 | evidence/03_symbols.md | 4252-4252 |
| ev.03_symbols_md.tests_unit_scripts_test_promote_py.test_run_alias_fails_fast_when_artifact_uri_is_empty.l4253 | evidence/03_symbols.md | 4253-4253 |
| ev.03_symbols_md.tests_unit_scripts_test_promote_py.test_run_alias_applies_when_artifact_uri_has_objects.l4254 | evidence/03_symbols.md | 4254-4254 |
| ev.03_symbols_md.tests_unit_scripts_test_promote_py.test_bst_rename_no_op_when_bst_already_exists.l4255 | evidence/03_symbols.md | 4255-4255 |
| ev.03_symbols_md.tests_unit_scripts_test_promote_py.test_bst_rename_plans_copy_in_dry_run.l4256 | evidence/03_symbols.md | 4256-4256 |
| ev.03_symbols_md.tests_unit_scripts_test_promote_py.fail_cp.l4257 | evidence/03_symbols.md | 4257-4257 |
| ev.03_symbols_md.tests_unit_scripts_test_promote_py.test_bst_rename_returns_none_when_neither_file_present.l4258 | evidence/03_symbols.md | 4258-4258 |
| ev.03_symbols_md.tests_unit_scripts_test_repo_relative_paths_py.test_scripts_parents_paths_resolve.l4262 | evidence/03_symbols.md | 4262-4262 |
| ev.03_symbols_md.tests_unit_scripts_test_resolve_api_target_py.clear_target_env.l4266 | evidence/03_symbols.md | 4266-4266 |
| ev.03_symbols_md.tests_unit_scripts_test_resolve_api_target_py.test_explicit_api_url_wins_over_target_and_skips_token_by_default.l4267 | evidence/03_symbols.md | 4267-4267 |
| ev.03_symbols_md.tests_unit_scripts_test_resolve_api_target_py.test_explicit_api_url_honors_host_and_insecure_overrides.l4268 | evidence/03_symbols.md | 4268-4268 |
| ev.03_symbols_md.tests_unit_scripts_test_resolve_api_target_py.test_explicit_api_url_mints_token_when_require_token_truthy.l4269 | evidence/03_symbols.md | 4269-4269 |
| ev.03_symbols_md.tests_unit_scripts_test_resolve_api_target_py.test_target_local_uses_default_local_url_without_token.l4270 | evidence/03_symbols.md | 4270-4270 |
| ev.03_symbols_md.tests_unit_scripts_test_resolve_api_target_py.test_target_local_honors_local_api_url_override.l4271 | evidence/03_symbols.md | 4271-4271 |
| ev.03_symbols_md.tests_unit_scripts_test_resolve_api_target_py.test_target_gcp_default_uses_public_domain_with_valid_tls.l4272 | evidence/03_symbols.md | 4272-4272 |
| ev.03_symbols_md.tests_unit_scripts_test_resolve_api_target_py.test_target_gcp_public_domain_honors_insecure_tls_override.l4273 | evidence/03_symbols.md | 4273-4273 |
| ev.03_symbols_md.tests_unit_scripts_test_resolve_api_target_py.test_target_gcp_falls_back_to_gateway_ip_when_public_domain_empty.l4274 | evidence/03_symbols.md | 4274-4274 |
| ev.03_symbols_md.tests_unit_scripts_test_resolve_api_target_py.test_target_gcp_fallback_honors_api_host_header_override.l4275 | evidence/03_symbols.md | 4275-4275 |
| ev.03_symbols_md.tests_unit_scripts_test_resolve_api_target_py.test_unknown_target_raises.l4276 | evidence/03_symbols.md | 4276-4276 |
| ev.03_symbols_md.tests_unit_scripts_test_run_all_orchestrator_py.isolate_csv.l4280 | evidence/03_symbols.md | 4280-4280 |
| ev.03_symbols_md.tests_unit_scripts_test_run_all_orchestrator_py.test_steps_are_the_canonical_validation_sequence.l4281 | evidence/03_symbols.md | 4281-4281 |
| ev.03_symbols_md.tests_unit_scripts_test_run_all_orchestrator_py.test_main_runs_every_step_in_order_then_records_ok.l4282 | evidence/03_symbols.md | 4282-4282 |
| ev.03_symbols_md.tests_unit_scripts_test_run_all_orchestrator_py.fake_run.l4283 | evidence/03_symbols.md | 4283-4283 |
| ev.03_symbols_md.tests_unit_scripts_test_run_all_orchestrator_py.test_main_fails_fast_on_first_nonzero_step.l4284 | evidence/03_symbols.md | 4284-4284 |
| ev.03_symbols_md.tests_unit_scripts_test_run_all_orchestrator_py.fake_run.l4285 | evidence/03_symbols.md | 4285-4285 |
| ev.03_symbols_md.tests_unit_scripts_test_run_all_orchestrator_py.test_makefile_run_all_core_delegates_to_orchestrator.l4286 | evidence/03_symbols.md | 4286-4286 |
| ev.03_symbols_md.tests_unit_scripts_test_setup_policy_guard_py.read.l4290 | evidence/03_symbols.md | 4290-4290 |
| ev.03_symbols_md.tests_unit_scripts_test_setup_policy_guard_py.test_setup_scripts_use_canonical_and_ci_import_paths.l4291 | evidence/03_symbols.md | 4291-4291 |
| ev.03_symbols_md.tests_unit_scripts_test_setup_policy_guard_py.test_setup_scripts_target_dev_terraform_environment.l4292 | evidence/03_symbols.md | 4292-4292 |
| ev.03_symbols_md.tests_unit_scripts_test_setup_policy_guard_py.test_api_deploy_targets_gke_rollout_path.l4293 | evidence/03_symbols.md | 4293-4293 |
| ev.03_symbols_md.tests_unit_scripts_test_setup_policy_guard_py.test_makefile_has_canonical_ops_targets.l4294 | evidence/03_symbols.md | 4294-4294 |
| ev.03_symbols_md.tests_unit_scripts_test_setup_policy_guard_py.test_makefile_sync_elasticsearch_passes_required_args.l4295 | evidence/03_symbols.md | 4295-4295 |
| ev.03_symbols_md.tests_unit_scripts_test_setup_policy_guard_py.test_seed_and_feature_group_contract_pin_feature_timestamp.l4296 | evidence/03_symbols.md | 4296-4296 |
| ev.03_symbols_md.tests_unit_scripts_test_step_timing_py.isolate_csv.l4300 | evidence/03_symbols.md | 4300-4300 |
| ev.03_symbols_md.tests_unit_scripts_test_step_timing_py.test_fmt_duration_human_readable.l4301 | evidence/03_symbols.md | 4301-4301 |
| ev.03_symbols_md.tests_unit_scripts_test_step_timing_py.test_record_writes_header_then_rows_and_baselines_use_median_of_ok_runs.l4302 | evidence/03_symbols.md | 4302-4302 |
| ev.03_symbols_md.tests_unit_scripts_test_step_timing_py.test_record_keeps_only_recent_runs_per_step_for_the_median.l4303 | evidence/03_symbols.md | 4303-4303 |
| ev.03_symbols_md.tests_unit_scripts_test_step_timing_py.test_record_is_best_effort_and_never_raises.l4304 | evidence/03_symbols.md | 4304-4304 |
| ev.03_symbols_md.tests_unit_scripts_test_step_timing_py.test_print_eta_no_history.l4305 | evidence/03_symbols.md | 4305-4305 |
| ev.03_symbols_md.tests_unit_scripts_test_step_timing_py.test_print_eta_sums_known_step_baselines.l4306 | evidence/03_symbols.md | 4306-4306 |
| ev.03_symbols_md.tests_unit_scripts_test_step_timing_py.test_print_eta_all_known_uses_tilde_prefix.l4307 | evidence/03_symbols.md | 4307-4307 |
| ev.03_symbols_md.tests_unit_scripts_test_submit_train_pipeline_py.test_main_requires_pipeline_root_bucket.l4311 | evidence/03_symbols.md | 4311-4311 |
| ev.03_symbols_md.tests_unit_scripts_test_submit_train_pipeline_py.env_no_bucket.l4312 | evidence/03_symbols.md | 4312-4312 |
| ev.03_symbols_md.tests_unit_scripts_test_submit_train_pipeline_py.test_main_calls_compile_with_expanded_argv.l4313 | evidence/03_symbols.md | 4313-4313 |
| ev.03_symbols_md.tests_unit_scripts_test_subprocess_run_kwargs_guard_py.is_subprocess_run.l4317 | evidence/03_symbols.md | 4317-4317 |
| ev.03_symbols_md.tests_unit_scripts_test_subprocess_run_kwargs_guard_py.offending_calls.l4318 | evidence/03_symbols.md | 4318-4318 |
| ev.03_symbols_md.tests_unit_scripts_test_subprocess_run_kwargs_guard_py.test_no_raw_subprocess_run_capture_kwarg.l4319 | evidence/03_symbols.md | 4319-4319 |
| ev.03_symbols_md.tests_unit_scripts_test_sync_elasticsearch_exit_codes_py.test_run_returns_one_when_project_id_missing.l4323 | evidence/03_symbols.md | 4323-4323 |
| ev.03_symbols_md.tests_unit_scripts_test_sync_elasticsearch_exit_codes_py.test_run_returns_one_when_es_url_missing.l4324 | evidence/03_symbols.md | 4324-4324 |
| ev.03_symbols_md.tests_unit_scripts_test_terraform_lock_py.test_parse_lock_id_from_terraform_stderr.l4328 | evidence/03_symbols.md | 4328-4328 |
| ev.03_symbols_md.tests_unit_scripts_test_terraform_lock_py.test_is_state_lock_error.l4329 | evidence/03_symbols.md | 4329-4329 |
| ev.03_symbols_md.tests_unit_scripts_test_terraform_lock_py.test_should_auto_force_unlock_aliases.l4330 | evidence/03_symbols.md | 4330-4330 |
| ev.03_symbols_md.tests_unit_scripts_test_terraform_lock_py.test_parse_lock_id_handles_real_ansi_color_output.l4331 | evidence/03_symbols.md | 4331-4331 |
| ev.03_symbols_md.tests_unit_scripts_test_terraform_lock_py.test_parse_lock_id_returns_none_when_absent.l4332 | evidence/03_symbols.md | 4332-4332 |
| ev.03_symbols_md.tests_unit_scripts_test_vertex_feature_store_wait_py.test_wait_until_feature_store_names_released_exits_when_empty.l4336 | evidence/03_symbols.md | 4336-4336 |
| ev.03_symbols_md.tests_unit_scripts_test_vertex_feature_store_wait_py.fake_token.l4337 | evidence/03_symbols.md | 4337-4337 |
| ev.03_symbols_md.tests_unit_scripts_test_vertex_feature_store_wait_py.fake_rest.l4338 | evidence/03_symbols.md | 4338-4338 |
| ev.03_symbols_md.tests_unit_scripts_test_vertex_feature_store_wait_py.test_wait_until_feature_store_names_released_times_out.l4339 | evidence/03_symbols.md | 4339-4339 |
| ev.03_symbols_md.tests_unit_scripts_test_vertex_feature_store_wait_py.fake_token.l4340 | evidence/03_symbols.md | 4340-4340 |
| ev.03_symbols_md.tests_unit_scripts_test_vertex_feature_store_wait_py.fake_rest.l4341 | evidence/03_symbols.md | 4341-4341 |
| ev.03_symbols_md.tests_unit_scripts_test_vertex_ops_scripts_py.test_vector_search_probe_vector_has_expected_shape.l4345 | evidence/03_symbols.md | 4345-4345 |
| ev.03_symbols_md.tests_unit_scripts_test_vertex_ops_scripts_py.test_ops_search_retries_transient_timeout.l4346 | evidence/03_symbols.md | 4346-4346 |
| ev.03_symbols_md.tests_unit_scripts_test_vertex_ops_scripts_py.fake_once.l4347 | evidence/03_symbols.md | 4347-4347 |
| ev.03_symbols_md.tests_unit_scripts_test_vertex_ops_scripts_py.test_ops_search_fails_after_retry_budget.l4348 | evidence/03_symbols.md | 4348-4348 |
| ev.03_symbols_md.tests_unit_scripts_test_vertex_ops_scripts_py.test_backfill_build_spec_reads_required_env.l4349 | evidence/03_symbols.md | 4349-4349 |
| ev.03_symbols_md.tests_unit_scripts_test_vertex_ops_scripts_py.test_backfill_build_spec_falls_back_to_terraform_output.l4350 | evidence/03_symbols.md | 4350-4350 |
| ev.03_symbols_md.tests_unit_scripts_test_vertex_ops_scripts_py.test_backfill_build_spec_rejects_non_int_batch_size.l4351 | evidence/03_symbols.md | 4351-4351 |
| ev.03_symbols_md.tests_unit_scripts_test_vertex_ops_scripts_py.test_feature_group_uses_feature_view_env.l4352 | evidence/03_symbols.md | 4352-4352 |
| ev.03_symbols_md.tests_unit_scripts_test_vertex_ops_scripts_py.adminclient.l4353 | evidence/03_symbols.md | 4353-4353 |
| ev.03_symbols_md.tests_unit_scripts_test_vertex_ops_scripts_py.init.l4354 | evidence/03_symbols.md | 4354-4354 |
| ev.03_symbols_md.tests_unit_scripts_test_vertex_ops_scripts_py.get_feature_online_store.l4355 | evidence/03_symbols.md | 4355-4355 |
| ev.03_symbols_md.tests_unit_scripts_test_vertex_ops_scripts_py.get_feature_view.l4356 | evidence/03_symbols.md | 4356-4356 |
| ev.03_symbols_md.tests_unit_scripts_test_vertex_ops_scripts_py.datakey.l4357 | evidence/03_symbols.md | 4357-4357 |
| ev.03_symbols_md.tests_unit_scripts_test_vertex_ops_scripts_py.init.l4358 | evidence/03_symbols.md | 4358-4358 |
| ev.03_symbols_md.tests_unit_scripts_test_vertex_ops_scripts_py.request.l4359 | evidence/03_symbols.md | 4359-4359 |
| ev.03_symbols_md.tests_unit_scripts_test_vertex_ops_scripts_py.init.l4360 | evidence/03_symbols.md | 4360-4360 |
| ev.03_symbols_md.tests_unit_scripts_test_vertex_ops_scripts_py.servingclient.l4361 | evidence/03_symbols.md | 4361-4361 |
| ev.03_symbols_md.tests_unit_scripts_test_vertex_ops_scripts_py.init.l4362 | evidence/03_symbols.md | 4362-4362 |
| ev.03_symbols_md.tests_unit_scripts_test_vertex_ops_scripts_py.fetch_feature_values.l4363 | evidence/03_symbols.md | 4363-4363 |
| ev.03_symbols_md.tests_unit_scripts_test_vertex_ops_scripts_py.test_feature_group_404_emits_sync_and_bq_diagnostics.l4364 | evidence/03_symbols.md | 4364-4364 |
| ev.03_symbols_md.tests_unit_scripts_test_vertex_ops_scripts_py.notfounderror.l4365 | evidence/03_symbols.md | 4365-4365 |
| ev.03_symbols_md.tests_unit_scripts_test_vertex_ops_scripts_py.adminclient.l4366 | evidence/03_symbols.md | 4366-4366 |
| ev.03_symbols_md.tests_unit_scripts_test_vertex_ops_scripts_py.init.l4367 | evidence/03_symbols.md | 4367-4367 |
| ev.03_symbols_md.tests_unit_scripts_test_vertex_ops_scripts_py.get_feature_online_store.l4368 | evidence/03_symbols.md | 4368-4368 |
| ev.03_symbols_md.tests_unit_scripts_test_vertex_ops_scripts_py.get_feature_view.l4369 | evidence/03_symbols.md | 4369-4369 |
| ev.03_symbols_md.tests_unit_scripts_test_vertex_ops_scripts_py.datakey.l4370 | evidence/03_symbols.md | 4370-4370 |
| ev.03_symbols_md.tests_unit_scripts_test_vertex_ops_scripts_py.init.l4371 | evidence/03_symbols.md | 4371-4371 |
| ev.03_symbols_md.tests_unit_scripts_test_vertex_ops_scripts_py.request.l4372 | evidence/03_symbols.md | 4372-4372 |
| ev.03_symbols_md.tests_unit_scripts_test_vertex_ops_scripts_py.init.l4373 | evidence/03_symbols.md | 4373-4373 |
| ev.03_symbols_md.tests_unit_scripts_test_vertex_ops_scripts_py.servingclient.l4374 | evidence/03_symbols.md | 4374-4374 |
| ev.03_symbols_md.tests_unit_scripts_test_vertex_ops_scripts_py.init.l4375 | evidence/03_symbols.md | 4375-4375 |
| ev.03_symbols_md.tests_unit_scripts_test_vertex_ops_scripts_py.fetch_feature_values.l4376 | evidence/03_symbols.md | 4376-4376 |
| ev.03_symbols_md.tests_unit_scripts_test_vertex_ops_scripts_py.test_vector_search_resolves_ids_from_terraform_outputs.l4377 | evidence/03_symbols.md | 4377-4377 |
| ev.03_symbols_md.tests_unit_scripts_test_vertex_ops_scripts_py.endpoint.l4378 | evidence/03_symbols.md | 4378-4378 |
| ev.03_symbols_md.tests_unit_scripts_test_vertex_ops_scripts_py.init.l4379 | evidence/03_symbols.md | 4379-4379 |
| ev.03_symbols_md.tests_unit_scripts_test_vertex_ops_scripts_py.find_neighbors.l4380 | evidence/03_symbols.md | 4380-4380 |
| ev.03_symbols_md.tests_unit_scripts_test_vertex_ops_scripts_py.aiplatform.l4381 | evidence/03_symbols.md | 4381-4381 |
| ev.03_symbols_md.tests_unit_scripts_test_vertex_ops_scripts_py.init.l4382 | evidence/03_symbols.md | 4382-4382 |
| ev.03_symbols_md.tests_unit_scripts_test_vertex_ops_scripts_py.clear_aiplatform_sys_modules.l4383 | evidence/03_symbols.md | 4383-4383 |
| ev.03_symbols_md.tests_unit_scripts_test_vertex_ops_scripts_py.test_pipeline_wait_passes_when_latest_run_succeeds.l4384 | evidence/03_symbols.md | 4384-4384 |
| ev.03_symbols_md.tests_unit_scripts_test_vertex_ops_scripts_py.state.l4385 | evidence/03_symbols.md | 4385-4385 |
| ev.03_symbols_md.tests_unit_scripts_test_vertex_ops_scripts_py.init.l4386 | evidence/03_symbols.md | 4386-4386 |
| ev.03_symbols_md.tests_unit_scripts_test_vertex_ops_scripts_py.fake_latest.l4387 | evidence/03_symbols.md | 4387-4387 |
| ev.03_symbols_md.tests_unit_scripts_test_vertex_ops_scripts_py.test_pipeline_wait_resolves_project_from_gcp_project.l4388 | evidence/03_symbols.md | 4388-4388 |
| ev.03_symbols_md.tests_unit_scripts_test_vertex_ops_scripts_py.state.l4389 | evidence/03_symbols.md | 4389-4389 |
| ev.03_symbols_md.tests_unit_scripts_test_vertex_ops_scripts_py.init.l4390 | evidence/03_symbols.md | 4390-4390 |
| ev.03_symbols_md.tests_unit_scripts_test_vertex_ops_scripts_py.fake_latest.l4391 | evidence/03_symbols.md | 4391-4391 |
| ev.03_symbols_md.tests_unit_scripts_test_vertex_ops_scripts_py.test_pipeline_wait_fails_when_latest_run_fails.l4392 | evidence/03_symbols.md | 4392-4392 |
| ev.03_symbols_md.tests_unit_scripts_test_vertex_ops_scripts_py.state.l4393 | evidence/03_symbols.md | 4393-4393 |
| ev.03_symbols_md.tests_unit_scripts_test_vertex_ops_scripts_py.init.l4394 | evidence/03_symbols.md | 4394-4394 |
| ev.03_symbols_md.tests_unit_scripts_test_vertex_ops_scripts_py.fake_latest.l4395 | evidence/03_symbols.md | 4395-4395 |
| ev.03_symbols_md.tools_check_docker_layout_py.checkresult.l4399 | evidence/03_symbols.md | 4399-4399 |
| ev.03_symbols_md.tools_check_docker_layout_py.exists.l4400 | evidence/03_symbols.md | 4400-4400 |
| ev.03_symbols_md.tools_check_docker_layout_py.check_required.l4401 | evidence/03_symbols.md | 4401-4401 |
| ev.03_symbols_md.tools_check_docker_layout_py.check_unexpected_suffix_dockerfiles.l4402 | evidence/03_symbols.md | 4402-4402 |
| ev.03_symbols_md.tools_check_docker_layout_py.check_phase_layout_and_naming.l4403 | evidence/03_symbols.md | 4403-4403 |
| ev.03_symbols_md.tools_check_docker_layout_py.main.l4404 | evidence/03_symbols.md | 4404-4404 |
| ev.04_symbols_json | evidence/04_symbols.json | 1-3190 |
| ev.05_tests_md | evidence/05_tests.md | 1-1229 |
| ev.05_tests_md.app_static_js_search_ui_js | evidence/05_tests.md | 3-6 |
| ev.05_tests_md.tests_conftest_py | evidence/05_tests.md | 7-10 |
| ev.05_tests_md.tests_e2e_test_full_recreate_gate_py | evidence/05_tests.md | 11-16 |
| ev.05_tests_md.tests_e2e_test_live_acceptance_gate_py | evidence/05_tests.md | 17-21 |
| ev.05_tests_md.tests_integration_infra_test_destroy_all_table_parity_py | evidence/05_tests.md | 22-32 |
| ev.05_tests_md.tests_integration_infra_test_infra_ranker_tables_py | evidence/05_tests.md | 33-49 |
| ev.05_tests_md.tests_integration_infra_test_makefile_py | evidence/05_tests.md | 50-53 |
| ev.05_tests_md.tests_integration_infra_test_manifests_structure_py | evidence/05_tests.md | 54-70 |
| ev.05_tests_md.tests_integration_infra_test_public_domain_consistency_py | evidence/05_tests.md | 71-87 |
| ev.05_tests_md.tests_integration_infra_test_terraform_module_structure_py | evidence/05_tests.md | 88-93 |
| ev.05_tests_md.tests_integration_infra_test_workflows_structure_py | evidence/05_tests.md | 94-104 |
| ev.05_tests_md.tests_integration_parity_test_api_route_prefixes_py | evidence/05_tests.md | 105-120 |
| ev.05_tests_md.tests_integration_parity_test_codebase_invariants_py | evidence/05_tests.md | 121-133 |
| ev.05_tests_md.tests_integration_parity_test_configmap_drift_py | evidence/05_tests.md | 134-139 |
| ev.05_tests_md.tests_integration_parity_test_dataform_workflow_settings_py | evidence/05_tests.md | 140-145 |
| ev.05_tests_md.tests_integration_parity_test_event_schema_parity_py | evidence/05_tests.md | 146-160 |
| ev.05_tests_md.tests_integration_parity_test_feature_parity_feature_group_py | evidence/05_tests.md | 161-168 |
| ev.05_tests_md.tests_integration_parity_test_feature_parity_ranking_py | evidence/05_tests.md | 169-178 |
| ev.05_tests_md.tests_integration_parity_test_feature_parity_sql_ranker_py | evidence/05_tests.md | 179-186 |
| ev.05_tests_md.tests_integration_pipeline_test_pipeline_compile_py | evidence/05_tests.md | 187-193 |
| ev.05_tests_md.tests_integration_workflow_test_composer_dags_contract_py | evidence/05_tests.md | 194-204 |
| ev.05_tests_md.tests_integration_workflow_test_composer_gcloud_json_contract_py | evidence/05_tests.md | 205-213 |
| ev.05_tests_md.tests_integration_workflow_test_composer_module_contract_py | evidence/05_tests.md | 214-243 |
| ev.05_tests_md.tests_integration_workflow_test_deploy_all_contract_py | evidence/05_tests.md | 244-259 |
| ev.05_tests_md.tests_integration_workflow_test_destroy_all_contract_py | evidence/05_tests.md | 260-280 |
| ev.05_tests_md.tests_integration_workflow_test_docs_canonical_contract_py | evidence/05_tests.md | 281-286 |
| ev.05_tests_md.tests_integration_workflow_test_elasticsearch_workflow_contract_py | evidence/05_tests.md | 287-293 |
| ev.05_tests_md.tests_integration_workflow_test_ground_truth_contract_py | evidence/05_tests.md | 294-300 |
| ev.05_tests_md.tests_integration_workflow_test_infra_apis_contract_py | evidence/05_tests.md | 301-308 |
| ev.05_tests_md.tests_integration_workflow_test_local_workflow_contract_py | evidence/05_tests.md | 309-318 |
| ev.05_tests_md.tests_integration_workflow_test_vertex_pipeline_submit_contract_py | evidence/05_tests.md | 319-324 |
| ev.05_tests_md.tests_integration_workflow_test_vertex_resources_contract_py | evidence/05_tests.md | 325-333 |
| ev.05_tests_md.tests_unit_app_test_adapters_py | evidence/05_tests.md | 334-356 |
| ev.05_tests_md.tests_unit_app_test_api_contract_template_py | evidence/05_tests.md | 357-374 |
| ev.05_tests_md.tests_unit_app_test_bq_retrain_queries_py | evidence/05_tests.md | 375-386 |
| ev.05_tests_md.tests_unit_app_test_check_retrain_endpoint_py | evidence/05_tests.md | 387-398 |
| ev.05_tests_md.tests_unit_app_test_elasticsearch_lexical_py | evidence/05_tests.md | 399-403 |
| ev.05_tests_md.tests_unit_app_test_event_repositories_py | evidence/05_tests.md | 404-411 |
| ev.05_tests_md.tests_unit_app_test_explain_py | evidence/05_tests.md | 412-422 |
| ev.05_tests_md.tests_unit_app_test_feature_fetcher_adapters_py | evidence/05_tests.md | 423-443 |
| ev.05_tests_md.tests_unit_app_test_feedback_handler_http_py | evidence/05_tests.md | 444-449 |
| ev.05_tests_md.tests_unit_app_test_feedback_service_py | evidence/05_tests.md | 450-455 |
| ev.05_tests_md.tests_unit_app_test_health_handler_py | evidence/05_tests.md | 456-462 |
| ev.05_tests_md.tests_unit_app_test_kserve_wiring_py | evidence/05_tests.md | 463-479 |
| ev.05_tests_md.tests_unit_app_test_local_boot_contract_py | evidence/05_tests.md | 480-484 |
| ev.05_tests_md.tests_unit_app_test_logging_middleware_py | evidence/05_tests.md | 485-490 |
| ev.05_tests_md.tests_unit_app_test_main_routing_py | evidence/05_tests.md | 491-504 |
| ev.05_tests_md.tests_unit_app_test_model_handler_py | evidence/05_tests.md | 505-516 |
| ev.05_tests_md.tests_unit_app_test_observability_py | evidence/05_tests.md | 517-523 |
| ev.05_tests_md.tests_unit_app_test_ops_handler_py | evidence/05_tests.md | 524-532 |
| ev.05_tests_md.tests_unit_app_test_optional_adapter_helper_py | evidence/05_tests.md | 533-540 |
| ev.05_tests_md.tests_unit_app_test_publisher_py | evidence/05_tests.md | 541-544 |
| ev.05_tests_md.tests_unit_app_test_pubsub_event_writer_py | evidence/05_tests.md | 545-557 |
| ev.05_tests_md.tests_unit_app_test_ranking_service_py | evidence/05_tests.md | 558-578 |
| ev.05_tests_md.tests_unit_app_test_retrain_py | evidence/05_tests.md | 579-598 |
| ev.05_tests_md.tests_unit_app_test_run_search_feature_fetcher_py | evidence/05_tests.md | 599-614 |
| ev.05_tests_md.tests_unit_app_test_search_api_py | evidence/05_tests.md | 615-638 |
| ev.05_tests_md.tests_unit_app_test_search_builder_canonical_py | evidence/05_tests.md | 639-656 |
| ev.05_tests_md.tests_unit_app_test_search_handler_http_py | evidence/05_tests.md | 657-664 |
| ev.05_tests_md.tests_unit_app_test_search_mapper_py | evidence/05_tests.md | 665-669 |
| ev.05_tests_md.tests_unit_app_test_search_service_py | evidence/05_tests.md | 670-681 |
| ev.05_tests_md.tests_unit_app_test_settings_sources_py | evidence/05_tests.md | 682-686 |
| ev.05_tests_md.tests_unit_app_test_synonym_expander_py | evidence/05_tests.md | 687-701 |
| ev.05_tests_md.tests_unit_app_test_vertex_vector_search_semantic_search_py | evidence/05_tests.md | 702-716 |
| ev.05_tests_md.tests_unit_arch_test_import_boundaries_py | evidence/05_tests.md | 717-720 |
| ev.05_tests_md.tests_unit_ml_common_test_gcs_py | evidence/05_tests.md | 721-729 |
| ev.05_tests_md.tests_unit_ml_common_test_gcs_io_py | evidence/05_tests.md | 730-735 |
| ev.05_tests_md.tests_unit_ml_common_test_logging_py | evidence/05_tests.md | 736-740 |
| ev.05_tests_md.tests_unit_ml_common_test_run_id_py | evidence/05_tests.md | 741-745 |
| ev.05_tests_md.tests_unit_ml_data_test_bigquery_ranker_repository_py | evidence/05_tests.md | 746-756 |
| ev.05_tests_md.tests_unit_ml_data_test_embedding_batch_py | evidence/05_tests.md | 757-769 |
| ev.05_tests_md.tests_unit_ml_data_test_feature_engineering_ranker_py | evidence/05_tests.md | 770-775 |
| ev.05_tests_md.tests_unit_ml_evaluation_test_label_gain_py | evidence/05_tests.md | 776-780 |
| ev.05_tests_md.tests_unit_ml_evaluation_test_ranking_metrics_py | evidence/05_tests.md | 781-791 |
| ev.05_tests_md.tests_unit_ml_test_encoder_server_py | evidence/05_tests.md | 792-798 |
| ev.05_tests_md.tests_unit_ml_test_lightgbm_trainer_adapter_py | evidence/05_tests.md | 799-802 |
| ev.05_tests_md.tests_unit_ml_training_test_cli_run_py | evidence/05_tests.md | 803-822 |
| ev.05_tests_md.tests_unit_ml_training_test_trainer_py | evidence/05_tests.md | 823-830 |
| ev.05_tests_md.tests_unit_ml_training_test_vertex_experiments_tracker_py | evidence/05_tests.md | 831-839 |
| ev.05_tests_md.tests_unit_pipeline_dags_test_dag_files_py | evidence/05_tests.md | 840-850 |
| ev.05_tests_md.tests_unit_pipeline_test_data_job_dag_wiring_py | evidence/05_tests.md | 851-859 |
| ev.05_tests_md.tests_unit_pipeline_test_ground_truth_jobs_py | evidence/05_tests.md | 860-868 |
| ev.05_tests_md.tests_unit_pipeline_test_kfp_orchestrator_py | evidence/05_tests.md | 869-875 |
| ev.05_tests_md.tests_unit_pipeline_test_pipeline_trigger_py | evidence/05_tests.md | 876-883 |
| ev.05_tests_md.tests_unit_pipeline_test_vector_search_writer_py | evidence/05_tests.md | 884-898 |
| ev.05_tests_md.tests_unit_scripts_test_adapters_py | evidence/05_tests.md | 899-909 |
| ev.05_tests_md.tests_unit_scripts_test_common_resolve_project_py | evidence/05_tests.md | 910-917 |
| ev.05_tests_md.tests_unit_scripts_test_composer_deploy_dags_py | evidence/05_tests.md | 918-931 |
| ev.05_tests_md.tests_unit_scripts_test_composer_task_states_py | evidence/05_tests.md | 932-936 |
| ev.05_tests_md.tests_unit_scripts_test_configmap_overlay_py | evidence/05_tests.md | 937-941 |
| ev.05_tests_md.tests_unit_scripts_test_deploy_all_step_timing_py | evidence/05_tests.md | 942-967 |
| ev.05_tests_md.tests_unit_scripts_test_destroy_check_py | evidence/05_tests.md | 968-974 |
| ev.05_tests_md.tests_unit_scripts_test_elasticsearch_wait_py | evidence/05_tests.md | 975-984 |
| ev.05_tests_md.tests_unit_scripts_test_infra_cleanup_py | evidence/05_tests.md | 985-1004 |
| ev.05_tests_md.tests_unit_scripts_test_infra_feature_view_sync_py | evidence/05_tests.md | 1005-1014 |
| ev.05_tests_md.tests_unit_scripts_test_infra_terraform_state_py | evidence/05_tests.md | 1015-1029 |
| ev.05_tests_md.tests_unit_scripts_test_kserve_models_deploy_py | evidence/05_tests.md | 1030-1045 |
| ev.05_tests_md.tests_unit_scripts_test_lib_config_py | evidence/05_tests.md | 1046-1055 |
| ev.05_tests_md.tests_unit_scripts_test_lib_gcp_resources_py | evidence/05_tests.md | 1056-1064 |
| ev.05_tests_md.tests_unit_scripts_test_local_hybrid_py | evidence/05_tests.md | 1065-1073 |
| ev.05_tests_md.tests_unit_scripts_test_monitor_py | evidence/05_tests.md | 1074-1085 |
| ev.05_tests_md.tests_unit_scripts_test_promote_py | evidence/05_tests.md | 1086-1106 |
| ev.05_tests_md.tests_unit_scripts_test_repo_relative_paths_py | evidence/05_tests.md | 1107-1110 |
| ev.05_tests_md.tests_unit_scripts_test_resolve_api_target_py | evidence/05_tests.md | 1111-1124 |
| ev.05_tests_md.tests_unit_scripts_test_run_all_orchestrator_py | evidence/05_tests.md | 1125-1134 |
| ev.05_tests_md.tests_unit_scripts_test_setup_policy_guard_py | evidence/05_tests.md | 1135-1144 |
| ev.05_tests_md.tests_unit_scripts_test_step_timing_py | evidence/05_tests.md | 1145-1155 |
| ev.05_tests_md.tests_unit_scripts_test_submit_train_pipeline_py | evidence/05_tests.md | 1156-1161 |
| ev.05_tests_md.tests_unit_scripts_test_subprocess_run_kwargs_guard_py | evidence/05_tests.md | 1162-1167 |
| ev.05_tests_md.tests_unit_scripts_test_sync_elasticsearch_exit_codes_py | evidence/05_tests.md | 1168-1172 |
| ev.05_tests_md.tests_unit_scripts_test_terraform_lock_py | evidence/05_tests.md | 1173-1180 |
| ev.05_tests_md.tests_unit_scripts_test_vertex_feature_store_wait_py | evidence/05_tests.md | 1181-1189 |
| ev.05_tests_md.tests_unit_scripts_test_vertex_ops_scripts_py | evidence/05_tests.md | 1190-1229 |
| ev.07_entrypoints_md | evidence/07_entrypoints.md | 1-94 |
| ev.08_config_env_md | evidence/08_config_env.md | 1-641 |
| ev.08_config_env_md.scan_limitations | evidence/08_config_env.md | 637-641 |
| ev.09_diff_evidence_md | evidence/09_diff_evidence.md | 1-42 |
| ev.09_diff_evidence_md.working_tree | evidence/09_diff_evidence.md | 5-10 |
| ev.09_diff_evidence_md.staged_files | evidence/09_diff_evidence.md | 11-16 |
| ev.09_diff_evidence_md.unstaged_files | evidence/09_diff_evidence.md | 17-22 |
| ev.09_diff_evidence_md.last_commit_files | evidence/09_diff_evidence.md | 23-28 |
| ev.09_diff_evidence_md.since_scope | evidence/09_diff_evidence.md | 29-42 |
| ev.10_observed_change_signals_md | evidence/10_observed_change_signals.md | 1-33 |
| ev.10_observed_change_signals_md.notes | evidence/10_observed_change_signals.md | 30-33 |
| ev.10_observed_change_signals_json | evidence/10_observed_change_signals.json | 1-3130 |
| ev.11_dependency_inventory_md | evidence/11_dependency_inventory.md | 1-1928 |
| ev.11_dependency_inventory_md.guardrail | evidence/11_dependency_inventory.md | 1926-1928 |
| ev.11_dependency_inventory_json | evidence/11_dependency_inventory.json | 1-1918 |
| ev.12_code_metrics_md | evidence/12_code_metrics.md | 1-594 |
| ev.12_code_metrics_md.guardrail | evidence/12_code_metrics.md | 592-594 |
| ev.12_code_metrics_json | evidence/12_code_metrics.json | 1-584 |
| ev.13_public_api_surface_md | evidence/13_public_api_surface.md | 1-951 |
| ev.13_public_api_surface_md.guardrail | evidence/13_public_api_surface.md | 949-951 |
| ev.13_public_api_surface_json | evidence/13_public_api_surface.json | 1-941 |
| ev.14_code_excerpts_md | evidence/14_code_excerpts.md | 1-345 |
| ev.14_code_excerpts_md.github_workflows_ci_yml_35_41__dataform_check | evidence/14_code_excerpts.md | 7-20 |
| ev.14_code_excerpts_md.github_workflows_ci_yml_11_17__lint_typecheck_test | evidence/14_code_excerpts.md | 21-34 |
| ev.14_code_excerpts_md.github_workflows_ci_yml_15_21__matrix | evidence/14_code_excerpts.md | 35-48 |
| ev.14_code_excerpts_md.github_workflows_ci_yml_1_7__pull_request | evidence/14_code_excerpts.md | 49-62 |
| ev.14_code_excerpts_md.github_workflows_ci_yml_3_9__push | evidence/14_code_excerpts.md | 63-76 |
| ev.14_code_excerpts_md.github_workflows_ci_yml_13_19__strategy | evidence/14_code_excerpts.md | 77-90 |
| ev.14_code_excerpts_md.github_workflows_ci_yml_5_11__workflow_dispatch | evidence/14_code_excerpts.md | 91-104 |
| ev.14_code_excerpts_md.github_workflows_deploy_api_yml_25_31__build_and_deploy | evidence/14_code_excerpts.md | 105-118 |
| ev.14_code_excerpts_md.github_workflows_deploy_api_yml_3_9__paths | evidence/14_code_excerpts.md | 119-132 |
| ev.14_code_excerpts_md.github_workflows_deploy_api_yml_1_7__push | evidence/14_code_excerpts.md | 133-146 |
| ev.14_code_excerpts_md.github_workflows_deploy_api_yml_11_17__workflow_dispatch | evidence/14_code_excerpts.md | 147-160 |
| ev.14_code_excerpts_md.github_workflows_deploy_dataform_yml_3_9__paths | evidence/14_code_excerpts.md | 161-174 |
| ev.14_code_excerpts_md.github_workflows_deploy_dataform_yml_1_7__push | evidence/14_code_excerpts.md | 175-188 |
| ev.14_code_excerpts_md.github_workflows_deploy_dataform_yml_19_25__push_definitions | evidence/14_code_excerpts.md | 189-202 |
| ev.14_code_excerpts_md.github_workflows_deploy_dataform_yml_7_13__workflow_dispatch | evidence/14_code_excerpts.md | 203-216 |
| ev.14_code_excerpts_md.github_workflows_deploy_encoder_image_yml_30_36__build_and_push | evidence/14_code_excerpts.md | 217-230 |
| ev.14_code_excerpts_md.github_workflows_deploy_encoder_image_yml_8_14__paths | evidence/14_code_excerpts.md | 231-244 |
| ev.14_code_excerpts_md.github_workflows_deploy_encoder_image_yml_6_12__push | evidence/14_code_excerpts.md | 245-258 |
| ev.14_code_excerpts_md.github_workflows_deploy_encoder_image_yml_17_23__workflow_dispatch | evidence/14_code_excerpts.md | 259-272 |
| ev.14_code_excerpts_md.github_workflows_deploy_pipeline_yml_36_42__compile_and_upload | evidence/14_code_excerpts.md | 273-286 |
| ev.14_code_excerpts_md.github_workflows_deploy_pipeline_yml_12_18__paths | evidence/14_code_excerpts.md | 287-300 |
| ev.14_code_excerpts_md.github_workflows_deploy_pipeline_yml_10_16__push | evidence/14_code_excerpts.md | 301-314 |
| ev.14_code_excerpts_md.github_workflows_deploy_pipeline_yml_24_30__workflow_dispatch | evidence/14_code_excerpts.md | 315-328 |
| ev.14_code_excerpts_md.github_workflows_deploy_reranker_image_yml_30_36__build_and_push | evidence/14_code_excerpts.md | 329-342 |
| ev.14_code_excerpts_md.guardrail | evidence/14_code_excerpts.md | 343-345 |
| ev.14_code_excerpts_json | evidence/14_code_excerpts.json | 1-26 |
| ev.15_decision_memory_md | evidence/15_decision_memory.md | 1-5 |
| ev.15_decision_memory_json | evidence/15_decision_memory.json | 1-3 |
| ev.domain_00_infra_resources_md | evidence/domain/00_infra_resources.md | 1-948 |
| ev.domain_00_infra_resources_md.resources | evidence/domain/00_infra_resources.md | 11-730 |
| ev.domain_00_infra_resources_md.secret_and_env_references | evidence/domain/00_infra_resources.md | 731-948 |
| ev.30_static_signal_hits_md | evidence/30_static_signal_hits.md | 1-22 |
| ev.30_static_signal_hits_md.guardrail | evidence/30_static_signal_hits.md | 20-22 |
| ev.98_redaction_report_md | evidence/98_redaction_report.md | 1-20 |
| ev.99_scan_limitations_md | evidence/99_scan_limitations.md | 1-18 |
| ev.99_scan_limitations_md.parser_limitations__infra_python_web | evidence/99_scan_limitations.md | 3-9 |
| ev.99_scan_limitations_md.search_limitations | evidence/99_scan_limitations.md | 10-14 |
| ev.99_scan_limitations_md.current_limits | evidence/99_scan_limitations.md | 15-18 |
| ev.grep_01_todos_md | evidence/grep/01_todos.md | 1-11 |
| ev.grep_02_job_lifecycle_md | evidence/grep/02_job_lifecycle.md | 1-1060 |
| ev.grep_03_env_secret_md | evidence/grep/03_env_secret.md | 1-618 |
| ev.grep_04_high_risk_ops_md | evidence/grep/04_high_risk_ops.md | 1-607 |
| ev.grep_05_auth_permission_md | evidence/grep/05_auth_permission.md | 1-764 |
| ev.grep_06_infra_surface_md | evidence/grep/06_infra_surface.md | 1-1625 |
| ev.grep_99_no_hits_md | evidence/grep/99_no_hits.md | 1-2 |
| ev.grep_00_queries_json | evidence/grep/00_queries.json | 1-8 |

## Evidence Inputs

### evidence/00_scan_manifest.md

```markdown
# Scan Manifest

schema_version: 1
tool_version: 0.1.0
scan_id: 20260705T052739Z_d14a7f69c9eb
generated_at: 2026-07-05T05:27:39Z
tool: decision-catalog (dcm)
language: infra+python+web
root: /home/ubuntu/repos/study-gcp-search-mlops-gke
git_commit: 6e2858f83aa27d9e18e3080f3c5f981bcf938ce7
git_branch: master
git_dirty: false
freshness_status: fresh

query_config_hash: e9dac3c3870d09c48c44a7f09c409e5a055fb41f762463fbe198c0ee6c5769aa
ignore_rules_hash: e8f0b03b63182f211b568f1e240f120892ed77d888a5fbac0075c20478e975a4
source_tree_hash: 0927d3a94d3b35076aa8cf26bcac487a085e8a01ff2c971e04b8a89c46b1f5c6
output_schema_version: 1

profile_resolution:
mode: auto
resolver: deterministic
llm_router_used: false
llm_router_is_evidence: false
candidates: infra,python,web
profiles_run: infra+python+web

requested_profiles: auto
detected_profiles: css,html,infra,node,python,typescript
coverage_warnings: unsupported extensions detected: csv,mdc,sh,sql,sqlx,toml,zip

included_file_count: 692
symbol_count: 3188
test_count: 888
entrypoint_count: 92

extractor:
  rust: syn AST exact v1 (line fallback only on parse failure)
  python: indent-heuristic v2 (public-by-convention/import/dependency inventory)
  typescript: line-heuristic v2 (export/import/dependency inventory)
  metrics: deterministic loc/symbol counts v1
  grep: substring v1

notes:
  - symbol 抽出は heuristic。macro / 動的生成は取りこぼす（99_scan_limitations.md 参照）。
  - grep no-hit は不存在の証明ではない。
```

### evidence/03_symbols.md

```markdown
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


[truncated for context pack]
```

### evidence/08_config_env.md

```markdown
# Config / Env Inventory

- 
  found_in:
    - infra/terraform/environments/dev/outputs.tf:L230
    - infra/terraform/modules/data/main.tf:L709
    - infra/terraform/modules/redis_synonym/outputs.tf:L18
    - pipeline/dags/_common.py:L22
    - pipeline/workflow/trigger.py:L20
    - pipeline/workflow/trigger.py:L27
    - pipeline/workflow/trigger_zip/main.py:L20
    - pipeline/workflow/trigger_zip/main.py:L27
    - scripts/_common.py:L147
    - scripts/domain/gcp/state_recovery.py:L691
    - scripts/domain/terraform/lock.py:L41
    - scripts/ops/composer_dag.py:L25
    - scripts/ops/promote.py:L253
    - scripts/ops/promote.py:L259
  value: redacted (name/参照のみ)
  requiredness: unknown
- <unset>
  found_in:
    - scripts/ops/check_retrain.py:L24
  value: redacted (name/参照のみ)
  requiredness: unknown
- ACTION
  found_in:
    - scripts/ops/feedback.py:L15
  value: redacted (name/参照のみ)
  requiredness: unknown
- AIP_EXPLAIN_ROUTE
  found_in:
    - ml/serving/reranker.py:L130
  value: redacted (name/参照のみ)
  requiredness: unknown
- AIP_HEALTH_ROUTE
  found_in:
    - ml/serving/encoder.py:L159
    - ml/serving/reranker.py:L109
  value: redacted (name/参照のみ)
  requiredness: unknown
- AIP_HTTP_PORT
  found_in:
    - ml/serving/encoder.py:L183
    - ml/serving/reranker.py:L149
  value: redacted (name/参照のみ)
  requiredness: unknown
- AIP_PREDICT_ROUTE
  found_in:
    - ml/serving/encoder.py:L164
    - ml/serving/reranker.py:L114
  value: redacted (name/参照のみ)
  requiredness: unknown
- AIP_STORAGE_URI
  found_in:
    - ml/serving/encoder.py:L129
    - ml/serving/reranker.py:L66
  value: redacted (name/参照のみ)
  requiredness: unknown
- API_HOST_HEADER
  found_in:
    - scripts/_common.py:L393
    - scripts/_common.py:L408
    - scripts/_common.py:L415
  value: redacted (name/参照のみ)
  requiredness: unknown
- API_URL
  found_in:
    - scripts/_common.py:L386
  value: redacted (name/参照のみ)
  requiredness: unknown
- ARTIFACT_REPO_ID
  found_in:
    - pipeline/dags/_pod.py:L67
  value: redacted (name/参照のみ)
  requiredness: unknown
- BQ_PROPERTIES_TABLE
  found_in:
    - scripts/ops/sync_elasticsearch.py:L111
  value: redacted (name/参照のみ)
  requiredness: unknown
- CLOUD_RUN_JOB
  found_in:
    - ml/common/logging/structured_logging.py:L52
  value: redacted (name/参照のみ)
  requiredness: unknown
- CLOUD_RUN_SERVICE_ACCOUNT
  found_in:
    - app/services/adapters/internal/pubsub_diagnostics.py:L29
  value: redacted (name/参照のみ)
  requiredness: unknown
- COMPOSER_RUNNER_IMAGE
  found_in:
    - pipeline/dags/_pod.py:L61
  value: redacted (name/参照のみ)
  requiredness: unknown
- DAG
  found_in:
    - scripts/ops/composer_dag.py:L56
    - scripts/ops/composer_task_states.py:L140
  value: redacted (name/参照のみ)
  requiredness: unknown
- ELASTICSEARCH_API_KEY
  found_in:
    - scripts/ops/sync_elasticsearch.py:L115
  value: redacted (name/参照のみ)
  requiredness: unknown
- ELASTICSEARCH_INDEX
  found_in:
    - scripts/ops/sync_elasticsearch.py:L114
  value: redacted (name/参照のみ)
  requiredness: unknown
- ELASTICSEARCH_PASSWORD
  found_in:
    - scripts/ops/sync_elasticsearch.py:L117
  value: redacted (name/参照のみ)
  requiredness: unknown
- ELASTICSEARCH_URL
  found_in:
    - scripts/ops/sync_elasticsearch.py:L113

[truncated for context pack]
```

### evidence/30_static_signal_hits.md

```markdown
# Static Signal Hits

This is a machine-generated signal inventory, not a decision.
Every row points back to grep evidence.

| query_id | hit_state | hits | evidence_ref | follow_up |
|---|---|---:|---|---|
| `todos` | `matched` | 6 | `file=evidence/grep/01_todos.md query_id=todos` | review matching lines before deciding |
| `job_lifecycle` | `matched` | 1055 | `file=evidence/grep/02_job_lifecycle.md query_id=job_lifecycle` | review matching lines before deciding |
| `env_secret` | `matched` | 613 | `file= <REDACTED>
| `high_risk_ops` | `matched` | 602 | `file=evidence/grep/04_high_risk_ops.md query_id=high_risk_ops` | review matching lines before deciding |
| `auth_permission` | `matched` | 759 | `file=evidence/grep/05_auth_permission.md query_id=auth_permission` | review matching lines before deciding |
| `infra_surface` | `matched` | 1620 | `file=evidence/grep/06_infra_surface.md query_id=infra_surface` | review matching lines before deciding |
| `change_signal:docs/tasks/TASKS_ROADMAP.md` | `observed` | 36 | `file=evidence/10_observed_change_signals.md path=docs/tasks/TASKS_ROADMAP.md` | inspect change history before editing |
| `change_signal:"docs/architecture/03_\345\256\237\350\243\205\343\202\253\343\202\277\343\203\255\343\202\260.md"` | `observed` | 29 | `file=evidence/10_observed_change_signals.md path="docs/architecture/03_\345\256\237\350\243\205\343\202\253\343\202\277\343\203\255\343\202\260.md"` | inspect change history before editing |
| `change_signal:docs/tasks/TASKS.md` | `observed` | 25 | `file=evidence/10_observed_change_signals.md path=docs/tasks/TASKS.md` | inspect change history before editing |
| `change_signal:"docs/architecture/01_\344\273\225\346\247\230\343\201\250\350\250\255\350\250\210.md"` | `observed` | 20 | `file=evidence/10_observed_change_signals.md path="docs/architecture/01_\344\273\225\346\247\230\343\201\250\350\250\255\350\250\210.md"` | inspect change history before editing |
| `change_signal:CLAUDE.md` | `observed` | 19 | `file=evidence/10_observed_change_signals.md path=CLAUDE.md` | inspect change history before editing |

## Guardrail

- Static signal entries are observations only. Decision Catalog claims still need explicit `evidence_ref` values.
```

### evidence/99_scan_limitations.md

```markdown
# Scan Limitations

## Parser Limitations (infra+python+web)

- シンボル抽出は行ベース heuristic であり AST ではない。
- Rust: macro / proc-macro 生成、複数行シグネチャ、conditional compilation は取りこぼす。
- Python: 動的生成 class/function、デコレータ経由の登録、import hook は静的には見えない。
- impl 内メソッドと自由関数の区別（Rust）は近似。

## Search Limitations

- grep は指定 query 語彙に依存する。no-hit は不存在の証明ではない。
- 同義語・ドメイン固有命名は取りこぼす可能性がある。

## Current Limits

- 検出したシンボルの責務は未判定（investigate / Decision Catalog で扱う）。
- env の required/optional、secret の取り扱いは未確認。
```

### evidence/evidence_index.jsonl

```markdown
{"evidence_id":"ev.00_scan_manifest_md","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"00_scan_manifest.md","line_start":1,"line_end":46,"sha256":"10de7754368cc1b2975b70ea2f5422131181b6ae499c1173977c8b92aac1756f"}
{"evidence_id":"ev.00_evidence_freshness_md","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"00_evidence_freshness.md","line_start":1,"line_end":12,"sha256":"d3683ebc6bcc17a8dceb16688c407233847693d3f3b0e77ec43818d943204bc7"}
{"evidence_id":"ev.01_file_tree_md","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"01_file_tree.md","line_start":1,"line_end":694,"sha256":"ef7e5ae605c5adf038e0b01ea66d739b061e029eb84b64064fef6ee3419b6e75"}
{"evidence_id":"ev.02_files_json","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"02_files.json","line_start":1,"line_end":694,"sha256":"a8af7a672428bc05e239537b062c94f6c557fe2289c966781958720fcfc5bae7"}
{"evidence_id":"ev.03_symbols_md","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":1,"line_end":4405,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.github_workflows_ci_yml","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":3,"line_end":12,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.github_workflows_deploy_api_yml","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":13,"line_end":19,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.github_workflows_deploy_dataform_yml","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":20,"line_end":26,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.github_workflows_deploy_encoder_image_yml","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":27,"line_end":33,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.github_workflows_deploy_pipeline_yml","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":34,"line_end":40,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.github_workflows_deploy_reranker_image_yml","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":41,"line_end":47,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.github_workflows_deploy_trainer_image_yml","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":48,"line_end":54,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.github_workflows_terraform_yml","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":55,"line_end":62,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.app_api_dependencies_py","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":63,"line_end":69,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.app_api_mappers_search_mapper_py","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":70,"line_end":76,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.app_api_middleware_request_logging_py","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":77,"line_end":83,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.app_api_routers_admin_mlops_router_py","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":84,"line_end":90,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.app_api_routers_feedback_router_py","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":91,"line_end":94,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.app_api_routers_health_router_py","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":95,"line_end":99,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.app_api_routers_model_router_py","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":100,"line_end":105,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.app_api_routers_ops_router_py","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":106,"line_end":114,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.app_api_routers_retrain_router_py","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":115,"line_end":118,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.app_api_routers_search_router_py","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":119,"line_end":122,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.app_api_routers_ui_router_py","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":123,"line_end":133,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.app_composition_root_py","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":134,"line_end":149,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.app_container_infra_py","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":150,"line_end":166,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.app_container_internal_optional_adapter_py","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":167,"line_end":170,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.app_container_ml_py","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":171,"line_end":183,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.app_container_search_py","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":184,"line_end":201,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.app_domain_candidate_py","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":202,"line_end":206,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.app_domain_event_py","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":207,"line_end":212,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.app_domain_labeling_py","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":213,"line_end":216,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.app_domain_retrieval_py","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":217,"line_end":221,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.app_domain_search_py","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":222,"line_end":228,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.app_domain_training_py","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":229,"line_end":233,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.app_main_py","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":234,"line_end":241,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.app_observability_py","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":242,"line_end":251,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.app_schemas_admin_mlops_py","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":252,"line_end":258,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.app_schemas_model_py","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":259,"line_end":267,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.app_schemas_ops_py","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":268,"line_end":276,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.app_schemas_search_py","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":277,"line_end":285,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.app_services_adapters_bigquery_candidate_retriever_py","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":286,"line_end":292,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.app_services_adapters_bigquery_data_catalog_reader_py","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":293,"line_end":309,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.app_services_adapters_bigquery_event_repository_py","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":310,"line_end":324,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.app_services_adapters_bigquery_label_repository_py","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":325,"line_end":331,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.app_services_adapters_bigquery_metrics_repository_py","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":332,"line_end":339,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.app_services_adapters_bqml_popularity_scorer_py","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":340,"line_end":345,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.app_services_adapters_cloud_logging_event_writer_py","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":346,"line_end":354,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.app_services_adapters_elasticsearch_lexical_py","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":355,"line_end":362,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.app_services_adapters_feature_online_store_fetcher_py","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":363,"line_end":375,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.app_services_adapters_gcs_training_dataset_repository_py","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":376,"line_end":385,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.app_services_adapters_internal_kserve_common_py","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":386,"line_end":394,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.app_services_adapters_internal_pubsub_diagnostics_py","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":395,"line_end":400,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.app_services_adapters_kserve_encoder_py","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":401,"line_end":407,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.app_services_adapters_kserve_reranker_py","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":408,"line_end":416,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.app_services_adapters_publisher_py","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":417,"line_end":422,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.app_services_adapters_pubsub_event_writer_py","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":423,"line_end":432,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.app_services_adapters_pubsub_feedback_recorder_py","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":433,"line_end":438,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.app_services_adapters_pubsub_ranking_log_publisher_py","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":439,"line_end":444,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.app_services_adapters_redis_synonym_expander_py","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":445,"line_end":452,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.app_services_adapters_retrain_py","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":453,"line_end":461,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.app_services_adapters_vertex_vector_search_semantic_search_py","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":462,"line_end":468,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.app_services_data_catalog_service_py","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":469,"line_end":474,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.app_services_feedback_service_py","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":475,"line_end":480,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.app_services_model_metrics_service_py","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":481,"line_end":497,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.app_services_noop_adapters_noop_data_catalog_reader_py","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":498,"line_end":502,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.app_services_noop_adapters_noop_event_repository_py","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":503,"line_end":509,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.app_services_noop_adapters_noop_event_writer_py","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":510,"line_end":516,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.app_services_noop_adapters_noop_feedback_recorder_py","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":517,"line_end":521,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.app_services_noop_adapters_noop_label_repository_py","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":522,"line_end":527,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.app_services_noop_adapters_noop_lexical_search_py","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":528,"line_end":532,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.app_services_noop_adapters_noop_metrics_repository_py","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":533,"line_end":539,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.app_services_noop_adapters_noop_ranking_log_publisher_py","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":540,"line_end":544,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.app_services_noop_adapters_noop_retrain_queries_py","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":545,"line_end":551,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.app_services_noop_adapters_noop_synonym_expander_py","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":552,"line_end":556,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.app_services_noop_adapters_noop_training_dataset_repository_py","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":557,"line_end":563,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.app_services_protocols_candidate_retriever_py","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":564,"line_end":568,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.app_services_protocols_data_catalog_reader_py","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":569,"line_end":575,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.app_services_protocols_encoder_client_py","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":576,"line_end":580,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.app_services_protocols_event_repository_py","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":581,"line_end":587,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.app_services_protocols_event_writer_py","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":588,"line_end":594,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.app_services_protocols_feature_fetcher_py","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":595,"line_end":600,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.app_services_protocols_feedback_recorder_py","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":601,"line_end":605,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.app_services_protocols_label_repository_py","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":606,"line_end":611,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.app_services_protocols_lexical_search_py","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":612,"line_end":616,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.app_services_protocols_metrics_repository_py","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":617,"line_end":623,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.app_services_protocols_popularity_scorer_py","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":624,"line_end":628,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.app_services_protocols_publisher_py","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":629,"line_end":635,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.app_services_protocols_ranking_log_publisher_py","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":636,"line_end":640,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.app_services_protocols_reranker_client_py","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":641,"line_end":647,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.app_services_protocols_retrain_queries_py","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":648,"line_end":654,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.app_services_protocols_semantic_search_py","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":655,"line_end":659,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.app_services_protocols_synonym_expander_py","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":660,"line_end":664,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.app_services_protocols_training_dataset_repository_py","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":665,"line_end":671,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.app_services_ranking_py","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":672,"line_end":681,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.app_services_retrain_policy_py","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":682,"line_end":687,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.app_services_search_service_py","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":688,"line_end":700,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.app_settings_api_py","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":701,"line_end":714,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.app_static_css_custom_css","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":715,"line_end":839,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.app_static_css_pico_admin_components_css","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":840,"line_end":1013,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.app_static_css_pico_admin_layout_css","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":1014,"line_end":1083,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.app_static_css_pico_admin_theme_css","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":1084,"line_end":1134,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.app_static_js_search_ui_js","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":1135,"line_end":1149,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.app_templates__feedback_panel_html","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":1150,"line_end":1165,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.app_templates__search_form_html","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":1166,"line_end":1192,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.app_templates__search_results_html","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":1193,"line_end":1224,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.app_templates_base_html","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":1225,"line_end":1255,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.app_templates_data_html","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":1256,"line_end":1276,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.app_templates_index_html","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":1277,"line_end":1281,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.app_templates_model_metrics_html","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":1282,"line_end":1311,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.app_templates_ops_html","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":1312,"line_end":1358,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.app_templates_property_detail_html","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":1359,"line_end":1378,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.app_templates_search_dev_html","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":1379,"line_end":1395,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.infra_run_services_composer_runner_dockerfile","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":1396,"line_end":1400,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.infra_run_services_encoder_dockerfile","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":1401,"line_end":1405,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.infra_run_services_ml_base_dockerfile","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":1406,"line_end":1409,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.infra_run_services_reranker_dockerfile","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":1410,"line_end":1414,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.infra_run_services_search_api_dockerfile","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":1415,"line_end":1419,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.infra_terraform_environments_dev_apis_tf","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":1420,"line_end":1423,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}
{"evidence_id":"ev.03_symbols_md.infra_terraform_modules_composer_main_tf","scan_id":"20260705T052739Z_d14a7f69c9eb","target_git_commit":"6e2858f83aa27d9e18e3080f3c5f981bcf938ce7","artifact":"03_symbols.md","line_start":1424,"line_end":1427,"sha256":"26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba"}

[truncated for context pack]
```

### evidence/01_file_tree.md

```markdown
# File Tree

- .claude/agents/derivation-by-subtraction-reviewer.agent.md
- .claude/agents/feature-parity-checker.agent.md
- .claude/agents/port-adapter-boundary-reviewer.agent.md
- .claude/commands/check-parity.md
- .claude/hooks/check-layers.sh
- .claude/hooks/show-tasks.sh
- .claude/scheduled_tasks.lock
- .claude/settings.json
- .claude/settings.local.json
- .claude/skills/doc-sync/SKILL.md
- .claude/skills/port-adapter-scaffolder/SKILL.md
- .codex/README.md
- .codex/playbooks.md
- .cursor/commands/check-parity.md
- .cursor/rules/agent-no-time-waste.mdc
- .cursor/rules/python-fastapi-ml.mdc
- .cursor/rules/study-gcp-mlops-core.mdc
- .cursor/rules/terraform-gcp-mlops.mdc
- .dockerignore
- .gcloudignore
- .github/actions/build-and-push/action.yml
- .github/actions/setup-gcp/action.yml
- .github/actions/setup-python-env/action.yml
- .github/agents/gcp-mlops-theme-research.agent.md
- .github/skills/doc-sync/SKILL.md
- .github/workflows/README.md
- .github/workflows/ci.yml
- .github/workflows/deploy-api.yml
- .github/workflows/deploy-dataform.yml
- .github/workflows/deploy-encoder-image.yml
- .github/workflows/deploy-pipeline.yml
- .github/workflows/deploy-reranker-image.yml
- .github/workflows/deploy-trainer-image.yml
- .github/workflows/terraform.yml
- .gitignore
- .python-version
- AGENTS.md
- CLAUDE.md
- Makefile
- README.md
- app/__init__.py
- app/api/__init__.py
- app/api/dependencies.py
- app/api/mappers/__init__.py
- app/api/mappers/search_mapper.py
- app/api/middleware/__init__.py
- app/api/middleware/request_logging.py
- app/api/routers/__init__.py
- app/api/routers/admin_mlops_router.py
- app/api/routers/feedback_router.py
- app/api/routers/health_router.py
- app/api/routers/model_router.py
- app/api/routers/ops_router.py
- app/api/routers/retrain_router.py
- app/api/routers/search_router.py
- app/api/routers/ui_router.py
- app/composition_root.py
- app/container/__init__.py
- app/container/infra.py
- app/container/internal/__init__.py
- app/container/internal/optional_adapter.py
- app/container/ml.py
- app/container/search.py
- app/data/accuracy_eval_cases.json
- app/domain/__init__.py
- app/domain/candidate.py
- app/domain/event.py
- app/domain/labeling.py
- app/domain/retrieval.py
- app/domain/search.py
- app/domain/training.py
- app/main.py
- app/observability.py
- app/schemas/__init__.py
- app/schemas/admin_mlops.py
- app/schemas/model.py
- app/schemas/ops.py
- app/schemas/search.py
- app/services/__init__.py
- app/services/adapters/__init__.py
- app/services/adapters/bigquery_candidate_retriever.py
- app/services/adapters/bigquery_data_catalog_reader.py
- app/services/adapters/bigquery_event_repository.py
- app/services/adapters/bigquery_label_repository.py
- app/services/adapters/bigquery_metrics_repository.py
- app/services/adapters/bqml_popularity_scorer.py
- app/services/adapters/cloud_logging_event_writer.py
- app/services/adapters/elasticsearch_lexical.py
- app/services/adapters/feature_online_store_fetcher.py
- app/services/adapters/gcs_training_dataset_repository.py
- app/services/adapters/internal/__init__.py
- app/services/adapters/internal/kserve_common.py
- app/services/adapters/internal/pubsub_diagnostics.py
- app/services/adapters/kserve_encoder.py
- app/services/adapters/kserve_reranker.py
- app/services/adapters/publisher.py
- app/services/adapters/pubsub_event_writer.py
- app/services/adapters/pubsub_feedback_recorder.py
- app/services/adapters/pubsub_ranking_log_publisher.py
- app/services/adapters/redis_synonym_expander.py
- app/services/adapters/retrain.py
- app/services/adapters/vertex_vector_search_semantic_search.py
- app/services/data_catalog_service.py
- app/services/feedback_service.py
- app/services/model_metrics_service.py
- app/services/noop_adapters/__init__.py
- app/services/noop_adapters/noop_data_catalog_reader.py
- app/services/noop_adapters/noop_event_repository.py
- app/services/noop_adapters/noop_event_writer.py
- app/services/noop_adapters/noop_feedback_recorder.py
- app/services/noop_adapters/noop_label_repository.py
- app/services/noop_adapters/noop_lexical_search.py
- app/services/noop_adapters/noop_metrics_repository.py
- app/services/noop_adapters/noop_ranking_log_publisher.py
- app/services/noop_adapters/noop_retrain_queries.py
- app/services/noop_adapters/noop_synonym_expander.py
- app/services/noop_adapters/noop_training_dataset_repository.py
- app/services/protocols/__init__.py

[truncated for context pack]
```

### evidence/98_redaction_report.md

```markdown
# Redaction Report

status: passed
redacted_count: 371

checked_keywords:
  - secret
  - token
  - password
  - api_key
  - apikey
  - key

scope:
  - env_secret grep の代入形 (`KEY = ...` / `KEY: <REDACTED>

notes:
  - name / 参照箇所は残し、value のみ `<redacted>` に置換している。
  - これは網羅的な secret スキャンではない（高エントロピー文字列検出は対象外）。
  - env 参照の呼び出し（env::var / os.environ）は value を持たないため redaction 対象外。
```

## Investigated Findings

```markdown
# Investigated Findings

generated_by: dcm investigate
source: non_llm_evidence_investigation
judgment_status: llm_enriched

## observed_signals

- Evidence Pack exists and has the required scan, symbol, config, risk, and scan-limitation files. evidence_ref: file=evidence/00_scan_manifest.md
- Symbol evidence exists for code navigation and candidate responsibility boundaries. evidence_ref: file=evidence/03_symbols.md
- Configuration and environment evidence exists for secret and runtime-risk review. evidence_ref: file=evidence/08_config_env.md
- Static signal evidence exists and must be investigated before draft. evidence_ref: file=evidence/30_static_signal_hits.md
- Scan limitation evidence exists and can inform descriptive current implications when judgment-relevant. evidence_ref: file=evidence/99_scan_limitations.md

## available_evidence_files

- `00_evidence_freshness.md`
- `00_scan_manifest.md`
- `01_file_tree.md`
- `02_files.json`
- `03_symbols.md`
- `04_symbols.json`
- `05_tests.md`
- `07_entrypoints.md`
- `08_config_env.md`
- `09_diff_evidence.md`
- `10_observed_change_signals.json`
- `10_observed_change_signals.md`
- `11_dependency_inventory.json`
- `11_dependency_inventory.md`
- `12_code_metrics.json`
- `12_code_metrics.md`
- `13_public_api_surface.json`
- `13_public_api_surface.md`
- `14_code_excerpts.json`
- `14_code_excerpts.md`
- `15_decision_memory.json`
- `15_decision_memory.md`
- `30_static_signal_hits.md`
- `98_redaction_report.md`
- `99_scan_limitations.md`

## llm_enrichment

## item_meaning_candidates

- **Config env variables** – The inventory of environment variables (e.g., `AIP_STORAGE_URI`, `ENCODER_MODEL_NAME`, `ELASTICSEARCH_URL`, `REDIS_AUTH`) indicates the system is heavily parameterised at runtime, with per-service overrides for ML model serving (KServe), lexical search (Elasticsearch), synonym expansion (Redis), and GCP project/region identity.  
  *Evidence_ref*: `evidence/08_config_env.md`

- **Static signal hits** – High counts for `env_secret` (613), `high_risk_ops` (602), `auth_permission` (759), and `infra_surface` (1620) suggest the codebase contains a significant surface area of privileged operations, secret management, and infrastructure manipulation. These signals are observations only, not decisions.  
  *Evidence_ref*: `evidence/30_static_signal_hits.md`

- **Change signals** – Frequent changes to `docs/tasks/TASKS_ROADMAP.md`, `docs/architecture/03_実装カタログ.md`, and `CLAUDE.md` imply ongoing architectural documentation and roadmap evolution, likely reflecting active development.  
  *Evidence_ref*: `evidence/30_static_signal_hits.md` (change_signal rows, `evidence/10_observed_change_signals.md` not fully provided but referenced)

- **Symbol structure** – The large symbol set (3188 symbols, 888 tests) across Python, TypeScript, CSS, HTML, Terraform, Docker, and shell scripts indicates a polyglot project with deep test coverage. The presence of both `noop_adapters` and real adapters (e.g., PubSub, BigQuery, KServe) suggests a clean architecture pattern with testable interfaces.  
  *Evidence_ref*: `evidence/00_scan_manifest.md`, `evidence/03_symbols.md`

- **Domain objects** – Classes like `RankedCandidate`, `SearchEvent`, `TrainingDatasetRef`, `EvaluationMetric` define core data flow entities, while `ContainerBuilder` and `InfraBuilder` show dependency injection patterns for GCP services.  
  *Evidence_ref*: `evidence/03_symbols.md`

## role_notes

- **`app/` – API and search orchestration**  
  FastAPI routers, middleware, service layer, and adapters implement the search API, feedback, ops endpoints, and model management. The `container/` directory manages dependency injection for GCP clients (BigQuery, PubSub, Vertex AI).  
  *Evidence_ref*: `evidence/03_symbols.md` (e.g., `app/api/routers/`, `app/container/`, `app/services/adapters/`)

- **`ml/` – ML model serving and training**  
  Encoder and reranker KServe inference services (E5, LightGBM), training pipelines, experiment tracking, and registry management. Includes `streaming/` for Dataflow-based click-stream processing.  
  *Evidence_ref*: `evidence/03_symbols.md` (e.g., `ml/serving/`, `ml/training/`, `ml/streaming/`)

- **`pipeline/` – Orchestrated ML pipelines**  
  Composer DAGs, KFP pipeline compilation, batch serving and evaluation jobs, labeling, and training. Uses modular components (`training_job/`, `data_job/`, etc.).  
  *Evidence_ref*: `evidence/03_symbols.md` (e.g., `pipeline/dags/`, `pipeline/training_job/`)

- **`scripts/` – Deployment, ops, and infrastructure management**  
  Shell-like Python scripts for terraform apply, GCP resource recovery, ES sync, model promotion, and full lifecycle (deploy_all, destroy_all).  
  *Evidence_ref*: `evidence/03_symbols.md` (e.g., `scripts/deploy/`, `scripts/ops/`, `scripts/setup/`)

- **`infra/terraform/` – Infrastructure as Code**  
  Terraform modules for GKE, Cloud Composer, Vertex AI, BigQuery, PubSub, IAM, DNS, monitoring/SLOs, and Redis synonym store.  
  *Evidence_ref*: `evidence/03_symbols.md` (e.g., `infra/terraform/modules/*/main.tf`)

- **`tests/` – Multi-layer test suite**  
  Unit tests (`tests/unit/`), integration tests (`tests/integration/`), e2e acceptance tests (`tests/e2e/`), and in-memory fakes/stubs for controller-style testing.  
  *Evidence_ref*: `evidence/00_scan_manifest.md` (test_count: 888), `evidence/03_symbols.md` (tests/ section)

## current_implications

- **Active development documented in change signals** – The roadmap and architectural docs have recent modifications, implying the system is still evolving. Changes to `TASKS_ROADMAP.md` and architecture catalogs suggest ongoing refactoring or feature work.  
  *Evidence_ref*: `evidence/30_static_signal_hits.md` (change_signal:docs/tasks/TASKS_ROADMAP.md, etc.)

- **High test coverage (888 tests) enables confident refactoring** – The project has unit, integration, and e2e tests covering API contract, infrastructure invariants, data pipeline wiring, and ML metrics. This reduces risk when modifying core logic.  
  *Evidence_ref*: `evidence/00_scan_manifest.md` (test_count: 888)

- **Production readiness indicated by SLOs, monitoring, and retrain policies** – Terraform modules for SLO alerts, logging metrics, BigQuery data transfers for skew/drift checks, and a retrain policy (thresholds based on feedback volume and NDCG) show operational maturity.  
  *Evidence_ref*: `evidence/03_symbols.md` (e.g., `infra/terraform/modules/slo/`, `infra/terraform/modules/monitoring/`), `app/services/retrain_policy.py`

- **Secret management is widespread** – The high `env_secret` hit count (613) and references to Secret Manager, Workload Identity, and external-secrets-operator indicate that secrets are a critical and carefully managed concern.  
  *Evidence_ref*: `evidence/30_static_signal_hits.md`, `evidence/08_config_env.md` (redacted secret references)

- **Infrastructure surface is broad** – 1620 infra_surface hits plus 602 high_risk_ops hits imply many automation scripts modify cloud resources (terraform, kubectl, gcloud). This raises operational risk and requires tight change control.  
  *Evidence_ref*: `evidence/30_static_signal_hits.md`

- **Dependency injection pattern for GCP clients** – The `ContainerBuilder` and `InfraBuilder` classes conditionally resolve adapters (e.g., fetcher, publisher, scorer) based on configuration, making the system locally testable while supporting cloud-only services.  
  *Evidence_ref*: `evidence/03_symbols.md` (e.g., `app/container/infra.py`, `app/container/search.py`)

## uncertainty_notes

- **Parser limitations for dynamic symbols** – Symbols extracted heuristically may miss macros, dynamic classes, or decorator-registered routes. Rust macro expansions, Python import hooks, and decorated functions are not fully captured.  
  *Evidence_ref*: `evidence/99_scan_limitations.md`

- **Grep dependence** – Static signal hits rely on substring matching; no-hit does not prove absence. Domain-specific naming or synonyms may cause false negatives.  
  *Evidence_ref*: `evidence/99_scan_limitations.md`

- **Environment variable requiredness unknown** – The config/env inventory does not differentiate required vs. optional variables, nor default values. Usage context from code may clarify but is not fully provided.  
  *Evidence_ref*: `evidence/08_config_env.md` (final line: "required/optional は未確認")

- **Secrets redacted** – Many environment variable values, secret IDs, and resource names are redacted. This prevents full assessment of dependency paths and access patterns.  
  *Evidence_ref*: `evidence/08_config_env.md` (all values are `redacted (name/参照のみ)`)

[truncated for context pack]
```
