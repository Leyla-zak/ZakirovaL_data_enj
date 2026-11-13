"""
main.py

CLI-точка входа для ETL.

Использование:
    python -m src.etl.main --source csv --rows 100
    python -m src.etl.main --source parquet --rows 100
    python -m src.etl.main --dry-run
"""
import argparse
import sys

from . import extract, transform, validate, load

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='ETL-пайплайн для данных супермаркетов.')
    parser.add_argument('--source', choices=['csv', 'parquet'], default='csv',
                        help='Источник данных (csv или parquet).')
    parser.add_argument('--rows', type=int, default=100,
                        help='Сколько строк загрузить (по умолчанию 100).')
    parser.add_argument('--table', type=str, default='zakiroval',
                        help='Имя таблицы в БД.')
    parser.add_argument('--dry-run', action='store_true',
                        help='Только извлечь и проверить, без записи.')
    return parser.parse_args()

def main() -> None:
    args = parse_args()
    print(f'ETL: source={args.source}, rows={args.rows}, table={args.table}')

    df_raw = extract.extract(source=args.source)
    print(f'Извлечено: {len(df_raw)} строк, {len(df_raw.columns)} столбцов')

    df = transform.transform(df_raw, n_rows=args.rows)
    print(f'Трансформировано: {len(df)} строк')

    validate.validate(df)

    if args.dry_run:
        print('Dry-run: запись пропущена.')
    else:
        load.load_to_db(df, table_name=args.table)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f'ETL упал: {e}', file=sys.stderr)
        sys.exit(1)