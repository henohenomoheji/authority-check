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

---

## アプリの起動

```bash
streamlit run app.py
```

- デフォルトでは `http://localhost:8501` で起動します。
- エントリーポイントのファイル名が異なる場合は、`app.py` を実際のファイル名に置き換えてください。

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
