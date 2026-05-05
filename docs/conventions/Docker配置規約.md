# Docker 配置規約

## 目的

- Dockerfile の置き場所を揃える
- CI / 運用スクリプトの参照先を固定する
- 旧形式の混在を抑える

---

## 標準配置

- Service 用: `infra/run/services/<service_name>/Dockerfile`
- Job 用: `infra/run/jobs/<job_name>/Dockerfile`

`<service_name>` / `<job_name>` は `snake_case` を使う。

---

## 命名ルール

- ファイル名は原則 `Dockerfile` 固定
- `Dockerfile.<suffix>` は legacy 扱い
- legacy を使う場合は、対象フェーズと理由を明記する

---

## チェック

ルートで以下を実行:

```bash
python3 tools/check_docker_layout.py
```

実際の required パスや例外ルールは、上記スクリプト実装を正とする。

---

## 運用メモ

- 配置変更が発生したら、まず `tools/check_docker_layout.py` を更新
- この文書は原則「方針のみ」を保持する
