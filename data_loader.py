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


if __name__ == '__main__':
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', 50)

    df = load_dataset()

    print(f"\nДатасет загружен: {df.shape[0]} строк, {df.shape[1]} столбцов")
    print("\nПервые 10 строк:")
    print(df.head(10))
