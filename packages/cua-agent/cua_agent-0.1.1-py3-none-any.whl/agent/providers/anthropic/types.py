from enum import StrEnum


class APIProvider(StrEnum):
    """Enum for supported API providers."""

    ANTHROPIC = "anthropic"
    BEDROCK = "bedrock"
    VERTEX = "vertex"


PROVIDER_TO_DEFAULT_MODEL_NAME: dict[APIProvider, str] = {
    APIProvider.ANTHROPIC: "claude-3-7-sonnet-20250219",
    APIProvider.BEDROCK: "anthropic.claude-3-7-sonnet-20250219-v2:0",
    APIProvider.VERTEX: "claude-3-5-sonnet-v2@20241022",
}
