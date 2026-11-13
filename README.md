# Анализ товаров и цен в австралийских супермаркетах
ITMO lessons hometasks

## Структура проекта
ZakirovaL_data_enj/
├── src/
│ └── etl/
│ ├── __init.py
│ ├── extract.py <- загрузка CSV/parquet
│ ├── transform.py <- приведение типов
│ ├── validate.py <- проверки качества
│ ├── load.py <- запись в PostgreSQL
│ └── main.py <- CLI
├── scripts/
├── notebooks/
├── requirements.txt
└── README.md

## Датасет

### Описание
Датасет содержит информацию о товарах и ценах в австралийских супермаркетах Coles и Woolworths. 
Данные собраны 17 сентября 2026 года с помощью скраперов Apify.

**Структура:**
- `au_supermarket_products.csv` - 48 867 строк, информация о товарах: название, цена, скидка, штрих-код, категория.

**Типы признаков:** числовые (цена, широта, долгота), категориальные (сеть, штат, пригород), текстовые (адрес).

**Особенности:** Данные содержат пропуски (например, пустой столбец `store_url`), что требует предобработки.

### Источник
- **Платформа:** Kaggle
- **Ссылка на оригинал:** [Australian Supermarket Prices, September 2026](https://www.kaggle.com/datasets/freshcrawl/australian-supermarket-prices)
- **Автор:** FreshCrawl

### Размер скачиваемого файла
- `au_supermarket_products.csv` - **15.3 МБ** (15 270 476 байт)

### Ссылка на хранилище
[Google Drive](https://drive.google.com/file/d/1htOifYWaLTAOHthCCek9AB6hx82z01Qe/view?usp=sharing)

## Установка и запуск

### 1. Клонирование репозитория
```bash
git clone https://github.com/Leyla-zak/ZakirovaL_data_enj.git
cd ZakirovaL_data_enj 
```
### 2. Установка зависимостей
```bash
pip install -r requirements.txt
```
### 3. Скачивание датасета
Скачайте CSV по ссылке из раздела „Ссылка на хранилище".

### 4. Запуск скрипта
```bash
python data_loader.py
```

## EDA

Разведочный анализ качества данных: [notebooks/EDA.ipynb](notebooks/EDA.ipynb)

```bash
jupyter notebook notebooks/EDA.ipynb
```

## HW7: Запись в удалённую БД (Load в ETL)

### 1. Получение кредов
Креды читаются из файла `creds.db` (SQLite) скриптом `scripts/read_creds.py`.
Для записи используется «тайный пользователь» (доступ к `homeworks`).

### 2. Настройка `.env`
Создайте файл `.env` в корне проекта:

DB_NAME=...
DB_HOST=...
DB_PORT=...
DB_USER=...
DB_PASSWORD=...

**Не коммитьте `.env`!** Он в `.gitignore`.

### 3. Запуск
```bash
pip install -r requirements.txt
python scripts/write_to_db.py
```
---

### Шаг 5: Уберите тестовый мусор

1.  **Удалите** `scripts/test_write_to_db.py` (если ещё не удалили).
2.  **Удалите** `.env.student`.
3.  Проверьте `git status`:

```bash
git status
```

Не должно быть: .env, .env.student, creds.db, *.parquet, *.csv.

Должно быть: scripts/read_creds.py, scripts/write_to_db.py, requirements.txt, README.md, .gitignore.

## Пакет `etl`

Самодостаточный ETL-пайплайн:
1. **Extract** - загружает CSV/parquet.
2. **Transform** - приводит типы.
3. **Validate** - проверяет инварианты.
4. **Load** - записывает до 100 строк в PostgreSQL через `pd.to_sql()`.

### Запуск

```bash
pip install -r requirements.txt

# Dry-run (без записи)
python -m src.etl.main --dry-run

# С записью
python -m src.etl.main --source csv --rows 100 --table zakiroval
```
