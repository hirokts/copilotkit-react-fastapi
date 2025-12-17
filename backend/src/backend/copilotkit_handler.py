from ag_ui.core import RunAgentInput
from ag_ui.encoder import EventEncoder
from copilotkit import LangGraphAGUIAgent
from fastapi import Request
from fastapi.responses import StreamingResponse


async def run_agent_with_state(
    agent: LangGraphAGUIAgent,
    input_data: RunAgentInput,
    request: Request,
    extra_state: dict | None = None,
) -> StreamingResponse:
    if extra_state:
        input_data.state = {**(input_data.state or {}), **extra_state}

    accept_header = request.headers.get("accept")
    encoder = EventEncoder(accept=accept_header)

    async def event_generator():
        async for event in agent.run(input_data):
            yield encoder.encode(event)

    return StreamingResponse(event_generator(), media_type=encoder.get_content_type())
