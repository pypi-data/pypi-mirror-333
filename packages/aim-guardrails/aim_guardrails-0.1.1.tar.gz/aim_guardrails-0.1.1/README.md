## Aim Security Guardrails for OpenAI Agents
This package provides guardrails for OpenAI agents that integrate with the Aim Security API to detect and prevent harmful content.

## Installation

```bash
# install with pip
pip install aim-guardrails

# or install with poetry
poetry add aim-guardrails
```

## Configuration
Set your Aim Security API key as an environment variable:

```bash
export AIM_API_KEY=<your-api-key>
```

## Usage

You can use the helper functions to create guardrails with specific configurations:

```python
from pydantic import BaseModel
from agents import Agent, Runner
from aim_guardrails import get_aim_input_guardrail, get_aim_output_guardrail

class MessageOutput(BaseModel):
    response: str

# Create guardrails with custom configuration
input_guardrail = get_aim_input_guardrail(
    api_key="your-custom-api-key",  # Optional: defaults to AIM_API_KEY env var
    api_base="https://your-custom-api-base.example.com",  # Optional
    user_email="user@example.com"  # Optional: for tracking
)

output_guardrail = get_aim_output_guardrail(
    api_key="your-custom-api-key",  # Optional: defaults to AIM_API_KEY env var
    api_base="https://your-custom-api-base.example.com",  # Optional
    user_email="user@example.com"  # Optional: for tracking
)

# Create an agent with the configured guardrails
agent = Agent(
    name="Customer support agent",
    instructions="You are a customer support agent. You help customers with their questions.",
    input_guardrails=[input_guardrail],
    output_guardrails=[output_guardrail],
    output_type=MessageOutput,
)

async def main():
    try:
        # This will be checked by the input guardrail
        result = await Runner.run(agent, "Hello, can you help me with my question?")
        print(f"Response: {result.final_output.response}")
    except InputGuardrailTripwireTriggered as e:
        print(f"Input guardrail triggered: {e}")
    except OutputGuardrailTripwireTriggered as e:
        print(f"Output guardrail triggered: {e}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

## How It Works

1. The input guardrail checks user messages before they're processed by the agent
2. The output guardrail checks agent responses before they're returned to the user
3. If harmful content is detected, a tripwire is triggered, raising an exception

## Creating an Aim Security Guard

1. Go to the [Aim Application](https://app.aim.security) and create a new guard
2. Configure your guard's policies in the prompt policy center
3. Get your API key from the guard's page



