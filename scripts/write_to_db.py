import os
import sys
import pandas as pd
import psycopg2
from psycopg2 import sql
from psycopg2.extras import execute_values
from dotenv import load_dotenv

from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / '.env')

TABLE_NAME = 'zakirovalr'
PARQUET_PATH = ROOT / 'au_supermarket_products.parquet'
N_ROWS = 100


def load_data(n_rows: int = N_ROWS) -> pd.DataFrame:
    """Загружает первые n строк датасета из parquet."""
    if not PARQUET_PATH.exists():
        raise FileNotFoundError(f"Файл {PARQUET_PATH} не найден.")
    df = pd.read_parquet(PARQUET_PATH)
    return df.head(n_rows)


def main():
    print(f'Загрузка {N_ROWS} строк из {PARQUET_PATH}...')
    df = load_data()
    print(f'Загружено: {len(df)} строк, {len(df.columns)} столбцов')

    print(f'Подключение к {os.getenv("DB_NAME")}...')
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT'),
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
    )
    cursor = conn.cursor()

    try:
        # 1. Удаляем таблицу, если есть
        cursor.execute(sql.SQL('DROP TABLE IF EXISTS {};').format(
            sql.Identifier(TABLE_NAME)
        ))

        # 2. Создаём таблицу с безопасными идентификаторами
        columns_sql = sql.SQL(', ').join(
            sql.SQL('{} TEXT').format(sql.Identifier(col)) for col in df.columns
        )
        cursor.execute(sql.SQL('CREATE TABLE {} ({});').format(
            sql.Identifier(TABLE_NAME), columns_sql
        ))

        # 3. Вставляем данные батчем (быстро и безопасно)
        cols_identifiers = sql.SQL(', ').join(sql.Identifier(col) for col in df.columns)
        query = sql.SQL('INSERT INTO {} ({}) VALUES %s;').format(
            sql.Identifier(TABLE_NAME), cols_identifiers
        )

        # Преобразуем DataFrame в список кортежей, заменяя NaN на None
        rows = [tuple(row) for row in df.astype(object).where(pd.notnull(df), None).values]

        execute_values(cursor, query, rows)
        conn.commit()

        # 4. Проверка
        cursor.execute(sql.SQL('SELECT COUNT(*) FROM {};').format(
            sql.Identifier(TABLE_NAME)
        ))
        count = cursor.fetchone()[0]
        print(f'Успех! В таблице {TABLE_NAME} строк: {count}')

    except Exception as e:
        conn.rollback()
        print(f'Ошибка: {e}')
        sys.exit(1)
    finally:
        cursor.close()
        conn.close()
        print('Соединение закрыто.')


if __name__ == '__main__':
    main()