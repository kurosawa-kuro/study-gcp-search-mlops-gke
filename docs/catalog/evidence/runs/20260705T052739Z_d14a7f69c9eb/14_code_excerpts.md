# Controlled Code Excerpts

evidence_id: ev.code_excerpts.summary

Small deterministic source excerpts around public/test anchors. This is controlled raw evidence for investigation; it is not a license to read or paste the full repository.

## .github/workflows/ci.yml:35-41 `dataform-check`

language: `yaml`

```text
35:         if: matrix.check == 'pytest'
36:         run: uv run pytest --cov=app --cov=ml --cov=pipeline --cov-report=term
37: 
38:   dataform-check:
39:     runs-on: ubuntu-latest
40:     if: ${{ !cancelled() }}
41:     steps:
```

## .github/workflows/ci.yml:11-17 `lint-typecheck-test`

language: `yaml`

```text
11:   contents: read
12: 
13: jobs:
14:   lint-typecheck-test:
15:     runs-on: ubuntu-latest
16:     strategy:
17:       fail-fast: false
```

## .github/workflows/ci.yml:15-21 `matrix`

language: `yaml`

```text
15:     runs-on: ubuntu-latest
16:     strategy:
17:       fail-fast: false
18:       matrix:
19:         check: [ruff, mypy, pytest]
20:     steps:
21:       - uses: actions/checkout@v4
```

## .github/workflows/ci.yml:1-7 `pull_request`

language: `yaml`

```text
1: name: CI
2: 
3: on:
4:   pull_request:
5:     branches: [main]
6:   push:
7:     branches: [main]
```

## .github/workflows/ci.yml:3-9 `push`

language: `yaml`

```text
3: on:
4:   pull_request:
5:     branches: [main]
6:   push:
7:     branches: [main]
8:   workflow_dispatch:
9: 
```

## .github/workflows/ci.yml:13-19 `strategy`

language: `yaml`

```text
13: jobs:
14:   lint-typecheck-test:
15:     runs-on: ubuntu-latest
16:     strategy:
17:       fail-fast: false
18:       matrix:
19:         check: [ruff, mypy, pytest]
```

## .github/workflows/ci.yml:5-11 `workflow_dispatch`

language: `yaml`

```text
5:     branches: [main]
6:   push:
7:     branches: [main]
8:   workflow_dispatch:
9: 
10: permissions:
11:   contents: read
```

## .github/workflows/deploy-api.yml:25-31 `build-and-deploy`

language: `yaml`

```text
25:   NAMESPACE: search
26: 
27: jobs:
28:   build-and-deploy:
29:     runs-on: ubuntu-latest
30:     steps:
31:       - uses: actions/checkout@v4
```

## .github/workflows/deploy-api.yml:3-9 `paths`

language: `yaml`

```text
3: on:
4:   push:
5:     branches: [main]
6:     paths:
7:       - app/**
8:       - ml/**
9:       - pyproject.toml
```

## .github/workflows/deploy-api.yml:1-7 `push`

language: `yaml`

```text
1: name: Deploy API
2: 
3: on:
4:   push:
5:     branches: [main]
6:     paths:
7:       - app/**
```

## .github/workflows/deploy-api.yml:11-17 `workflow_dispatch`

language: `yaml`

```text
11:       - infra/manifests/**
12:       - .github/workflows/deploy-api.yml
13:       - .github/actions/**
14:   workflow_dispatch:
15: 
16: permissions:
17:   contents: read
```

## .github/workflows/deploy-dataform.yml:3-9 `paths`

language: `yaml`

```text
3: on:
4:   push:
5:     branches: [main]
6:     paths:
7:       - pipeline/data_job/dataform/**
8:       - .github/workflows/deploy-dataform.yml
9:       - .github/actions/**
```

## .github/workflows/deploy-dataform.yml:1-7 `push`

language: `yaml`

```text
1: name: Deploy Dataform
2: 
3: on:
4:   push:
5:     branches: [main]
6:     paths:
7:       - pipeline/data_job/dataform/**
```

## .github/workflows/deploy-dataform.yml:19-25 `push-definitions`

language: `yaml`

```text
19:   REPOSITORY: hybrid-search-cloud
20: 
21: jobs:
22:   push-definitions:
23:     runs-on: ubuntu-latest
24:     steps:
25:       - uses: actions/checkout@v4
```

## .github/workflows/deploy-dataform.yml:7-13 `workflow_dispatch`

language: `yaml`

```text
7:       - pipeline/data_job/dataform/**
8:       - .github/workflows/deploy-dataform.yml
9:       - .github/actions/**
10:   workflow_dispatch:
11: 
12: permissions:
13:   contents: read
```

## .github/workflows/deploy-encoder-image.yml:30-36 `build-and-push`

language: `yaml`

```text
30:   IMAGE: property-encoder
31: 
32: jobs:
33:   build-and-push:
34:     runs-on: ubuntu-latest
35:     steps:
36:       - uses: actions/checkout@v4
```

## .github/workflows/deploy-encoder-image.yml:8-14 `paths`

language: `yaml`

```text
8: on:
9:   push:
10:     branches: [main]
11:     paths:
12:       - ml/serving/**
13:       - ml/common/**
14:       - ml/registry/**
```

## .github/workflows/deploy-encoder-image.yml:6-12 `push`

language: `yaml`

```text
6: # aiplatform.Model.deploy) from scripts/setup or the KFP embed_pipeline.
7: 
8: on:
9:   push:
10:     branches: [main]
11:     paths:
12:       - ml/serving/**
```

## .github/workflows/deploy-encoder-image.yml:17-23 `workflow_dispatch`

language: `yaml`

```text
17:       - uv.lock
18:       - .github/workflows/deploy-encoder-image.yml
19:       - .github/actions/**
20:   workflow_dispatch:
21: 
22: permissions:
23:   contents: read
```

## .github/workflows/deploy-pipeline.yml:36-42 `compile-and-upload`

language: `yaml`

```text
36:   PIPELINE_ROOT_BUCKET: mlops-dev-a-pipeline-root
37: 
38: jobs:
39:   compile-and-upload:
40:     runs-on: ubuntu-latest
41:     steps:
42:       - uses: actions/checkout@v4
```

## .github/workflows/deploy-pipeline.yml:12-18 `paths`

language: `yaml`

```text
12: on:
13:   push:
14:     branches: [main]
15:     paths:
16:       - pipeline/data_job/**
17:       - pipeline/training_job/**
18:       - pipeline/evaluation_job/**
```

## .github/workflows/deploy-pipeline.yml:10-16 `push`

language: `yaml`

```text
10: # Composer 二重起動になるので、resolver only に絞り apply ステップを撤去する。
11: 
12: on:
13:   push:
14:     branches: [main]
15:     paths:
16:       - pipeline/data_job/**
```

## .github/workflows/deploy-pipeline.yml:24-30 `workflow_dispatch`

language: `yaml`

```text
24:       - uv.lock
25:       - .github/workflows/deploy-pipeline.yml
26:       - .github/actions/**
27:   workflow_dispatch:
28: 
29: permissions:
30:   contents: read
```

## .github/workflows/deploy-reranker-image.yml:30-36 `build-and-push`

language: `yaml`

```text
30:   IMAGE: property-reranker
31: 
32: jobs:
33:   build-and-push:
34:     runs-on: ubuntu-latest
35:     steps:
36:       - uses: actions/checkout@v4
```

## Guardrail

- Excerpts are capped and redacted for sensitive-looking assignment lines. Confirm full context with owner approval before relying on omitted lines.
