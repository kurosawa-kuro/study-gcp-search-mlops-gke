# Infra Domain Evidence

evidence_id: ev.domain.infra

scope: Terraform / GitHub Actions / Dockerfile static definitions.

guardrail:
- IaC 定義は本番に存在する証明ではない。ここでは `found_in` の観測事実だけを出す。
- secret 値は出さず、参照名と場所だけを出す。

## Resources

- kind: `ci-job`
  name: `pull_request`
  found_in: .github/workflows/ci.yml:L4
- kind: `ci-job`
  name: `push`
  found_in: .github/workflows/ci.yml:L6
- kind: `ci-job`
  name: `workflow_dispatch`
  found_in: .github/workflows/ci.yml:L8
- kind: `ci-job`
  name: `lint-typecheck-test`
  found_in: .github/workflows/ci.yml:L14
- kind: `ci-job`
  name: `strategy`
  found_in: .github/workflows/ci.yml:L16
- kind: `ci-job`
  name: `matrix`
  found_in: .github/workflows/ci.yml:L18
- kind: `ci-job`
  name: `dataform-check`
  found_in: .github/workflows/ci.yml:L38
- kind: `ci-job`
  name: `push`
  found_in: .github/workflows/deploy-api.yml:L4
- kind: `ci-job`
  name: `paths`
  found_in: .github/workflows/deploy-api.yml:L6
- kind: `ci-job`
  name: `workflow_dispatch`
  found_in: .github/workflows/deploy-api.yml:L14
- kind: `ci-job`
  name: `build-and-deploy`
  found_in: .github/workflows/deploy-api.yml:L28
- kind: `ci-job`
  name: `push`
  found_in: .github/workflows/deploy-dataform.yml:L4
- kind: `ci-job`
  name: `paths`
  found_in: .github/workflows/deploy-dataform.yml:L6
- kind: `ci-job`
  name: `workflow_dispatch`
  found_in: .github/workflows/deploy-dataform.yml:L10
- kind: `ci-job`
  name: `push-definitions`
  found_in: .github/workflows/deploy-dataform.yml:L22
- kind: `ci-job`
  name: `push`
  found_in: .github/workflows/deploy-encoder-image.yml:L9
- kind: `ci-job`
  name: `paths`
  found_in: .github/workflows/deploy-encoder-image.yml:L11
- kind: `ci-job`
  name: `workflow_dispatch`
  found_in: .github/workflows/deploy-encoder-image.yml:L20
- kind: `ci-job`
  name: `build-and-push`
  found_in: .github/workflows/deploy-encoder-image.yml:L33
- kind: `ci-job`
  name: `push`
  found_in: .github/workflows/deploy-pipeline.yml:L13
- kind: `ci-job`
  name: `paths`
  found_in: .github/workflows/deploy-pipeline.yml:L15
- kind: `ci-job`
  name: `workflow_dispatch`
  found_in: .github/workflows/deploy-pipeline.yml:L27
- kind: `ci-job`
  name: `compile-and-upload`
  found_in: .github/workflows/deploy-pipeline.yml:L39
- kind: `ci-job`
  name: `push`
  found_in: .github/workflows/deploy-reranker-image.yml:L9
- kind: `ci-job`
  name: `paths`
  found_in: .github/workflows/deploy-reranker-image.yml:L11
- kind: `ci-job`
  name: `workflow_dispatch`
  found_in: .github/workflows/deploy-reranker-image.yml:L20
- kind: `ci-job`
  name: `build-and-push`
  found_in: .github/workflows/deploy-reranker-image.yml:L33
- kind: `ci-job`
  name: `push`
  found_in: .github/workflows/deploy-trainer-image.yml:L8
- kind: `ci-job`
  name: `paths`
  found_in: .github/workflows/deploy-trainer-image.yml:L10
- kind: `ci-job`
  name: `workflow_dispatch`
  found_in: .github/workflows/deploy-trainer-image.yml:L21
- kind: `ci-job`
  name: `build-and-push`
  found_in: .github/workflows/deploy-trainer-image.yml:L34
- kind: `ci-job`
  name: `pull_request`
  found_in: .github/workflows/terraform.yml:L4
- kind: `ci-job`
  name: `push`
  found_in: .github/workflows/terraform.yml:L7
- kind: `ci-job`
  name: `workflow_dispatch`
  found_in: .github/workflows/terraform.yml:L10
- kind: `ci-job`
  name: `plan`
  found_in: .github/workflows/terraform.yml:L23
- kind: `ci-job`
  name: `apply`
  found_in: .github/workflows/terraform.yml:L79
- kind: `container-base-image`
  name: `ghcr.io/astral-sh/uv:0.5.4-python3.12-bookworm-slim`
  found_in: infra/run/services/composer_runner/Dockerfile:L36
- kind: `container-base-image`
  name: `python:3.12-slim-bookworm`
  found_in: infra/run/services/composer_runner/Dockerfile:L53
- kind: `container-base-image`
  name: `${ML_BUILDER_IMAGE}`
  found_in: infra/run/services/encoder/Dockerfile:L7
- kind: `container-base-image`
  name: `python:3.12-slim-bookworm`
  found_in: infra/run/services/encoder/Dockerfile:L20
- kind: `container-base-image`
  name: `ghcr.io/astral-sh/uv:0.5.4-python3.12-bookworm-slim`
  found_in: infra/run/services/ml_base/Dockerfile:L6
- kind: `container-base-image`
  name: `${ML_BUILDER_IMAGE}`
  found_in: infra/run/services/reranker/Dockerfile:L7
- kind: `container-base-image`
  name: `python:3.12-slim-bookworm`
  found_in: infra/run/services/reranker/Dockerfile:L20
- kind: `container-base-image`
  name: `ghcr.io/astral-sh/uv:0.5.4-python3.12-bookworm-slim`
  found_in: infra/run/services/search_api/Dockerfile:L14
- kind: `container-base-image`
  name: `python:3.12-slim-bookworm`
  found_in: infra/run/services/search_api/Dockerfile:L31
