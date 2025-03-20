import json
import logging
import os
import warnings
from pathlib import Path

import httpx
from langchain_core.load import loads
from sven.client.api.types import AgentCompletionRequest

# Configure logging to suppress httpx logs
logging.getLogger("httpx").setLevel(logging.ERROR)

# Suppress LangChain beta warnings
warnings.filterwarnings("ignore", category=UserWarning, module="langchain_core")


class ClientAPI:
    def __init__(self, base_url: str, api_key: str = None):
        headers = {}

        # If API key is not provided, try to load from config file
        if not api_key:
            config_file = Path.home() / ".sven" / "config.json"
            if config_file.exists():
                try:
                    with open(config_file) as f:
                        config = json.load(f)
                        api_key = config.get("api_key")
                        # If base_url is not specified, use from config
                        if (
                            base_url == "https://api.swedishembedded.com"
                            and "base_url" in config
                        ):
                            base_url = config["base_url"]
                except Exception as e:
                    logging.error(f"Error loading config: {str(e)}")

        # If API key is still not found, try environment variable
        if not api_key:
            api_key = os.getenv("SWE_API_KEY")

        if api_key:
            headers["X-API-Key"] = api_key

        self.client = httpx.Client(base_url=base_url, headers=headers)

    def create_completion(self, completion: AgentCompletionRequest):
        response = self.client.post(
            "/agent/completion", json=completion.model_dump(), timeout=None
        )

        # Use a generator to process the response line by line
        def process_stream():
            event_type = None
            for line in response.iter_lines():
                if line:
                    if line.startswith("event:"):
                        event_type = line[6:].strip()
                    elif line.startswith("data:") and event_type:
                        data = line[5:].strip()
                        yield (event_type, data)

        for event_type, data in process_stream():
            if event_type == "step":
                # Suppress warnings when loading data
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    yield event_type, loads(data)
            elif event_type == "status":
                yield event_type, data
            else:
                raise ValueError(f"Unknown event type: {event_type}")
