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
  value: redacted (name/参照のみ)
  requiredness: unknown
- ELASTICSEARCH_USERNAME
  found_in:
    - scripts/ops/sync_elasticsearch.py:L116
  value: redacted (name/参照のみ)
  requiredness: unknown
- ENCODER_MODEL_NAME
  found_in:
    - ml/serving/encoder.py:L134
  value: redacted (name/参照のみ)
  requiredness: unknown
- EVAL_CASES_FILE
  found_in:
    - scripts/ops/accuracy_report.py:L118
  value: redacted (name/参照のみ)
  requiredness: unknown
- EVAL_CASES_TAG
  found_in:
    - scripts/ops/accuracy_report.py:L43
  value: redacted (name/参照のみ)
  requiredness: unknown
- EVAL_K
  found_in:
    - scripts/ops/accuracy_report.py:L119
  value: redacted (name/参照のみ)
  requiredness: unknown
- Enable AUTH (random secret managed by Memorystore)
  found_in:
    - infra/terraform/modules/redis_synonym/variables.tf:L37
  value: redacted (name/参照のみ)
  requiredness: unknown
- FLEX_TEMPLATE_PYTHON_PY_FILE
  found_in:
    - ml/streaming/container/Dockerfile:L17
  value: redacted (name/参照のみ)
  requiredness: unknown
- GCP_PROJECT
  found_in:
    - app/api/middleware/request_logging.py:L22
    - pipeline/dags/_pod.py:L65
    - pipeline/dags/daily_feature_refresh.py:L44
    - scripts/_common.py:L129
  value: redacted (name/参照のみ)
  requiredness: unknown
- GITHUB_REPO
  found_in:
    - scripts/setup/tf_plan.py:L26
  value: redacted (name/参照のみ)
  requiredness: unknown
- GIT_SHA
  found_in:
    - ml/training/trainer.py:L304
  value: redacted (name/参照のみ)
  requiredness: unknown
- GOOGLE_APPLICATION_CREDENTIALS
  found_in:
    - app/services/adapters/internal/pubsub_diagnostics.py:L28
  value: redacted (name/参照のみ)
  requiredness: unknown
- GOOGLE_CLOUD_PROJECT
  found_in:
    - app/api/middleware/request_logging.py:L22
  value: redacted (name/参照のみ)
  requiredness: unknown
- HOST
  found_in:
    - ml/serving/encoder.py:L182
    - ml/serving/reranker.py:L148
  value: redacted (name/参照のみ)
  requiredness: unknown
- K_SERVICE
  found_in:
    - ml/common/logging/structured_logging.py:L52
  value: redacted (name/参照のみ)
  requiredness: unknown
- K_SERVICE_ACCOUNT
  found_in:
    - app/services/adapters/internal/pubsub_diagnostics.py:L27
  value: redacted (name/参照のみ)
  requiredness: unknown
- LIMIT
  found_in:
    - scripts/ops/vertex/monitoring.py:L32
    - scripts/ops/vertex/pipeline_status.py:L27
  value: redacted (name/参照のみ)
  requiredness: unknown
- LOCAL_API_URL
  found_in:
    - scripts/_common.py:L398
  value: redacted (name/参照のみ)
  requiredness: unknown
- LOCAL_ENCODER_MODEL_DIR
  found_in:
    - ml/serving/encoder.py:L126
  value: redacted (name/参照のみ)
  requiredness: unknown
- LOCAL_RERANKER_MODEL_PATH
  found_in:
    - ml/serving/reranker.py:L63
  value: redacted (name/参照のみ)
  requiredness: unknown
- LOG_AS_JSON
  found_in:
    - ml/common/logging/structured_logging.py:L52
  value: redacted (name/参照のみ)
  requiredness: unknown
- LOG_LEVEL
  found_in:
    - app/main.py:L106
    - ml/serving/encoder.py:L184
    - ml/serving/reranker.py:L150
  value: redacted (name/参照のみ)
  requiredness: unknown
