from re import S
from socket import timeout
from types import NoneType
import unicodedata
from wsgiref import headers
from bs4 import BeautifulSoup as bs
import requests
import csv
from lxml import etree
from fake_useragent import UserAgent
from itertools import count, groupby
from unicodedata import normalize


UA = UserAgent()
URL = 'http://t.intimcity.com/'
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': UA.random
}



def main(url):
    count = 1
    req = requests.get(url, headers = HEADERS)
    soup = bs(req.text, 'lxml')
    pagin_num = soup.find('div', class_ = 'pagingList').find_all('a')[-2].text
    for i in range(0,int(pagin_num)):
        print(f'Парсим страничку №{count}')
        count += 1

        req = requests.get(url, headers = HEADERS , params = {'page': i}, timeout = 30)

        with open('index.html', 'w') as file:
            file.write(req.text)
        with open('index.html', 'r') as file:
            html = file.read()

        soup = bs(html, 'lxml')
        girls_cards = soup.find_all('div', class_ = 'storyLeft adp_edin_ank ank_txtview')

        for card in girls_cards:
            ref_on_data = card.find('a').get('href')
            req_girls_table = requests.get(f'http://t.intimcity.com{ref_on_data}', headers = HEADERS, timeout = 30)
            src_girls_table = req_girls_table.text

            with open('table.html', 'w', encoding = 'utf-8') as table:
                table.write(src_girls_table)
            with open('table.html', 'r', encoding = 'utf-8') as table:
                tables = table.read()

            soup_table = bs(tables, 'lxml')
            girls_tables = soup_table.find('div', id = 'content').find('table').find_all('p', class_ = 't')
            
            girls_dict_1 = []

            for k in girls_tables:
                girls_dict_1.append(k.text.strip())

            with open('girls_cards.csv', 'a', newline='', encoding = '1251') as file:
                writer = csv.writer(file, delimiter = ';')
                try:
                    writer.writerow(['Телефон', girls_dict_1.pop(girls_dict_1.index('Телефон')+1)])
                except:
                    'Телефон не найден'
                try:
                    writer.writerow(['Метро', girls_dict_1.pop(girls_dict_1.index('Метро')+1)])
                except:
                    'Метро не найдено'
                try:
                    writer.writerow(['Район', girls_dict_1.pop(girls_dict_1.index('Район')+1)])
                except:
                    'Район не найден'
                try:
                    writer.writerow(['Дата\xa0обновления', girls_dict_1.pop(girls_dict_1.index('Дата\xa0обновления')+1)])
                except:
                    'Дата обновления не найдена'
                try:
                    writer.writerow(['Номер анкеты', girls_dict_1.pop(girls_dict_1.index('Номер анкеты')+1)])
                except:
                    'Номер анкеты не найден'


if __name__ == '__main__':
    main(URL)