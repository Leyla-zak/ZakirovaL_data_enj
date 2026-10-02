import pandas as pd
import os

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
    
    #Пока грязные строки я скипаю, в дальнейшем разберусь как всё это привести к правильному виду
    df = pd.read_csv(file_path, on_bad_lines='skip')

    # pd.set_option('display.max_columns', None)
    # pd.set_option('display.width', None)   
    # pd.set_option('display.max_colwidth', 50)

    print(f"Датасет загружен: {df.shape[0]} строк, {df.shape[1]} столбцов")
    print("\nПервые 10 строк:")
    print(df.head(10))

    return df


if __name__ == '__main__':
    load_dataset()