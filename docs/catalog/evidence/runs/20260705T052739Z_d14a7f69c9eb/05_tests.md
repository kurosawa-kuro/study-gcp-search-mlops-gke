# Test Inventory

## app/static/js/search_ui.js

- L154: function `init`

## tests/conftest.py

- L161: function `test_x`

## tests/e2e/test_full_recreate_gate.py

- L37: function `_require_full_recreate`
- L45: function `_run`
- L60: function `test_full_recreate_acceptance_live`

## tests/e2e/test_live_acceptance_gate.py

- L33: function `_require_acceptance_env`
- L38: function `test_live_acceptance_on_existing_env`

## tests/integration/infra/test_destroy_all_table_parity.py

- L35: function `_resources_with_deletion_protection`
- L55: function `_destroy_all_targets`
- L61: function `_destroy_bq_table_names`
- L69: function `_destroy_gke_cluster_names`
- L77: function `test_every_protected_bq_table_is_in_destroy_all_targets`
- L92: function `test_destroy_all_bq_targets_do_not_reference_removed_tables`
- L106: function `test_protected_gke_cluster_is_in_destroy_all_targets`
- L123: function `test_protected_targets_baseline`

## tests/integration/infra/test_infra_ranker_tables.py

- L27: function `_read`
- L31: function `_extract_resource_block`
- L54: function `test_property_features_daily_declared`
- L61: function `test_property_embeddings_declared_with_repeated_float64`
- L72: function `test_search_logs_declared`
- L81: function `test_ranking_log_declared_with_dual_cluster`
- L93: function `test_feedback_events_declared`
- L99: function `test_search_events_declared`
- L105: function `test_search_impressions_declared`
- L111: function `test_user_actions_declared`
- L118: function `test_ranking_labels_declared`
- L127: function `test_training_runs_metrics_has_ranker_columns`
- L134: function `test_training_runs_hyperparams_has_lambdarank_fields`
- L142: function `test_legacy_predictions_log_removed`

## tests/integration/infra/test_makefile.py

- L8: function `test_makefile_declares_destroy_coast_down_target`

## tests/integration/infra/test_manifests_structure.py

- L28: function `_load`
- L40: function `test_kustomization_lists_every_yaml_under_manifests`
- L59: function `test_search_api_deployment_resource_limits_match_nonnegotiable`
- L79: function `test_search_api_deployment_exposes_kserve_env_vars`
- L120: function `test_search_api_secretstore_uses_gcpsm_provider`
- L128: function `test_search_api_external_secret_syncs_iap_client_secret`
- L143: function `test_search_api_deployment_probes_have_canonical_paths`
- L172: function `test_search_api_hpa_bounds_and_thresholds`
- L192: function `test_search_api_networkpolicy_allows_egress_to_kserve_inference`
- L218: function `test_kserve_inferenceservice_has_correct_shape`
- L233: function `test_kserve_reranker_uses_lightgbm_model_format`
- L243: function `test_kserve_networkpolicy_restricts_ingress_to_search_namespace`
- L264: function `test_search_api_iap_policy_targets_gateway_service_with_gcp_backend_policy`
- L286: function `test_configmap_example_covers_expected_keys`

## tests/integration/infra/test_public_domain_consistency.py

- L28: function `_read`
- L32: function `_setting_value`
- L46: function `test_setting_yaml_holds_canonical_domain_and_zone`
- L55: function `test_gateway_manifest_uses_setting_public_domain_and_certmap`
- L76: function `test_dns_module_has_static_ip_apex_a_and_cert_manager_chain`
- L97: function `test_dns_module_defaults_match_gateway_annotation`
- L107: function `test_dev_main_wires_dns_module_and_passes_public_domain_everywhere`
- L125: function `test_apis_tf_enables_cloud_dns`
- L131: function `test_variables_tf_declares_public_domain_and_zone_without_default`
- L140: function `test_canonical_tf_var_names_includes_public_domain_and_zone`
- L151: function `test_makefile_exports_public_domain_and_zone`
- L160: function `test_tf_plan_feeds_terraform_the_canonical_var_set`
- L180: function `test_tf_apply_stage1_targets_includes_module_dns`
- L190: function `test_build_all_local_is_single_line_script_call`

## tests/integration/infra/test_terraform_module_structure.py

- L27: function `_modules`
- L33: function `test_module_has_required_file`
- L41: function `test_every_variable_has_description`

## tests/integration/infra/test_workflows_structure.py

- L40: function `test_workflow_file_exists`
- L47: function `test_retired_workflows_are_absent`
- L68: function `test_deploy_workflows_request_oidc_token`
- L75: function `test_encoder_image_workflow_paths`
- L81: function `test_reranker_image_workflow_paths`
- L87: function `test_trainer_image_workflow_paths`
- L93: function `test_pipeline_workflow_paths`
- L102: function `test_api_workflow_keeps_broad_filter_and_rolls_out_via_kubectl`

## tests/integration/parity/test_api_route_prefixes.py

- L54: function `app_no_lifespan`
- L69: function `_build`
- L81: function `_all_paths`
- L91: function `_classify`
- L103: function `test_all_routes_belong_to_a_known_axis`
- L117: function `test_canonical_public_endpoints_exist`
- L124: function `test_canonical_ops_endpoints_exist`
- L139: function `test_legacy_paths_redirect_to_new_prefix`
- L158: function `test_probes_are_not_namespaced`
- L170: function `test_metrics_endpoint_at_root`
- L176: function `test_legacy_redirects_excluded_from_openapi_schema`
- L183: function `test_canonical_paths_appear_in_openapi_schema`
- L197: function `test_route_iap_policy_documents_prefix_axes`

## tests/integration/parity/test_codebase_invariants.py

- L44: function `_walk_files`
- L57: function `_find_substring_hits`
- L71: function `test_w2_8_legacy_tokens_absent_in_python_trees`
- L81: function `test_w2_8_legacy_tokens_absent_in_manifests_yaml`
- L91: function `test_lexical_es_canonical_no_meilisearch_in_app`
- L101: function `test_makefile_has_no_removed_sync_meili_target`
- L108: function `test_pyproject_has_no_sync_meili_console_script`
- L115: function `test_search_api_deployment_has_no_meili_env_refs`
- L121: function `test_es_networkpolicy_allows_eck_operator_namespace`
- L139: function `test_es_manifest_pins_http_and_anonymous_auth`

## tests/integration/parity/test_configmap_drift.py

- L37: function `test_committed_configmap_matches_generator_output`
- L46: function `test_configmap_keys_cover_every_deployment_reference`
- L80: function `test_generated_configmap_keeps_deployment_referenced_keys`

## tests/integration/parity/test_dataform_workflow_settings.py

- L21: function `test_generator_includes_every_required_dataform_key`
- L34: function `test_generator_values_match_setting_yaml`
- L52: function `test_setting_yaml_has_all_required_keys`

## tests/integration/parity/test_event_schema_parity.py

- L51: function `test_app_emit_keys_match_domain_action_type`
- L60: function `test_app_emit_keys_match_pydantic_feedback_request`
- L75: function `test_app_emit_keys_match_terraform_user_actions_description`
- L91: function `test_terraform_user_actions_description_excludes_synthetic`
- L110: function `_load_synthetic_yaml`
- L120: function `test_synthetic_yaml_action_types_match_policy`
- L128: function `test_synthetic_yaml_weights_match_policy`
- L138: function `test_synthetic_yaml_label_source_format`
- L154: function `test_action_weights_is_app_emit_union_synthetic_no_overlap`
- L168: function `test_canonical_weight_values_pinned`
- L191: function `test_evaluation_metrics_table_declared`
- L221: function `test_ranking_labels_description_documents_label_source_canonical`

