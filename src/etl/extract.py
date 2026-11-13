"""
extract.py

Загрузка сырых данных из CSV или parquet.
"""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent.parent
DEFAULT_CSV = ROOT / 'au_supermarket_products.csv'
DEFAULT_PARQUET = ROOT / 'au_supermarket_products.parquet'

def load_csv(path: Path = DEFAULT_CSV) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"CSV не найден: {path}")
    return pd.read_csv(path, dtype={'barcode': str}, on_bad_lines='skip', low_memory=False)


def load_parquet(path: Path = DEFAULT_PARQUET) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Parquet не найден: {path}")
    return pd.read_parquet(path)


def extract(source: str = 'csv', path: Path | None = None) -> pd.DataFrame:
    """Загружает данные из указанного источника."""
    if source == 'csv':
        return load_csv(path or DEFAULT_CSV)
    elif source == 'parquet':
        return load_parquet(path or DEFAULT_PARQUET)
    raise ValueError(f"Неизвестный источник: {source}")