import sqlite3
from pathlib import Path

DB_FILENAME = 'creds.db'
USERNAME = 'deexpert'

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / DB_FILENAME


def read_creds(db_path: Path = DB_PATH, username: str = USERNAME) -> dict | None:
    """
    Читает креды пользователя из SQLite базы.

    Args:
        db_path (Path): Путь к файлу creds.db.
        username (str): Имя пользователя для поиска.

    Returns:
        dict | None: Словарь с кредами или None, если не найдено.
    """
    if not db_path.exists():
        raise FileNotFoundError(f"Файл {db_path} не найден.")

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM access WHERE user = ?;", (username,))
    row = cursor.fetchone()

    cursor.close()
    conn.close()

    return dict(row) if row else None


if __name__ == '__main__':
    creds = read_creds()
    if creds:
        print(f"User: {creds.get('user')}")
        print(f"Host: {creds.get('url')}:{creds.get('port')}")
        print(f"DB: {creds.get('db_name')}")
        print(f"Password length: {len(creds.get('pass', ''))}")
    else:
        print(f"Пользователь {USERNAME} не найден.")