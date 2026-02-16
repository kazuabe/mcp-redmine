# Redmine MCP Server

コーディングエージェント（Claude Code等）からRedmineのチケットを直接操作するためのMCP Serverです。

## 提供ツール一覧

### チケット操作

| ツール名 | 説明 |
|---------|------|
| `list_issues` | チケット一覧取得（プロジェクト、ステータス、担当者等でフィルタ可能） |
| `get_issue` | チケット詳細取得（コメント履歴、添付ファイル等の関連情報を含む） |
| `search_issues` | キーワードによるチケット検索 |
| `create_issue` | チケット新規作成 |
| `update_issue` | チケット更新（ステータス変更、担当者変更等） |
| `add_comment` | チケットへのコメント追加 |
| `bulk_update_issues` | 複数チケットの一括更新 |

### プロジェクト

| ツール名 | 説明 |
|---------|------|
| `list_projects` | プロジェクト一覧取得 |
| `get_project` | プロジェクト詳細取得 |

### マスタデータ参照

| ツール名 | 説明 |
|---------|------|
| `list_statuses` | ステータス一覧 |
| `list_trackers` | トラッカー一覧 |
| `list_priorities` | 優先度一覧 |
| `list_users` | ユーザー一覧（管理者権限が必要） |

### Wiki

| ツール名 | 説明 |
|---------|------|
| `list_wiki_pages` | プロジェクトのWikiページ一覧取得 |
| `get_wiki_page` | Wikiページの内容取得 |
| `get_ticket_rules` | チケット起票ルール取得（`TicketRules`ページ） |

> **起票ルールの運用方法**: プロジェクトのWikiに`TicketRules`ページを作成すると、エージェントがチケット作成前にルールを参照します。記載規約の詳細は [docs/wiki-convention.md](docs/wiki-convention.md) を参照してください。

## セットアップ

### 方法1: Docker（推奨）

Python や uv のインストールが不要です。

```bash
docker build -t redmine-mcp-server .
```

#### Claude Codeでの設定例（Docker）

`.claude/settings.json`:

```json
{
  "mcpServers": {
    "redmine": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "-e", "REDMINE_URL", "-e", "REDMINE_API_KEY", "redmine-mcp-server"],
      "env": {
        "REDMINE_URL": "https://your-redmine.example.com",
        "REDMINE_API_KEY": "your-api-key"
      }
    }
  }
}
```

### 方法2: ローカル実行

#### 必要環境

- Python 3.12+
- [uv](https://docs.astral.sh/uv/)
- REST APIが有効化されたRedmine環境

#### インストール

```bash
uv sync
```

#### Claude Codeでの設定例（ローカル）

`.claude/settings.json`:

```json
{
  "mcpServers": {
    "redmine": {
      "command": "uv",
      "args": ["run", "--directory", "/path/to/mcp-redmine", "python", "main.py"],
      "env": {
        "REDMINE_URL": "https://your-redmine.example.com",
        "REDMINE_API_KEY": "your-api-key"
      }
    }
  }
}
```

## 環境変数

| 変数名 | 必須 | 説明 |
|--------|------|------|
| `REDMINE_URL` | Yes | RedmineのベースURL |
| `REDMINE_API_KEY` | Yes | RedmineのAPIキー（個人設定 → APIアクセスキーから取得） |
| `MCP_TRANSPORT` | No | トランスポート種別: `stdio`（デフォルト）または `sse` |
| `MCP_HOST` | No | SSE時のホスト（デフォルト: `0.0.0.0`） |
| `MCP_PORT` | No | SSE時のポート（デフォルト: `8000`） |

## SSE トランスポート

stdio の代わりに SSE (Server-Sent Events) トランスポートで起動できます。

```bash
# SSEモードで起動
REDMINE_URL=https://your-redmine.example.com REDMINE_API_KEY=your-key MCP_TRANSPORT=sse uv run python main.py
# → http://localhost:8000/sse でアクセス可能
```

ホストやポートを変更する場合:

```bash
MCP_TRANSPORT=sse MCP_HOST=127.0.0.1 MCP_PORT=3000 uv run python main.py
```