## tests/integration/parity/test_feature_parity_feature_group.py

- L31: function `_extract_feature_group_block`
- L41: function `_extract_feature_group_names`
- L45: function `_extract_feature_group_value_types`
- L49: function `test_vertex_feature_group_order_matches_property_side_cols`
- L57: function `test_vertex_feature_group_uses_double_features`

## tests/integration/parity/test_feature_parity_ranking.py

- L37: function `_extract_ranking_log_fields`
- L50: function `test_feature_cols_ranker_has_ten_columns`
- L54: function `test_feature_cols_ranker_no_duplicates`
- L61: function `test_build_ranker_features_keys_match_schema_exactly`
- L82: function `test_infra_ranking_log_features_order_matches_schema`
- L90: function `test_infra_ranking_log_features_are_float64_nullable`
- L104: function `test_dataform_property_features_has_behavioral_cols`

## tests/integration/parity/test_feature_parity_sql_ranker.py

- L28: function `_extract_unpivot_feature_lists`
- L38: function `test_ranker_sql_file_exists`
- L42: function `test_ranker_sql_has_both_unpivots`
- L50: function `test_ranker_unpivot_matches_property_side_cols`
- L61: function `test_ranker_sql_reads_ranking_log_not_predictions_log`

## tests/integration/pipeline/test_pipeline_compile.py

- L10: function `test_build_embed_pipeline_spec_contains_expected_steps`
- L17: function `test_build_train_pipeline_spec_contains_expected_steps`
- L29: function `test_coerce_parameter_value_handles_primitives_and_json`
- L37: function `test_merge_parameter_values_overrides_defaults`

## tests/integration/workflow/test_composer_dags_contract.py

- L24: function `test_dag_files_have_valid_python_syntax`
- L35: function `test_dag_files_pin_canonical_schedule_and_dag_id`
- L50: function `test_dag_schedules_are_valid_5_field_cron`
- L67: function `test_dag_schedules_avoid_simultaneous_run`
- L89: function `test_dag_files_avoid_kfp_2_16_module_level_compile_import`
- L97: function `test_retrain_dag_is_canonical_retrain_trigger`
- L112: function `test_dag_files_call_only_existing_scripts`
- L134: function `test_layers_rules_isolate_pipeline_dags_from_app_imports`

## tests/integration/workflow/test_composer_gcloud_json_contract.py

- L18: function `test_extract_json_array_skips_executing_command_prologue`
- L32: function `test_extract_json_array_prefers_array_of_objects_over_inner_brackets`
- L40: function `test_extract_json_array_handles_empty_array`
- L46: function `test_latest_run_id_from_list_runs_finds_manual_run_id`
- L55: function `test_balanced_array_respects_string_literals_with_brackets`
- L65: function `test_extract_json_array_missing_array_raises`

## tests/integration/workflow/test_composer_module_contract.py

- L22: function `test_composer_module_exists_with_required_files`
- L29: function `test_composer_module_uses_gen3_image_with_enable_flag_gate`
- L47: function `test_composer_env_variables_avoid_reserved_names`
- L84: function `test_composer_image_version_is_known_supported_form`
- L94: function `test_composer_environment_uses_correct_region_var`
- L104: function `test_composer_environment_has_proper_create_destroy_timeouts`
- L111: function `test_composer_workloads_have_max_count_to_bound_cost`
- L126: function `test_composer_module_workloads_config_has_scheduler_web_worker`
- L132: function `test_composer_module_outputs_dag_bucket_and_airflow_uri`
- L142: function `test_composer_module_wired_into_dev_environment_with_correct_depends_on`
- L154: function `test_composer_module_passes_required_terraform_inputs`
- L176: function `test_dev_environment_has_composer_variables_and_outputs`
- L195: function `test_enable_composer_default_is_flipped_to_true`
- L206: function `test_iam_module_provisions_sa_composer_with_required_roles`
- L229: function `test_composer_sa_used_in_workload_identity_binding_chain`
- L242: function `test_composer_sa_email_consumed_by_module`
- L247: function `test_tf_apply_stage1_targets_includes_module_composer`
- L254: function `test_composer_deploy_dags_step_inserted_between_overlay_and_deploy_api`
- L270: function `test_deploy_all_step_runner_imports_composer_deploy_dags`
- L280: function `test_composer_deploy_dags_early_returns_when_disabled`
- L286: function `_fake_run`
- L294: function `test_composer_deploy_dags_uses_gsutil_m_for_parallel_upload`
- L299: function `test_composer_dag_bucket_terraform_output_consumed_by_deploy_script`
- L311: function `test_makefile_exposes_composer_deploy_dags_and_smoke_targets`
- L329: function `test_composer_runner_dockerfile_does_not_bake_setting_yaml`
- L343: function `test_make_composer_env_default_matches_terraform_default`
- L363: function `test_pyproject_does_not_pull_apache_airflow_into_runtime`

## tests/integration/workflow/test_deploy_all_contract.py

- L26: function `test_deploy_all_step_sequence_pins_one_shot_pdca_contract`
- L50: function `test_deploy_all_seed_test_runs_before_feature_view_sync`
- L68: function `test_deploy_all_overlay_configmap_runs_before_deploy_api`
- L77: function `test_configmap_overlay_injects_live_vertex_outputs`
- L84: function `_fake_generate`
- L126: function `test_configmap_overlay_fills_fos_endpoint_from_api_when_terraform_empty`
- L135: function `_fake_generate`
- L171: function `test_local_boot_contract_does_not_require_adc_when_search_disabled`
- L178: function `_forbidden`
- L198: function `test_run_all_core_pins_canonical_validation_path`
- L240: function `test_wait_for_deployed_index_absent_is_idempotent_on_resume`
- L259: function `test_deploy_all_waits_vertex_feature_store_and_retries_stage1_on_409`
- L271: function `test_run_all_core_steps_all_have_makefile_targets`

## tests/integration/workflow/test_destroy_all_contract.py

- L15: function `test_destroy_all_keeps_pdca_reproducibility_guards`
- L30: function `test_destroy_all_destroy_apply_symmetry`
- L56: function `test_destroy_all_undeploys_vertex_endpoint_models_before_destroy`
- L67: function `test_destroy_all_proactively_undeploys_stale_vvs_indexes`
- L85: function `test_destroy_all_flips_bq_deletion_protection_before_destroy`
- L105: function `test_destroy_all_force_destroys_blocking_gcs_buckets`
- L113: function `test_recover_wif_handles_soft_delete_undelete`
- L127: function `test_sync_elasticsearch_step_waits_for_es_health_first`
- L179: function `test_destroy_all_provides_step_slicing_symmetric_with_deploy_all`
- L228: function `test_tf_apply_invokes_recover_wif_as_pre_step`
- L255: function `test_destroy_all_persists_vvs_index_and_endpoint`
- L316: function `test_no_vertex_pipeline_job_schedule_resource_in_terraform`
- L340: function `test_runbook_documents_emergency_kill_switch_for_composer_gke_cloudrun`
- L368: function `test_runbook_documents_orphan_state_cleanup_after_emergency_delete`
- L394: function `test_deploy_all_invokes_state_recovery_before_tf_apply`
- L454: function `test_state_recovery_iam_sa_mapping_matches_terraform`
- L478: function `test_runbook_warns_against_bare_state_rm_without_state_recovery`
- L501: function `test_destroy_all_lessons_learned_documented_in_roadmap`

