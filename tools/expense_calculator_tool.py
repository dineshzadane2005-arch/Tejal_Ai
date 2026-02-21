from utils.expense_calculator import Calculator
from typing import List, Any
from langchain.tools import StructuredTool
from pydantic import BaseModel, Field

class CalculatorTool:
    def __init__(self):
        self.calculator = Calculator()
        self.calculator_tool_list = self._setup_tools()

    def _setup_tools(self) -> List:
        """Setup all tools for the calculator tool"""
        
        def hotel_cost_func(price_per_night: float, total_days: int) -> float:
            """Calculate total hotel cost"""
            return self.calculator.multiply(price_per_night, total_days)
        
        def daily_budget_func(total_cost: float, days: int) -> float:
            """Calculate daily expense budget"""
            return self.calculator.calculate_daily_budget(total_cost, days)
        
        def total_expense_func(cost1: float = 0, cost2: float = 0, cost3: float = 0, 
                              cost4: float = 0, cost5: float = 0) -> float:
            """Calculate total expense by adding up to 5 costs"""
            costs = [c for c in [cost1, cost2, cost3, cost4, cost5] if c > 0]
            return self.calculator.calculate_total(*costs) if costs else 0
        
        hotel_tool = StructuredTool.from_function(
            func=hotel_cost_func,
            name="estimate_total_hotel_cost",
            description="Calculate total hotel cost based on price per night and total days"
        )
        
        budget_tool = StructuredTool.from_function(
            func=daily_budget_func,
            name="calculate_daily_expense_budget",
            description="Calculate daily expense budget based on total cost and number of days"
        )
        
        expense_tool = StructuredTool.from_function(
            func=total_expense_func,
            name="calculate_total_expense",
            description="Calculate total expense by adding individual costs (up to 5 items)"
        )
        
        return [hotel_tool, budget_tool, expense_tool]