- kind: `gcp-resource`
  name: `google_project_service.enabled`
  found_in: infra/terraform/environments/dev/apis.tf:L36
- kind: `gcp-resource`
  name: `google_composer_environment.this`
  found_in: infra/terraform/modules/composer/main.tf:L26
- kind: `gcp-resource`
  name: `google_bigquery_dataset.mlops`
  found_in: infra/terraform/modules/data/main.tf:L5
- kind: `gcp-resource`
  name: `google_bigquery_dataset.feature_mart`
  found_in: infra/terraform/modules/data/main.tf:L11
- kind: `gcp-resource`
  name: `google_bigquery_dataset.predictions`
  found_in: infra/terraform/modules/data/main.tf:L17
- kind: `gcp-resource`
  name: `google_bigquery_table.training_runs`
  found_in: infra/terraform/modules/data/main.tf:L23
- kind: `gcp-resource`
  name: `google_bigquery_table.property_features_daily`
  found_in: infra/terraform/modules/data/main.tf:L112
- kind: `gcp-resource`
  name: `google_bigquery_table.property_features_online_latest`
  found_in: infra/terraform/modules/data/main.tf:L142
- kind: `gcp-resource`
  name: `google_bigquery_table.property_embeddings`
  found_in: infra/terraform/modules/data/main.tf:L166
- kind: `gcp-resource`
  name: `google_bigquery_table.search_logs`
  found_in: infra/terraform/modules/data/main.tf:L182
- kind: `gcp-resource`
  name: `google_bigquery_table.ranking_log`
  found_in: infra/terraform/modules/data/main.tf:L214
- kind: `gcp-resource`
  name: `google_bigquery_table.feedback_events`
  found_in: infra/terraform/modules/data/main.tf:L256
- kind: `gcp-resource`
  name: `google_bigquery_table.search_events`
  found_in: infra/terraform/modules/data/main.tf:L275
- kind: `gcp-resource`
  name: `google_bigquery_table.search_impressions`
  found_in: infra/terraform/modules/data/main.tf:L299
- kind: `gcp-resource`
  name: `google_bigquery_table.user_actions`
  found_in: infra/terraform/modules/data/main.tf:L325
- kind: `gcp-resource`
  name: `google_bigquery_table.ranking_labels`
  found_in: infra/terraform/modules/data/main.tf:L346
- kind: `gcp-resource`
  name: `google_bigquery_table.evaluation_metrics`
  found_in: infra/terraform/modules/data/main.tf:L366
- kind: `gcp-resource`
  name: `google_bigquery_table.validation_results`
  found_in: infra/terraform/modules/data/main.tf:L389
- kind: `gcp-resource`
  name: `google_bigquery_table.model_monitoring_alerts`
  found_in: infra/terraform/modules/data/main.tf:L409
- kind: `gcp-resource`
  name: `google_bigquery_table.ranking_log_hourly_ctr`
  found_in: infra/terraform/modules/data/main.tf:L434
- kind: `gcp-bucket`
  name: `google_storage_bucket.models`
  found_in: infra/terraform/modules/data/main.tf:L458
- kind: `gcp-bucket`
  name: `google_storage_bucket.artifacts`
  found_in: infra/terraform/modules/data/main.tf:L479
- kind: `gcp-bucket`
  name: `google_storage_bucket.pipeline_root`
  found_in: infra/terraform/modules/data/main.tf:L495
- kind: `gcp-resource`
  name: `google_artifact_registry_repository.mlops`
  found_in: infra/terraform/modules/data/main.tf:L516
- kind: `gcp-resource`
  name: `google_secret_manager_secret.search_api_iap_oauth_client_secret`
  found_in: infra/terraform/modules/data/main.tf:L526
- kind: `gcp-resource`
  name: `google_secret_manager_secret_version.search_api_iap_oauth_client_secret_dev_placeholder`
  found_in: infra/terraform/modules/data/main.tf:L545
- kind: `gcp-resource`
  name: `google_bigquery_dataset_iam_member.api_mlops_viewer`
  found_in: infra/terraform/modules/data/main.tf:L558
- kind: `gcp-resource`
  name: `google_bigquery_dataset_iam_member.api_feature_viewer`
  found_in: infra/terraform/modules/data/main.tf:L564
- kind: `gcp-resource`
  name: `google_storage_bucket_iam_member.api_models_read`
  found_in: infra/terraform/modules/data/main.tf:L570
- kind: `gcp-resource`
  name: `google_secret_manager_secret_iam_member.external_secrets_search_api_iap_oauth_client_secret_access`
  found_in: infra/terraform/modules/data/main.tf:L576
- kind: `gcp-resource`
  name: `google_bigquery_dataset_iam_member.train_feature_viewer`
  found_in: infra/terraform/modules/data/main.tf:L583
- kind: `gcp-resource`
  name: `google_bigquery_dataset_iam_member.train_mlops_editor`
  found_in: infra/terraform/modules/data/main.tf:L589
- kind: `gcp-resource`
  name: `google_storage_bucket_iam_member.train_models_admin`
  found_in: infra/terraform/modules/data/main.tf:L595
- kind: `gcp-resource`
  name: `google_storage_bucket_iam_member.train_pipeline_root_admin`
  found_in: infra/terraform/modules/data/main.tf:L601
- kind: `gcp-resource`
  name: `google_bigquery_dataset_iam_member.embed_feature_viewer`
  found_in: infra/terraform/modules/data/main.tf:L611
- kind: `gcp-resource`
  name: `google_bigquery_dataset_iam_member.embed_feature_editor`
  found_in: infra/terraform/modules/data/main.tf:L617
- kind: `gcp-resource`
  name: `google_storage_bucket_iam_member.embed_models_viewer`
  found_in: infra/terraform/modules/data/main.tf:L623
- kind: `gcp-resource`
  name: `google_bigquery_dataset_iam_member.pipeline_feature_viewer`
  found_in: infra/terraform/modules/data/main.tf:L629
