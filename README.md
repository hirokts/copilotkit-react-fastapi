# CopilotKit + React + FastAPI

CopilotKitを使用したAIチャットアプリケーションのサンプルプロジェクト。
JWT認証によるユーザー識別とLangGraphへのユーザープロファイル注入機能を実装。

![CopilotKit Chat](copilotkit_chat.png)

## 構成

```
.
├── frontend/          # React + Vite (TypeScript)
├── runtime/           # CopilotKit Runtime (Express)
├── backend/           # LangGraph Agent (FastAPI)
└── docker-compose.yml # PostgreSQL
```

### frontend (port: 5173)

- React + TypeScript + Vite
- CopilotKit UIコンポーネント（CopilotSidebar）
- JWT Bearer Token送信

### runtime (port: 4000)

- Express + TypeScript
- CopilotKit Runtimeエンドポイント
- frontendとbackendの中継層（Authorizationヘッダー転送）

### backend (port: 8000)

- FastAPI + Python
- LangGraphエージェント
- JWT認証 & ユーザープロファイル注入
- PostgreSQL接続

## 機能

### JWT認証によるユーザープロファイル注入

1. FrontendがJWTトークンをAuthorizationヘッダーで送信
2. BackendでJWTを検証し、`user_id`を抽出
3. PostgreSQLからユーザープロファイルを取得
4. LangGraphのAgentStateに注入
5. エージェントがユーザー情報を認識してパーソナライズされた応答を生成

```
Frontend → Runtime → Backend → JWT検証 → DB取得 → LangGraph State注入
```

## セットアップ

### 1. PostgreSQL起動

```bash
docker compose up -d
```

### 2. backend

```bash
cd backend
cp .env.example .env
# .envにOPENAI_API_KEYを設定
uv sync
```

### 3. runtime

```bash
cd runtime
cp .env.example .env
npm install
```

### 4. frontend

```bash
cd frontend
cp .env.example .env
# .envにVITE_ACCESS_TOKEN（JWTトークン）を設定
npm install
```

### JWTトークン生成（開発用）

```bash
cd backend
uv run python scripts/generate_token.py
```

## 起動

4つのサービスを起動する。

```bash
# PostgreSQL（バックグラウンド）
docker compose up -d

# backend (port: 8000)
cd backend && uv run serve

# runtime (port: 4000)
cd runtime && npm run dev

# frontend (port: 5173)
cd frontend && npm run dev
```

## 環境変数

### backend/.env

```
CORS_ORIGINS=http://localhost:5173,http://localhost:4000
OPENAI_API_KEY=your-openai-api-key
JWT_SECRET=dev-secret-key
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/app
```

### runtime/.env

```
PORT=4000
AGENT_URL=http://localhost:8000/copilotkit
CORS_ORIGINS=http://localhost:5173
```

### frontend/.env

```
VITE_API_URL=http://localhost:8000
VITE_COPILOT_RUNTIME_URL=http://localhost:4000/copilotkit
VITE_ACCESS_TOKEN=your-jwt-token
```

## 通信フロー

```
frontend (5173)
    ↓ POST /copilotkit + Authorization: Bearer <JWT>
runtime (4000)
    ↓ POST /copilotkit + Authorization: Bearer <JWT>
backend (8000)
    ↓ JWT検証 → user_id抽出
    ↓ PostgreSQLからユーザープロファイル取得
    ↓ AgentStateに注入
LangGraph Agent → OpenAI API
```

## 技術スタック

- **Frontend**: React, TypeScript, Vite, CopilotKit React UI
- **Runtime**: Express, TypeScript, CopilotKit Runtime
- **Backend**: FastAPI, LangGraph, CopilotKit AG-UI, PyJWT, psycopg2
- **Database**: PostgreSQL 16
- **Infrastructure**: Docker Compose
