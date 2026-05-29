import logging
from unittest.mock import patch
import logging
import pandas as pd

from src.report import spending_by_category


def test_spending_by_category_is_positive(test_data_for_spending_by_category, done_data_for_data_for_spending_by_category):
    result = spending_by_category(test_data_for_spending_by_category, "Супермаркеты", "20.05.2020")
    assert result == done_data_for_data_for_spending_by_category
