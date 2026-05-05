# APIエンドポイント整理 — 再設計案

## 1. 結論

**4軸で分離する。`/api/v1/` (公開API) / `/ops/` (運用API) / `/ui/` (Jinja UI) / `/` 直下 (k8s + Prom予約)。**

現状の歪みの本質は「business APIだけprefixなし、operator UIだけ`/ui/`、それ以外はバラバラ」という非対称性。`/search` と `/model/info` が同じ階層に並ぶのが歪みの正体。アクセス主体 (エンドユーザー / 開発者・運用者 / k8s / Prometheus) で物理的にprefixを切るのが正解。

---

## 2. 理由

### 2.1 アクセス主体ごとに「壊していい範囲」が違う

| 主体 | 壊していい頻度 | バージョニング | 認証境界 |
|---|---|---|---|
| エンドユーザー (検索フロント) | 低 (契約) | 必須 (`v1`) | IAP or APIキー |
| 開発者・運用者 (UI操作・調査) | 中 | 不要 | IAP (社内のみ) |
| k8s (probe) | 不可 | 不要 | 認証なし (cluster内) |
| Prometheus (scrape) | 不可 | 不要 | 認証なし (GMP) |

`/search` (エンドユーザー契約) と `/model/info` (運用者向け debug) を同じ root に並べると、**v2移行時に運用APIまで巻き込む** か、**運用API変更でエンドユーザー契約を壊すリスク**が出る。分離すれば独立に進化できる。

### 2.2 IAP policy / NetworkPolicy の記述が綺麗になる

現状はpath単位で OIDC gate を書く必要があるが、prefix で分けると `GCPBackendPolicy` が「`/api/v1/*` は APIキー or IAP」「`/ops/*` と `/ui/*` は IAP必須」と**prefixルールだけで完結**する。policyのテストもprefix単位で書ける。

### 2.3 Swagger UI (FastAPI標準) を壊さない構造

FastAPI の `/docs` `/redoc` `/openapi.json` は**ルート直下が最も自然**。`docs_url=None` で無効化して `/api/v1/docs` に再配置もできるが、その必要が出るのはエンドユーザーにOpenAPIを見せたくないケースのみ。今回は**運用UIと同じくIAP配下なので `/docs` のままで問題ない**。

---

## 3. 有力シナリオ — 推奨構造

```
/                                308 → /ui/
/livez  /healthz  /readyz        k8s probes (auth なし、cluster内)
/metrics                         Prometheus exposition (GMP scrape)
/docs  /redoc  /openapi.json     FastAPI標準 (IAP配下なので公開でOK)
/static/*                        UI assets

/api/v1/                         エンドユーザー契約API (バージョン付き)
  POST   /api/v1/search
  POST   /api/v1/feedback

/ops/                            運用・開発者専用API (バージョンなし)
  POST   /ops/jobs/check-retrain
  GET    /ops/model/info
  GET    /ops/model/metrics

/ui/                             Operator UI (Jinja2、AJAXで /api/v1 と /ops を叩く)
  GET    /ui/
  GET    /ui/model/metrics
  GET    /ui/data
```

### 3.1 各surfaceの責務マトリクス

| surface | prefix | 認証 | バージョニング | OpenAPI掲載 | k8s probe対象 |
|---|---|---|---|---|---|
| App API | `/api/v1/` | IAP (将来 APIキー併用可) | あり | あり | 否 |
| Ops API | `/ops/` | IAP必須 | なし (内部API) | あり (社内向け) | 否 |
| Probes | `/livez` `/readyz` | なし | なし | **除外** | 是 |
| Prom | `/metrics` | なし | なし | **除外** | 否 |
| Operator UI | `/ui/` | IAP必須 | なし | 不要 (HTML) | 否 |
| FastAPI docs | `/docs` `/redoc` | IAP配下なら公開可 | — | — | 否 |

### 3.2 router配線 (`app/main.py`) の書き換え案

```python
# Public API (versioned)
api_v1 = APIRouter(prefix="/api/v1")
api_v1.include_router(search_router)      # /api/v1/search
api_v1.include_router(feedback_router)    # /api/v1/feedback
app.include_router(api_v1)

# Operations API (internal, IAP-gated, unversioned)
ops = APIRouter(prefix="/ops", include_in_schema=True)  # 社内向けOpenAPIに載せる
ops.include_router(retrain_router)        # /ops/jobs/check-retrain
ops.include_router(model_router)          # /ops/model/info /ops/model/metrics
app.include_router(ops)

# Probes (k8s)
app.include_router(health_router)         # /livez /healthz /readyz
                                          # OpenAPIから除外: include_in_schema=False

# Operator UI (AJAX で /api/v1 と /ops を叩く)
app.include_router(build_ui_router(...), prefix="/ui", include_in_schema=False)

# Reserved roots
@app.get("/", include_in_schema=False)
def root(): return RedirectResponse("/ui/", 308)

app.mount("/static", StaticFiles(...), name="static")
Instrumentator(...).instrument(app).expose(
    app, endpoint="/metrics",
    include_in_schema=False,
)
```

### 3.3 OpenAPIへの掲載/除外ポリシー

