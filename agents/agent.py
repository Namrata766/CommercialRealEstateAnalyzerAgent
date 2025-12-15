import os
from dotenv import load_dotenv
from google.adk.agents import LlmAgent, ParallelAgent, SequentialAgent

load_dotenv()

MODEL = os.getenv("MODEL", "gemini-3-pro-preview")

# ---------------------------------------------------------------------
# 1. PROMPT ORCHESTRATOR AGENT
# ---------------------------------------------------------------------

prompt_orchestrator_agent = LlmAgent(
    name="PromptOrchestratorAgent",
    model=MODEL,
    instruction="""
You are an underwriting workflow orchestrator.

Given a loan request and property context, generate a JSON object with:
- property_analysis_prompt
- income_analysis_prompt
- climate_risk_prompt

Each value must be a clear, focused prompt.
Do not perform analysis.
""",
    output_key="analysis_prompts"
)


# ---------------------------------------------------------------------
# 2. PARALLEL ANALYSIS AGENTS
# ---------------------------------------------------------------------

property_analysis_agent = LlmAgent(
    name="PropertyAnalysisAgent",
    model=MODEL,
    instruction="""
You will receive an object called `analysis_prompts`.

Use ONLY the value of `property_analysis_prompt`
as your analysis instruction.

Produce property underwriting insights only.
""",
    output_key="property_analysis"
)

income_analysis_agent = LlmAgent(
    name="IncomeAnalysisAgent",
    model=MODEL,
    instruction="""
You will receive an object called `analysis_prompts`.

Use ONLY the value of `income_analysis_prompt`
as your analysis instruction.

Produce income stability and risk insights.
""",
    output_key="income_analysis"
)

climate_risk_agent = LlmAgent(
    name="ClimateRiskAgent",
    model=MODEL,
    instruction="""
You will receive an object called `analysis_prompts`.

Use ONLY the value of `climate_risk_prompt`
as your analysis instruction.

Produce climate and catastrophe risk assessment.
""",
    output_key="climate_risk_analysis"
)


parallel_analysis_agent = ParallelAgent(
    name="ParallelAnalysisAgent",
    sub_agents=[
        property_analysis_agent,
        income_analysis_agent,
        climate_risk_agent,
    ],
    description="Runs property, income, and climate risk analysis in parallel."
)

# ---------------------------------------------------------------------
# 3. FINAL CREDIT MEMO AGENT
# ---------------------------------------------------------------------

final_memo_agent = LlmAgent(
    name="FinalCreditMemoAgent",
    model=MODEL,
    instruction="""
You are a senior credit committee agent.

Using the combined analysis outputs:
- Property analysis
- Income analysis
- Climate risk analysis

Produce a professional credit memo including:
- Executive summary
- Key strengths
- Key risks
- Overall risk rating (Low / Medium / High)
- Lending recommendation (Approve / Conditional / Reject)
""",
    output_key="credit_memo"
)

# ---------------------------------------------------------------------
# 4. ROOT SEQUENTIAL AGENT
# ---------------------------------------------------------------------

root_agent = SequentialAgent(
    name="CommercialRealEstateLoanAnalyzerRootAgent",
    sub_agents=[
        prompt_orchestrator_agent,
        parallel_analysis_agent,
        final_memo_agent,
    ],
    description="""
Root sequential agent that:
1. Orchestrates prompt generation
2. Executes parallel analysis agents
3. Produces final underwriting credit memo
"""
)
