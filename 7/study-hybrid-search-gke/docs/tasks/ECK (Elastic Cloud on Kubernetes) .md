# 結論

**Cloud Runでは不可。** ESは設計思想上 Cloud Run と相性が悪い。**GKE Autopilot に乗せるのが正解**、既にGKE使っているなら追加学習コストもほぼゼロ。

---

# 理由

Cloud Run が ES に向かない構造的理由:

| 制約 | Cloud Run | ESの要求 |
|---|---|---|
| ストレージ | エフェメラル(コンテナ消滅でデータ消滅) | 永続ボリューム必須 |
| 起動モデル | リクエスト駆動・スケールゼロ | **常駐前提**(クラスタ状態管理) |
| メモリ上限 | 32GB(第2世代) | 動くが割高 |
| ネットワーク | HTTPのみ | transport層(9300)はクラスタ通信用 |
| ヘルスチェック | HTTP想定 | ESは初期化に数十秒かかる |

特に致命的なのは**ストレージのエフェメラル性**。Cloud Runはインスタンスが落ちるとデータ消滅 → 起動のたびにインデックス再構築。Cloud Storage FUSEマウントで回避は可能だが、ESが期待するPOSIX I/O性能が出ず**インデックス破損リスク**が高い。「検証が終わったら落とす」用途なら、なおさら**毎回インデックス再構築するコスト**が無駄。

---

# 有力シナリオ

| 構成 | 適性 | コスト感(セッション都度起動・終了で破棄前提) |
|---|---|---|
| **GKE Autopilot + PVC** | ◎ 本命 | Pod稼働時間課金。1-2時間/セッションなら数十円〜数百円 |
| GKE Autopilot + ECK (Elastic Cloud on K8s) | ◎ アピール最強 | 同上 + Operatorパターンの学習ボーナス |
| Compute Engine単発 | △ 起動遅い | プリエンプティブル使えば安いが手間 |
| Cloud Run | ✕ 不可 | - |
| Elastic Cloud (SaaS) | △ お金は溶ける | 学習価値が薄い(マネージドすぎ) |

**ECK (Elastic Cloud on Kubernetes) を強く推奨。** Elastic公式のOperator。`kubectl apply`でES/Kibanaが立ち上がる。ストレージ・証明書・スケーリングをOperatorが面倒見る。

転職アピール観点で:
- 「GKE上に**ECK Operator**でElasticsearchをデプロイし、multilingual-e5のembeddingをdense_vectorで投入、BM25とkNNのハイブリッド検索を実装」
- これはMLOps求人で**そのまま刺さる構成**

---

# 破綻条件

GKEに乗せても破綻するケース:

- **PVCを `prevent_destroy` 相当で守らない** → セッション破棄でPVCも消えてインデックス再構築コストを毎回払う。**Vector Searchで学んだ3層永続化の発想をES側にも適用**すべき
- **常時稼働させる** → Autopilotでも月数千円〜1万のランニング。**Cloud Schedulerで自動shutdown**を仕込む
- **ECKの学習工数を読み違える** → 素のk8s manifestでESを動かすより楽だが、初回1日は溶ける
- **GKE Autopilotのリソース最小値**: ESは1Pod最低 1 vCPU / 2GB は欲しい。Autopilotの課金粒度と噛み合うか事前確認

---

# 実務・行動への影響

**推奨アーキテクチャ(Vector Searchの3層思想をES側に転用):**

```
Layer 1 (永続・無料): GCS にスナップショット保存
  └─ ES snapshot repository → gs://...
Layer 2 (永続・低コスト): GKE PVC(retain policy)
  └─ Pod削除されてもPV残存、再起動時に即マウント
Layer 3 (セッション): GKE Pod本体 + Service
  └─ 検証終わったら kubectl delete で破棄
```

**着手手順(2-3日想定):**

**1日目:**
- `terraform/stacks/elasticsearch/` を新規追加
- ECK Operator導入(Helm or YAML)
- 単一ノードES + PVC + GCS snapshot repo

**2日目:**
- multilingual-e5 embeddingをdense_vectorとして投入するパイプライン
- KFPコンポーネント化(`ml/sync/` 配下)
- `make es-up` / `make es-down` をMakefile拡張

**3日目:**
- BM25 + kNN ハイブリッドクエリ実装
- Adapter層に `ElasticsearchLexicalAdapter` 追加
- 既存Meili adapterと並列で動かしてベンチ取得

---

# Cloud Run案を完全に捨てる必要がある理由(もう一押し)

Toshifumiさんが「すぐ落とすから」を理由にCloud Runを検討するロジックは健全。**だが落とす前提ならGKEでも同じ**(`kubectl delete namespace es-lab` で全消し)。

Cloud Runの優位性は「リクエスト駆動でスケールゼロ」だが、**ESはスケールゼロするとそもそもクラスタが死ぬ**ので優位性が機能しない。Cloud Runに無理やり乗せるのは、Vector Searchを Cloud Functions で動かそうとするのと同じ筋の悪さ。

---

# 一行サマリー

**ES on GKE Autopilot + ECK Operator + GCSスナップショット**が最適解。Cloud Runは構造的に不可。既存GKE資産が活きるので、追加学習工数は2-3日で済み、転職アピール価値は最大化される。


# 結論

**認識ズレた、すまん。** Phase 7 が既に **GKE + KServe** を含む到達ゴールなのを見落としていた。

正解は **Phase 7 内で Meilisearch → Elasticsearch on ECK へ置き換え**、もしくは **Phase 7 完成後に Phase 7.5 として ECK 移行 PR シリーズ**。Phase 8新設は不要。

---

# 理由

Phase 7 の現状を再整理:

