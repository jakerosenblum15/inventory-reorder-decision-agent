import csv
import sys
from tools.reorder_calculator import calculate_reorder_decision


def load_csv(path: str):
    daily_sales = []
    current_inventory = None
    lead_time_days = None

    with open(path, newline="") as f:
        reader = csv.DictReader(f)

        required = {"daily_sales", "current_inventory", "lead_time_days"}
        if not reader.fieldnames or not required.issubset(set(reader.fieldnames)):
            raise ValueError(
                f"CSV must include headers: {sorted(required)}. Found: {reader.fieldnames}"
            )

        for row in reader:
            # validate required fields are present + not blank
            for key in required:
                if row.get(key) is None or str(row.get(key)).strip() == "":
                    raise ValueError(f"Missing value for '{key}' in row: {row}")

            daily_sales.append(float(row["daily_sales"]))
            current_inventory = int(row["current_inventory"])
            lead_time_days = int(row["lead_time_days"])

    if current_inventory is None or lead_time_days is None:
        raise ValueError("CSV contained no rows or missing required fields.")

    return daily_sales, current_inventory, lead_time_days



def explain(decision: dict, lead_time_days: int, safety_buffer_days: int = 7) -> str:
    avg = decision["avg_daily_sales"]
    days = decision["days_inventory_remaining"]
    reorder_now = decision["reorder_now"]
    qty = decision["recommended_quantity"]
    conf = decision["confidence_level"]
    risks = decision["risk_factors"]

    threshold = lead_time_days + safety_buffer_days

    lines = []
    lines.append(f"Average daily sales: {avg} units/day.")
    lines.append(f"Inventory coverage: {days} days.")
    lines.append(
        f"Lead time + safety buffer: {threshold} days "
        f"(lead time {lead_time_days} + buffer {safety_buffer_days})."
    )

    if reorder_now:
        lines.append(f"Decision: REORDER NOW. Recommended quantity: {qty} units.")
    else:
        lines.append("Decision: Do not reorder yet (coverage is above the threshold).")

    lines.append(f"Confidence: {conf}.")
    lines.append("Risks: " + ", ".join(risks) + ".")

    return "\n".join(lines)


def main():
    import sys

    if len(sys.argv) < 2:
        print("Usage: python run_local.py <csv_file>")
        sys.exit(1)

    csv_path = sys.argv[1]

    daily_sales, current_inventory, lead_time_days = load_csv(csv_path)
    decision = calculate_reorder_decision(
        daily_sales, current_inventory, lead_time_days
    )
    print(explain(decision, lead_time_days))




if __name__ == "__main__":
    main()
