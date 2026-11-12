"""
validate.py

Проверки качества данных.
"""
import pandas as pd

def validate(df: pd.DataFrame) -> bool:
    print('Валидация...')

    if df.empty:
        raise ValueError('Датафрейм пуст.')

    if len(df) > 100:
        raise ValueError(f'Слишком много строк: {len(df)} > 100.')

    for col in ['name', 'price', 'chain']:
        if col in df.columns and df[col].isna().all():
            raise ValueError(f'Столбец {col} полностью пуст.')

    if 'price' in df.columns:
        negative = (df['price'] < 0).sum()
        if negative > 0:
            raise ValueError(f'Найдено {negative} отрицательных цен.')

    print(f'Валидация пройдена: {len(df)} строк.')
    return True