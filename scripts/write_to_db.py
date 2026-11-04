import os
import pandas as pd
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv

load_dotenv()

TABLE_NAME = 'zakirovalr'  # ваша фамилия + инициалы
PARQUET_PATH = 'au_supermarket_products.parquet'
N_ROWS = 100


def load_data(n_rows: int = N_ROWS) -> pd.DataFrame:
    """Загружает первые n строк датасета из parquet."""
    if not os.path.exists(PARQUET_PATH):
        raise FileNotFoundError(f"Файл {PARQUET_PATH} не найден. Сначала запустите data_loader.py.")
    df = pd.read_parquet(PARQUET_PATH)
    return df.head(n_rows)


def create_table(cursor, df: pd.DataFrame) -> None:
    """Создаёт таблицу с колонками из датасета (все TEXT для простоты)."""
    columns = ', '.join([f'"{col}" TEXT' for col in df.columns])
    cursor.execute(sql.SQL('DROP TABLE IF EXISTS {};').format(sql.Identifier(TABLE_NAME)))
    cursor.execute(sql.SQL('CREATE TABLE {} ({});').format(
        sql.Identifier(TABLE_NAME),
        sql.SQL(columns)
    ))


def insert_data(cursor, df: pd.DataFrame) -> None:
    """Вставляет строки в таблицу."""
    cols = ', '.join([f'"{col}"' for col in df.columns])
    placeholders = ', '.join(['%s'] * len(df.columns))
    query = f'INSERT INTO {TABLE_NAME} ({cols}) VALUES ({placeholders});'

    for _, row in df.iterrows():
        cursor.execute(query, tuple(row.fillna('').astype(str)))


def main():
    print(f'Загрузка {N_ROWS} строк из {PARQUET_PATH}...')
    df = load_data()
    print(f'Загружено: {len(df)} строк, {len(df.columns)} столбцов')

    print(f'Подключение к {os.getenv("DB_NAME")} на {os.getenv("DB_HOST")}...')
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT'),
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
    )
    cursor = conn.cursor()

    try:
        print(f'Создание таблицы {TABLE_NAME}...')
        create_table(cursor, df)
        conn.commit()

        print(f'Вставка {len(df)} строк...')
        insert_data(cursor, df)
        conn.commit()

        cursor.execute(f'SELECT COUNT(*) FROM {TABLE_NAME};')
        count = cursor.fetchone()[0]
        print(f'Вставлено строк: {count}')

    except Exception as e:
        conn.rollback()
        print(f'Ошибка: {e}')
    finally:
        cursor.close()
        conn.close()
        print('Соединение закрыто.')


if __name__ == '__main__':
    main()