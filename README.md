# CopilotKit + React + FastAPI

CopilotKitを使用したAIチャットアプリケーションのサンプルプロジェクト。

## 構成

```
.
├── frontend/   # React + Vite (TypeScript)
├── runtime/    # CopilotKit Runtime (Express)
└── backend/    # LangGraph Agent (FastAPI)
```

### frontend (port: 5173)

- React + TypeScript + Vite
- CopilotKit UIコンポーネント（CopilotSidebar）

### runtime (port: 4000)

- Express + TypeScript
- CopilotKit Runtimeエンドポイント
- frontendとbackendの中継層

### backend (port: 8000)

- FastAPI + Python
- LangGraphエージェント
- CopilotKit AG-UI統合

## セットアップ

### 1. backend

```bash
cd backend
cp .env.example .env
# .envにOPENAI_API_KEYを設定
uv sync
```

### 2. runtime

```bash
cd runtime
cp .env.example .env
npm install
```

### 3. frontend

```bash
cd frontend
cp .env.example .env
npm install
```

## 起動

3つのサーバーを別々のターミナルで起動する。

```bash
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
```

## 通信フロー

```
frontend (5173)
    ↓ /copilotkit
runtime (4000)
    ↓ /copilotkit
backend (8000)
    ↓
LangGraph Agent → OpenAI API
```
