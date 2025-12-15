import os
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.tools import google_search

from .prompt import AGENT_INSTRUCTIONS
from .tools import bigquery_tool

load_dotenv()

MODEL = os.getenv("MODEL", "gemini-2.5-pro")

market_analysis_agent = LlmAgent(
    name="MarketAnalysisAgent",
    model=MODEL,
    instruction=AGENT_INSTRUCTIONS,
    tools=[bigquery_tool, google_search],
    output_key="market_analysis"
)