- kind: `gcp-resource`
  name: `google_bigquery_dataset_iam_member.pipeline_mlops_editor`
  found_in: infra/terraform/modules/data/main.tf:L635
- kind: `gcp-resource`
  name: `google_storage_bucket_iam_member.pipeline_models_admin`
  found_in: infra/terraform/modules/data/main.tf:L641
- kind: `gcp-resource`
  name: `google_storage_bucket_iam_member.pipeline_root_pipeline_admin`
  found_in: infra/terraform/modules/data/main.tf:L647
- kind: `gcp-resource`
  name: `google_storage_bucket_iam_member.pipeline_root_composer_object_admin`
  found_in: infra/terraform/modules/data/main.tf:L656
- kind: `gcp-resource`
  name: `google_storage_bucket_iam_member.endpoint_encoder_models_viewer`
  found_in: infra/terraform/modules/data/main.tf:L662
- kind: `gcp-resource`
  name: `google_storage_bucket_iam_member.endpoint_reranker_models_viewer`
  found_in: infra/terraform/modules/data/main.tf:L668
- kind: `gcp-resource`
  name: `google_bigquery_dataset_iam_member.dataform_feature_editor`
  found_in: infra/terraform/modules/data/main.tf:L675
- kind: `gcp-resource`
  name: `google_bigquery_dataset_iam_member.dataform_mlops_editor`
  found_in: infra/terraform/modules/data/main.tf:L684
- kind: `gcp-resource`
  name: `google_dataform_repository.main`
  found_in: infra/terraform/modules/data/main.tf:L698
- kind: `gcp-resource`
  name: `google_dataform_repository_iam_member.admin_self`
  found_in: infra/terraform/modules/data/main.tf:L725
- kind: `gcp-resource`
  name: `google_dataform_repository_iam_member.deployer_editor`
  found_in: infra/terraform/modules/data/main.tf:L737
- kind: `gcp-resource`
  name: `google_compute_global_address.search_api`
  found_in: infra/terraform/modules/dns/main.tf:L28
- kind: `gcp-resource`
  name: `google_dns_record_set.apex_a`
  found_in: infra/terraform/modules/dns/main.tf:L36
- kind: `gcp-resource`
  name: `google_certificate_manager_dns_authorization.search_api`
  found_in: infra/terraform/modules/dns/main.tf:L46
- kind: `gcp-resource`
  name: `google_dns_record_set.cert_auth_cname`
  found_in: infra/terraform/modules/dns/main.tf:L56
- kind: `gcp-resource`
  name: `google_certificate_manager_certificate.search_api`
  found_in: infra/terraform/modules/dns/main.tf:L65
- kind: `gcp-resource`
  name: `google_certificate_manager_certificate_map.search_api`
  found_in: infra/terraform/modules/dns/main.tf:L79
- kind: `gcp-resource`
  name: `google_certificate_manager_certificate_map_entry.search_api`
  found_in: infra/terraform/modules/dns/main.tf:L85
- kind: `terraform-resource`
  name: `kubernetes_namespace.elastic_system`
  found_in: infra/terraform/modules/elasticsearch/main.tf:L1
- kind: `terraform-resource`
  name: `helm_release.eck_operator`
  found_in: infra/terraform/modules/elasticsearch/main.tf:L10
- kind: `gcp-resource`
  name: `google_container_cluster.hybrid_search`
  found_in: infra/terraform/modules/gke/main.tf:L9
- kind: `gcp-iam`
  name: `google_service_account_iam_member.api_wi`
  found_in: infra/terraform/modules/gke/main.tf:L54
- kind: `gcp-iam`
  name: `google_service_account_iam_member.encoder_wi`
  found_in: infra/terraform/modules/gke/main.tf:L60
- kind: `gcp-iam`
  name: `google_service_account_iam_member.reranker_wi`
  found_in: infra/terraform/modules/gke/main.tf:L66
- kind: `gcp-iam`
  name: `google_service_account_iam_member.external_secrets_wi`
  found_in: infra/terraform/modules/gke/main.tf:L72
- kind: `gcp-service-account`
  name: `google_service_account.api`
  found_in: infra/terraform/modules/iam/main.tf:L3
- kind: `gcp-service-account`
  name: `google_service_account.job_train`
  found_in: infra/terraform/modules/iam/main.tf:L8
- kind: `gcp-service-account`
  name: `google_service_account.job_embed`
  found_in: infra/terraform/modules/iam/main.tf:L13
- kind: `gcp-service-account`
  name: `google_service_account.dataform`
  found_in: infra/terraform/modules/iam/main.tf:L18
- kind: `gcp-service-account`
  name: `google_service_account.scheduler`
  found_in: infra/terraform/modules/iam/main.tf:L23
- kind: `gcp-service-account`
  name: `google_service_account.pipeline`
  found_in: infra/terraform/modules/iam/main.tf:L28
- kind: `gcp-service-account`
  name: `google_service_account.endpoint_encoder`
  found_in: infra/terraform/modules/iam/main.tf:L33
- kind: `gcp-service-account`
  name: `google_service_account.endpoint_reranker`
  found_in: infra/terraform/modules/iam/main.tf:L38
- kind: `gcp-service-account`
  name: `google_service_account.pipeline_trigger`
  found_in: infra/terraform/modules/iam/main.tf:L43
- kind: `gcp-service-account`
  name: `google_service_account.external_secrets`
  found_in: infra/terraform/modules/iam/main.tf:L48
- kind: `gcp-resource`
  name: `google_iam_workload_identity_pool.github`
  found_in: infra/terraform/modules/iam/main.tf:L55
- kind: `gcp-resource`
  name: `google_iam_workload_identity_pool_provider.github`
  found_in: infra/terraform/modules/iam/main.tf:L60
- kind: `gcp-service-account`
  name: `google_service_account.github_deployer`
  found_in: infra/terraform/modules/iam/main.tf:L78
- kind: `gcp-iam`
  name: `google_service_account_iam_member.github_wif_binding`
  found_in: infra/terraform/modules/iam/main.tf:L83
