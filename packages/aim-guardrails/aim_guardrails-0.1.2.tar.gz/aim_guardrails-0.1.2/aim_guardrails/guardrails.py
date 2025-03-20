from typing import Any, Dict, List, Optional, Union, Callable

from pydantic import BaseModel
from agents import (
    Agent,
    GuardrailFunctionOutput,
    RunContextWrapper,
    TResponseInputItem,
    input_guardrail,
    output_guardrail,
)

from .utils import AimClient


class AimDetectionResult(BaseModel):
    """Model for Aim detection results."""

    detected: bool
    detection_message: str | None = None
    details: Dict[str, Any]
    entities: Optional[List[Dict[str, Any]]] = None
    analysis_time_ms: Optional[int] = None


async def aim_input_guardrail(
    ctx: RunContextWrapper[None],
    agent: Agent,
    input: Union[str, List[TResponseInputItem]],
    api_key: Optional[str] = None,
    api_base: Optional[str] = None,
    user_email: Optional[str] = None,
) -> GuardrailFunctionOutput:
    """
    Input guardrail that checks user input against Aim Security API.

    Args:
        ctx: Run context wrapper
        agent: The agent being guarded
        input: User input to check
        api_key: Optional Aim API key (defaults to AIM_API_KEY env var)
        api_base: Optional Aim API base URL (defaults to AIM_API_BASE env var or https://api.aim.security)
        user_email: Optional user email for tracking

    Returns:
        GuardrailFunctionOutput with detection results
    """
    aim_client = AimClient(api_key=api_key, api_base=api_base)

    # Extract content from input - get the last message
    content = ""
    if isinstance(input, str):
        content = input
    else:
        # Handle complex input types - get the last user message
        for item in reversed(input):
            if (
                hasattr(item, "content")
                and hasattr(item, "role")
                and item.role == "user"
            ):
                content = item.content
                break
            elif isinstance(item, str):
                content = item
                break

    # Call Aim API with direct detection endpoint
    result = await aim_client.detect_prompt(content, user_email=user_email)

    # Create detection result
    detection_result = AimDetectionResult(
        detected=result.get("detected", False),
        detection_message=result.get(
            "detection_message", "Content violates security policies"
        ),
        details=result.get("details", {}),
        entities=result.get("entities", []),
        analysis_time_ms=result.get("analysis_time_ms"),
    )

    return GuardrailFunctionOutput(
        output_info=detection_result,
        tripwire_triggered=detection_result.detected,
    )


def get_aim_input_guardrail(
    api_key: Optional[str] = None,
    api_base: Optional[str] = None,
    user_email: Optional[str] = None,
) -> Callable:
    """
    Creates an input guardrail function with the specified parameters.

    Args:
        api_key: Optional Aim API key (defaults to AIM_API_KEY env var)
        api_base: Optional Aim API base URL (defaults to AIM_API_BASE env var or https://api.aim.security)
        user_email: Optional user email for tracking

    Returns:
        A configured input guardrail function
    """

    # Create a new function that's properly decorated
    @input_guardrail
    async def configured_input_guardrail(
        ctx: RunContextWrapper[None],
        agent: Agent,
        input: Union[str, List[TResponseInputItem]],
    ) -> GuardrailFunctionOutput:
        return await aim_input_guardrail(
            ctx, agent, input, api_key=api_key, api_base=api_base, user_email=user_email
        )

    return configured_input_guardrail


async def aim_output_guardrail(
    ctx: RunContextWrapper,
    agent: Agent,
    output: Any,
    api_key: Optional[str] = None,
    api_base: Optional[str] = None,
    user_email: Optional[str] = None,
) -> GuardrailFunctionOutput:
    """
    Output guardrail that checks agent output against Aim Security API.

    Args:
        ctx: Run context wrapper
        agent: The agent being guarded
        output: Agent output to check
        api_key: Optional Aim API key (defaults to AIM_API_KEY env var)
        api_base: Optional Aim API base URL (defaults to AIM_API_BASE env var or https://api.aim.security)
        user_email: Optional user email for tracking

    Returns:
        GuardrailFunctionOutput with detection results
    """
    aim_client = AimClient(api_key=api_key, api_base=api_base)

    # Extract content from output
    content = ""
    if hasattr(output, "response"):
        content = output.response
    elif hasattr(output, "content"):
        content = output.content
    elif isinstance(output, str):
        content = output
    else:
        # Best effort to convert to string
        content = str(output)

    # Call Aim API with direct detection endpoint
    result = await aim_client.detect_prompt(content, user_email=user_email)

    # Create detection result
    detection_result = AimDetectionResult(
        detected=result.get("detected", False),
        detection_message=result.get("detection_message", None),
        details=result.get("details", {}),
        entities=result.get("entities", []),
        analysis_time_ms=result.get("analysis_time_ms"),
    )

    return GuardrailFunctionOutput(
        output_info=detection_result,
        tripwire_triggered=detection_result.detected,
    )


def get_aim_output_guardrail(
    api_key: Optional[str] = None,
    api_base: Optional[str] = None,
    user_email: Optional[str] = None,
) -> Callable:
    """
    Creates an output guardrail function with the specified parameters.

    Args:
        api_key: Optional Aim API key (defaults to AIM_API_KEY env var)
        api_base: Optional Aim API base URL (defaults to AIM_API_BASE env var or https://api.aim.security)
        user_email: Optional user email for tracking

    Returns:
        A configured output guardrail function
    """

    # Create a new function that's properly decorated
    @output_guardrail
    async def configured_output_guardrail(
        ctx: RunContextWrapper, agent: Agent, output: Any
    ) -> GuardrailFunctionOutput:
        return await aim_output_guardrail(
            ctx,
            agent,
            output,
            api_key=api_key,
            api_base=api_base,
            user_email=user_email,
        )

    return configured_output_guardrail
