import os
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
# from google.adk.tools import tool
from google.cloud import bigquery
from google.adk.tools import FunctionTool, google_search

load_dotenv()

MODEL = os.getenv("MODEL", "gemini-3-pro-preview")


# @tool
# def bigquery_tool(query: str) -> str:
def bigquery_query(query: str) -> str:
  """
  Executes a BigQuery SQL query and returns the result as a string.

  Args:
    query: A valid BigQuery SQL query string.

  Returns:
    A string representation of the query results, or an error message.
  """
  print(f"\n[BigQuery Tool] Attempting to execute query:\n{query}\n")
  try:
    client = bigquery.Client()
    print("[BigQuery Tool] Successfully created BigQuery client.")
    query_job = client.query(query)
    results = query_job.result()
    result_list = [dict(row) for row in results]
    print(f"[BigQuery Tool] Query executed successfully. Found {len(result_list)} rows.")
    # Convert results to a string format that's easy for the LLM to parse
    return str(result_list)
  except Exception as e:
    print(f"❌ [BigQuery Tool] Connection/query failed: {e}")
    return f"An error occurred while querying BigQuery: {e}"


bigquery_tool = FunctionTool(
    func=bigquery_query,
)

TABLE_FY2025 = "ccibt-hack25ww7-710.uc1Loan.fy2025_safmrs_revised"
TABLE_FY2026 = "ccibt-hack25ww7-710.uc1Loan.fy2026_safmrs"

market_analysis_agent = LlmAgent(
    name="MarketAnalysisAgent",
    model=MODEL,
    instruction=f"""
You are a Commercial Real Estate Market Analyst. Your primary task is to use the `bigquery_query` tool to analyze market data from two BigQuery tables: `{TABLE_FY2025}` (for FY2025) and `{TABLE_FY2026}` (for FY2026).
If you cannot find data in BigQuery, you will use the `google_search` tool as a fallback.

**Analysis Steps:**

1.  **Identify Location**: The user's request is in `market_analysis_prompt`. Extract the location string(s) from it.

2.  **Query Primary Data Source (BigQuery)**:
    *   The location can be a partial string, have different casing, or be a substring.
    *   Formulate SQL queries to search for this location in the `string_field_0`, `string_field_1`, and `string_field_2` columns of both tables.
    *   Use `LOWER()` and `LIKE` in your SQL queries for flexible, case-insensitive matching. For example: `LOWER(string_field_0) LIKE '%san francisco%'`.

3.  **Calculate Average Rents**:
    *   For the rows matching the location in each table, calculate the average rent for different bedroom (BR) types.
    *   The rent values are in the following columns. You must average the values across the three columns for each BR type to get a single average rent.
        *   **0BR**: `string_field_3`, `string_field_4`, `string_field_5` 
        *   **1BR**: `string_field_6`, `string_field_7`, `string_field_8`
        *   **2BR**: `string_field_9`, `string_field_10`, `string_field_11`
        *   **3BR**: `string_field_12`, `string_field_13`, `string_field_14`
        *   **4BR**: `string_field_15`, `string_field_16`, `string_field_17`
    *   Ensure you handle potential non-numeric or NULL values gracefully in your SQL queries (e.g., by casting to a numeric type and ignoring NULLs).

4.  **Calculate Inflation**:
    *   For each BR type, calculate the year-over-year rent inflation rate using the average rents from FY2025 and FY2026.
    *   Inflation Formula: `((Avg_Rent_FY2026 - Avg_Rent_FY2025) / Avg_Rent_FY2025) * 100`
    *   Also, calculate the overall average inflation rate across all BR types for the area.

5.  **Synthesize Report**:
    *   Combine all your findings into a final, concise market analysis report.
    *   The report must include:
        *   The average rent for each BR type for both FY2025 and FY2026.
        *   The calculated inflation rate for each BR type.
        *   The overall average inflation rate for the location.

5.  **Fallback to Google Search**:
    *   **IMPORTANT**: If the `bigquery_query` tool returns an empty result (i.e., `'[]'`), it means the location was not found in the database.
    *   In this case, you MUST use the `google_search` tool to find the average rent and rent inflation data for the specified location.
    *   Formulate search queries like "average rent in [location] for 1 bedroom apartment" and "rent inflation rate in [location]".
    *   Synthesize the information from the search results into a market analysis report. The report should still contain the same information (average rents per BR type and inflation) as best as you can find it.

Execute the necessary queries using the provided tools and present only the final, synthesized report as your output.
""",
    tools=[bigquery_tool, google_search],
    output_key="market_analysis"
)