- kind: `gcp-iam`
  name: `google_service_account_iam_member.api_token_creator_for_admins`
  found_in: infra/terraform/modules/iam/main.tf:L99
- kind: `gcp-iam`
  name: `google_project_iam_member.github_deployer_editor`
  found_in: infra/terraform/modules/iam/main.tf:L108
- kind: `gcp-iam`
  name: `google_project_iam_member.github_deployer_sa_user`
  found_in: infra/terraform/modules/iam/main.tf:L114
- kind: `gcp-iam`
  name: `google_project_iam_member.api_bq_job_user`
  found_in: infra/terraform/modules/iam/main.tf:L122
- kind: `gcp-iam`
  name: `google_project_iam_member.gmp_compute_metric_writer`
  found_in: infra/terraform/modules/iam/main.tf:L136
- kind: `gcp-iam`
  name: `google_project_iam_member.api_aiplatform_user`
  found_in: infra/terraform/modules/iam/main.tf:L146
- kind: `gcp-iam`
  name: `google_project_iam_member.train_bq_job_user`
  found_in: infra/terraform/modules/iam/main.tf:L152
- kind: `gcp-iam`
  name: `google_project_iam_member.train_bq_read_session`
  found_in: infra/terraform/modules/iam/main.tf:L158
- kind: `gcp-iam`
  name: `google_project_iam_member.embed_bq_job_user`
  found_in: infra/terraform/modules/iam/main.tf:L164
- kind: `gcp-iam`
  name: `google_project_iam_member.embed_bq_read_session`
  found_in: infra/terraform/modules/iam/main.tf:L170
- kind: `gcp-iam`
  name: `google_project_iam_member.dataform_bq_job_user`
  found_in: infra/terraform/modules/iam/main.tf:L176
- kind: `gcp-iam`
  name: `google_project_iam_member.pipeline_bq_job_user`
  found_in: infra/terraform/modules/iam/main.tf:L182
- kind: `gcp-iam`
  name: `google_project_iam_member.pipeline_bq_read_session`
  found_in: infra/terraform/modules/iam/main.tf:L188
- kind: `gcp-iam`
  name: `google_project_iam_member.pipeline_aiplatform_user`
  found_in: infra/terraform/modules/iam/main.tf:L194
- kind: `gcp-iam`
  name: `google_project_iam_member.pipeline_trigger_aiplatform_user`
  found_in: infra/terraform/modules/iam/main.tf:L200
- kind: `gcp-iam`
  name: `google_project_iam_member.pipeline_trigger_eventarc_receiver`
  found_in: infra/terraform/modules/iam/main.tf:L206
- kind: `gcp-iam`
  name: `google_project_iam_member.pipeline_trigger_pubsub_subscriber`
  found_in: infra/terraform/modules/iam/main.tf:L212
- kind: `gcp-iam`
  name: `google_project_iam_member.pipeline_trigger_logging_writer`
  found_in: infra/terraform/modules/iam/main.tf:L218
- kind: `gcp-iam`
  name: `google_service_account_iam_member.pipeline_trigger_can_use_pipeline_sa`
  found_in: infra/terraform/modules/iam/main.tf:L224
- kind: `gcp-iam`
  name: `google_service_account_iam_member.composer_can_use_pipeline_sa`
  found_in: infra/terraform/modules/iam/main.tf:L234
- kind: `gcp-iam`
  name: `google_project_iam_member.endpoint_encoder_logging_writer`
  found_in: infra/terraform/modules/iam/main.tf:L240
- kind: `gcp-iam`
  name: `google_project_iam_member.endpoint_reranker_logging_writer`
  found_in: infra/terraform/modules/iam/main.tf:L246
- kind: `gcp-iam`
  name: `google_project_iam_member.endpoint_reranker_aiplatform_user`
  found_in: infra/terraform/modules/iam/main.tf:L269
- kind: `gcp-service-account`
  name: `google_service_account.composer`
  found_in: infra/terraform/modules/iam/main.tf:L293
- kind: `gcp-iam`
  name: `google_project_iam_member.composer_worker`
  found_in: infra/terraform/modules/iam/main.tf:L298
- kind: `gcp-iam`
  name: `google_project_iam_member.composer_aiplatform_user`
  found_in: infra/terraform/modules/iam/main.tf:L304
- kind: `gcp-iam`
  name: `google_project_iam_member.composer_bq_job_user`
  found_in: infra/terraform/modules/iam/main.tf:L310
- kind: `gcp-iam`
  name: `google_project_iam_member.composer_bq_data_viewer`
  found_in: infra/terraform/modules/iam/main.tf:L316
- kind: `gcp-iam`
  name: `google_project_iam_member.composer_run_invoker`
  found_in: infra/terraform/modules/iam/main.tf:L322
- kind: `gcp-iam`
  name: `google_project_iam_member.composer_artifactregistry_reader`
  found_in: infra/terraform/modules/iam/main.tf:L340
- kind: `gcp-iam`
  name: `google_project_iam_member.composer_storage_object_viewer`
  found_in: infra/terraform/modules/iam/main.tf:L346
- kind: `gcp-iam`
  name: `google_project_iam_member.github_deployer_composer_admin`
  found_in: infra/terraform/modules/iam/main.tf:L354
- kind: `terraform-resource`
  name: `kubernetes_namespace.search`
  found_in: infra/terraform/modules/kserve/main.tf:L13
- kind: `terraform-resource`
  name: `kubernetes_namespace.inference`
  found_in: infra/terraform/modules/kserve/main.tf:L19
- kind: `terraform-resource`
  name: `kubernetes_service_account.api`
  found_in: infra/terraform/modules/kserve/main.tf:L26
- kind: `terraform-resource`
  name: `kubernetes_service_account.encoder`
  found_in: infra/terraform/modules/kserve/main.tf:L36
- kind: `terraform-resource`
  name: `kubernetes_service_account.reranker`
  found_in: infra/terraform/modules/kserve/main.tf:L46
