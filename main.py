from my_lib import get_html, get_window_size, save_file
from urllib.parse import quote
from bs4 import BeautifulSoup as BS
from datetime import datetime



E_SITE = 'cp1251'
i_count = 0

def get_pages(html):
    soup = BS(html, 'lxml')
    img_count = soup.find('div', class_='header-text').find('h2').text

    try:
        r = soup.find('div', class_='navigation').find_all('a')[-2].text
        return int(r),  img_count
    except AttributeError:
        return 1, img_count



def parsing(html, obj, win_size_w, wib_size_h):
    global i_count
    soup = BS(html, 'lxml')
    r = soup.find('div', id='dle-content').find_all('a', class_='screen-link')
    for inc, a in enumerate(r, start=1):
        soup = BS(get_html(a.get('href'), E_SITE), 'lxml')
        req = soup.find('div', class_='llink').find_all('a')
        for aa in req:
            size_w = int(aa.get('href').split('/')[-2].split('x')[0])
            size_h = int(aa.get('href').split('/')[-2].split('x')[1])
            if win_size_w == size_w and wib_size_h == size_h:
                url_size = aa.get('href')
            else:
                continue
            soup2 = BS(get_html(url_size, E_SITE), 'lxml')
            image_url = soup2.find(id='img').get('src')
            name = f'img/{obj} - {image_url.split("-")[-1]}'
            save_file(image_url, name)
            print(f'|{inc:^{4}}|{name.split("/")[-1]:^{33}}|{"Загружен":^{10}}|')
            i_count += 1
    return i_count


#
def main(list_obj):

    start_time = datetime.now()

    win_width, win_heigth = get_window_size()

    for obj in list_obj:
        obj = obj.strip()
        url = f'http://www.nastol.com.ua/tags/{quote(obj, encoding=E_SITE)}/page/1/'
        pages, img_count = get_pages(get_html(url, E_SITE))
        obj = obj.strip()

        for page in range(1, pages + 1):

            base_url = f'http://www.nastol.com.ua/tags/{quote(obj, encoding=E_SITE)}/page/{page}/'
            print(f'{img_count}\nСтраница:{page}-{pages}')
            print('-'*51)
            print(f'|{"№":^{4}}|{"Категория - имя файла":^{33}}|{"Статус":^{10}}|')
            print('-' * 51)
            inc = parsing(get_html(base_url, E_SITE), obj, win_width, win_heigth)
            print('-' * 51, end='\n')
            print(f'Скачено:{inc}')
    end_time = datetime.now()
    print(f'Затрачено времени:{str(end_time-start_time).split(".")[0]:^{50}}')
    print('-' * 51)


if __name__ == '__main__':
    main(input(':>').split(','))