## tests/integration/workflow/test_docs_canonical_contract.py

- L20: function `test_canonical_docs_describe_workflow_contract_goals`
- L75: function `test_composer_canonical_doc_section_exists`
- L97: function `test_cost_estimate_documented_in_runbook`

## tests/integration/workflow/test_elasticsearch_workflow_contract.py

- L12: function `test_makefile_exposes_sync_elasticsearch_canonical_target`
- L20: function `test_run_all_core_keeps_sync_elasticsearch_before_search_smokes`
- L35: function `test_deploy_all_sync_elasticsearch_step_wiring_stays_canonical`
- L48: function `test_docs_runbook_and_catalog_pin_elasticsearch_workflow`

## tests/integration/workflow/test_ground_truth_contract.py

- L17: function `test_makefile_exposes_ground_truth_targets`
- L44: function `test_kserve_dockerfiles_use_split_ml_extras`
- L57: function `test_training_pipeline_contract_uses_ranking_labels_not_feedback_events`
- L78: function `test_dataform_and_app_contract_use_canonical_event_schema`

## tests/integration/workflow/test_infra_apis_contract.py

- L16: function `test_required_apis_cover_all_modules_actually_used`
- L74: function `test_all_modules_use_consistent_region_var`
- L92: function `test_gke_two_stage_apply_pattern_preserved`
- L106: function `test_search_api_image_lifecycle_ignore_changes_pinned`
- L113: function `test_ops_vertex_all_includes_vvs_and_feature_view_checks`

## tests/integration/workflow/test_local_workflow_contract.py

- L13: function `test_verify_local_hybrid_recipe_pins_fast_local_order`
- L42: function `test_verify_local_app_contract_pins_local_only_scope`
- L53: function `test_verify_local_ml_contract_pins_local_only_scope`
- L65: function `test_ui_templates_fetch_canonical_api_v1_and_ops_paths`
- L86: function `test_ops_scripts_use_canonical_api_v1_and_ops_paths`
- L118: function `test_readme_documents_local_verification_entrypoints`
- L131: function `test_runbook_pins_local_hybrid_required_env_exports`

## tests/integration/workflow/test_vertex_pipeline_submit_contract.py

- L13: function `test_pipeline_wait_resolves_project_via_common_helper`
- L19: function `test_submit_train_pipeline_resolves_project_via_common_helper`
- L25: function `test_common_documents_gcp_project_precedence_in_resolve_project_id`

## tests/integration/workflow/test_vertex_resources_contract.py

- L16: function `test_vvs_module_lifecycle_protects_against_stale_id_recreation`
- L37: function `test_vvs_module_min_max_replica_pinned_to_one_for_dev`
- L58: function `test_feature_view_online_serving_source_is_direct_bigquery`
- L85: function `test_legacy_cloud_scheduler_demoted_to_monthly_smoke`
- L93: function `test_legacy_cloud_function_eventarc_marked_as_smoke`
- L100: function `test_retrain_router_marked_as_smoke_endpoint`

## tests/unit/app/test_adapters.py

- L17: function `_fake_httpx_client`
- L28: function `test_create_retrain_queries_wires_bigquery_client`
- L46: function `test_pubsub_publisher_publishes_json_bytes`
- L65: function `test_kserve_encoder_parses_embedding_dict_response_v1`
- L85: function `test_kserve_reranker_parses_scalar_scores_v1`
- L101: function `test_kserve_encoder_parses_v2_open_inference_response`
- L112: function `test_kserve_reranker_predict_with_explain_via_predict_route`
- L148: function `test_kserve_reranker_predict_with_explain_via_dedicated_url`
- L186: function `test_kserve_reranker_predict_with_explain_degrades_when_attrs_missing`
- L202: function `test_kserve_reranker_predict_with_explain_empty_instances_short_circuits`
- L211: function `test_kserve_reranker_predict_with_explain_v2_degrades_to_predict_only`
- L251: function `test_kserve_reranker_satisfies_reranker_explainer_protocol`
- L261: function `test_kserve_encoder_rejects_html_error_page_as_non_json`
- L287: function `test_kserve_encoder_rejects_empty_embedding_vector`
- L296: function `test_kserve_encoder_enforces_768d_by_default`
- L310: function `test_kserve_encoder_rejects_nan_in_embedding`
- L319: function `test_kserve_encoder_rejects_inf_in_embedding`
- L328: function `test_kserve_reranker_rejects_score_count_mismatch`
- L341: function `test_kserve_reranker_predict_with_explain_logs_count_mismatch_and_degrades`
- L375: function `test_kserve_reranker_parses_v2_attributions_output`

## tests/unit/app/test_api_contract_template.py

- L10: function `_search_payload`
- L18: function `_assert_search_shape`
- L25: function `_assert_trace_identifier`
- L30: function `_assert_result_item_required_fields`
- L36: function `_assert_feedback_shape`
- L40: function `_replace_search_container`
- L55: function `test_api_contract_readyz_returns_ok`
- L64: function `test_api_contract_search_success_shape`
- L70: function `test_api_contract_search_has_trace_identifier`
- L76: function `test_api_contract_search_result_item_required_fields`
- L82: function `test_api_contract_feedback_accepts_click`
- L94: function `test_api_contract_search_validation_error`
- L101: function `test_api_contract_feedback_rejects_unknown_action`
- L112: function `test_api_contract_feedback_validation_error`
- L121: function `test_api_contract_search_unavailable_behavior`

## tests/unit/app/test_bq_retrain_queries.py

- L11: function `_client_with_rows`
- L17: function `_make_q`
- L24: function `test_last_run_finished_at_returns_timestamp`
- L30: function `test_last_run_finished_at_returns_none_when_null`
- L35: function `test_last_run_finished_at_returns_none_when_empty_result`
- L40: function `test_feedback_rows_since_casts_to_int`
- L52: function `test_feedback_rows_since_returns_none_on_exception`
- L60: function `test_ndcg_in_window_returns_float`
- L68: function `test_ndcg_in_window_returns_none_when_no_runs`

## tests/unit/app/test_check_retrain_endpoint.py

- L8: method `__init__`
- L19: method `last_run_finished_at`
- L22: method `feedback_rows_since`
- L25: method `ndcg_in_window`
- L32: method `__init__`
- L35: method `publish`
- L39: function `test_check_retrain_does_nothing_when_fresh`
- L56: function `test_check_retrain_publishes_when_feedback_threshold_exceeded`
- L75: function `test_check_retrain_publishes_when_ndcg_drops`

## tests/unit/app/test_elasticsearch_lexical.py

- L11: function `test_elasticsearch_lexical_maps_hits_to_lexical_result`
- L38: function `test_elasticsearch_lexical_returns_empty_on_exception`

## tests/unit/app/test_event_repositories.py

- L11: function `_result_with_rows`
- L17: function `test_bigquery_event_repository_reads_search_events_with_since_param`
- L49: function `test_bigquery_event_repository_reads_impressions_and_user_actions`
- L92: function `test_bigquery_label_repository_write_ranking_labels_merges_rows`
- L120: function `test_bigquery_label_repository_reads_labels`

## tests/unit/app/test_explain.py

- L22: method `retrieve`
- L37: method `publish_candidates`
- L59: method `predict`
- L66: method `predict`
- L69: method `predict_with_explain`
- L82: function `_candidate`
- L100: function `test_run_search_returns_attributions_when_reranker_supports_explain`
- L127: function `test_run_search_falls_back_to_no_attributions_when_reranker_lacks_explain`

