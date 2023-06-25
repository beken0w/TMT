# Проект бота-ассистента TO DO LIST  

## Возможности бота

- создавать задачи
- менять статус задачи на "Выполнено"
- удалять задачи

## Как запустить проект  
  
### Перейти в нужную директорию и склонировать репозиторий через SSH:  

```git clone git@github.com:beken0w/TMT.git```

### Cоздать и активировать виртуальное окружение:

```python -m venv venv```

```venv/Scripts/activate```

### Установить зависимости из файла requirements.txt:

```python -m pip install --upgrade pip```

```pip install -r requirements.txt```

### Создать файл с переменными окружения .env и внести следующие значения:

```token="<токен вашего бота>"``` (Обязательно)  

```db_name="<имя названия БД>"``` (Необязательно, по умолчанию 'main.db')  

### Создать базу и таблицу с помощью скрипта 'prepare_db.py'

```python prepare_db.py```

### Запустить бота командой:

```python views.py```