| 構成要素 | 既存 | ES/ECK との関係 |
|---|---|---|
| GKE Deployment | ✅ 既にあり | ECK Operator 載せるだけ |
| KServe InferenceService | ✅ 既にあり | reranker 推論。ES とは独立 |
| Vertex Vector Search | ✅ 既にあり | dense vector 担当 |
| **Meilisearch** | ✅ lexical 担当 | **ここを ES に置換** |
| Vertex Feature Store | ✅ 既にあり | 特徴量。ES とは独立 |
| Cloud Composer | ✅ 既にあり | orchestration |

つまり**追加すべきは ECK Operator + ES Deployment + lexical adapter 差し替えだけ**。Phase 8 を作る理由がない。GKE 基盤は既に Phase 7 の前提なので、ECK は「既存 GKE 上の追加コンポーネント」に収まる。

前回 Phase 8 推奨したのは「GKE 導入が新規」と誤認していたから。GKE が既に Phase 7 の中核なら、ES は**Phase 7 内の lexical adapter swap** が最も筋が良い。

---

# 有力シナリオ

3案を比較:

| 案 | 内容 | 学習価値 | 工数 | 推奨度 |
|---|---|---|---|---|
| A | Phase 7 内で Meili → ES に置換(Meili削除) | △ Meili 知見が消える | 中 | ✕ |
| **B** | **Phase 7 内で ES adapter 追加・Meili と並走** | **◎ 比較学習可能** | **中** | **◎ 本命** |
| C | Phase 7.5 を新設し ES 移行 PR 群を分離 | ○ 履歴が綺麗 | 大 | △ |

**案B推奨理由:**

Port/Adapter の真価は**同一 Port に複数 Adapter を差し替え可能**なこと。Phase 7 の `LexicalSearchPort` 配下に:

```
ml/serve/adapters/lexical/
├── meilisearch_adapter.py   # 既存(Phase 3 から継承の思想)
└── elasticsearch_adapter.py # 新規(ECK on GKE)
```

`config/lexical_backend: meili | elasticsearch` で切り替え可能にすれば、**継続改善サイクルの中で A/B 比較できる教材**になる。これは Phase 7 が掲げる「継続改善 MLOps サイクル」の主旨にも合致。

---

# 破綻条件

案Bが破綻するケース:

- **Meili と ES を両方常時稼働** → GKE リソース二重消費。**セッション毎に片方だけ起動**する Makefile 制御が必須(`make lexical-up BACKEND=es` 等)
- **adapter インターフェースが Meili 仕様に引きずられている** → ES 追加時に Port 抽象が漏れていた事実が露呈する。**先に Port 再点検**が必要
- **Phase 3 の Meili 実装まで遡って改修したくなる** → Phase 間コード非共有原則を破る誘惑。**Phase 7 だけで完結**させる規律が要る
- **ECK Operator + GKE Autopilot のリソース競合** → KServe Pod / Composer worker / ES node の同居で Autopilot ノード上限に当たる可能性。事前にリソース見積もり必須

---

# 実務・行動への影響

**推奨ロードマップ(Phase 7 内 ES 統合):**

```
現在地: docs/conventions.md(命名規則ロック)
   ↓
Phase 7→1 構造修正(進行中・最優先)
   ↓
Phase 7 3層永続化 5PR(Vector Search コスト最適化)
   ↓
Phase 7 ES 統合 PR シリーズ(新規・案B本命)
   ├─ PR1: ECK Operator deployment(Terraform + Helm)
   ├─ PR2: Elasticsearch cluster manifest(PVC + GCS snapshot)
   ├─ PR3: lexical_elasticsearch_adapter 実装
   ├─ PR4: index 構築 KFP component(multilingual-e5 dense_vector 投入)
   ├─ PR5: BM25 + kNN ハイブリッドクエリ実装
   ├─ PR6: A/B 比較 evaluation(Meili vs ES on NDCG@10/Recall@K)
   └─ PR7: Makefile / Composer DAG 統合
```

**永続化方針(Vector Search 3層思想を ES に転用):**

```
Layer 1: GCS snapshot repository(prevent_destroy)
   └─ ES snapshot を gs://...es-snapshots/ に保存
Layer 2: GKE PVC retain policy
   └─ Pod 削除されても PV 残存
Layer 3: ES Pod 本体 + Service
   └─ セッション終了で kubectl delete
```

**転職アピール時の構造化:**

- 「Phase 7 で **Vertex Vector Search(dense)+ Elasticsearch on ECK(lexical/BM25)+ KServe(reranker)** のハイブリッド検索基盤を構築」
- 「Port/Adapter で Meilisearch / Elasticsearch をスワップ可能にし、**NDCG@10 / Recall@K / CTR で実測比較**」
- 「**ECK Operator + GCS snapshot + PVC retain** で 3層永続化、セッション都度起動でコスト最適化」

これは「Vertex AI だけ」「OSS だけ」のエンジニアと比較して**論点が圧倒的に厚い**。

---

# Phase 7.5 案を捨てた理由

Phase 7.5 を作る案は綺麗に見えるが:

- Phase 構成原則(コード化対象 vs 論理 Phase)に新カテゴリが入り破綻
- Phase 7 が「到達ゴール / canonical 起点」と定義されているため、**それ以降の Phase は意味的に存在しえない**
- ES 統合は「lexical adapter 差し替え」という Phase 7 内部の話であり、Phase 境界を作るほどのテーマではない

---

# 一行サマリー

**Phase 7 内で Meilisearch と並走する形で Elasticsearch on ECK adapter を追加するのが最適解。** Phase 8 も Phase 7.5 も不要。GKE + KServe が既に Phase 7 にある以上、ES/ECK は同 Phase 内の正当な拡張。Port/Adapter の比較学習価値も最大化される。