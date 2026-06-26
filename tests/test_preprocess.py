import pandas as pd

from chatbot_data.preprocess import clean_raw_data, clean_text, normalize_column_name, normalize_price


def test_clean_text_removes_html_entities_and_extra_spaces():
    assert clean_text(" A&nbsp;  &amp;\\n B ") == "A & B"


def test_normalize_column_name():
    assert normalize_column_name(" Kích thước màn hình ") == "kích_thước_màn_hình"


def test_normalize_price():
    assert normalize_price("12.990.000đ") == 12990000
    assert normalize_price("Liên hệ") is None


def test_clean_raw_data_removes_empty_names_and_duplicates():
    raw = pd.DataFrame(
        [
            {"url": "u1", "ten_san_pham": "A", "sku": "s1", "gia_ban": "1.000đ"},
            {"url": "u1", "ten_san_pham": "A", "sku": "s1", "gia_ban": "1.000đ"},
            {"url": "u2", "ten_san_pham": "", "sku": "s2", "gia_ban": "Liên hệ"},
        ]
    )

    clean, before_rows = clean_raw_data(raw)

    assert before_rows == 3
    assert len(clean) == 1
    assert clean.iloc[0]["price_vnd"] == 1000
