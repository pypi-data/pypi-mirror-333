import os
import httpx
from typing import Dict, Optional, Any

from .exceptions import AimGuardrailMissingSecrets, AimGuardrailAPIError


class AimClient:
    def __init__(self, api_key: Optional[str] = None, api_base: Optional[str] = None):
        self.api_key = api_key or os.environ.get("AIM_API_KEY")
        if not self.api_key:
            msg = "Couldn't get Aim API key. Set `AIM_API_KEY` in the environment."
            raise AimGuardrailMissingSecrets(msg)

        self.api_base = (
            api_base or os.environ.get("AIM_API_BASE") or "https://api.aim.security"
        )
        self.client = httpx.AsyncClient(timeout=30.0)

    async def detect_prompt(
        self, prompt: str, user_email: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Check content against Aim Security API using the direct detection endpoint.

        Args:
            prompt: The text to check
            user_email: Optional user email for tracking

        Returns:
            API response as dictionary
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        if user_email:
            headers["x-aim-user-email"] = user_email

        try:
            response = await self.client.post(
                f"{self.api_base}/detect", headers=headers, json={"user_prompt": prompt}
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise AimGuardrailAPIError(
                f"Aim API returned error: {e.response.status_code}"
            )
        except httpx.RequestError as e:
            raise AimGuardrailAPIError(f"Error connecting to Aim API: {str(e)}")
