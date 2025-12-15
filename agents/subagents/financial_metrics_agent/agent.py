# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""financial_metrics_agent for calculating financial metrics."""

from google.adk import Agent
from google.adk.tools import google_search

from . import prompt
from . import tools

MODEL = "gemini-2.5-pro"

google_search.bypass_multi_tools_limit = True

financial_metrics_agent = Agent(
    model=MODEL,
    name="financial_metrics_agent",
    instruction=prompt.FINANCIAL_METRICS_AGENT_PROMPT,
    output_key="financial_report",
    tools=[google_search] + tools.FINANCIAL_CALCULATION_TOOLS,
)
