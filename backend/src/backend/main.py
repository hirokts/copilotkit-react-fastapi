import random

from dotenv import load_dotenv

load_dotenv()

from ag_ui.core import RunAgentInput
from ag_ui.encoder import EventEncoder
from copilotkit import LangGraphAGUIAgent
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from backend.agent import graph, joke_graph
from backend.auth import verify_jwt
from backend.config import settings
from backend.database import init_db
from backend.services import get_user_profile

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBearer()

agents = {
    "sample_agent": LangGraphAGUIAgent(
        name="sample_agent",
        description="A helpful assistant agent.",
        graph=graph,
    ),
    "joke_agent": LangGraphAGUIAgent(
        name="joke_agent",
        description="A comedian agent that tells jokes.",
        graph=joke_graph,
    ),
}


@app.on_event("startup")
def startup_event():
    init_db()


@app.post("/copilotkit/{agent_name}")
async def copilotkit_endpoint(
    agent_name: str,
    input_data: RunAgentInput,
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    agent = agents.get(agent_name)
    if not agent:
        raise HTTPException(status_code=404, detail=f"Agent '{agent_name}' not found")

    user_id = verify_jwt(credentials.credentials)
    user_profile = get_user_profile(user_id)

    input_data.state = {
        **(input_data.state or {}),
        "user_id": user_id,
        "user_profile": user_profile,
    }

    accept_header = request.headers.get("accept")
    encoder = EventEncoder(accept=accept_header)

    async def event_generator():
        async for event in agent.run(input_data):
            yield encoder.encode(event)

    return StreamingResponse(event_generator(), media_type=encoder.get_content_type())


@app.get("/copilotkit/{agent_name}/health")
def copilotkit_health(agent_name: str):
    agent = agents.get(agent_name)
    if not agent:
        raise HTTPException(status_code=404, detail=f"Agent '{agent_name}' not found")
    return {"status": "ok", "agent": {"name": agent.name}}


@app.get("/copilotkit/agents")
def list_agents():
    return {
        "agents": [
            {"name": agent.name, "description": agent.description}
            for agent in agents.values()
        ]
    }


GREETINGS = [
    "こんにちは、今日もがんばりましょう",
    "好きな料理はなんですか？",
    "いい天気ですね！",
    "最近なにかおもしろいことありました？",
    "お元気ですか？",
    "今日のご予定は？",
    "コーヒーでも飲みませんか？",
    "素敵な一日になりますように",
    "何かお手伝いできることはありますか？",
    "今日も一日お疲れさまです",
]


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/greetings")
def greetings():
    return {"message": random.choice(GREETINGS)}
