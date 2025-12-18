import csv
import asyncio
from agent import inventory_agent


def load_csv(path: str):
    daily_sales = []
    current_inventory = None
    lead_time_days = None

    with open(path, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            daily_sales.append(float(row["daily_sales"]))
            current_inventory = int(row["current_inventory"])
            lead_time_days = int(row["lead_time_days"])

    return daily_sales, current_inventory, lead_time_days


async def run(csv_path: str):
    daily_sales, current_inventory, lead_time_days = load_csv(csv_path)

    user_message = f"""
Analyze the following inventory situation and provide a reorder recommendation.

Daily sales history: {daily_sales}
Current inventory: {current_inventory}
Supplier lead time (days): {lead_time_days}

Rules:
- You must call the calculation tool to compute the decision.
- Explain in plain language.
- State confidence level and risk factors.
"""

    # NOTE: This ADK version expects (parent_context, message)
    events = inventory_agent.run_live(None, user_message)

    async for event in events:
        if hasattr(event, "content") and event.content:
            print(event.content, end="")
        elif hasattr(event, "text") and event.text:
            print(event.text, end="")
        else:
            # Fallback so we at least see *something*
            print(event)


if __name__ == "__main__":
    asyncio.run(run("sample_inventory.csv"))
