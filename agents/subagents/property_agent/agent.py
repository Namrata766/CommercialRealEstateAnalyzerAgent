from google.adk.agents import LlmAgent
from google.adk.tools import google_search

from .prompt import AGENT_INSTRUCTIONS


__all__ = ["property_agent"]

property_agent = LlmAgent(
    name="property_agent",
    model="gemini-2.5-pro",
    instruction=AGENT_INSTRUCTIONS,
    tools=[google_search],
    output_key="property_analysis",
)
