# tools/reorder_calculator.py

from typing import List, Dict
import math


def calculate_reorder_decision(
    daily_sales: List[float],
    current_inventory: int,
    lead_time_days: int,
    safety_buffer_days: int = 7
) -> Dict:
    if not daily_sales:
        avg_daily_sales = 0
    else:
        avg_daily_sales = sum(daily_sales) / len(daily_sales)

    if avg_daily_sales > 0:
        days_inventory_remaining = current_inventory / avg_daily_sales
    else:
        days_inventory_remaining = math.inf

    reorder_threshold = lead_time_days + safety_buffer_days
    reorder_now = days_inventory_remaining < reorder_threshold

    recommended_quantity = 0
    if reorder_now and avg_daily_sales > 0:
        recommended_quantity = max(
            round(
                (lead_time_days + safety_buffer_days) * avg_daily_sales
                - current_inventory
            ),
            0
        )

    # confidence logic
    confidence = "low"
    risk_factors = []

    if daily_sales:
        sales_variance = max(daily_sales) - min(daily_sales)
        if sales_variance < avg_daily_sales * 0.3:
            confidence = "high"
        elif sales_variance < avg_daily_sales * 0.7:
            confidence = "medium"
        else:
            confidence = "low"
            risk_factors.append("Demand variability")
    else:
        risk_factors.append("No historical sales data")

    if lead_time_days > 30:
        risk_factors.append("Long supplier lead time")

    if avg_daily_sales == 0:
        risk_factors.append("Zero observed demand")

    if not risk_factors:
        risk_factors.append("Limited historical data")

    return {
        "avg_daily_sales": round(avg_daily_sales, 2),
        "days_inventory_remaining": (
            round(days_inventory_remaining, 1)
            if math.isfinite(days_inventory_remaining)
            else "infinite"
        ),
        "reorder_now": reorder_now,
        "recommended_quantity": recommended_quantity,
        "confidence_level": confidence,
        "risk_factors": risk_factors,
    }