| エンドポイント | `include_in_schema` | 理由 |
|---|---|---|
| `/api/v1/*` | `True` | エンドユーザー契約 |
| `/ops/*` | `True` | 開発者がSwagger UIから叩く運用ツールにする |
| `/livez` `/healthz` `/readyz` | `False` | k8s専用、人が叩かない |
| `/metrics` | `False` (Instrumentatorのデフォルト) | Prom専用 |
| `/ui/*` | `False` | HTMLレスポンス、契約なし |

`/ops/*` を Swagger に載せておくと、**運用者は `/docs` から直接 `check-retrain` を dry-run できる**。これが「FastAPIのAPI層が多目的に活用できる」の正しい使い方。

---

## 4. 破綻条件

### 4.1 `/api/v1/` 切り替えで本当に契約が変わる
現状 `/search` を叩いている既存クライアント (社内別チーム、商品検索本番への転用先) があるなら、`/api/v1/search` への移行は**互換期間が必要**。対策: 旧パスを `RedirectResponse(..., 307)` で残す (POSTを保持する308は不可な環境がある、307が安全)、または router を両prefixに register して `Deprecation` header を付与。

### 4.2 IAP policy のpath書き換えコスト
`infra/manifests/policies/search-api-iap-policy.yaml` の matcher を全部書き直す必要がある。だがこれは**1回限りの移行コスト**で、以降のpolicy追加は楽になる。

### 4.3 SLO定義の filter変更
`infra/terraform/modules/slo/main.tf` の `service="search-api"` ラベルは維持されるが、**SLO対象の path filter が変わる** (`/api/v1/search` だけをSLO対象にしたい等)。`prometheus-fastapi-instrumentator` の `should_group_status_codes` と path label を確認し、SLO module 側の filter を `path=~"/api/v1/.*"` に絞ると**運用API由来の5xxがエンドユーザーSLOを汚染しない**メリットがある。

### 4.4 `/healthz` を Cloud Run 予約問題で避けた経緯
現状 `/livez` が canonical なのは Cloud Run 都合。GKE 専有なら `/healthz` を canonical に戻してもいいが、**「Cloud Run へ戻る選択肢を残す」なら `/livez` 維持**。今回はGKE前提でも、ポータビリティ観点で `/livez` 維持を推奨。

---

## 5. 実務・行動への影響

### 5.1 移行の優先順位 (非対称性で並べる)

| # | 作業 | リスク | リターン |
|---|---|---|---|
| 1 | `/ops/` prefix 新設 + `model_router` / `retrain_router` 移送 | 低 (内部利用のみ) | 高 (アクセス境界が即明確化) |
| 2 | `/api/v1/` prefix 新設 + 旧パス307互換 | 中 (契約変更) | 高 (将来のv2移行が無痛化) |
| 3 | `include_in_schema` 整理 (probes/metrics除外) | 極小 | 中 (Swagger UIが運用ツール化) |
| 4 | IAP policy / NetworkPolicy のprefix書き換え | 中 (manifest変更) | 高 (policy記述が宣言的に) |
| 5 | SLO filter を `/api/v1/*` に絞る | 低 | 中 (SLOがエンドユーザー視点に純化) |

**着手順の推奨**: 1 → 3 → 2 → 4 → 5。`/ops/` から始めるのは契約影響ゼロで構造改善効果が最大だから。

### 5.2 PMLE学習との接続

この整理は **「Vertex AI Endpoint の online prediction (エンドユーザー契約) と Pipelines / Model Registry 操作 (運用API) を別surfaceで露出する」**という Vertex AI 側の設計思想と完全に同型。`/api/v1/` = Vertex AI Endpoint、`/ops/` = Vertex AI Pipelines API、と読み替えると、PMLEで問われる **「prediction surface と control plane の分離」** がそのまま自分のコードベースで体現される。study repo の Phase 5 にもこの構造を継承する価値あり。

### 5.3 テスト追加候補

- `tests/integration/api/test_route_prefixes.py`: `/api/v1/search` `/ops/model/info` `/livez` `/metrics` `/ui/` がそれぞれ期待ステータスを返す contract pin
- `tests/integration/infra/test_manifests_structure.py` 拡張: IAP policy が `/ops/*` `/ui/*` をIAP必須、`/livez` `/readyz` `/metrics` を認証なしに gate していることを assert
- `tests/unit/api/test_openapi_schema.py`: `openapi.json` に probes/metrics が**含まれていない**ことを assert (誤って公開しない gate)

---

## 補足: 1点だけ判断が要る論点

**`/ops/` をエンドユーザー向けOpenAPI (`/openapi.json`) に含めるか分けるか。**

- **含める案**: 単一 `/docs` で運用者も開発者も同じUIを使える。IAPで境界が引かれているので情報漏洩リスクは低い。**推奨。**
- **分ける案**: `app = FastAPI(openapi_url="/api/v1/openapi.json")` + 別途 `ops_app` をsub-applicationとしてmount。`/docs` をエンドユーザー向けに純化できるが、構造が複雑化。エンドユーザーに `/docs` を公開する将来計画があるなら検討。

現状はIAP配下なので**含める案**で十分。エンドユーザーにOpenAPIを公開するフェーズになったら分離を再検討、で良い。