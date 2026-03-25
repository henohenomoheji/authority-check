# devcontainer で `az` / `azd` を使うための素案

この素案は、`authority-check` の開発環境を devcontainer 化し、
**Azure CLI (`az`)** と **Azure Developer CLI (`azd`)** を利用できるようにするための最小構成です。

## 1. 追加ファイル

```text
.devcontainer/
  ├── devcontainer.json
  └── Dockerfile
```

## 2. 設計方針

- ベースイメージは `mcr.microsoft.com/devcontainers/python:1-3.11-bullseye`
- `Dockerfile` 内で `az` と `azd` をインストール
- `~/.azure` をコンテナにマウントし、ローカルの認証情報を再利用
- `postCreateCommand` で `requirements.txt` をインストール
- `postStartCommand` で `az` / `azd` のバージョン確認

## 3. `devcontainer.json` のポイント

- VS Code 拡張（Python / Bicep / Azure 系）を初期導入
- 既定インタプリタを `/usr/local/bin/python` に固定
- `mounts` で `${localEnv:HOME}/.azure` を `/home/vscode/.azure` にバインド

> 補足: セキュリティ観点で共有を避けたい場合は、`mounts` を削除し、コンテナ内で `az login` を実施。

## 4. `Dockerfile` のポイント

- Microsoft の apt リポジトリを追加して `azure-cli` をインストール
- 公式インストールスクリプトで `azd` を導入

## 5. 想定利用手順

1. VS Code で `authority-check` を開く
2. **Reopen in Container** を実行
3. ターミナルで以下を確認

```bash
az version
azd version
```

4. 必要に応じて認証

```bash
az login
azd auth login
```

## 6. 今後の拡張案

- `postCreateCommand` に `pre-commit` や lint セットアップを追加
- `azd` で使う環境変数テンプレート（`.env.example`）を整備
- CI と同じ Python バージョンへ厳密固定
