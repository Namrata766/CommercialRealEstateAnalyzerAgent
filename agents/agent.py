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

Given a loan request and property context, extract key information and generate analysis prompts.

1.  **Extract Key Data**: From the user's request, extract the following fields. If a value is not present, use `null`.
    *   `property_address` (string)
    *   `property_type` (string, e.g., "Multifamily", "Office")
    *   `gross_rental_income` (float)
    *   `operating_expenses` (float)
    *   `purchase_price` (float)
    *   `loan_amount` (float)
    *   `annual_debt_service` (float)

2.  **Generate Prompts**: Create clear, focused prompts for the following analysis areas.
    *   `property_analysis_prompt`
    *   `market_analysis_prompt`
    *   `risk_analysis_prompt`
    *   `regulatory_analysis_prompt`

Return a single JSON object containing all extracted data and generated prompts. Do not perform the analysis yourself.
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


market_analysis_agent = LlmAgent(
    name="MarketAnalysisAgent",
    model=MODEL,
    instruction="""
You will receive an object called `analysis_prompts`.

Use ONLY the value of `market_analysis_prompt`
as your analysis instruction.

Produce income stability and risk insights.
""",
    output_key="market_analysis"
)

from agents.subagents.financial_metrics_agent import financial_metrics_agent
from agents.subagents.demographic_details_agent import demographic_details_agent
from agents.subagents.regulatory_agent import property_regulatory_analyst_agent 
from agents.subagents.risk_analysis_agent import risk_analysis_agent
 
parallel_analysis_agent = ParallelAgent(
    name="ParallelAnalysisAgent",
    sub_agents=[
        property_analysis_agent,
        market_analysis_agent,
        property_regulatory_analyst_agent,
        financial_metrics_agent,
        demographic_details_agent,
    ],
    description="Runs property, market, risk, regulatory, and financial analysis in parallel."
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
- property analysis
- market analysis
- regulatory analysis
- financial analysis
- demographic analysis
- risk and stress test analysis

Produce a professional credit memo including:
- Executive summary
- Key strengths
- Key risks
- Key Financial Metrics (NOI, DSCR, LTV, Cap Rate)
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
        risk_analysis_agent,
        final_memo_agent,
    ],
    description="""
Root sequential agent that:
1. Orchestrates prompt generation
2. Executes parallel analysis agents
3. Produces final underwriting credit memo
"""
)
