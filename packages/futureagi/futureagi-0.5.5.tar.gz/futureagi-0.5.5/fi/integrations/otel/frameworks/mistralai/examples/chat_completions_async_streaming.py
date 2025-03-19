import asyncio
import os

from mistralai import Mistral

from fi.integrations.otel import MistralAIInstrumentor, register
from fi.integrations.otel.fi_types import (
    EvalName,
    EvalSpanKind,
    EvalTag,
    EvalTagType,
    ProjectType,
)

# Configure trace provider with custom evaluation tags
eval_tags = [
    EvalTag(
        eval_name=EvalName.DETERMINISTIC_EVALS,
        value=EvalSpanKind.TOOL,
        type=EvalTagType.OBSERVATION_SPAN,
        config={
            "multi_choice": False,
            "choices": ["Yes", "No"],
            "rule_prompt": "Evaluate if the response is correct",
        },
        custom_eval_name="<custom_eval_name>",
    )
]

# Configure trace provider with custom evaluation tags
trace_provider = register(
    project_type=ProjectType.EXPERIMENT,
    eval_tags=eval_tags,
    project_name="FUTURE_AGI",
    project_version_name="v1",
)

# Initialize the Mistral AI instrumentor
MistralAIInstrumentor().instrument(tracer_provider=trace_provider)


async def run_async_streaming_chat_completion() -> None:
    client = Mistral(api_key=os.environ["MISTRAL_API_KEY"])
    response_stream = await client.chat.stream_async(
        model="mistral-small-latest",
        messages=[
            {
                "content": "Who won the World Cup in 2018?",
                "role": "user",
            },
        ],
    )
    async for chunk in response_stream:
        print(chunk)
    print()


if __name__ == "__main__":
    asyncio.run(run_async_streaming_chat_completion())
