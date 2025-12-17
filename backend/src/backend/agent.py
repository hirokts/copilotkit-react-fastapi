import random
from typing import Any

from copilotkit import CopilotKitState
from langchain.tools import tool
from langchain_core.messages import AIMessage, SystemMessage
from langchain_core.runnables import RunnableConfig
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode
from langgraph.types import Command
from typing_extensions import Literal


class AgentState(CopilotKitState):
    tools: list[Any]
    user_id: str | None = None
    user_profile: dict | None = None


@tool
def get_weather(location: str):
    """Get the weather for a given location."""
    return f"The weather in {location} is sunny, 22°C."


tools = [get_weather]

MOCK_RESPONSES = [
    "こんにちは！何かお手伝いできることはありますか？",
    "了解しました。他に質問はありますか？",
    "それは興味深いですね。もう少し詳しく教えていただけますか？",
    "お役に立てて嬉しいです！",
    "なるほど、理解しました。",
]


async def mock_chat_node(
    state: AgentState, config: RunnableConfig
) -> Command[Literal["__end__"]]:
    response = AIMessage(content=random.choice(MOCK_RESPONSES))
    return Command(goto="__end__", update={"messages": response})


async def chat_node(
    state: AgentState, config: RunnableConfig
) -> Command[Literal["tool_node", "__end__"]]:
    model = ChatOpenAI(model="gpt-4o")
    fe_tools = state.get("tools", [])
    model_with_tools = model.bind_tools([*fe_tools, *tools])

    user_profile = state.get("user_profile")
    if user_profile:
        system_content = f"You are a helpful assistant. User info: {user_profile}"
    else:
        system_content = "You are a helpful assistant."
    system_message = SystemMessage(content=system_content)

    response = await model_with_tools.ainvoke(
        [system_message, *state["messages"]],
        config,
    )

    if response.tool_calls:
        return Command(goto="tool_node", update={"messages": response})

    return Command(goto="__end__", update={"messages": response})


workflow = StateGraph(AgentState)
workflow.add_node("chat_node", chat_node)
workflow.add_node("tool_node", ToolNode(tools=tools))
workflow.add_edge("tool_node", "chat_node")
workflow.set_entry_point("chat_node")

checkpointer = MemorySaver()
graph = workflow.compile(checkpointer=checkpointer)

mock_workflow = StateGraph(AgentState)
mock_workflow.add_node("chat_node", mock_chat_node)
mock_workflow.set_entry_point("chat_node")

mock_checkpointer = MemorySaver()
mock_graph = mock_workflow.compile(checkpointer=mock_checkpointer)


async def joke_chat_node(
    state: AgentState, config: RunnableConfig
) -> Command[Literal["__end__"]]:
    model = ChatOpenAI(model="gpt-4o")

    user_profile = state.get("user_profile")
    user_name = user_profile.get("name", "ゲスト") if user_profile else "ゲスト"
    system_message = SystemMessage(
        content=f"あなたは面白いジョークを言うコメディアンです。{user_name}さんを笑わせてください。"
    )

    response = await model.ainvoke(
        [system_message, *state["messages"]],
        config,
    )

    return Command(goto="__end__", update={"messages": response})


joke_workflow = StateGraph(AgentState)
joke_workflow.add_node("chat_node", joke_chat_node)
joke_workflow.set_entry_point("chat_node")

joke_checkpointer = MemorySaver()
joke_graph = joke_workflow.compile(checkpointer=joke_checkpointer)
