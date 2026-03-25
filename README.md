# Authority Check (Streamlit App)

`authority-check` は、権限・承認の確認を行うための **Streamlit アプリ**です。  
この README では、ローカルでの起動手順と開発時の基本的な使い方をまとめています。

---

## 前提環境

- Python 3.9 以上（推奨: 3.10+）
- `pip` または `uv` / `poetry` などのパッケージマネージャ

---

## セットアップ

### 1) リポジトリを取得

```bash
git clone <YOUR_REPOSITORY_URL>
cd authority-check
```

### 2) 仮想環境を作成（任意だが推奨）

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3) 依存関係をインストール

`requirements.txt` がある場合:

```bash
pip install -r requirements.txt
```

`requirements.txt` がまだ無い場合は最低限以下をインストール:

```bash
pip install streamlit
```

### 4) 環境変数を `.env` に設定

```bash
cp .env.example .env
```

`.env` に以下を設定してください。

```dotenv
AZURE_OPENAI_API_KEY=your_azure_openai_key
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com
AZURE_OPENAI_DEPLOYMENT_NAME=your-vision-deployment
SSL_CERT_FILE=/absolute/path/to/certifi/cacert.pem
VISION_TIMEOUT_SEC=10
MAX_IMAGE_SIZE_MB=10
```

`SSL_CERT_FILE` は、Python 実行時に `SSLCertVerificationError` が出る環境向けの設定です。`certifi` をインストールしたうえで、次のコマンドで確認したパスを設定してください。

```bash
python -c "import certifi; print(certifi.where())"
```

---

## アプリの起動

```bash
streamlit run app.py
```

- デフォルトでは `http://localhost:8501` で起動します。
- エントリーポイントのファイル名が異なる場合は、`app.py` を実際のファイル名に置き換えてください。
- 画像解釈機能の詳細な実行手順は [docs/画像解釈機能_実行手順書.md](/Users/kanemotosatoko/Documents/workspace/authority-check/docs/画像解釈機能_実行手順書.md) を参照してください。

---

## 開発のポイント

- UI 変更時は、`streamlit run ...` で動作を確認しながら実装してください。
- セキュリティ・権限周りのロジックは、入出力と判定条件がわかるように関数を分割することを推奨します。
- 機密情報（API キー等）は `.env` や環境変数で管理し、コードへ直書きしないでください。

---


## Azure デプロイ（azd）

Azure へ `azd` で **組み込み Python ランタイム（App Service）** デプロイする場合は、以下ドキュメントを参照してください。

- [Azure デプロイガイド（azd 利用）](docs/Azure_azd_デプロイガイド.md)

---

## よく使うコマンド

```bash
# Streamlit 起動
streamlit run app.py

# Streamlit バージョン確認
streamlit --version
```

---

## ライセンス

必要に応じて追記してください（例: MIT License）。
