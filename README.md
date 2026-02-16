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

| 変数名 | 説明 |
|--------|------|
| `REDMINE_URL` | RedmineのベースURL |
| `REDMINE_API_KEY` | RedmineのAPIキー（個人設定 → APIアクセスキーから取得） |
