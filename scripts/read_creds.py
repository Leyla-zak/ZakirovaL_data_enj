import sqlite3
import os

db_path = 'creds.db'

if not os.path.exists(db_path):
    raise FileNotFoundError(f"Файл {db_path} не найден.")

conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# Смотрим структуру таблицы
cursor.execute("PRAGMA table_info(access);")
print("Колонки в таблице access:")
for col in cursor.fetchall():
    print(f"  - {col['name']} ({col['type']})")

# Смотрим данные пользователя deexpert
cursor.execute("SELECT * FROM access WHERE user = 'deexpert';")
row = cursor.fetchone()
if row:
    print("\nДанные deexpert:")
    for key in row.keys():
        # Пароль не выводим полностью, только длину
        val = row[key]
        if 'pass' in key.lower():
            val = f"*** (длина: {len(str(val))})"
        print(f"  {key}: {val}")

cursor.close()
conn.close()