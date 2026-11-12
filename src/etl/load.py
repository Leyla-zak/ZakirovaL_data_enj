"""
load.py

Запись данных в PostgreSQL
"""
import os
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent.parent
load_dotenv(ROOT / '.env')

TABLE_NAME = 'zakiroval'

def get_engine():
    """Создаёт SQLAlchemy engine из переменных окружения."""
    required = ['DB_HOST', 'DB_PORT', 'DB_NAME', 'DB_USER', 'DB_PASSWORD']
    missing = [k for k in required if not os.getenv(k)]
    if missing:
        raise ValueError(f"Не заданы переменные: {missing}")

    conn_str = (
        f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )
    return create_engine(conn_str)

def load_to_db(df: pd.DataFrame, table_name: str = TABLE_NAME) -> int:
    print(f'Подключение к {os.getenv("DB_NAME")}...')
    engine = get_engine()

    # NaN -> None, всё -> str (в БД все колонки TEXT)
    df_clean = df.copy()
    for col in df_clean.columns:
        df_clean[col] = df_clean[col].apply(lambda v: None if pd.isna(v) else str(v))

    print(f'Запись {len(df_clean)} строк в таблицу {table_name}...')
    try:
        df_clean.to_sql(
            name=table_name,
            con=engine,
            if_exists='replace',
            index=False,
            method='multi',
            chunksize=100,
        )
    except Exception as e:
        print(f'Ошибка загрузки: {e}')
        raise

    with engine.connect() as conn:
        count = pd.read_sql(
            f'SELECT COUNT(*) AS cnt FROM {table_name};', conn
        )['cnt'].iloc[0]

    print(f'Успех! В таблице {table_name} строк: {count}')
    return int(count)