import os
import logging
from datetime import date, datetime
import requests
from bs4 import BeautifulSoup


KURS = {}
logging.basicConfig(level=logging.INFO,
                    filename='log_file.log',
                    filemode='a')


def parse_mir():
    if not os.path.isfile(f"./downloads/mir_money_{date.today()}.html"):
        logging.info("Загружаю обновленный курс")
        url = "https://mironline.ru/support/list/kursy_mir/"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(url, headers=headers)

        with open(f"./downloads/mir_money_{date.today()}.html", "wb") as f:
            f.write(response.content)

    for file in os.listdir("./downloads"):
        origin_name = file
        name_file = file.replace("mir_money_", "").replace(".html", "")
        file_date = datetime.strptime(name_file, r'%Y-%m-%d').date()
        if file_date < date.today():
            logging.info("Удаляю старый файл html МИР")
            os.remove(f"./downloads/{origin_name}")

    if os.path.isfile(f"./downloads/mir_money_{date.today()}.html"):
        logging.info("Считываю файл HTML и вывожу актуальные значения")
        with open(f"./downloads/mir_money_{date.today()}.html", "r", encoding='utf-8') as html:
            site = html.read()
            soup = BeautifulSoup(site, 'html.parser')
            rows = soup.find_all('tr')
            for row in rows[1:]:
                columns = row.find_all('td')
                currency = columns[0].get_text(strip=True)
                value = columns[1].get_text(strip=True)
                KURS[currency] = float(value.replace(',', '.'))
    return KURS


def convert_to_rub():
    lst = []
    for name, value in parse_mir().items():
        if value < 1:
            lst.append(f"1 рубль == {round(1/value, 3)} - {name}")
        else:
            lst.append(f"1 рубль == {round(value, 3)} - {name}")
    return "\n".join(lst)


def count_rub(value, currency):
    pass


if __name__ == '__main__':
    print(convert_to_rub())
