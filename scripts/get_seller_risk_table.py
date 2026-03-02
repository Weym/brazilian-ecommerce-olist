"""Get top-10 sellers by mean risk score for slides outline."""
import sys
import pandas as pd
import joblib

sys.path.insert(0, 'C:/Users/Wey/Desktop/Alpha/Projetos/python')
from src.features import PRE_DELIVERY_FEATURES

gold = pd.read_parquet('C:/Users/Wey/Desktop/Alpha/Projetos/python/data/gold/olist_gold.parquet')
pipeline = joblib.load('C:/Users/Wey/Desktop/Alpha/Projetos/python/models/final_pipeline.joblib')

THRESHOLD = 0.785
X = gold[PRE_DELIVERY_FEATURES]
scores = pipeline.predict_proba(X)[:, 1]
gold = gold.copy()
gold['risk_score'] = scores

seller_risk = (
    gold.groupby('seller_id')
    .agg(
        total_orders=('order_id', 'count'),
        mean_risk_score=('risk_score', 'mean'),
        high_risk_orders=('risk_score', lambda x: (x >= THRESHOLD).sum())
    )
    .query('total_orders >= 10')
    .sort_values('mean_risk_score', ascending=False)
    .head(10)
    .reset_index()
)

seller_risk['seller_short'] = seller_risk['seller_id'].str[:8] + '...'
print(seller_risk[['seller_short', 'mean_risk_score', 'total_orders', 'high_risk_orders']].to_string(index=False))