- LOG_ROOT
  found_in:
    - scripts/deploy/monitor.py:L82
    - scripts/verify/_runner.py:L30
  value: redacted (name/参照のみ)
  requiredness: unknown
- MAX_RENT
  found_in:
    - scripts/ops/search.py:L23
    - scripts/ops/search_components.py:L42
  value: redacted (name/参照のみ)
  requiredness: unknown
- MIN_HIT_RATE_AT_K
  found_in:
    - scripts/ops/accuracy_report.py:L120
  value: redacted (name/参照のみ)
  requiredness: unknown
- ML_BUILDER_IMAGE
  found_in:
    - infra/run/services/encoder/Dockerfile:L6
    - infra/run/services/reranker/Dockerfile:L6
  value: redacted (name/参照のみ)
  requiredness: unknown
- MONITOR_LOG_DIR
  found_in:
    - scripts/deploy/monitor.py:L79
  value: redacted (name/参照のみ)
  requiredness: unknown
- NUM_NEIGHBORS
  found_in:
    - scripts/ops/vertex/vector_search.py:L82
  value: redacted (name/参照のみ)
  requiredness: unknown
- N_PER_ACTION
  found_in:
    - scripts/ops/label_seed.py:L28
  value: redacted (name/参照のみ)
  requiredness: unknown
- ONCALL_EMAIL
  found_in:
    - scripts/setup/tf_plan.py:L27
  value: redacted (name/参照のみ)
  requiredness: unknown
- OTEL_SERVICE_NAME
  found_in:
    - app/observability.py:L70
  value: redacted (name/参照のみ)
  requiredness: unknown
- PATH
  found_in:
    - infra/run/services/composer_runner/Dockerfile:L76
    - infra/run/services/encoder/Dockerfile:L27
    - infra/run/services/reranker/Dockerfile:L32
    - infra/run/services/search_api/Dockerfile:L43
  value: redacted (name/参照のみ)
  requiredness: unknown
- PIPELINE_DISPLAY_NAME
  found_in:
    - scripts/ops/vertex/pipeline_wait.py:L54
  value: redacted (name/参照のみ)
  requiredness: unknown
- PIPELINE_DISPLAY_NAME_PREFIX
  found_in:
    - pipeline/workflow/trigger.py:L86
    - pipeline/workflow/trigger_zip/main.py:L86
  value: redacted (name/参照のみ)
  requiredness: unknown
- PIPELINE_ENABLE_CACHING
  found_in:
    - pipeline/workflow/trigger.py:L88
    - pipeline/workflow/trigger_zip/main.py:L88
  value: redacted (name/参照のみ)
  requiredness: unknown
- PIPELINE_SERVICE_ACCOUNT
  found_in:
    - pipeline/workflow/trigger.py:L87
    - pipeline/workflow/trigger_zip/main.py:L87
  value: redacted (name/参照のみ)
  requiredness: unknown
- PIPELINE_WAIT_POLL_SECONDS
  found_in:
    - scripts/ops/vertex/pipeline_wait.py:L56
  value: redacted (name/参照のみ)
  requiredness: unknown
- PIPELINE_WAIT_TIMEOUT_SECONDS
  found_in:
    - scripts/ops/vertex/pipeline_wait.py:L55
  value: redacted (name/参照のみ)
  requiredness: unknown
- PORT
  found_in:
    - ml/serving/encoder.py:L183
    - ml/serving/reranker.py:L149
  value: redacted (name/参照のみ)
  requiredness: unknown
- PROJECT_ID
  found_in:
    - app/api/middleware/request_logging.py:L22
    - pipeline/dags/_pod.py:L65
    - pipeline/dags/daily_feature_refresh.py:L44
    - scripts/_common.py:L130
    - scripts/domain/gcp/state_recovery.py:L676
    - scripts/ops/sync_elasticsearch.py:L108
    - scripts/ops/sync_synonyms.py:L121
  value: redacted (name/参照のみ)
  requiredness: unknown
