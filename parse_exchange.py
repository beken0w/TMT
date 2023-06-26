import os
from datetime import date, timedelta, datetime
import requests
from bs4 import BeautifulSoup

KURS = {}


def parse_mir():
    if not os.path.isfile(f"./downloads/mir_money_{date.today()}.html"):
        url = "https://mironline.ru/support/list/kursy_mir/"
        response = requests.get(url)

        with open(f"./downloads/mir_money_{date.today()}.html", "wb") as f:
            f.write(response.content)

    for file in os.listdir("./downloads"):
        origin_name = file
        name_file = file.replace("mir_money_", "").replace(".html", "")
        file_date = datetime.strptime(name_file, r'%Y-%m-%d').date()
        if file_date < date.today():
            os.remove(f"./downloads/{origin_name}")

    if os.path.isfile(f"./downloads/mir_money_{date.today()}.html"):
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


if __name__ == '__main__':
    convert_to_rub()
