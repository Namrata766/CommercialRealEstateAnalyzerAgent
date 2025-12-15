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

"""property_regulatory_analyst_agent for finding property regulatory information using Google Search"""

from google.adk import Agent
from google.adk.tools import google_search

from . import prompt

MODEL = "gemini-2.5-pro"

property_regulatory_analyst_agent = Agent(
    model=MODEL,
    name="property_regulatory_analyst_agent",
    instruction=prompt.PROPERTY_REGULATORY_ANALYST_PROMPT,
    output_key="property_regulatory_report",
    tools=[google_search],
)