- PROMOTE_KIND
  found_in:
    - scripts/ops/promote.py:L267
  value: redacted (name/参照のみ)
  requiredness: unknown
- PROPERTY_ID
  found_in:
    - scripts/ops/vertex/feature_group.py:L120
  value: redacted (name/参照のみ)
  requiredness: unknown
- PYTHONPATH
  found_in:
    - ml/streaming/container/Dockerfile:L18
  value: redacted (name/参照のみ)
  requiredness: unknown
- QUERY
  found_in:
    - scripts/ops/feedback.py:L14
    - scripts/ops/label_seed.py:L27
    - scripts/ops/ranking.py:L15
    - scripts/ops/search.py:L21
    - scripts/ops/search_components.py:L40
    - scripts/ops/vertex/explain.py:L27
  value: redacted (name/参照のみ)
  requiredness: unknown
- REDIS_AUTH
  found_in:
    - scripts/ops/sync_synonyms.py:L97
    - scripts/ops/sync_synonyms.py:L113
    - scripts/ops/sync_synonyms.py:L230
  value: redacted (name/参照のみ)
  requiredness: unknown
- REGION
  found_in:
    - pipeline/dags/_pod.py:L66
    - scripts/domain/gcp/state_recovery.py:L677
    - scripts/ops/sync_synonyms.py:L125
  value: redacted (name/参照のみ)
  requiredness: unknown
- RUN_ID
  found_in:
    - scripts/ops/composer_task_states.py:L145
    - scripts/ops/composer_task_states.py:L151
  value: redacted (name/参照のみ)
  requiredness: unknown
- RUN_LIVE_GCP_ACCEPTANCE
  found_in:
    - tests/e2e/test_live_acceptance_gate.py:L34
  value: redacted (name/参照のみ)
  requiredness: unknown
- RUN_LIVE_GCP_FULL_RECREATE
  found_in:
    - tests/e2e/test_full_recreate_gate.py:L38
  value: redacted (name/参照のみ)
  requiredness: unknown
- SEARCH_RETRIES
  found_in:
    - scripts/ops/search.py:L24
  value: redacted (name/参照のみ)
  requiredness: unknown
- SEARCH_RETRY_SLEEP
  found_in:
    - scripts/ops/search.py:L25
  value: redacted (name/参照のみ)
  requiredness: unknown
- SYNONYM_KEY_PREFIX
  found_in:
    - scripts/ops/sync_synonyms.py:L149
  value: redacted (name/参照のみ)
  requiredness: unknown
- SYNONYM_REDIS_AUTH_SECRET_ID
  found_in:
    - scripts/ops/sync_synonyms.py:L134
  value: redacted (name/参照のみ)
  requiredness: unknown
- SYNONYM_REDIS_INSTANCE
  found_in:
    - scripts/ops/sync_synonyms.py:L129
  value: redacted (name/参照のみ)
  requiredness: unknown
- SYNONYM_REDIS_URL
  found_in:
    - scripts/ops/sync_synonyms.py:L63
  value: redacted (name/参照のみ)
  requiredness: unknown
- Secret Manager resource ID (projects/.../secrets/dataform-github-token/versions/latest) for the GitHub PAT that Dataform uses to pull definitions/. Empty string = no remote sync, use Dataform UI.
  found_in:
    - infra/terraform/modules/data/variables.tf:L49
  value: redacted (name/参照のみ)
  requiredness: unknown
- Secret Manager secret ID holding the Memorystore AUTH string (External Secrets Operator mirrors it to the ``REDIS_AUTH`` env in the search-api Pod).
  found_in:
    - infra/terraform/environments/dev/outputs.tf:L229
  value: redacted (name/参照のみ)
  requiredness: unknown
- Secret Manager secret ID where the AUTH string is mirrored for KSA / ESO
  found_in:
    - infra/terraform/modules/redis_synonym/variables.tf:L48
  value: redacted (name/参照のみ)
  requiredness: unknown