## tests/unit/app/test_feature_fetcher_adapters.py

- L24: function `_make_feature_value`
- L32: function `_make_feature`
- L39: function `_fos_client_returning`
- L43: function `_fetch`
- L55: function `test_fos_fetcher_extracts_three_known_features`
- L81: function `test_fos_fetcher_ignores_unknown_feature_names`
- L104: function `test_fos_fetcher_returns_all_none_when_per_id_call_raises`
- L108: function `_fetch`
- L132: function `test_fos_fetcher_returns_empty_for_empty_input`
- L143: function `test_fos_fetcher_raises_when_endpoint_resolver_returns_empty`
- L153: function `test_fos_fetcher_rejects_empty_feature_view`
- L161: function `test_fos_fetcher_canonicalizes_feature_view_name_via_admin_lookup`
- L165: method `__init__`
- L168: method `get_feature_view`
- L179: method `__init__`
- L183: method `__init__`
- L188: method `__init__`
- L191: method `fetch_feature_values`

## tests/unit/app/test_feedback_handler_http.py

- L6: function `test_feedback_endpoint_records_event`
- L21: function `test_feedback_endpoint_rejects_invalid_action`
- L30: function `test_feedback_endpoint_accepts_all_canonical_actions`

## tests/unit/app/test_feedback_service.py

- L9: function `test_record_returns_true_on_success`
- L23: function `test_record_returns_false_on_publish_failure`
- L32: function `test_record_emits_new_user_action_contract`

## tests/unit/app/test_health_handler.py

- L6: function `test_livez_returns_ok`
- L12: function `test_healthz_returns_ok`
- L17: function `test_readyz_returns_ready_when_search_wired`
- L25: function `test_readyz_returns_loading_when_retriever_missing`

## tests/unit/app/test_kserve_wiring.py

- L23: function `_settings`
- L37: function `_build_encoder_client`
- L41: function `_build_reranker_client`
- L50: function `test_apisettings_kserve_fields_default_to_empty_string`
- L67: function `test_apisettings_kserve_fields_populated_from_env`
- L97: function `test_apisettings_exposes_grouped_views_for_flags_messaging_and_popularity`
- L122: function `test_build_encoder_client_returns_none_when_url_empty`
- L130: function `test_build_encoder_client_instantiates_kserve_encoder_when_url_set`
- L146: function `test_build_reranker_client_returns_none_when_enable_rerank_false`
- L152: function `test_build_reranker_client_returns_none_when_url_empty`
- L158: function `test_build_reranker_client_instantiates_with_explain_url_when_set`
- L175: function `test_build_reranker_client_passes_none_when_explain_url_is_empty_string`
- L192: function `test_build_reranker_client_handles_whitespace_explain_url`
- L211: function `test_build_reranker_client_has_predict_with_explain_for_ranking_gate`

## tests/unit/app/test_local_boot_contract.py

- L23: function `test_container_builder_avoids_gcp_clients_when_search_disabled`
- L32: function `_forbidden`

## tests/unit/app/test_logging_middleware.py

- L12: function `test_middleware_generates_request_id_when_absent`
- L19: function `test_middleware_preserves_client_supplied_request_id`
- L25: function `test_middleware_request_id_matches_search_response`

## tests/unit/app/test_main_routing.py

- L29: function `app_no_lifespan`
- L43: function `_build`
- L55: function `test_root_redirects_to_ui`
- L62: function `test_ui_home_returns_html`
- L70: function `test_ui_dev_returns_html`
- L77: function `test_ui_model_metrics_returns_html`
- L84: function `test_ui_data_returns_html`
- L91: function `test_ui_ops_returns_html`
- L98: function `test_metrics_serves_prometheus_exposition`
- L115: function `test_metrics_emits_slo_compatible_labels`
- L136: function `test_livez_unconditional`

## tests/unit/app/test_model_handler.py

- L31: function `_build_client`
- L42: function `_wire_candidates`
- L63: function `test_model_metrics_returns_summary_and_per_case`
- L86: function `test_model_metrics_503_when_service_missing`
- L99: function `test_model_metrics_rejects_invalid_k`
- L109: function `test_model_info_reports_container_state`
- L126: function `test_model_data_returns_preview_tables`
- L141: function `test_load_cases_rejects_empty_file`
- L150: function `test_evaluate_default_cases_returns_report`

## tests/unit/app/test_observability.py

- L18: function `test_for_test_uses_stdlib_logger_and_default_service`
- L29: function `test_for_test_accepts_custom_service_name`
- L34: function `test_from_env_reads_otel_service_name`
- L45: function `test_from_env_default_matches_slo_label_contract`

## tests/unit/app/test_ops_handler.py

- L14: function `_build_test_app`
- L22: function `test_destroy_check_returns_summary`
- L45: function `test_search_volume_returns_summary`
- L65: function `test_runs_recent_returns_rows`
- L90: function `test_search_volume_returns_503_with_json_detail_on_bq_error`
- L104: function `test_runs_recent_returns_503_with_json_detail_on_bq_error`

## tests/unit/app/test_optional_adapter_helper.py

- L19: function `test_returns_none_when_disabled_without_calling_factory`
- L22: function `factory`
- L37: function `test_returns_factory_result_when_enabled`
- L48: function `test_swallows_factory_exception_and_logs_with_name`
- L51: function `factory`

## tests/unit/app/test_publisher.py

- L11: function `test_noop_publisher_accepts_any_payload`

## tests/unit/app/test_pubsub_event_writer.py

- L19: function `_client_for`
- L24: function `topic_path`
- L31: function `_build`
- L43: function `test_emit_search_event_publishes_to_search_events_topic`
- L70: function `test_emit_impression_publishes_to_search_impressions_topic`
- L95: function `test_emit_user_action_publishes_to_user_actions_topic`
- L115: function `test_publish_failure_is_logged_and_reraised`
- L134: function `_api_settings`
- L147: function `test_build_event_writer_selects_pubsub_when_topics_set`
- L169: function `test_build_event_writer_falls_back_to_cloud_logging_when_topic_missing`

## tests/unit/app/test_ranking_service.py

- L19: method `retrieve`
- L35: method `publish_candidates`
- L58: method `predict`
- L62: function `_candidate`
- L83: function `test_run_search_preserves_lexical_order`
- L99: function `test_run_search_final_rank_equals_lexical_rank_without_reranker`
- L117: function `test_run_search_continues_when_publisher_raises`
- L127: method `__init__`
- L130: method `publish_candidates`
- L151: function `test_run_search_publishes_full_pool_not_just_top_k`
- L167: function `test_run_search_forwards_filters_to_retriever`
- L186: function `test_run_search_empty_result`
- L207: function `test_run_search_rerank_reverses_order_when_reranker_says_so`
- L230: function `test_run_search_rerank_truncates_to_top_k`
- L249: function `test_run_search_rerank_with_higher_score_wins`
- L253: method `predict`
- L273: function `test_run_search_rerank_tie_breaks_by_lexical_then_semantic_rank`
- L275: method `predict`

## tests/unit/app/test_retrain.py

