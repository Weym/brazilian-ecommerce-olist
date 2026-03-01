"""
Enrich gold table with missing PRE_DELIVERY_FEATURES.

Missing features vs. contract declared in src/features.py:
  - price            -> sum of items.price per order_id
  - estimated_delivery_days -> rename from estimated_days
  - order_item_count -> count of items per order_id
  - payment_type     -> mode of payment_type per order_id
  - payment_installments -> sum of payment_installments per order_id

This script reads the frozen gold table, joins the missing columns from
raw CSVs, and overwrites olist_gold.parquet with the enriched version.
"""
import os
import sys

import pandas as pd
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GOLD_PATH = os.path.join(ROOT, "data", "gold", "olist_gold.parquet")
RAW_PATH = os.path.join(ROOT, "data", "raw")

# Load gold table
gold = pd.read_parquet(GOLD_PATH)
print(f"Gold (before): {gold.shape}")

# Load raw items
items = pd.read_csv(os.path.join(RAW_PATH, "olist_order_items_dataset.csv"))

# Aggregate items per order: sum(price), count(order_item_id)
items_agg = (
    items.groupby("order_id")
    .agg(
        price=("price", "sum"),
        order_item_count=("order_item_id", "count"),
    )
    .reset_index()
)

# Load raw payments
payments = pd.read_csv(os.path.join(RAW_PATH, "olist_order_payments_dataset.csv"))

# Aggregate payments per order: mode(payment_type), sum(payment_installments)
def mode_first(series):
    """Return the most frequent value; ties broken by first occurrence."""
    return series.value_counts().index[0]

payments_agg = (
    payments.groupby("order_id")
    .agg(
        payment_type=("payment_type", mode_first),
        payment_installments=("payment_installments", "sum"),
    )
    .reset_index()
)

# Join to gold
n_before = len(gold)
gold = gold.merge(items_agg, on="order_id", how="left")
gold = gold.merge(payments_agg, on="order_id", how="left")
assert len(gold) == n_before, f"Row count changed after join: {n_before} -> {len(gold)}"

# Add estimated_delivery_days from existing estimated_days (rename semantics)
if "estimated_days" in gold.columns:
    gold["estimated_delivery_days"] = gold["estimated_days"]
    print("OK: estimated_delivery_days created from estimated_days")

# Verify all PRE_DELIVERY_FEATURES are now present
sys.path.insert(0, ROOT)
from src.features import PRE_DELIVERY_FEATURES, FORBIDDEN_FEATURES, TARGET_COLUMN

missing = [c for c in PRE_DELIVERY_FEATURES if c not in gold.columns]
assert not missing, f"Still missing after enrich: {missing}"
print(f"OK: all {len(PRE_DELIVERY_FEATURES)} PRE_DELIVERY_FEATURES present")

# Anti-leakage: FORBIDDEN_FEATURES should NOT be in PRE_DELIVERY_FEATURES
leakage = [c for c in FORBIDDEN_FEATURES if c in PRE_DELIVERY_FEATURES]
assert not leakage, f"LEAKAGE: {leakage}"
print("OK: zero leakage confirmed")

# Null check for new features
for col in ["price", "order_item_count", "payment_type", "payment_installments", "estimated_delivery_days"]:
    nulls = gold[col].isnull().sum()
    print(f"  {col}: {nulls} nulls ({nulls/len(gold):.2%})")

# Save enriched gold table
gold.to_parquet(GOLD_PATH, index=False)
print(f"\nGold (after): {gold.shape}")
print(f"Saved: {GOLD_PATH}")
print("DONE: gold table enriched with missing PRE_DELIVERY_FEATURES")
