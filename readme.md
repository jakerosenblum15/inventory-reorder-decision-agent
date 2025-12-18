# Inventory Reorder Decision Agent

A small, explainable decision-support tool that recommends inventory reorder actions
based on historical sales, current inventory, and supplier lead time.

The system intentionally separates deterministic calculation logic from
narrative explanation to improve transparency and reduce hallucination risk.

## Quick Start

```bash
git clone https://github.com/jakerosenblum15/inventory-reorder-decision-agent.git
cd inventory-reorder-decision-agent
python run_local.py inventory_template.csv
```

## What This Does

- Ingests daily sales data from a CSV file
- Computes average demand and inventory coverage
- Evaluates reorder risk using lead time and safety buffer
- Outputs a clear recommendation with confidence and risk factors

This tool provides **decision support only** and does not automate purchasing.

## Assumptions
- Sales history is representative of near-term demand
- Lead time is fixed and known
- Inventory is a single SKU and location
- Recommendations are reviewed by a human before action

CSV → Calculation Engine → Explanation → Human Review


## Future Extensions
- Conversational agent interface (e.g., LLM-based)

## Usage

```bash
python run_local.py inventory_template.csv
