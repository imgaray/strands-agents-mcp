from typing import Dict, List

from boto3 import Session
from strands import Agent
from strands.models import BedrockModel

from strands_agent_mcp.registry import AgentEntry


def build_agents() -> List[AgentEntry]:
    return [
        AgentEntry(
            name="simple-agent",
            agent=Agent(
                model=BedrockModel(
                    boto_session=Session(region_name="us-west-2")
                )
            ),
            skills=["general-knowledge"]
        )
    ]
