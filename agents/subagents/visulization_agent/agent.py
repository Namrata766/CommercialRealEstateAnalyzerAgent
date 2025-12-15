# loan_analyzer/visualization_agent.py
from google.adk import Agent
from google.adk.tools import google_search
from agents.tools.visulization_tool import VisualizationTool

MODEL = "gemini-2.5-pro"

VISUAL_AGENT_PROMPT = """
Agent Role: visualization_agent
Tool Usage: Allowed tools: visualization.generic_create (required), google_search (optional)
Overall Goal: Given a structured analysis payload or LLM-generated insight list, construct a visual_spec
(list of chart specs) and call visualization.generic_create to render charts and optionally upload to GCS.
Inputs:
 - analysis (dict) or insights (list of key-value pairs)
 - bucket_name (optional): prefer env var if not supplied
 - expires_seconds (optional)
Output:
 - JSON with key 'visuals' containing the returned visuals metadata.
Constraints:
 - Do not invent numbers; use supplied analysis fields.
 - Keep visuals simple: line, bar, pie, scatter.
"""

visualization_agent = Agent(
    model=MODEL,
    name="visualization_agent",
    instruction=VISUAL_AGENT_PROMPT,
    output_key="visualization_output",
    tools=[google_search, VisualizationTool()],
)
