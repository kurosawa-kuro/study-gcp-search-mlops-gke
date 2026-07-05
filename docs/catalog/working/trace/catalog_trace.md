# Catalog Trace

machine_only: true
model_body: false

## catalog_items

### app/api/routers/search_router.py
  - evidence_id: ev.03_symbols_md.app_api_routers_search_router_py
    canonical_ref: file=evidence/03_symbols.md line=119-122 scan_id=20260705T052739Z_d14a7f69c9eb sha256=26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba
  - evidence_id: ev.03_symbols_md.app_services_search_service_py
    canonical_ref: file=evidence/03_symbols.md line=688-700 scan_id=20260705T052739Z_d14a7f69c9eb sha256=26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba
  - evidence_id: ev.03_symbols_md.app_api_mappers_search_mapper_py
    canonical_ref: file=evidence/03_symbols.md line=70-76 scan_id=20260705T052739Z_d14a7f69c9eb sha256=26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba
  - evidence_id: ev.00_scan_manifest_md
    canonical_ref: file=evidence/00_scan_manifest.md line=1-46 scan_id=20260705T052739Z_d14a7f69c9eb sha256=10de7754368cc1b2975b70ea2f5422131181b6ae499c1173977c8b92aac1756f

### app/services/adapters/kserve_encoder.py
  - evidence_id: ev.03_symbols_md.app_services_adapters_kserve_encoder_py
    canonical_ref: file=evidence/03_symbols.md line=401-407 scan_id=20260705T052739Z_d14a7f69c9eb sha256=26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba
  - evidence_id: ev.03_symbols_md.ml_serving_encoder_py
    canonical_ref: file=evidence/03_symbols.md line=1805-1824 scan_id=20260705T052739Z_d14a7f69c9eb sha256=26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba
  - evidence_id: ev.08_config_env_md
    canonical_ref: file=evidence/08_config_env.md line=1-641 scan_id=20260705T052739Z_d14a7f69c9eb sha256=1a4996ac7914192381e0ca505ff91b200d198b34a6ec1d7dcd19aa8e54451b49

### scripts/setup/destroy_all.py
  - evidence_id: ev.03_symbols_md.scripts_setup_destroy_all_py
    canonical_ref: file=evidence/03_symbols.md line=2660-2679 scan_id=20260705T052739Z_d14a7f69c9eb sha256=26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba
  - evidence_id: ev.03_symbols_md.scripts_setup_destroy_all_py
    canonical_ref: file=evidence/03_symbols.md line=2660-2679 scan_id=20260705T052739Z_d14a7f69c9eb sha256=26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba
  - evidence_id: ev.30_static_signal_hits_md
    canonical_ref: file=evidence/30_static_signal_hits.md line=1-22 scan_id=20260705T052739Z_d14a7f69c9eb sha256=f33bf139d720fbeea3833f041a81cff856ac74afc8fa2fc4382b11518668350e
  - evidence_id: ev.01_file_tree_md
    canonical_ref: file=evidence/01_file_tree.md line=1-694 scan_id=20260705T052739Z_d14a7f69c9eb sha256=ef7e5ae605c5adf038e0b01ea66d739b061e029eb84b64064fef6ee3419b6e75

### tests/ (test surface)
  - evidence_id: ev.03_symbols_md.tests_conftest_py
    canonical_ref: file=evidence/03_symbols.md line=3078-3098 scan_id=20260705T052739Z_d14a7f69c9eb sha256=26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba
  - evidence_id: ev.00_scan_manifest_md
    canonical_ref: file=evidence/00_scan_manifest.md line=1-46 scan_id=20260705T052739Z_d14a7f69c9eb sha256=10de7754368cc1b2975b70ea2f5422131181b6ae499c1173977c8b92aac1756f
  - evidence_id: ev.05_tests_md
    canonical_ref: file=evidence/05_tests.md line=1-1229 scan_id=20260705T052739Z_d14a7f69c9eb sha256=14d200f95e9c92ac20ac2c73e5c966cf54735e383ad469391bcbfa0bee703c1d

## flow_items

### primary_task_lifecycle_candidate
- step: 1
  - evidence_id: ev.03_symbols_md.app_api_routers_search_router_py
    canonical_ref: file=evidence/03_symbols.md line=119-122 scan_id=20260705T052739Z_d14a7f69c9eb sha256=26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba
  - evidence_id: ev.03_symbols_md.app_api_middleware_request_logging_py
    canonical_ref: file=evidence/03_symbols.md line=77-83 scan_id=20260705T052739Z_d14a7f69c9eb sha256=26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba
- step: 2
  - evidence_id: ev.03_symbols_md.app_services_search_service_py
    canonical_ref: file=evidence/03_symbols.md line=688-700 scan_id=20260705T052739Z_d14a7f69c9eb sha256=26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba
  - evidence_id: ev.03_symbols_md.app_api_mappers_search_mapper_py
    canonical_ref: file=evidence/03_symbols.md line=70-76 scan_id=20260705T052739Z_d14a7f69c9eb sha256=26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba
- step: 3
  - evidence_id: ev.03_symbols_md.app_services_adapters_bigquery_candidate_retriever_py
    canonical_ref: file=evidence/03_symbols.md line=286-292 scan_id=20260705T052739Z_d14a7f69c9eb sha256=26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba
  - evidence_id: ev.03_symbols_md.app_services_adapters_vertex_vector_search_semantic_search_py
    canonical_ref: file=evidence/03_symbols.md line=462-468 scan_id=20260705T052739Z_d14a7f69c9eb sha256=26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba
  - evidence_id: ev.03_symbols_md.app_services_adapters_redis_synonym_expander_py
    canonical_ref: file=evidence/03_symbols.md line=445-452 scan_id=20260705T052739Z_d14a7f69c9eb sha256=26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba
- step: 4
  - evidence_id: ev.03_symbols_md.app_services_adapters_kserve_encoder_py
    canonical_ref: file=evidence/03_symbols.md line=401-407 scan_id=20260705T052739Z_d14a7f69c9eb sha256=26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba
  - evidence_id: ev.03_symbols_md.ml_serving_encoder_py
    canonical_ref: file=evidence/03_symbols.md line=1805-1824 scan_id=20260705T052739Z_d14a7f69c9eb sha256=26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba
- step: 5
  - evidence_id: ev.03_symbols_md.app_services_adapters_kserve_reranker_py
    canonical_ref: file=evidence/03_symbols.md line=408-416 scan_id=20260705T052739Z_d14a7f69c9eb sha256=26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba
  - evidence_id: ev.03_symbols_md.app_services_ranking_py
    canonical_ref: file=evidence/03_symbols.md line=672-681 scan_id=20260705T052739Z_d14a7f69c9eb sha256=26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba
  - evidence_id: ev.03_symbols_md.app_services_adapters_pubsub_ranking_log_publisher_py
    canonical_ref: file=evidence/03_symbols.md line=439-444 scan_id=20260705T052739Z_d14a7f69c9eb sha256=26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba
- step: 6
  - evidence_id: ev.03_symbols_md.app_api_mappers_search_mapper_py
    canonical_ref: file=evidence/03_symbols.md line=70-76 scan_id=20260705T052739Z_d14a7f69c9eb sha256=26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba
  - evidence_id: ev.03_symbols_md.app_api_routers_search_router_py
    canonical_ref: file=evidence/03_symbols.md line=119-122 scan_id=20260705T052739Z_d14a7f69c9eb sha256=26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba

### destructive_management_candidate
- step: 1
  - evidence_id: ev.03_symbols_md.scripts_setup_destroy_all_py
    canonical_ref: file=evidence/03_symbols.md line=2660-2679 scan_id=20260705T052739Z_d14a7f69c9eb sha256=26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba
- step: 2
  - evidence_id: ev.03_symbols_md.scripts_domain_gcp_state_recovery_py
    canonical_ref: file=evidence/03_symbols.md line=2332-2352 scan_id=20260705T052739Z_d14a7f69c9eb sha256=26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba
  - evidence_id: ev.03_symbols_md.scripts_domain_gcp_vertex_cleanup_py
    canonical_ref: file=evidence/03_symbols.md line=2353-2361 scan_id=20260705T052739Z_d14a7f69c9eb sha256=26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba
  - evidence_id: ev.03_symbols_md.scripts_setup_destroy_all_py
    canonical_ref: file=evidence/03_symbols.md line=2660-2679 scan_id=20260705T052739Z_d14a7f69c9eb sha256=26a88b8073aefa1fb9f2e0f727bfd2b7fbb75aa6544e9ecaf1b99c2b7753beba