- kind: `terraform-resource`
  name: `helm_release.cert_manager`
  found_in: infra/terraform/modules/kserve/main.tf:L66
- kind: `terraform-resource`
  name: `helm_release.external_secrets`
  found_in: infra/terraform/modules/kserve/main.tf:L87
- kind: `terraform-resource`
  name: `helm_release.kserve_crd`
  found_in: infra/terraform/modules/kserve/main.tf:L139
- kind: `terraform-resource`
  name: `helm_release.kserve`
  found_in: infra/terraform/modules/kserve/main.tf:L150
- kind: `terraform-resource`
  name: `tls_private_key.search_api_dev`
  found_in: infra/terraform/modules/kserve/tls_dev.tf:L20
- kind: `terraform-resource`
  name: `tls_self_signed_cert.search_api_dev`
  found_in: infra/terraform/modules/kserve/tls_dev.tf:L26
- kind: `terraform-resource`
  name: `kubernetes_secret.search_api_tls`
  found_in: infra/terraform/modules/kserve/tls_dev.tf:L46
- kind: `gcp-resource`
  name: `google_pubsub_topic.ranking_log`
  found_in: infra/terraform/modules/messaging/main.tf:L11
- kind: `gcp-resource`
  name: `google_pubsub_topic.search_feedback`
  found_in: infra/terraform/modules/messaging/main.tf:L15
- kind: `gcp-resource`
  name: `google_pubsub_topic.retrain_trigger`
  found_in: infra/terraform/modules/messaging/main.tf:L19
- kind: `gcp-resource`
  name: `google_pubsub_topic.search_events`
  found_in: infra/terraform/modules/messaging/main.tf:L26
- kind: `gcp-resource`
  name: `google_pubsub_topic.search_impressions`
  found_in: infra/terraform/modules/messaging/main.tf:L30
- kind: `gcp-resource`
  name: `google_pubsub_topic.user_actions`
  found_in: infra/terraform/modules/messaging/main.tf:L34
- kind: `gcp-resource`
  name: `google_pubsub_topic_iam_member.api_publish_ranking_log`
  found_in: infra/terraform/modules/messaging/main.tf:L38
- kind: `gcp-resource`
  name: `google_pubsub_topic_iam_member.api_publish_feedback`
  found_in: infra/terraform/modules/messaging/main.tf:L44
- kind: `gcp-resource`
  name: `google_pubsub_topic_iam_member.api_publish_retrain`
  found_in: infra/terraform/modules/messaging/main.tf:L50
- kind: `gcp-resource`
  name: `google_pubsub_topic_iam_member.scheduler_publish_retrain`
  found_in: infra/terraform/modules/messaging/main.tf:L56
- kind: `gcp-resource`
  name: `google_pubsub_topic_iam_member.api_publish_search_events`
  found_in: infra/terraform/modules/messaging/main.tf:L62
- kind: `gcp-resource`
  name: `google_pubsub_topic_iam_member.api_publish_search_impressions`
  found_in: infra/terraform/modules/messaging/main.tf:L68
- kind: `gcp-resource`
  name: `google_pubsub_topic_iam_member.api_publish_user_actions`
  found_in: infra/terraform/modules/messaging/main.tf:L74
- kind: `gcp-resource`
  name: `google_pubsub_subscription.ranking_log_to_bq`
  found_in: infra/terraform/modules/messaging/main.tf:L80
- kind: `gcp-resource`
  name: `google_pubsub_subscription.search_feedback_to_bq`
  found_in: infra/terraform/modules/messaging/main.tf:L100
- kind: `gcp-resource`
  name: `google_pubsub_subscription.search_events_to_bq`
  found_in: infra/terraform/modules/messaging/main.tf:L120
- kind: `gcp-resource`
  name: `google_pubsub_subscription.search_impressions_to_bq`
  found_in: infra/terraform/modules/messaging/main.tf:L140
- kind: `gcp-resource`
  name: `google_pubsub_subscription.user_actions_to_bq`
  found_in: infra/terraform/modules/messaging/main.tf:L160
- kind: `gcp-iam`
  name: `google_project_iam_member.pubsub_bq_writer`
  found_in: infra/terraform/modules/messaging/main.tf:L184
- kind: `gcp-iam`
  name: `google_project_iam_member.pubsub_bq_metadata_viewer`
  found_in: infra/terraform/modules/messaging/main.tf:L190
- kind: `gcp-resource`
  name: `google_cloud_scheduler_job.check_retrain_daily`
  found_in: infra/terraform/modules/messaging/main.tf:L206
- kind: `gcp-resource`
  name: `google_logging_metric.api_error_rate`
  found_in: infra/terraform/modules/monitoring/main.tf:L7
- kind: `gcp-resource`
  name: `google_logging_metric.api_p95_latency`
  found_in: infra/terraform/modules/monitoring/main.tf:L23
- kind: `gcp-resource`
  name: `google_monitoring_notification_channel.email`
  found_in: infra/terraform/modules/monitoring/main.tf:L54
- kind: `terraform-resource`
  name: `time_sleep.wait_for_log_metric_indexing`
  found_in: infra/terraform/modules/monitoring/main.tf:L73
- kind: `gcp-resource`
  name: `google_monitoring_alert_policy.api_error_rate`
  found_in: infra/terraform/modules/monitoring/main.tf:L94
- kind: `gcp-resource`
  name: `google_monitoring_alert_policy.api_p95_latency`
  found_in: infra/terraform/modules/monitoring/main.tf:L118
- kind: `gcp-resource`
  name: `google_bigquery_data_transfer_config.property_feature_skew_check`
  found_in: infra/terraform/modules/monitoring/main.tf:L153
- kind: `gcp-resource`
  name: `google_bigquery_data_transfer_config.model_output_drift_check`
  found_in: infra/terraform/modules/monitoring/main.tf:L171
- kind: `gcp-resource`
  name: `google_redis_instance.synonym`
  found_in: infra/terraform/modules/redis_synonym/main.tf:L13
