import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
from multiprocessing import Pool

def get_html(url):
    r = requests.get(url)
    return r.text

def get_total_pages(html):
    soup = BeautifulSoup(html, 'html.parser' )
    pages = soup.find('ul', class_ = 'pagn').find_all('a')[-1].get('href')
    total_pages = pages.split('=')[-1]
    return int(total_pages) 

def write_csv(data):
    with open('lalafo.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow((data['title'], 
                         data['price'],
                         data['url'],
                         data['photo'] ))



def get_page_data(html):
    soup = BeautifulSoup(html, 'html.parser')
    ads = soup.find('div', id='main-listing-block').find_all('article', class_="listing-item")
    for ad in ads:
        # title, price, url
        try:
            title = ad.find('a', class_="item listing-item-title").text.strip(' ')
        
        except:
            title = ''
        try: 
            url ='https://lalafo.kg' + ad.find('a', class_="item listing-item-title").get('href')
        except:
            url = ''
        try:
            price =ad.find('p', class_="listing-item-title").text.strip()
            #price = price.split("\")
        except:
            price = ''
        try: 
            photo =ad.find('img', class_="listing-item-photo link-image").get('src')
        except:
            photo = ''
        data = {
            'title': title, 
            'price': price,
            'url': url,
            'photo': photo
        }
        write_csv(data)

# def​ ​make_all​(url​):
#     url_gen = base_part + page_part + str(i)
#         # print(url_gen)
#     html = get_html(url_gen)
#     get_page_data(html) 

def main():
    start = datetime.now()
    url = 'https://lalafo.kg/kyrgyzstan/mobilnye-telefony-i-aksessuary/mobilnye-telefony'
    base_part = 'https://lalafo.kg/kyrgyzstan/mobilnye-telefony-i-aksessuary/mobilnye-telefony?'
    page_part = 'page=' 
    total_pages = get_total_pages(get_html(url))
    for i in range (1, total_pages+1):
        url_gen = base_part + page_part + str(i)
        # print(url_gen)
        html = get_html(url_gen)
        get_page_data(html) 
    end = datetime.now()
    time = end - start
    print (time)
if __name__ == '__main__':
    main()