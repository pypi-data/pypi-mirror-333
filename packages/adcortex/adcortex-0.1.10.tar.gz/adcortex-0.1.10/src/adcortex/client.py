"""Client for ADCortex API"""

import os
from typing import Optional, List
import requests
from dotenv import load_dotenv

from .types import SessionInfo, Message, Ad

# Load environment variables from .env file
load_dotenv()

# TODO: Fill up the Default Context Template
DEFAULT_CONTEXT_TEMPLATE = """

"""


class AdcortexClient:
    def __init__(
        self,
        session_info: SessionInfo,
        context_template: Optional[str] = DEFAULT_CONTEXT_TEMPLATE,
        api_key: Optional[str] = None,
    ):
        self.session_info = session_info
        self.context_template = context_template
        self.api_key = api_key or os.getenv("ADCORTEX_API_KEY")
        self.base_url = "https://adcortex.3102labs.com/ads/match"

        if not self.api_key:
            raise ValueError("ADCORTEX_API_KEY is not set and not provided")

        self.headers = {
            "Content-Type": "application/json",
            "X-API-KEY": self.api_key,
        }

    def _generate_payload(self, messages: List[Message]) -> dict:
        payload = {
            "RGUID": self.session_info.session_id,
            "session_info": self.session_info.model_dump(),
            "user_data": self.session_info.user_info.model_dump(),
            "messages": [message.model_dump() for message in messages],
            "platform": self.session_info.platform.model_dump(),
        }
        return payload

    # NOTE: @Rahul review this for functionality
    def fetch_ad(self, messages: List[Message]) -> Optional[Ad]:
        payload = self._generate_payload(messages)
        response = requests.post(self.base_url, headers=self.headers, json=payload)
        response.raise_for_status()

        # Extract the ad from the response
        ads = response.json().get("ads", [])
        if not ads:
            return None  # Return None if no ads are found

        return Ad(**ads[0])  # Unpack the ad data into the Ad constructor

    def generate_context(self, ad: Ad) -> str:
        return self.context_template.format(
            ad_title=ad.ad_title,
            ad_description=ad.ad_description,
            placement_template=ad.placement_template,
            link=ad.link,
        )
