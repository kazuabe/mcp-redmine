# Architecture

## Overview

MCP (Model Context Protocol) サーバーとして、Redmine REST API の操作をツールとして公開する。
Claude Code などのコーディングエージェントが stdio トランスポート経由で Redmine のチケット・プロジェクト・マスタデータを読み書きできる。

## コンポーネント構成

```
main.py                         # エントリーポイント（stdio transport で起動）
src/redmine_mcp/
├── server.py                   # FastMCP インスタンス生成 + ツール登録
├── client.py                   # RedmineClient（httpx ラッパー）
└── tools/
    ├── issues.py               # チケット操作ツール
    ├── projects.py             # プロジェクト操作ツール
    ├── master.py               # マスタデータ参照ツール
    └── wiki.py                 # Wiki 操作ツール
```

## データフロー

```
                         ┌─ stdio ─┐
Claude Code / MCP Client ┤         ├▶  FastMCP Server  ──▶  RedmineClient  ──HTTP──▶  Redmine API
                         └─ SSE  ──┘
```

トランスポートは環境変数 `MCP_TRANSPORT` で切り替え（デフォルト: `stdio`）。

## 主要コンポーネント

### エントリーポイント (`main.py`)

`server.py` から FastMCP インスタンスをインポートし、`MCP_TRANSPORT` 環境変数に応じて stdio または SSE トランスポートで起動する。

### サーバー組み立て (`src/redmine_mcp/server.py`)

- FastMCP インスタンスの生成
- RedmineClient の単一インスタンス生成
- 各ツールモジュールの `register(mcp, client)` を呼び出してツールを登録

### API クライアント (`src/redmine_mcp/client.py`)

- `RedmineClient` クラスが httpx による非同期 HTTP メソッド (`get/post/put/delete`) を提供
- 環境変数 `REDMINE_URL` と `REDMINE_API_KEY` をコンストラクタで読み取り
- `X-Redmine-API-Key` ヘッダーを自動付与

### ツールモジュール (`src/redmine_mcp/tools/`)

各モジュールは `register(mcp, client)` 関数をエクスポートし、共有の client をクロージャで受け取る `@mcp.tool()` デコレータ付き非同期関数を定義する。

| モジュール | ツール |
|-----------|--------|
| `issues.py` | list, get, search, create, update, comment, bulk update |
| `projects.py` | list, get |
| `master.py` | statuses, trackers, priorities, users |
| `wiki.py` | list pages, get page, get ticket rules |

## ツール追加手順

1. 適切なツールモジュール内の `register()` 関数に `@mcp.tool()` デコレータ付き非同期関数を追加
2. 関数はクロージャ経由で共有の `RedmineClient` を受け取る
3. 新しいツールモジュールを作る場合は `register()` 関数を定義し、`server.py` から呼び出す

## 環境変数

| 変数名 | 必須 | 説明 |
|--------|------|------|
| `REDMINE_URL` | Yes | Redmine のベース URL |
| `REDMINE_API_KEY` | Yes | API 認証キー |
| `MCP_TRANSPORT` | No | トランスポート種別: `stdio`（デフォルト）または `sse` |
| `MCP_HOST` | No | SSE 時のホスト（デフォルト: `0.0.0.0`） |
| `MCP_PORT` | No | SSE 時のポート（デフォルト: `8000`） |
