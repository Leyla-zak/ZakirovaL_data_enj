'''
подправила код под замечание:
"В реальных проектах лучше использовать верхнеуровневые функции для работы с БД. "
"При выполнении следующего дз используйте встроенный в Pandas функционал."

'''

import os
import sys
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv


ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / '.env')

TABLE_NAME = 'zakiroval'
PARQUET_PATH = ROOT / 'au_supermarket_products.parquet'
N_ROWS = 100


def load_data(n_rows: int = N_ROWS) -> pd.DataFrame:
    if not PARQUET_PATH.exists():
        raise FileNotFoundError(f"Файл {PARQUET_PATH} не найден.")
    return pd.read_parquet(PARQUET_PATH).head(n_rows)


def get_engine():
    conn_str = (
        f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )
    return create_engine(conn_str)


def main():
    print(f'Загрузка {N_ROWS} строк из {PARQUET_PATH}...')
    df = load_data()

    # Все значения -> строки, NaN -> None
    df_clean = df.copy()
    for col in df_clean.columns:
        df_clean[col] = df_clean[col].apply(lambda v: None if pd.isna(v) else str(v))

    print(f'🔌 Подключение к {os.getenv("DB_NAME")}...')
    engine = get_engine()

    print(f'Запись {len(df_clean)} строк в таблицу {TABLE_NAME}...')
    try:
        df_clean.to_sql(
            name=TABLE_NAME,
            con=engine,
            if_exists='replace',
            index=False,
            method='multi',
            chunksize=100,
        )
    except Exception as e:
        print(f'Ошибка: {e}')
        sys.exit(1)

    with engine.connect() as conn:
        count = pd.read_sql(f'SELECT COUNT(*) AS cnt FROM {TABLE_NAME};', conn)['cnt'].iloc[0]

    print(f'Успех! В таблице {TABLE_NAME} строк: {count}')


if __name__ == '__main__':
    main()