# ZakirovaL_data_enj
ITMO lessons hometasks

## Датасет

### Описание
Датасет содержит информацию о товарах и ценах в австралийских супермаркетах Coles и Woolworths. 
Данные собраны 17 сентября 2026 года с помощью скраперов Apify.

**Структура:**
- `au_supermarket_products.csv` — 48 867 строк, информация о товарах: название, цена, скидка, штрих-код, категория.

**Типы признаков:** числовые (цена, широта, долгота), категориальные (сеть, штат, пригород), текстовые (адрес).

**Особенности:** Данные содержат пропуски (например, пустой столбец `store_url`), что требует предобработки.

### Источник
- **Платформа:** Kaggle
- **Ссылка на оригинал:** [Australian Supermarket Prices, September 2026](https://www.kaggle.com/datasets/freshcrawl/australian-supermarket-prices)
- **Автор:** FreshCrawl

### Размер скачиваемого файла
- `au_supermarket_products.csv` — **15.3 МБ** (15 270 476 байт)

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
Скачайте CSV по ссылке из раздела „Ссылка на хранилище

### 4. Запуск скрипта
```bash
python data_loader.py
```
