"""
Feature contract for Olist Pre-Delivery Risk Model.

TEMPORAL ANCHOR: order_approved_at
    All features must be knowable at order approval time.
    No variable derived from post-delivery events may appear in PRE_DELIVERY_FEATURES.

RULE: No feature post-delivery.
    Any column that is only available after the order is physically delivered is
    strictly forbidden. Use FORBIDDEN_FEATURES to enforce this at code level.

CONSUMERS OF THIS FILE:
    - notebooks/FASE4-P4-ml-pipeline.ipynb  (ML training pipeline)
    - app/pages/03_modelo.py                 (Streamlit predictor page)

MAINTENANCE:
    If you add a column to PRE_DELIVERY_FEATURES, also add a row to
    docs/feature_contract.md — keep both sources in sync.
"""

# ---------------------------------------------------------------------------
# PRE_DELIVERY_FEATURES
# Columns knowable at order_approved_at — safe to use as model features.
# ---------------------------------------------------------------------------

PRE_DELIVERY_FEATURES: list[str] = [
    # --- Frete e preco ---
    "freight_value",               # raw: soma de freight_value por pedido (order_items.csv)
    "price",                       # raw: soma de price por pedido (order_items.csv)
    "freight_ratio",               # engineered: freight_value / price

    # --- Prazo estimado ---
    "estimated_delivery_days",     # engineered: order_estimated_delivery_date - order_approved_at
    # NOTE: anchor is order_approved_at, NOT order_purchase_timestamp (blocked decision)

    # --- Geografia ---
    "seller_state",                # raw: estado do vendedor (sellers.csv)
    "customer_state",              # raw: estado do comprador (customers.csv)
    "seller_customer_distance_km", # PHASE 2 — computed via Haversine; not available until gold table is built

    # --- Produto ---
    "product_weight_g",            # raw: peso do produto em gramas (products.csv)
    "product_volume_cm3",          # engineered: product_length_cm * product_width_cm * product_height_cm
    "product_category_name_english",  # join via product_category_name (category_translation.csv)

    # --- Pedido ---
    "order_item_count",            # engineered: contagem de itens por order_id (order_items.csv)
    "payment_type",                # raw: moda do tipo de pagamento por pedido (order_payments.csv)
    "payment_installments",        # raw: soma de parcelas por pedido (order_payments.csv)
]

# ---------------------------------------------------------------------------
# FORBIDDEN_FEATURES
# Columns that are NEVER allowed in the feature matrix X.
# All of these become available only after physical delivery or after the
# customer submits a review — i.e., after the prediction window closes.
# ---------------------------------------------------------------------------

FORBIDDEN_FEATURES: list[str] = [
    "order_delivered_customer_date",  # pos-entrega: so disponivel apos entrega fisica
    "review_score",                   # o proprio target / pos-entrega: source de bad_review — jamais como feature
    "review_comment_message",         # pos-entrega: texto submetido pelo cliente apos receber o pedido
    "review_creation_date",           # pos-entrega: data em que o cliente criou a review
    "review_answer_timestamp",        # pos-entrega: timestamp da resposta do vendedor a review
    "order_delivered_carrier_date",   # parcialmente pos-aprovacao, pouco confiavel: escaneado pela transportadora
]

# ---------------------------------------------------------------------------
# TARGET_COLUMN
# Binary label: 1 = insatisfacao real (review ruim), 0 = sem alerta
# ---------------------------------------------------------------------------

TARGET_COLUMN: str = "bad_review"
# bad_review = 1 if review_score in {1, 2}, else 0
# Rationale: estrelas 1-2 representam insatisfacao real e defensavel;
# estrela 3 e neutra e excluida da classe positiva.
