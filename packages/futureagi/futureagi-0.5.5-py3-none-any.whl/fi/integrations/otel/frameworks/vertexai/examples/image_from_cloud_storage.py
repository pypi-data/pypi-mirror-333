import os

import vertexai
from vertexai.generative_models import GenerativeModel, Part

from fi.integrations.otel import VertexAIInstrumentor, register
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

# Initialize the VertexAI instrumentor
VertexAIInstrumentor().instrument(tracer_provider=trace_provider)

vertexai.init(
    project=os.getenv("GOOGLE_CLOUD_PROJECT"),
)
model = GenerativeModel("gemini-1.5-flash")

if __name__ == "__main__":
    image_part = Part.from_uri(
        "https://fi-customer-data-dev.s3.ap-south-1.amazonaws.com/tempcust/002968fd-8b13-40e1-b936-ab65a20da091",
        mime_type="image/jpeg",
    )
    response = model.generate_content(["Describe this image", image_part])
    print(response)
