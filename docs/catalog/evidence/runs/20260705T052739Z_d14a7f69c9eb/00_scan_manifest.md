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
