from google.cloud import bigquery
from google.adk.tools import FunctionTool

__all__ = ["bigquery_tool"]

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
    return str(result_list)
  except Exception as e:
    print(f"❌ [BigQuery Tool] Connection/query failed: {e}")
    return f"An error occurred while querying BigQuery: {e}"

bigquery_tool = FunctionTool(func=bigquery_query)