- L11: method `__init__`
- L24: method `last_run_finished_at`
- L27: method `feedback_rows_since`
- L30: method `ndcg_in_window`
- L42: function `test_no_reason_no_retrain`
- L54: function `test_feedback_rows_trigger`
- L66: function `test_feedback_rows_below_threshold_does_not_trigger`
- L74: function `test_ndcg_drop_triggers_retrain`
- L85: function `test_ndcg_improvement_does_not_trigger`
- L94: function `test_ndcg_missing_does_not_trigger`
- L103: function `test_ndcg_small_drop_below_threshold`
- L113: function `test_custom_ndcg_threshold_flips_decision`
- L124: function `test_staleness_trigger`
- L136: function `test_no_prior_run_triggers`
- L143: function `test_custom_feedback_threshold`
- L154: function `test_custom_stale_days_triggers_on_shorter_window`
- L165: function `test_decision_exposes_ranker_fields`

## tests/unit/app/test_run_search_feature_fetcher.py

- L34: function `_candidate`
- L63: function `test_augment_overwrites_three_dynamic_features`
- L81: function `test_augment_preserves_bq_value_when_fos_field_is_none`
- L96: function `test_augment_keeps_candidate_unchanged_when_id_not_in_fos`
- L109: function `test_augment_returns_empty_list_for_empty_input`
- L115: function `test_augment_calls_fetch_once_with_all_property_ids`
- L129: function `test_run_search_default_feature_fetcher_is_none_no_fetch_happens`
- L155: function `test_run_search_with_feature_fetcher_merges_before_reranker_predict`
- L189: function `test_run_search_swallows_feature_fetcher_failure_and_continues`
- L197: method `fetch`
- L223: function `test_container_dataclass_has_feature_fetcher_field`
- L237: function `test_search_service_accepts_feature_fetcher_kwarg`
- L247: function `test_run_search_signature_lists_feature_fetcher_with_default_none`

## tests/unit/app/test_search_api.py

- L10: function `_search_payload`
- L18: function `_replace_search_container`
- L33: function `test_search_returns_200_with_results`
- L41: function `test_search_results_preserve_lexical_rank_when_rerank_disabled`
- L50: function `test_search_emits_ranking_log`
- L64: function `test_search_top_k_truncates_response`
- L72: function `test_search_rejects_empty_query`
- L79: function `test_search_503_when_disabled`
- L88: function `test_feedback_accepts_click`
- L105: function `test_feedback_rejects_unknown_action`
- L116: function `test_readyz_ok_when_search_enabled`
- L127: function `test_readyz_503_when_retriever_missing`
- L136: function `test_readyz_503_when_encoder_missing`
- L145: function `test_healthz_unconditional`
- L154: function `test_readyz_reports_rerank_disabled_when_client_missing`
- L163: function `test_readyz_reports_rerank_enabled_when_client_set`
- L169: method `predict`
- L184: function `test_search_returns_scores_when_reranker_loaded`
- L190: method `predict`
- L209: function `test_ranking_log_receives_scores_when_reranker_loaded`
- L215: method `predict`

## tests/unit/app/test_search_builder_canonical.py

- L38: method `__init__`
- L42: method `_bigquery`
- L46: function `_settings`
- L66: function `_builder`
- L75: function `test_build_vertex_vector_search_assembles_endpoint_resource_name`
- L85: function `test_build_vertex_vector_search_accepts_fully_qualified_endpoint_name`
- L100: function `test_build_vertex_vector_search_fails_loud_when_endpoint_missing`
- L106: function `test_build_vertex_vector_search_fails_loud_when_deployed_id_missing`
- L117: function `test_resolve_feature_fetcher_returns_fos_when_fully_configured`
- L126: function `test_resolve_feature_fetcher_fails_loud_when_store_missing`
- L132: function `test_resolve_feature_fetcher_fails_loud_when_view_missing`
- L138: function `test_resolve_feature_fetcher_fails_loud_when_endpoint_missing`
- L149: function `test_resolve_lexical_returns_elasticsearch_when_url_configured`
- L158: function `test_resolve_lexical_fails_loud_when_es_backend_enable_search_no_lexical_url`
- L164: function `test_resolve_lexical_noop_when_search_disabled_and_no_lexical_urls`

## tests/unit/app/test_search_handler_http.py

- L13: function `_candidate`
- L33: function `test_search_endpoint_returns_results`
- L53: function `test_search_endpoint_503_when_retriever_unavailable`
- L84: function `test_search_endpoint_explain_returns_attributions`
- L102: function `test_search_endpoint_emits_canonical_event_logs`

## tests/unit/app/test_search_mapper.py

- L14: function `test_search_request_to_input_propagates_filters_and_flags`
- L33: function `test_to_search_response_maps_items`

## tests/unit/app/test_search_service.py

- L26: function `_make_candidate`
- L45: function `_build_service`
- L75: function `test_search_returns_items_sorted_by_final_rank`
- L89: function `test_search_calls_publisher_once_with_full_pool`
- L106: function `test_search_uses_reranker_scores_when_available`
- L123: function `test_search_raises_unavailable_when_retriever_missing`
- L136: function `test_search_raises_unavailable_when_encoder_missing`
- L149: function `test_search_populates_popularity_score_when_scorer_present`
- L160: function `test_search_emits_search_event_and_impressions`

## tests/unit/app/test_settings_sources.py

- L9: function `test_apisettings_loads_non_secret_values_from_setting_yaml`
- L41: function `test_env_vars_override_yaml_sources`

## tests/unit/app/test_synonym_expander.py

- L33: function `_b`
- L42: method `__init__`
- L45: method `smembers`
- L52: method `smembers`
- L56: function `test_noop_returns_query_unchanged`
- L61: function `test_redis_expands_known_tokens_with_synonyms`
- L81: function `test_redis_keeps_query_when_no_synonyms_known`
- L86: function `test_redis_returns_original_on_backend_failure`
- L92: function `test_redis_caps_synonyms_per_token`
- L103: function `test_redis_dedupes_across_tokens`
- L119: function `test_redis_handles_string_decoded_values`
- L123: method `smembers`

## tests/unit/app/test_vertex_vector_search_semantic_search.py

- L25: function `_make_neighbor`
- L38: function `_factory_returning`
- L45: function `_adapter`
- L60: function `test_search_converts_neighbors_to_semantic_results_in_distance_order`
- L81: function `test_search_returns_empty_when_no_neighbors`
- L86: function `test_search_returns_empty_when_response_is_empty`
- L100: function `test_search_passes_top_k_and_query_vector_and_deployed_index_id`
- L120: function `test_search_ignores_filters_in_pr1_known_limitation`
- L149: function `test_endpoint_factory_called_with_resource_name_once`
- L155: function `factory`
- L174: function `test_search_handles_missing_distance_attribute_as_max_distance`
- L202: function `test_constructor_rejects_empty_required_args`

## tests/unit/arch/test_import_boundaries.py

- L32: function `test_no_forbidden_imports`

## tests/unit/ml/common/test_gcs.py

- L4: function `test_parse_round_trip`
- L11: function `test_parse_bucket_only`
- L18: function `test_parse_trailing_slash`
- L23: function `test_child_and_uri`
- L29: function `test_model_prefix_layout`
- L35: function `test_parse_rejects_non_gcs`

## tests/unit/ml/common/test_gcs_io.py

- L14: function `test_upload_directory_recurses_and_returns_uris`
- L44: function `test_upload_directory_handles_empty_prefix`
- L61: function `test_download_file_writes_to_local_path`

## tests/unit/ml/common/test_logging.py

- L7: function `test_json_formatter_basic`
- L25: function `test_json_formatter_extras`

## tests/unit/ml/common/test_run_id.py

- L6: function `test_generate_run_id_format`
- L11: function `test_generate_run_id_uniqueness`

## tests/unit/ml/data/test_bigquery_ranker_repository.py

