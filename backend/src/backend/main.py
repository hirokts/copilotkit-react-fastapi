import random

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.config import settings

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
