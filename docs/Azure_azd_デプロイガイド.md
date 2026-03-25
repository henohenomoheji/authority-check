# Azure デプロイガイド（`azd` / 組み込み Python ランタイム）

このドキュメントは、`authority-check`（Streamlit アプリ）を **コンテナなし**で Azure にデプロイするための手順です。  
`Azure Developer CLI (azd)` と **Azure App Service の組み込み Python ランタイム**を使う前提で説明します。

---

## 1. この構成の考え方

前回の「Container Apps + Docker」ではなく、今回は次の構成を採用します。

- 実行基盤: **Azure App Service (Linux)**
- ランタイム: **組み込み Python ランタイム**（Oryx によるビルド）
- デプロイ方式: `azd` で IaC + アプリ配備

### メリット

- Dockerfile 不要で運用がシンプル
- Python アプリとして直接デプロイできる
- `requirements.txt` ベースで依存関係を自動インストール可能

### 注意点（Streamlit 固有）

App Service の既定起動（gunicorn）では Streamlit は動かないため、
**起動コマンド（Startup Command）を明示**します。

---

## 2. 事前準備

- Azure サブスクリプション
- ローカルに以下をインストール
  - Azure CLI (`az`)
  - Azure Developer CLI (`azd`)

ログイン:

```bash
az login
azd auth login
```

---

## 3. リポジトリ内で用意するファイル

最低限、次の構成を想定します。

```text
authority-check/
├── app.py
├── requirements.txt
├── azure.yaml
└── infra/
    ├── main.bicep
    └── main.parameters.json
```

> この方式では `Dockerfile` は不要です。

---

## 4. `azure.yaml` の設定例（App Service / Python）

`azure.yaml` は次のように設定します。

```yaml
name: authority-check
metadata:
  template: authority-check-appservice@0.0.1

services:
  web:
    project: .
    language: python
    host: appservice
```

ポイント:

- `host: appservice` を指定する
- `language: python` で組み込み Python ランタイムを利用する

---

## 5. インフラ（`infra/`）で必要な要素

Bicep では少なくとも以下を定義します。

- App Service Plan（Linux）
- Web App（Linux, Python ランタイム）
- 必要に応じて Application Insights / Log Analytics

加えて、Web App のアプリ設定として以下を入れてください。

- `SCM_DO_BUILD_DURING_DEPLOYMENT=true`（Oryx ビルドを有効化）
- `ENABLE_ORYX_BUILD=true`
- （必要に応じて）Entra ID の設定値

---

## 6. Streamlit の起動コマンド設定（重要）

App Service の Web App に Startup Command を設定します。

```bash
python -m streamlit run app.py --server.port $PORT --server.address 0.0.0.0
```

推奨オプションを含める場合:

```bash
python -m streamlit run app.py --server.port $PORT --server.address 0.0.0.0 --server.headless true
```

> `PORT` は App Service 側が割り当てるため固定値（8501）ではなく `$PORT` を使います。

---

## 7. 初回デプロイ手順

### Step 1) `azd init`

```bash
azd init
```

既存 `azure.yaml` を利用して、環境（例: `dev`）を作成します。

### Step 2) 環境値を設定

```bash
azd env set AZURE_LOCATION japaneast
```

必要に応じて、Entra ID 用の値も環境に設定します。

```bash
azd env set ENTRA_CLIENT_ID <your-client-id>
azd env set ENTRA_TENANT_ID <your-tenant-id>
```

### Step 3) インフラ作成

```bash
azd provision
```

App Service Plan / Web App などが作成されます。

### Step 4) アプリ配備

```bash
azd deploy
```

`requirements.txt` をもとに依存が解決され、アプリが反映されます。

### まとめて実行

```bash
azd up
```

---

## 8. デプロイ後の確認

```bash
azd env get-values
```

出力された Web App の URL にアクセスし、以下を確認します。

- Streamlit 画面が表示される
- ログインボタン（Microsoft Entra）で認証導線が動く
- ページ遷移（PageA / PageB / PageC）が機能する

---

## 9. 運用コマンド

```bash
# コード変更のみの再反映
azd deploy

# インフラ変更の反映
azd provision

# 環境削除
azd down
```

---

## 10. Entra ID 利用時の注意点

`st.login("microsoft")` を使う場合は次を必ず合わせます。

- App Registration の Redirect URI を本番 URL に合わせる
- クライアント ID / シークレットはコード直書きせず、環境変数で管理
- 複数環境（dev/stg/prod）で URI を分ける

---

## 11. よくあるハマりどころ

- **起動するが 502/503 になる**  
  Startup Command 未設定、または `--server.port $PORT` が漏れている可能性があります。
- **依存関係エラー**  
  `requirements.txt` の不足/競合を確認します。
- **ログイン失敗**  
  Redirect URI と公開 URL の不一致を確認します。

---

## 12. 最短コマンド（チートシート）

```bash
az login
azd auth login
azd init
azd env set AZURE_LOCATION japaneast
azd up
```

以上で、組み込み Python ランタイムを使った Azure デプロイの基本フローを実行できます。