- L14: function `_make_repo`
- L26: function `test_fetch_training_rows_builds_parameterized_query`
- L61: function `test_save_run_records_ranker_metrics`
- L103: function `test_save_run_raises_on_insert_errors`
- L120: function `test_latest_model_path_returns_none_when_empty`
- L126: function `test_latest_model_path_returns_model_path`
- L134: function `test_save_run_dual_writes_to_vertex_experiments`
- L169: function `test_save_run_skips_vertex_experiments_without_env`

## tests/unit/ml/data/test_embedding_batch.py

- L17: method `encode_passages`
- L20: method `encode_queries`
- L28: method `fetch_all`
- L36: method `existing_hashes`
- L39: method `upsert`
- L46: method `__init__`
- L49: method `info`
- L53: function `test_encodes_all_on_empty_store`
- L69: function `test_skips_unchanged_rows_on_rerun`
- L80: function `test_re_encodes_when_text_changes`

## tests/unit/ml/data/test_feature_engineering_ranker.py

- L6: function `test_build_ranker_features_keys_match_feature_cols_ranker`
- L25: function `test_build_ranker_features_numeric_coercion`
- L47: function `test_build_ranker_features_handles_missing_behavior`

## tests/unit/ml/evaluation/test_label_gain.py

- L6: function `test_request_complete_beats_favorite_beats_click`
- L12: function `test_empty_or_unknown_returns_zero`

## tests/unit/ml/evaluation/test_ranking_metrics.py

- L8: function `test_ndcg_perfect_ranking_is_one`
- L14: function `test_ndcg_reversed_is_below_one`
- L20: function `test_ndcg_all_zero_labels_is_zero`
- L26: function `test_map_relevant_at_top_is_one`
- L32: function `test_map_no_relevance_is_zero`
- L38: function `test_recall_at_k_basic`
- L45: function `test_evaluate_over_groups_returns_all_three_keys`
- L56: function `test_evaluate_empty_input`

## tests/unit/ml/test_encoder_server.py

- L9: method `_encode`
- L13: function `test_normalize_instance_accepts_prefixed_string`
- L17: function `test_normalize_instance_accepts_legacy_object_payload`
- L22: function `test_predict_accepts_mixed_request_shapes`

## tests/unit/ml/test_lightgbm_trainer_adapter.py

- L18: function `test_lightgbm_trainer_satisfies_ranker_trainer_protocol`

## tests/unit/ml/training/test_cli_run.py

- L18: method `__init__`
- L22: method `fetch_training_rows`
- L25: method `save_run`
- L46: method `latest_model_path`
- L51: method `__init__`
- L54: method `upload`
- L60: method `__init__`
- L63: method `__enter__`
- L66: method `__exit__`
- L69: method `log_metrics`
- L73: function `_tracker_factory`
- L77: function `test_split_by_request_id_keeps_groups_intact`
- L85: function `test_split_by_request_id_empty`
- L91: function `test_run_non_dry_run_happy_path`
- L114: function `test_run_non_dry_run_raises_on_empty_dataset`
- L126: function `test_run_dry_run_skips_upload_and_save`
- L143: function `_frozen_time`

## tests/unit/ml/training/test_trainer.py

- L18: function `_synthetic_frame`
- L45: function `test_group_sizes_contiguous`
- L51: function `test_group_sizes_empty`
- L57: function `test_rank_train_produces_booster`
- L95: function `test_rank_train_missing_columns_raises`

## tests/unit/ml/training/test_vertex_experiments_tracker.py

- L19: function `fake_aiplatform`
- L38: function `test_enter_initializes_aiplatform_and_starts_run`
- L55: function `test_log_metrics_filters_non_numeric`
- L69: function `test_log_params_filters_non_scalar_and_none`
- L91: function `test_exit_propagates_aiplatform_exit_then_clears_handle`
- L105: function `test_satisfies_experiment_tracker_protocol`

## tests/unit/pipeline/dags/test_dag_files.py

- L41: function `test_dag_file_is_syntactically_valid`
- L47: function `test_dag_id_matches_filename_stem`
- L57: function `test_dag_has_schedule_and_catchup_false`
- L67: function `test_dag_does_not_use_bash_operator`
- L88: function `test_retrain_orchestration_invokes_compile_via_pod_runner_not_import`
- L110: function `test_dag_uses_pod_or_provider_operator`
- L127: function `test_monitoring_validation_sql_paths_resolve_to_real_files`
- L142: function `test_all_dag_files_present`

## tests/unit/pipeline/test_data_job_dag_wiring.py

- L26: function `_main_source`
- L35: function `test_pipeline_signature_declares_strangler_off_defaults`
- L50: function `test_build_pipeline_spec_lists_vector_search_params_with_strangler_defaults`
- L58: function `test_build_pipeline_spec_steps_include_upsert_vector_search`
- L74: function `test_pipeline_body_invokes_upsert_vector_search`
- L81: function `test_pipeline_imports_upsert_component`

## tests/unit/pipeline/test_ground_truth_jobs.py

- L11: function `test_labeling_job_builds_labels_from_impressions_and_actions`
- L17: method `read_impressions`
- L43: method `read_user_actions`
- L60: method `write_ranking_labels`
- L85: function `test_training_dataset_job_exports_relevance_label_csv`
- L109: method `fetch_training_rows`

## tests/unit/pipeline/test_kfp_orchestrator.py

- L22: method `__init__`
- L26: method `name`
- L29: method `to_runtime_task`
- L35: function `test_kfp_orchestrator_satisfies_protocol`

## tests/unit/pipeline/test_pipeline_trigger.py

- L13: function `test_decode_pubsub_message_reads_json_payload`
- L21: function `test_decode_pubsub_message_returns_empty_when_payload_missing`
- L27: function `test_merge_parameters_promotes_reasons`
- L35: function `test_merge_parameters_overrides_defaults_with_event_payload`
- L55: function `test_build_job_id_uses_prefix`

## tests/unit/pipeline/test_vector_search_writer.py

- L29: function `_datapoint`
- L38: function `test_in_memory_writer_records_datapoints`
- L51: function `test_in_memory_writer_is_idempotent`
- L61: function `test_in_memory_writer_skips_empty_batch`
- L73: function `_index_with_recorder`
- L78: function `_upsert`
- L85: function `test_vertex_writer_calls_upsert_datapoints_with_payload`
- L103: function `test_vertex_writer_chunks_large_batches`
- L127: function `test_vertex_writer_skips_empty_batch`
- L141: function `test_vertex_writer_resolves_index_once`
- L144: function `factory`
- L171: function `test_vertex_writer_rejects_invalid_args`

## tests/unit/scripts/test_adapters.py

- L17: method `__init__`
- L22: function `test_kubectl_run_prefixes_kubectl_to_args`
- L30: function `test_kubectl_run_forwards_capture_check_timeout`
- L43: function `test_kubectl_run_forwards_input_for_stdin_apply`
- L51: function `test_terraform_run_inserts_chdir_flag`
- L59: function `test_terraform_run_omits_chdir_when_none`
- L67: function `test_gcloud_run_prefixes_gcloud_to_args`
- L80: function `test_gcloud_run_forwards_capture_check_timeout`

## tests/unit/scripts/test_common_resolve_project.py

- L10: function `test_resolve_project_id_prefers_gcp_project`
- L16: function `test_resolve_project_id_falls_back_to_project_id`
- L22: function `test_resolve_project_id_falls_back_to_defaults`
- L29: function `test_env_project_id_reads_gcp_project_when_project_id_empty`
- L37: function `test_env_gcp_project_reads_project_id_when_gcp_empty`

