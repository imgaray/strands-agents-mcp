from boto3 import Session
from strands import Agent
from strands.models import BedrockModel

from strands_agent_mcp.registry import Registry


def register_plugin(registry: Registry) -> None:
    registry.register("simple-agent", Agent(
        model=BedrockModel(boto_session=Session(region_name="us-west-2")))
    )
