"""
transform.py

Приведение типов данных к правильным.
"""
import pandas as pd

def cast_types(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Числовые
    for col in ['price', 'was_price', 'save_percent', 'unit_price']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # ID
    for col in ['product_id', 'store_id']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').astype('Int64')

    # Barcode - строка
    if 'barcode' in df.columns:
        df['barcode'] = df['barcode'].astype('string')

    # Булевы
    bool_map = {'true': True, 'false': False, '1': True, '0': False,
                1: True, 0: False, True: True, False: False}
    for col in ['on_special', 'in_stock']:
        if col in df.columns:
            normalized = df[col].astype(str).str.strip().str.lower()
            df[col] = normalized.map(bool_map).astype('boolean')

    # Даты
    if 'collected_date' in df.columns:
        df['collected_date'] = pd.to_datetime(
            df['collected_date'], format='%Y-%m-%d', errors='coerce'
        )

    # Текстовые
    text_cols = ['chain', 'name', 'brand', 'size', 'department',
                 'unit_measure', 'special_type', 'offer_description',
                 'product_url', 'image_url']
    for col in text_cols:
        if col in df.columns:
            df[col] = df[col].astype('string').str.strip()

    return df

def transform(df: pd.DataFrame, n_rows: int = 100) -> pd.DataFrame:
    """Типы + срез до n_rows."""
    return cast_types(df).head(n_rows)