## tests/unit/scripts/test_composer_deploy_dags.py

- L23: function `_fake_run_factory`
- L24: function `_fake_run`
- L33: function `test_main_early_returns_when_dag_bucket_empty`
- L46: function `test_main_uploads_dags_when_bucket_set`
- L51: function `_fake_terraform_run`
- L58: function `_fake_run`
- L115: function `test_main_raises_when_terraform_output_fails`
- L125: function `test_main_raises_on_invalid_json`
- L135: function `test_top_level_dag_listing_excludes_underscore_files`
- L150: function `test_pipeline_pkg_files_listed_with_gcs_relative_paths`
- L166: function `test_data_files_listed_for_sql_assets`

## tests/unit/scripts/test_composer_task_states.py

- L8: function `test_extract_json_array_strips_prologue`
- L18: function `test_latest_run_id_first_row`

## tests/unit/scripts/test_configmap_overlay.py

- L13: function `test_feature_online_store_public_domain_from_api_parses_rest_shape`
- L33: function `test_feature_online_store_public_domain_from_api_returns_empty_on_missing_domain`

## tests/unit/scripts/test_deploy_all_step_timing.py

- L24: function `_reset_globals`
- L32: function `test_step_first_call_emits_header_without_elapsed_anchor`
- L45: function `test_step_subsequent_calls_emit_elapsed_anchor`
- L65: function `test_step_done_emits_elapsed_line_matching_monitor_contract`
- L83: function `test_step_done_noop_before_any_step`
- L91: function `test_resolve_step_ref_accepts_number_and_name`
- L97: function `test_main_honors_from_step_and_to_step`
- L102: function `_runner`
- L103: function `_run`
- L130: function `test_main_prints_failure_summary_for_nonzero_step`
- L152: function `test_run_tf_apply_uses_staged_apply_and_waits_for_readiness`
- L156: function `_fake_stage1`
- L159: function `_fake_stream`
- L211: function `test_run_sync_elasticsearch_uses_project_and_default_cluster_url`
- L234: function `test_run_sync_elasticsearch_propagates_nonzero_exit`
- L243: function `test_main_invokes_precondition_before_run`
- L250: function `fake_pre`
- L253: function `fake_run`
- L280: function `test_main_skips_precondition_when_none`
- L284: function `fake_run`
- L307: function `test_main_propagates_precondition_exception_as_step_failure`
- L312: function `fake_pre`
- L317: function `fake_run`

## tests/unit/scripts/test_destroy_check.py

- L6: function `test_classify_bucket_names_splits_fail_and_warn`
- L28: function `test_classify_artifact_repos_splits_google_managed_repo`
- L35: function `test_filter_high_cost_datasets_ignores_unrelated_datasets`
- L41: function `test_looks_like_api_disabled_detects_disabled_service_errors`

## tests/unit/scripts/test_elasticsearch_wait.py

- L25: method `__init__`
- L31: function `test_wait_returns_immediately_on_green`
- L44: function `test_wait_accepts_yellow_for_single_node_cluster`
- L57: function `test_wait_polls_until_health_becomes_green`
- L62: function `fake_kubectl_run`
- L83: function `test_wait_raises_timeout_on_stuck_unknown`
- L104: function `test_healthy_states_pin_green_and_yellow`

## tests/unit/scripts/test_infra_cleanup.py

- L17: function `_completed`
- L24: function `test_delete_orphan_workloads_invokes_two_kubectl_deletes`
- L27: function `_fake_run`
- L44: function `test_delete_orphan_workloads_swallows_kubectl_failure`
- L47: function `_fake_run`
- L60: function `test_wipe_bucket_passes_recursive_glob`
- L64: function `_fake_run`
- L83: function `test_wipe_all_iterates_bucket_suffixes`
- L87: function `_fake_run`
- L107: function `test_undeploy_endpoint_models_skips_when_endpoint_absent`
- L114: function `test_undeploy_endpoint_models_skips_when_no_deployed`
- L122: function `test_undeploy_endpoint_models_iterates_deployed_models`
- L126: function `_fake_run`
- L144: function `test_deployed_index_exists_reads_index_endpoint_payload`
- L156: function `test_wait_for_deployed_index_absent_polls_until_stale_index_disappears`
- L176: function `test_wait_for_deployed_index_absent_early_exits_on_ready_state`
- L192: function `test_deployed_index_state_classifies_ready_vs_transitional`

## tests/unit/scripts/test_infra_feature_view_sync.py

- L10: method `__init__`
- L13: method `read`
- L16: method `__enter__`
- L19: method `__exit__`
- L23: function `test_main_skips_when_fos_outputs_are_empty`
- L34: function `test_trigger_and_wait_posts_sync_then_polls_until_complete`
- L37: function `_fake_urlopen`

## tests/unit/scripts/test_infra_terraform_state.py

- L19: function `_completed`
- L25: function `test_state_list_returns_empty_on_cli_failure`
- L30: function `test_state_list_returns_lines_when_present`
- L36: function `test_state_size_counts_addresses`
- L41: function `test_state_size_zero_on_cli_failure`
- L46: function `test_addresses_starting_with_filters_by_prefix`
- L56: function `test_is_in_state_true_when_address_present`
- L63: function `test_filter_targets_keeps_only_in_state`
- L78: function `test_state_rm_returns_true_on_success`
- L83: function `test_state_rm_returns_false_on_failure`
- L93: function `test_state_list_passes_env_when_supplied`
- L97: function `_fake_run`

## tests/unit/scripts/test_kserve_models_deploy.py

- L32: method `__init__`
- L47: function `_install_fake_aiplatform`
- L77: function `test_resolve_latest_prefers_model_with_production_alias`
- L114: function `test_resolve_latest_falls_back_to_first_when_no_production_alias`
- L140: function `test_resolve_latest_raises_when_no_models`
- L148: function `test_resolve_latest_raises_when_artifact_uri_missing`
- L175: function `_capture_kubectl_patch_call`
- L180: function `fake_run`
- L192: function `_capture_kubectl_run_call`
- L201: function `fake_kubectl_run`
- L213: function `test_patch_reranker_storage_uri_emits_expected_kubectl_shape`
- L243: function `test_patch_encoder_storage_uri_is_noop_under_hf_runtime`
- L265: function `test_resolve_latest_warns_on_production_alias_fallback`

## tests/unit/scripts/test_lib_config.py

- L36: function `test_configmap_keys_pin`
- L40: function `test_generate_configmap_data_returns_all_keys_strings`
- L49: function `test_committed_example_defaults_are_empty_for_vertex_resources`
- L64: function `test_generate_configmap_data_passes_through_live_vertex_outputs`
- L81: function `test_render_committed_form_matches_example_yaml`
- L94: function `test_render_runtime_form_omits_header`
- L106: function `test_render_values_are_double_quoted`

## tests/unit/scripts/test_lib_gcp_resources.py

- L18: function `test_vertex_endpoints_pin`
- L25: function `test_bucket_suffixes_pin`
- L29: function `test_default_names_pin`
- L33: function `test_vertex_model_names_pin`
- L37: function `test_endpoint_names_have_endpoint_suffix`
- L49: function `test_model_names_no_endpoint_suffix`

## tests/unit/scripts/test_local_hybrid.py

- L9: function `test_resolve_elasticsearch_api_key_prefers_local_secret`
- L17: function `test_resolve_elasticsearch_api_key_empty_when_no_url`
- L21: function `test_resolve_elasticsearch_url_prefers_explicit_env`
- L31: function `test_resolve_elasticsearch_url_uses_local_when_http_available`
- L45: function `test_resolve_elasticsearch_url_returns_empty_when_unreachable`
- L59: function `test_ensure_local_reranker_model_skips_existing_file`