- kind: `gcp-resource`
  name: `google_secret_manager_secret.redis_auth`
  found_in: infra/terraform/modules/redis_synonym/main.tf:L40
- kind: `gcp-resource`
  name: `google_secret_manager_secret_version.redis_auth`
  found_in: infra/terraform/modules/redis_synonym/main.tf:L55
- kind: `terraform-resource`
  name: `namespace.${var.k8s_namespace}`
  found_in: infra/terraform/modules/slo/main.tf:L40
- kind: `terraform-resource`
  name: `service_name.${var.service_name}`
  found_in: infra/terraform/modules/slo/main.tf:L47
- kind: `terraform-resource`
  name: `namespace.${var.k8s_namespace}`
  found_in: infra/terraform/modules/slo/main.tf:L57
- kind: `terraform-resource`
  name: `service_name.${var.service_name}`
  found_in: infra/terraform/modules/slo/main.tf:L63
- kind: `terraform-resource`
  name: `namespace.${var.k8s_namespace}`
  found_in: infra/terraform/modules/slo/main.tf:L75
- kind: `terraform-resource`
  name: `service_name.${var.service_name}`
  found_in: infra/terraform/modules/slo/main.tf:L81
- kind: `gcp-resource`
  name: `google_monitoring_custom_service.search_api`
  found_in: infra/terraform/modules/slo/main.tf:L91
- kind: `gcp-resource`
  name: `google_monitoring_slo.availability`
  found_in: infra/terraform/modules/slo/main.tf:L107
- kind: `gcp-resource`
  name: `google_monitoring_slo.latency`
  found_in: infra/terraform/modules/slo/main.tf:L130
- kind: `gcp-resource`
  name: `google_monitoring_alert_policy.availability_fast_burn`
  found_in: infra/terraform/modules/slo/main.tf:L161
- kind: `gcp-resource`
  name: `google_monitoring_alert_policy.availability_slow_burn`
  found_in: infra/terraform/modules/slo/main.tf:L184
- kind: `gcp-resource`
  name: `google_monitoring_alert_policy.latency_fast_burn`
  found_in: infra/terraform/modules/slo/main.tf:L207
- kind: `gcp-resource`
  name: `google_monitoring_alert_policy.latency_slow_burn`
  found_in: infra/terraform/modules/slo/main.tf:L230
- kind: `gcp-service-account`
  name: `google_service_account.dataflow`
  found_in: infra/terraform/modules/streaming/main.tf:L19
- kind: `gcp-iam`
  name: `google_project_iam_member.dataflow_pubsub_subscriber`
  found_in: infra/terraform/modules/streaming/main.tf:L29
- kind: `gcp-iam`
  name: `google_project_iam_member.dataflow_worker`
  found_in: infra/terraform/modules/streaming/main.tf:L38
- kind: `gcp-iam`
  name: `google_project_iam_member.dataflow_storage`
  found_in: infra/terraform/modules/streaming/main.tf:L46
- kind: `gcp-iam`
  name: `google_project_iam_member.dataflow_bq_data_editor`
  found_in: infra/terraform/modules/streaming/main.tf:L55
- kind: `gcp-iam`
  name: `google_project_iam_member.dataflow_bq_jobs`
  found_in: infra/terraform/modules/streaming/main.tf:L63
- kind: `gcp-resource`
  name: `google_dataflow_flex_template_job.ranking_log_hourly_ctr`
  found_in: infra/terraform/modules/streaming/main.tf:L71
- kind: `gcp-resource`
  name: `google_vertex_ai_index.property_embeddings`
  found_in: infra/terraform/modules/vector_search/main.tf:L20
- kind: `gcp-resource`
  name: `google_vertex_ai_index_endpoint.property_embeddings`
  found_in: infra/terraform/modules/vector_search/main.tf:L66
- kind: `gcp-resource`
  name: `google_vertex_ai_index_endpoint_deployed_index.property_embeddings`
  found_in: infra/terraform/modules/vector_search/main.tf:L83
- kind: `gcp-resource`
  name: `google_pubsub_topic.model_monitoring_alerts`
  found_in: infra/terraform/modules/vertex/main.tf:L68
- kind: `gcp-resource`
  name: `google_bigquery_dataset_iam_member.pubsub_mlops_editor`
  found_in: infra/terraform/modules/vertex/main.tf:L72
- kind: `gcp-resource`
  name: `google_bigquery_dataset_iam_member.pubsub_mlops_metadata_viewer`
  found_in: infra/terraform/modules/vertex/main.tf:L78
- kind: `gcp-resource`
  name: `google_pubsub_subscription.monitoring_alerts_to_bq`
  found_in: infra/terraform/modules/vertex/main.tf:L84
- kind: `gcp-resource`
  name: `google_storage_bucket_object.pipeline_trigger_zip`
  found_in: infra/terraform/modules/vertex/main.tf:L110
- kind: `gcp-resource`
  name: `google_cloudfunctions2_function.pipeline_trigger`
  found_in: infra/terraform/modules/vertex/main.tf:L127
- kind: `gcp-resource`
  name: `google_cloud_run_service_iam_member.pipeline_trigger_invoker`
  found_in: infra/terraform/modules/vertex/main.tf:L162
- kind: `gcp-resource`
  name: `google_eventarc_trigger.retrain_to_pipeline`
  found_in: infra/terraform/modules/vertex/main.tf:L169
- kind: `gcp-resource`
  name: `google_eventarc_trigger.monitoring_to_pipeline`
  found_in: infra/terraform/modules/vertex/main.tf:L202
- kind: `gcp-resource`
  name: `google_vertex_ai_feature_group.property_features`
  found_in: infra/terraform/modules/vertex/main.tf:L244
- kind: `gcp-resource`
  name: `google_vertex_ai_feature_group_feature.property_features`
  found_in: infra/terraform/modules/vertex/main.tf:L260
- kind: `gcp-resource`
  name: `google_vertex_ai_feature_online_store.property_features`
  found_in: infra/terraform/modules/vertex/main.tf:L284
