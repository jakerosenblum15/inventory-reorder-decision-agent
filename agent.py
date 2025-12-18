from google.adk import Agent
from tools.reorder_calculator import calculate_reorder_decision

inventory_agent = Agent(
    name="inventory_reorder_agent",
    tools=[calculate_reorder_decision],
)
