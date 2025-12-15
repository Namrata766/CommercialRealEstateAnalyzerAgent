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

"""Tools for financial calculations."""

from google.adk.tools import FunctionTool as Tool


def calculate_noi(gross_rental_income: float, operating_expenses: float) -> float:
    """Calculates Net Operating Income (NOI)."""
    if gross_rental_income is None or operating_expenses is None:
        raise ValueError("Gross rental income and operating expenses are required.")
    return gross_rental_income - operating_expenses


def calculate_dscr(net_operating_income: float, annual_debt_service: float) -> float:
    """Calculates Debt Service Coverage Ratio (DSCR)."""
    if net_operating_income is None or annual_debt_service is None:
        raise ValueError("Net operating income and annual debt service are required.")
    if annual_debt_service == 0:
        raise ValueError("Annual debt service cannot be zero for DSCR calculation.")
    return round(net_operating_income / annual_debt_service, 2)


def calculate_ltv(loan_amount: float, purchase_price: float) -> float:
    """Calculates Loan-to-Value (LTV) ratio as a percentage."""
    if loan_amount is None or purchase_price is None:
        raise ValueError("Loan amount and purchase price are required.")
    if purchase_price == 0:
        raise ValueError("Purchase price cannot be zero for LTV calculation.")
    return round((loan_amount / purchase_price) * 100, 2)


def calculate_cap_rate(net_operating_income: float, purchase_price: float) -> float:
    """Calculates Capitalization Rate (Cap Rate) as a percentage."""
    if net_operating_income is None or purchase_price is None:
        raise ValueError("Net operating income and purchase price are required.")
    if purchase_price == 0:
        raise ValueError("Purchase price cannot be zero for Cap Rate calculation.")
    return round((net_operating_income / purchase_price) * 100, 2)


calculate_noi_tool = Tool(
    func=calculate_noi,
)

calculate_dscr_tool = Tool(
    func=calculate_dscr,
)

calculate_ltv_tool = Tool(
    func=calculate_ltv,
)

calculate_cap_rate_tool = Tool(
    func=calculate_cap_rate,
)

FINANCIAL_CALCULATION_TOOLS = [
    calculate_noi_tool,
    calculate_dscr_tool,
    calculate_ltv_tool,
    calculate_cap_rate_tool,
]