- Secret Manager secret holding the AUTH string (or empty when AUTH is disabled)
  found_in:
    - infra/terraform/modules/redis_synonym/outputs.tf:L17
  value: redacted (name/参照のみ)
  requiredness: unknown
- TARGET
  found_in:
    - scripts/_common.py:L385
  value: redacted (name/参照のみ)
  requiredness: unknown
- TOP_K
  found_in:
    - scripts/ops/ranking.py:L16
    - scripts/ops/search.py:L22
    - scripts/ops/search_components.py:L41
    - scripts/ops/vertex/explain.py:L28
  value: redacted (name/参照のみ)
  requiredness: unknown
- UV_LINK_MODE
  found_in:
    - infra/run/services/composer_runner/Dockerfile:L38
    - infra/run/services/encoder/Dockerfile:L9
    - infra/run/services/ml_base/Dockerfile:L8
    - infra/run/services/reranker/Dockerfile:L9
    - infra/run/services/search_api/Dockerfile:L16
  value: redacted (name/参照のみ)
  requiredness: unknown
- VERIFY_LOG_DIR
  found_in:
    - scripts/verify/_runner.py:L27
  value: redacted (name/参照のみ)
  requiredness: unknown
- VERTEX_EXPERIMENT_NAME
  found_in:
    - ml/data/loaders/ranker_repository.py:L197
    - ml/training/trainer.py:L260
  value: redacted (name/参照のみ)
  requiredness: unknown
- VERTEX_LOCATION
  found_in:
    - scripts/domain/gcp/state_recovery.py:L677
  value: redacted (name/参照のみ)
  requiredness: unknown
- VIRTUAL_ENV
  found_in:
    - scripts/setup/doctor.py:L45
  value: redacted (name/参照のみ)
  requiredness: unknown
- WORKDIR
  found_in:
    - ml/streaming/container/Dockerfile:L9
  value: redacted (name/参照のみ)
  requiredness: unknown
- auth_secret_id
  found_in:
    - infra/terraform/modules/redis_synonym/outputs.tf:L16
    - infra/terraform/modules/redis_synonym/variables.tf:L46
  value: redacted (name/参照のみ)
  requiredness: unknown
- dataform_git_token_secret_version
  found_in:
    - infra/terraform/environments/dev/variables.tf:L50
    - infra/terraform/modules/data/variables.tf:L48
  value: redacted (name/参照のみ)
  requiredness: unknown
- dev-placeholder-do-not-use-in-prod
  found_in:
    - infra/terraform/modules/data/main.tf:L547
  value: redacted (name/参照のみ)
  requiredness: unknown
- external-secrets
  found_in:
    - infra/terraform/modules/gke/variables.tf:L44
    - infra/terraform/modules/gke/variables.tf:L60
    - infra/terraform/modules/kserve/main.tf:L88
    - infra/terraform/modules/kserve/main.tf:L89
    - infra/terraform/modules/kserve/main.tf:L92
  value: redacted (name/参照のみ)
  requiredness: unknown
- external_secrets_chart_version
  found_in:
    - infra/terraform/modules/kserve/variables.tf:L13
  value: redacted (name/参照のみ)
  requiredness: unknown
- google_secret_manager_secret
  found_in:
    - infra/terraform/modules/data/main.tf:L526
    - infra/terraform/modules/redis_synonym/main.tf:L40
  value: redacted (name/参照のみ)
  requiredness: unknown
- google_secret_manager_secret_iam_member
  found_in:
    - infra/terraform/modules/data/main.tf:L576
  value: redacted (name/参照のみ)
  requiredness: unknown
- google_secret_manager_secret_version
  found_in:
    - infra/terraform/modules/data/main.tf:L545
    - infra/terraform/modules/redis_synonym/main.tf:L55
  value: redacted (name/参照のみ)
  requiredness: unknown
