import pandas as pd
gold = pd.read_parquet("C:/Users/Wey/Desktop/Alpha/Projetos/python/data/gold/olist_gold.parquet")

# Contract columns
assert "bad_review" in gold.columns
assert "seller_customer_distance_km" in gold.columns
assert "estimated_days" in gold.columns
assert "freight_ratio" in gold.columns
assert "product_volume_cm3" in gold.columns
assert "actual_delay_days" in gold.columns
assert "product_category_name_english" in gold.columns

# Integrity
assert gold["order_id"].is_unique
assert gold["bad_review"].isin([0, 1]).all()
assert gold["bad_review"].isna().sum() == 0

# Distance in km (not degrees) — threshold 10000 per Phase 02-02 decision
assert gold["seller_customer_distance_km"].max() > 100
assert gold["seller_customer_distance_km"].max() < 10000, f"Max = {gold['seller_customer_distance_km'].max()}"

# Enough data
assert len(gold) > 50000, f"Only {len(gold)} rows"

print("SMOKE TEST PASSOU — tabela gold validada")
print(gold.shape)
print(f"bad_review rate: {gold['bad_review'].mean():.1%}")
print(f"distance max: {gold['seller_customer_distance_km'].max():.1f} km")