- kind: `gcp-resource`
  name: `google_vertex_ai_feature_online_store_featureview.property_features`
  found_in: infra/terraform/modules/vertex/main.tf:L322
- kind: `gcp-resource`
  name: `google_vertex_ai_endpoint.encoder`
  found_in: infra/terraform/modules/vertex/main.tf:L348
- kind: `gcp-resource`
  name: `google_vertex_ai_endpoint.reranker`
  found_in: infra/terraform/modules/vertex/main.tf:L362
- kind: `gcp-resource`
  name: `google_storage_bucket_iam_member.endpoint_encoder_models_reader`
  found_in: infra/terraform/modules/vertex/main.tf:L372
- kind: `gcp-resource`
  name: `google_storage_bucket_iam_member.endpoint_reranker_models_reader`
  found_in: infra/terraform/modules/vertex/main.tf:L378
- kind: `container-base-image`
  name: `gcr.io/dataflow-templates-base/python3-template-launcher-base:latest`
  found_in: ml/streaming/container/Dockerfile:L7

## Secret And Env References

- name: `UV_LINK_MODE`
  found_in: infra/run/services/composer_runner/Dockerfile:L38
  value: redacted (name/参照のみ)
- name: `PATH`
  found_in: infra/run/services/composer_runner/Dockerfile:L76
  value: redacted (name/参照のみ)
- name: `ML_BUILDER_IMAGE`
  found_in: infra/run/services/encoder/Dockerfile:L6
  value: redacted (name/参照のみ)
- name: `UV_LINK_MODE`
  found_in: infra/run/services/encoder/Dockerfile:L9
  value: redacted (name/参照のみ)
- name: `PATH`
  found_in: infra/run/services/encoder/Dockerfile:L27
  value: redacted (name/参照のみ)
- name: `UV_LINK_MODE`
  found_in: infra/run/services/ml_base/Dockerfile:L8
  value: redacted (name/参照のみ)
- name: `ML_BUILDER_IMAGE`
  found_in: infra/run/services/reranker/Dockerfile:L6
  value: redacted (name/参照のみ)
- name: `UV_LINK_MODE`
  found_in: infra/run/services/reranker/Dockerfile:L9
  value: redacted (name/参照のみ)
- name: `PATH`
  found_in: infra/run/services/reranker/Dockerfile:L32
  value: redacted (name/参照のみ)
- name: `UV_LINK_MODE`
  found_in: infra/run/services/search_api/Dockerfile:L16
  value: redacted (name/参照のみ)
- name: `PATH`
  found_in: infra/run/services/search_api/Dockerfile:L43
  value: redacted (name/参照のみ)
- name: `secretmanager.googleapis.com`
  found_in: infra/terraform/environments/dev/apis.tf:L11
  value: redacted (name/参照のみ)
- name: `infra_secret_ref`
  found_in: infra/terraform/environments/dev/main.tf:L43
  value: redacted (name/参照のみ)
- name: `infra_secret_ref`
  found_in: infra/terraform/environments/dev/outputs.tf:L82
  value: redacted (name/参照のみ)
- name: `synonym_redis_auth_secret_id`
  found_in: infra/terraform/environments/dev/outputs.tf:L228
  value: redacted (name/参照のみ)
- name: `Secret Manager secret ID holding the Memorystore AUTH string (External Secrets Operator mirrors it to the ``REDIS_AUTH`` env in the search-api Pod).`
  found_in: infra/terraform/environments/dev/outputs.tf:L229
  value: redacted (name/参照のみ)
- name: ``
  found_in: infra/terraform/environments/dev/outputs.tf:L230
  value: redacted (name/参照のみ)
- name: `dataform_git_token_secret_version`
  found_in: infra/terraform/environments/dev/variables.tf:L50
  value: redacted (name/参照のみ)
- name: `google_secret_manager_secret`
  found_in: infra/terraform/modules/data/main.tf:L526
  value: redacted (name/参照のみ)
- name: `search-api-iap-oauth-client-secret`
  found_in: infra/terraform/modules/data/main.tf:L527
  value: redacted (name/参照のみ)
- name: `google_secret_manager_secret_version`
  found_in: infra/terraform/modules/data/main.tf:L545
  value: redacted (name/参照のみ)
- name: `infra_secret_ref`
  found_in: infra/terraform/modules/data/main.tf:L546
  value: redacted (name/参照のみ)
- name: `dev-placeholder-do-not-use-in-prod`
  found_in: infra/terraform/modules/data/main.tf:L547
  value: redacted (name/参照のみ)
- name: `google_secret_manager_secret_iam_member`
  found_in: infra/terraform/modules/data/main.tf:L576
  value: redacted (name/参照のみ)
- name: `infra_secret_ref`
  found_in: infra/terraform/modules/data/main.tf:L577
  value: redacted (name/参照のみ)
- name: `roles/secretmanager.secretAccessor`
  found_in: infra/terraform/modules/data/main.tf:L578
  value: redacted (name/参照のみ)
- name: `serviceAccount:${var.service_accounts.external_secrets.email}`
  found_in: infra/terraform/modules/data/main.tf:L579
  value: redacted (name/参照のみ)
- name: ``
  found_in: infra/terraform/modules/data/main.tf:L709
  value: redacted (name/参照のみ)
- name: `infra_secret_ref`
  found_in: infra/terraform/modules/data/main.tf:L713
  value: redacted (name/参照のみ)
- name: `secrets`
  found_in: infra/terraform/modules/data/outputs.tf:L90
  value: redacted (name/参照のみ)
- name: `infra_secret_ref`
  found_in: infra/terraform/modules/data/outputs.tf:L92
  value: redacted (name/参照のみ)
- name: `dataform_git_token_secret_version`
  found_in: infra/terraform/modules/data/variables.tf:L48
  value: redacted (name/参照のみ)
- name: `Secret Manager resource ID (projects/.../secrets/dataform-github-token/versions/latest) for the GitHub PAT that Dataform uses to pull definitions/. Empty string = no remote sync, use Dataform UI.`
  found_in: infra/terraform/modules/data/variables.tf:L49
  value: redacted (name/参照のみ)
