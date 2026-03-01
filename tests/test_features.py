"""Tests for src/features.py — feature contract for Olist Pre-Delivery Risk Model."""

import sys
import os

# Ensure src/ is importable from project root
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


def test_import_works():
    """Test 1: from src.features import PRE_DELIVERY_FEATURES must work without error."""
    from src.features import PRE_DELIVERY_FEATURES, FORBIDDEN_FEATURES, TARGET_COLUMN
    assert PRE_DELIVERY_FEATURES is not None
    assert FORBIDDEN_FEATURES is not None
    assert TARGET_COLUMN is not None


def test_pre_delivery_features_has_13_columns():
    """Test 2: PRE_DELIVERY_FEATURES must be a list with exactly 13 strings."""
    from src.features import PRE_DELIVERY_FEATURES
    assert isinstance(PRE_DELIVERY_FEATURES, list), "PRE_DELIVERY_FEATURES deve ser uma lista"
    assert len(PRE_DELIVERY_FEATURES) == 13, (
        f"PRE_DELIVERY_FEATURES deve ter 13 colunas, tem {len(PRE_DELIVERY_FEATURES)}"
    )
    for col in PRE_DELIVERY_FEATURES:
        assert isinstance(col, str), f"Todos os itens devem ser strings, encontrado: {type(col)}"


def test_required_forbidden_columns_present():
    """Test 3: Mandatory forbidden columns must be in FORBIDDEN_FEATURES."""
    from src.features import FORBIDDEN_FEATURES
    required_forbidden = [
        "order_delivered_customer_date",
        "review_score",
        "review_comment_message",
        "review_creation_date",
        "review_answer_timestamp",
    ]
    for col in required_forbidden:
        assert col in FORBIDDEN_FEATURES, (
            f"FAIL: '{col}' deve estar em FORBIDDEN_FEATURES"
        )


def test_target_column_is_bad_review():
    """Test 4: TARGET_COLUMN must equal 'bad_review'."""
    from src.features import TARGET_COLUMN
    assert TARGET_COLUMN == "bad_review", (
        f"TARGET_COLUMN deve ser 'bad_review', encontrado: '{TARGET_COLUMN}'"
    )


def test_no_forbidden_in_pre_delivery():
    """Test 5: No column from FORBIDDEN_FEATURES should appear in PRE_DELIVERY_FEATURES."""
    from src.features import PRE_DELIVERY_FEATURES, FORBIDDEN_FEATURES
    leakage = [c for c in FORBIDDEN_FEATURES if c in PRE_DELIVERY_FEATURES]
    assert not leakage, f"LEAKAGE DETECTADO: {leakage}"


def test_seller_customer_distance_km_present():
    """Test 6: seller_customer_distance_km must be in PRE_DELIVERY_FEATURES."""
    from src.features import PRE_DELIVERY_FEATURES
    assert "seller_customer_distance_km" in PRE_DELIVERY_FEATURES, (
        "seller_customer_distance_km deve estar em PRE_DELIVERY_FEATURES "
        "(computada na Phase 2, mas declarada aqui como contrato)"
    )