- google_service_account
  found_in:
    - infra/terraform/modules/iam/main.tf:L48
  value: redacted (name/参照のみ)
  requiredness: unknown
- google_service_account_iam_member
  found_in:
    - infra/terraform/modules/gke/main.tf:L72
    - infra/terraform/modules/iam/main.tf:L99
  value: redacted (name/参照のみ)
  requiredness: unknown
- helm_release
  found_in:
    - infra/terraform/modules/kserve/main.tf:L87
  value: redacted (name/参照のみ)
  requiredness: unknown
- https://charts.external-secrets.io
  found_in:
    - infra/terraform/modules/kserve/main.tf:L91
  value: redacted (name/参照のみ)
  requiredness: unknown
- https://token.actions.githubusercontent.com
  found_in:
    - infra/terraform/modules/iam/main.tf:L74
  value: redacted (name/参照のみ)
  requiredness: unknown
- infra_secret_ref
  found_in:
    - infra/terraform/environments/dev/main.tf:L43
    - infra/terraform/environments/dev/outputs.tf:L82
    - infra/terraform/modules/data/main.tf:L546
    - infra/terraform/modules/data/main.tf:L577
    - infra/terraform/modules/data/main.tf:L713
    - infra/terraform/modules/data/outputs.tf:L92
    - infra/terraform/modules/gke/main.tf:L73
    - infra/terraform/modules/gke/variables.tf:L39
    - infra/terraform/modules/gke/variables.tf:L54
    - infra/terraform/modules/iam/outputs.tf:L13
    - infra/terraform/modules/kserve/main.tf:L93
    - infra/terraform/modules/kserve/main.tf:L122
    - infra/terraform/modules/kserve/main.tf:L127
    - infra/terraform/modules/kserve/variables.tf:L43
    - infra/terraform/modules/kserve/variables.tf:L59
    - infra/terraform/modules/messaging/main.tf:L219
    - infra/terraform/modules/redis_synonym/main.tf:L43
    - infra/terraform/modules/redis_synonym/main.tf:L57
    - infra/terraform/modules/redis_synonym/main.tf:L58
  value: redacted (name/参照のみ)
  requiredness: unknown
- kubernetes_secret
  found_in:
    - infra/terraform/modules/kserve/tls_dev.tf:L46
  value: redacted (name/参照のみ)
  requiredness: unknown
- roles/secretmanager.secretAccessor
  found_in:
    - infra/terraform/modules/data/main.tf:L578
  value: redacted (name/参照のみ)
  requiredness: unknown
- sa-external-secrets
  found_in:
    - infra/terraform/modules/iam/main.tf:L49
  value: redacted (name/参照のみ)
  requiredness: unknown
- search-api-iap-oauth-client-secret
  found_in:
    - infra/terraform/modules/data/main.tf:L527
  value: redacted (name/参照のみ)
  requiredness: unknown
- secretmanager.googleapis.com
  found_in:
    - infra/terraform/environments/dev/apis.tf:L11
  value: redacted (name/参照のみ)
  requiredness: unknown
- secrets
  found_in:
    - infra/terraform/modules/data/outputs.tf:L90
  value: redacted (name/参照のみ)
  requiredness: unknown
- serviceAccount:${local.wi_principal}[${var.namespaces.external_secrets}/${var.ksa_names.external_secrets}]
  found_in:
    - infra/terraform/modules/gke/main.tf:L75
  value: redacted (name/参照のみ)
  requiredness: unknown
- serviceAccount:${var.service_accounts.external_secrets.email}
  found_in:
    - infra/terraform/modules/data/main.tf:L579
  value: redacted (name/参照のみ)
  requiredness: unknown
- synonym_redis_auth_secret_id
  found_in:
    - infra/terraform/environments/dev/outputs.tf:L228
  value: redacted (name/参照のみ)
  requiredness: unknown

## Scan Limitations

- required/optional は未確認。
- default 値は解析していない。
- secret 値は含めない。