## tests/unit/scripts/test_monitor.py

- L20: function `test_step_regex_matches_deploy_all_step_log_format`
- L33: function `test_step_regex_matches_single_space`
- L40: function `test_step_regex_ignores_unrelated_lines`
- L49: function `test_build_wait_regex_extracts_build_id_and_timeout`
- L57: function `test_build_wait_regex_requires_numeric_timeout`
- L62: function `test_maybe_parse_step_updates_state_and_clears_build_tracking`
- L81: function `test_maybe_parse_step_noop_for_unrelated_line`
- L89: function `test_maybe_parse_build_wait_records_build_id_and_start_time`
- L101: function `test_maybe_parse_build_wait_noop_for_unrelated_line`

## tests/unit/scripts/test_promote.py

- L23: method `__init__`
- L27: method `add_version_aliases`
- L30: method `remove_version_aliases`
- L35: method `__init__`
- L42: function `_args`
- L55: function `test_resolve_display_name_uses_model_not_endpoint`
- L70: function `test_resolve_display_name_env_override_uses_model_named_var`
- L86: function `test_select_version_picks_explicit_version_id`
- L93: function `test_select_version_picks_alias`
- L100: function `test_select_version_errors_when_no_selector_matches`
- L106: function `test_set_production_alias_moves_alias_between_versions`
- L114: function `test_set_production_alias_dry_run_does_not_call_registry`
- L122: function `test_run_alias_fails_fast_when_artifact_uri_is_empty`
- L139: function `test_run_alias_applies_when_artifact_uri_has_objects`
- L154: function `test_bst_rename_no_op_when_bst_already_exists`
- L164: function `test_bst_rename_plans_copy_in_dry_run`
- L168: function `_fail_cp`
- L176: function `test_bst_rename_returns_none_when_neither_file_present`

## tests/unit/scripts/test_repo_relative_paths.py

- L28: function `test_scripts_parents_paths_resolve`

## tests/unit/scripts/test_resolve_api_target.py

- L29: function `_clear_target_env`
- L41: function `test_explicit_api_url_wins_over_target_and_skips_token_by_default`
- L58: function `test_explicit_api_url_honors_host_and_insecure_overrides`
- L72: function `test_explicit_api_url_mints_token_when_require_token_truthy`
- L85: function `test_target_local_uses_default_local_url_without_token`
- L100: function `test_target_local_honors_local_api_url_override`
- L110: function `test_target_gcp_default_uses_public_domain_with_valid_tls`
- L131: function `test_target_gcp_public_domain_honors_insecure_tls_override`
- L143: function `test_target_gcp_falls_back_to_gateway_ip_when_public_domain_empty`
- L160: function `test_target_gcp_fallback_honors_api_host_header_override`
- L173: function `test_unknown_target_raises`

## tests/unit/scripts/test_run_all_orchestrator.py

- L22: function `_isolate_csv`
- L26: function `test_steps_are_the_canonical_validation_sequence`
- L53: function `test_main_runs_every_step_in_order_then_records_ok`
- L56: function `_fake_run`
- L70: function `test_main_fails_fast_on_first_nonzero_step`
- L73: function `_fake_run`
- L90: function `test_makefile_run_all_core_delegates_to_orchestrator`

## tests/unit/scripts/test_setup_policy_guard.py

- L8: function `_read`
- L12: function `test_setup_scripts_use_canonical_and_ci_import_paths`
- L25: function `test_setup_scripts_target_dev_terraform_environment`
- L42: function `test_api_deploy_targets_gke_rollout_path`
- L51: function `test_makefile_has_canonical_ops_targets`
- L62: function `test_makefile_sync_elasticsearch_passes_required_args`
- L84: function `test_seed_and_feature_group_contract_pin_feature_timestamp`

## tests/unit/scripts/test_step_timing.py

- L19: function `_isolate_csv`
- L23: function `test_fmt_duration_human_readable`
- L32: function `test_record_writes_header_then_rows_and_baselines_use_median_of_ok_runs`
- L52: function `test_record_keeps_only_recent_runs_per_step_for_the_median`
- L61: function `test_record_is_best_effort_and_never_raises`
- L70: function `test_print_eta_no_history`
- L75: function `test_print_eta_sums_known_step_baselines`
- L87: function `test_print_eta_all_known_uses_tilde_prefix`

## tests/unit/scripts/test_submit_train_pipeline.py

- L12: function `test_main_requires_pipeline_root_bucket`
- L20: function `env_no_bucket`
- L29: function `test_main_calls_compile_with_expanded_argv`

## tests/unit/scripts/test_subprocess_run_kwargs_guard.py

- L24: function `_is_subprocess_run`
- L35: function `_offending_calls`
- L45: function `test_no_raw_subprocess_run_capture_kwarg`

## tests/unit/scripts/test_sync_elasticsearch_exit_codes.py

- L14: function `test_run_returns_one_when_project_id_missing`
- L21: function `test_run_returns_one_when_es_url_missing`

## tests/unit/scripts/test_terraform_lock.py

- L12: function `test_parse_lock_id_from_terraform_stderr`
- L22: function `test_is_state_lock_error`
- L27: function `test_should_auto_force_unlock_aliases`
- L44: function `test_parse_lock_id_handles_real_ansi_color_output`
- L72: function `test_parse_lock_id_returns_none_when_absent`

## tests/unit/scripts/test_vertex_feature_store_wait.py

- L10: function `test_wait_until_feature_store_names_released_exits_when_empty`
- L15: function `fake_token`
- L18: function `fake_rest`
- L38: function `test_wait_until_feature_store_names_released_times_out`
- L39: function `fake_token`
- L42: function `fake_rest`

## tests/unit/scripts/test_vertex_ops_scripts.py

- L13: function `test_vector_search_probe_vector_has_expected_shape`
- L20: function `test_ops_search_retries_transient_timeout`
- L26: function `_fake_once`
- L41: function `test_ops_search_fails_after_retry_budget`
- L51: function `test_backfill_build_spec_reads_required_env`
- L69: function `test_backfill_build_spec_falls_back_to_terraform_output`
- L87: function `test_backfill_build_spec_rejects_non_int_batch_size`
- L103: function `test_feature_group_uses_feature_view_env`
- L113: method `__init__`
- L116: method `get_feature_online_store`
- L129: method `get_feature_view`
- L140: method `__init__`
- L144: method `__init__`
- L149: method `__init__`
- L152: method `fetch_feature_values`
- L187: function `test_feature_group_404_emits_sync_and_bq_diagnostics`
- L198: method `__init__`
- L201: method `get_feature_online_store`
- L213: method `get_feature_view`
- L223: method `__init__`
- L227: method `__init__`
- L232: method `__init__`
- L235: method `fetch_feature_values`
- L286: function `test_vector_search_resolves_ids_from_terraform_outputs`
- L295: method `__init__`
- L298: method `find_neighbors`
- L306: method `init`
- L329: function `_clear_aiplatform_sys_modules`
- L337: function `test_pipeline_wait_passes_when_latest_run_succeeds`
- L355: method `__init__`
- L360: function `fake_latest`
- L381: function `test_pipeline_wait_resolves_project_from_gcp_project`
- L400: method `__init__`
- L403: function `fake_latest`
- L422: function `test_pipeline_wait_fails_when_latest_run_fails`
- L438: method `__init__`
- L441: function `fake_latest`