- name: `google_service_account_iam_member`
  found_in: infra/terraform/modules/gke/main.tf:L72
  value: redacted (name/参照のみ)
- name: `infra_secret_ref`
  found_in: infra/terraform/modules/gke/main.tf:L73
  value: redacted (name/参照のみ)
- name: `serviceAccount:${local.wi_principal}[${var.namespaces.external_secrets}/${var.ksa_names.external_secrets}]`
  found_in: infra/terraform/modules/gke/main.tf:L75
  value: redacted (name/参照のみ)
- name: `infra_secret_ref`
  found_in: infra/terraform/modules/gke/variables.tf:L39
  value: redacted (name/参照のみ)
- name: `external-secrets`
  found_in: infra/terraform/modules/gke/variables.tf:L44
  value: redacted (name/参照のみ)
- name: `infra_secret_ref`
  found_in: infra/terraform/modules/gke/variables.tf:L54
  value: redacted (name/参照のみ)
- name: `external-secrets`
  found_in: infra/terraform/modules/gke/variables.tf:L60
  value: redacted (name/参照のみ)
- name: `google_service_account`
  found_in: infra/terraform/modules/iam/main.tf:L48
  value: redacted (name/参照のみ)
- name: `sa-external-secrets`
  found_in: infra/terraform/modules/iam/main.tf:L49
  value: redacted (name/参照のみ)
- name: `https://token.actions.githubusercontent.com`
  found_in: infra/terraform/modules/iam/main.tf:L74
  value: redacted (name/参照のみ)
- name: `google_service_account_iam_member`
  found_in: infra/terraform/modules/iam/main.tf:L99
  value: redacted (name/参照のみ)
- name: `infra_secret_ref`
  found_in: infra/terraform/modules/iam/outputs.tf:L13
  value: redacted (name/参照のみ)
- name: `helm_release`
  found_in: infra/terraform/modules/kserve/main.tf:L87
  value: redacted (name/参照のみ)
- name: `external-secrets`
  found_in: infra/terraform/modules/kserve/main.tf:L88
  value: redacted (name/参照のみ)
- name: `external-secrets`
  found_in: infra/terraform/modules/kserve/main.tf:L89
  value: redacted (name/参照のみ)
- name: `https://charts.external-secrets.io`
  found_in: infra/terraform/modules/kserve/main.tf:L91
  value: redacted (name/参照のみ)
- name: `external-secrets`
  found_in: infra/terraform/modules/kserve/main.tf:L92
  value: redacted (name/参照のみ)
- name: `infra_secret_ref`
  found_in: infra/terraform/modules/kserve/main.tf:L93
  value: redacted (name/参照のみ)
- name: `infra_secret_ref`
  found_in: infra/terraform/modules/kserve/main.tf:L122
  value: redacted (name/参照のみ)
- name: `infra_secret_ref`
  found_in: infra/terraform/modules/kserve/main.tf:L127
  value: redacted (name/参照のみ)
- name: `kubernetes_secret`
  found_in: infra/terraform/modules/kserve/tls_dev.tf:L46
  value: redacted (name/参照のみ)
- name: `external_secrets_chart_version`
  found_in: infra/terraform/modules/kserve/variables.tf:L13
  value: redacted (name/参照のみ)
- name: `infra_secret_ref`
  found_in: infra/terraform/modules/kserve/variables.tf:L43
  value: redacted (name/参照のみ)
- name: `infra_secret_ref`
  found_in: infra/terraform/modules/kserve/variables.tf:L59
  value: redacted (name/参照のみ)
- name: `infra_secret_ref`
  found_in: infra/terraform/modules/messaging/main.tf:L219
  value: redacted (name/参照のみ)
- name: `google_secret_manager_secret`
  found_in: infra/terraform/modules/redis_synonym/main.tf:L40
  value: redacted (name/参照のみ)
- name: `infra_secret_ref`
  found_in: infra/terraform/modules/redis_synonym/main.tf:L43
  value: redacted (name/参照のみ)
- name: `google_secret_manager_secret_version`
  found_in: infra/terraform/modules/redis_synonym/main.tf:L55
  value: redacted (name/参照のみ)
- name: `infra_secret_ref`
  found_in: infra/terraform/modules/redis_synonym/main.tf:L57
  value: redacted (name/参照のみ)
- name: `infra_secret_ref`
  found_in: infra/terraform/modules/redis_synonym/main.tf:L58
  value: redacted (name/参照のみ)
- name: `auth_secret_id`
  found_in: infra/terraform/modules/redis_synonym/outputs.tf:L16
  value: redacted (name/参照のみ)
- name: `Secret Manager secret holding the AUTH string (or empty when AUTH is disabled)`
  found_in: infra/terraform/modules/redis_synonym/outputs.tf:L17
  value: redacted (name/参照のみ)
- name: ``
  found_in: infra/terraform/modules/redis_synonym/outputs.tf:L18
  value: redacted (name/参照のみ)
- name: `Enable AUTH (random secret managed by Memorystore)`
  found_in: infra/terraform/modules/redis_synonym/variables.tf:L37
  value: redacted (name/参照のみ)
- name: `auth_secret_id`
  found_in: infra/terraform/modules/redis_synonym/variables.tf:L46
  value: redacted (name/参照のみ)
- name: `Secret Manager secret ID where the AUTH string is mirrored for KSA / ESO`
  found_in: infra/terraform/modules/redis_synonym/variables.tf:L48
  value: redacted (name/参照のみ)
- name: `WORKDIR`
  found_in: ml/streaming/container/Dockerfile:L9
  value: redacted (name/参照のみ)
- name: `FLEX_TEMPLATE_PYTHON_PY_FILE`
  found_in: ml/streaming/container/Dockerfile:L17
  value: redacted (name/参照のみ)
- name: `PYTHONPATH`
  found_in: ml/streaming/container/Dockerfile:L18
  value: redacted (name/参照のみ)
