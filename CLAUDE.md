# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

Redmine REST API を MCP (Model Context Protocol) ツールとして公開するサーバー。
Claude Code 等のコーディングエージェントが stdio 経由で Redmine を操作できる。

## Directory Structure

```
mcp-redmine/
├── docs/                  # 要求・仕様・設計ドキュメント
│   ├── requirements.md    #   機能要件と改善候補の整理
│   ├── architecture.md    #   アーキテクチャ詳細
│   └── wiki-convention.md #   Wiki起票ルール記載規約
├── scratch/               # 一時的な開発用ファイル（gitignored）
│   └── .gitkeep           #   実験コード・メモ・ドラフト等に使用
├── src/redmine_mcp/       # プロダクションコード
│   ├── server.py          #   FastMCP インスタンス + ツール登録
│   ├── client.py          #   RedmineClient（httpx ラッパー）
│   └── tools/             #   ツールモジュール群
│       ├── issues.py      #     チケット操作
│       ├── projects.py    #     プロジェクト操作
│       ├── master.py      #     マスタデータ参照
│       └── wiki.py        #     Wiki操作・起票ルール参照
├── tests/                 # テスト
├── main.py                # エントリーポイント
└── pyproject.toml         # プロジェクト設定
```

### ディレクトリの使い分け

- **docs/**: 要件定義・仕様・設計を整理する場所。新機能を検討する際はまず `docs/requirements.md` に要件を追記する。
- **scratch/**: 一時的な実験・メモ・ドラフトの置き場。Git にコミットされない。自由に使って良い。
- **src/**: プロダクションコード。変更は必ずテストを伴う。
- **tests/**: テストコード。

## Commands

```bash
# Install dependencies
uv sync

# Run tests
REDMINE_URL=https://redmine.example.com REDMINE_API_KEY=test-key uv run pytest tests/ -v

# Run a single test
REDMINE_URL=https://redmine.example.com REDMINE_API_KEY=test-key uv run pytest tests/test_client.py::test_get -v

# Start the MCP server
REDMINE_URL=https://your-redmine.example.com REDMINE_API_KEY=your-key uv run python main.py

# Test with MCP Inspector
REDMINE_URL=https://your-redmine.example.com REDMINE_API_KEY=your-key mcp dev main.py
```

## Architecture Overview

詳細は [docs/architecture.md](docs/architecture.md) を参照。

- **Entry point**: `main.py` → `server.py` の FastMCP を stdio で起動
- **Server**: `server.py` が RedmineClient とツールモジュールを組み立て
- **Client**: `client.py` が httpx で Redmine API と通信
- **Tools**: 各モジュールが `register(mcp, client)` パターンでツールを登録

### Adding a new tool

1. 適切なツールモジュール内の `register()` に `@mcp.tool()` 付き非同期関数を追加
2. 新モジュールの場合は `register()` を定義し `server.py` から呼び出す
3. 詳細は [docs/architecture.md](docs/architecture.md) のツール追加手順を参照

## Configuration

Environment variables (required at startup):
- `REDMINE_URL` — Base URL of the Redmine instance
- `REDMINE_API_KEY` — API key for authentication

Optional (transport):
- `MCP_TRANSPORT` — `stdio`（デフォルト）または `sse`
- `MCP_HOST` — SSE 時のホスト（デフォルト: `0.0.0.0`）
- `MCP_PORT` — SSE 時のポート（デフォルト: `8000`）
