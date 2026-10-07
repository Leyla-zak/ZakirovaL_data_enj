import pandas as pd
import os
import csv
import warnings

def load_dataset(file_path: str = 'au_supermarket_products.csv') -> pd.DataFrame:
    """
    Загружает датасет из CSV-файла и выводит первые 10 строк.

    Args:
        file_path (str): Путь к CSV-файлу с датасетом.

    Returns:
        pd.DataFrame: Загруженный датафрейм.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Файл {file_path} не найден. Убедитесь, что он скачан.")

    # Считаем количество строк в файле (без заголовка)
    with open(file_path, newline='', encoding='utf-8') as f:
        n_rows = sum(1 for _ in csv.reader(f)) - 1

    # Читаем CSV. on_bad_lines='skip' пропускает битые строки
    df = pd.read_csv(file_path, on_bad_lines='skip')

    # Проверяем, сколько строк потеряно
    skipped = n_rows - df.shape[0]
    if skipped > 0:
        warnings.warn(
            f"{skipped} строк(и) из {n_rows} были пропущены "
            f"из-за ошибок формата (on_bad_lines='skip').",
            RuntimeWarning,
        )
    return df

def cast_types(df: pd.DataFrame) -> pd.DataFrame:
    """
    Приводит типы данных датафрейма к правильным.

    Args:
        df (pd.DataFrame): Исходный датафрейм.

    Returns:
        pd.DataFrame: Датафрейм с правильными типами.
    """
    df = df.copy()

    #Числовые столбцы (деньги, проценты, ID)
    numeric_cols = ['price', 'was_price', 'save_percent', 'unit_price']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    #ID (целые числа)
    int_cols = ['product_id', 'store_id']
    for col in int_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').astype('Int64')

    #Штрих-код (важно: строка, чтобы не потерять ведущие нули!)
    if 'barcode' in df.columns:
        df['barcode'] = df['barcode'].astype('string')

    #Булевы столбцы
    bool_cols = ['on_special', 'in_stock']
    bool_map = {
        'True': True, 'False': False,
        'true': True, 'false': False,
        '1': True, '0': False,
        1: True, 0: False,
        True: True, False: False,
    }
    for col in bool_cols:
        if col in df.columns:
            df[col] = df[col].map(bool_map).astype('boolean')

    #Даты
    if 'collected_date' in df.columns:
        df['collected_date'] = pd.to_datetime(
            df['collected_date'],
            format='%Y-%m-%d',  # ISO-формат: год-месяц-день
            errors='coerce'
        )

    #Текстовые столбцы (остальные)
    text_cols = ['chain', 'name', 'brand', 'size', 'department',
                 'unit_measure', 'special_type', 'offer_description',
                 'product_url', 'image_url']
    for col in text_cols:
        if col in df.columns:
            df[col] = df[col].astype('string').str.strip()
    return df


def save_to_parquet(df: pd.DataFrame, output_path: str = 'au_supermarket_products.parquet') -> None:
    """
    Сохраняет датафрейм в формате .parquet.

    Args:
        df (pd.DataFrame): Датафрейм для сохранения.
        output_path (str): Путь к выходному файлу.
    """
    df.to_parquet(output_path, index=False, engine='pyarrow')
    print(f"Файл сохранён: {output_path}")


if __name__ == '__main__':
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', 50)

    # 1. Загружаем
    print("Загрузка датасета...")
    df = load_dataset()

    # 2. Приводим типы
    print("\nПриведение типов...")
    df = cast_types(df)

    # 3. Выводим информацию
    print(f"\nДатасет загружен: {df.shape[0]} строк, {df.shape[1]} столбцов")
    print("\nТипы данных после приведения:")
    print(df.dtypes)
    print("\nПервые 10 строк:")
    print(df.head(10))

    # 4. Сохраняем в parquet
    print("\nСохранение в parquet...")
    save_to_parquet(df)

    print("\nГотово!")
