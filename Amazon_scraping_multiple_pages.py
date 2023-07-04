import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd


headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"}

data_list = []


def get_soup(url):
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup


def scrape_data_list(url):
    soup = get_soup(url)
    global data_list
    data_list = []
    data = soup.find_all('li', class_='a-list-normal')
    for data_item in data:
        d = data_item.get_text(strip=True)
        data_list.append(d)


def scrape_titles(url):
    # collecting titles
    scrape_data_list(url)
    title_list = []
    for i in range(0, len(data_list), 3):
        title_list.append(data_list[i])
    return title_list


def scrape_prices(url):
    # collecting prices
    scrape_data_list(url)
    price_list = []
    for i in range(2, len(data_list), 3):
        price_list.append(data_list[i])
    # remove 'to buy' from price
    for price in range(len(price_list)):
        price_list[price] = price_list[price].replace('to buy', '')
    return price_list


def scrape_rating(url):
    # collecting rating stars data
    scrape_data_list(url)
    rating_list = []
    for i in range(1, len(data_list), 3):
        rating_list.append(data_list[i][0:3])
    return rating_list


def scrape_total_sells(url):
    # collecting  purchases
    scrape_data_list(url)
    purchase_list = []
    for i in range(1, len(data_list), 3):
        purchase_list.append(data_list[i][10:-1])
    return purchase_list


def scrape_multiple_pages(start_page, end_page):
    base_url = "https://www.amazon.com/kindle-dbs/browse/ref=dbs_b_def_rwt_brws_ts_recs_pg_{}?metadata=cardAppType%3ADESKTOP%24deviceTypeID%3AA2Y8LFC259B97P%24clientRequestId%3AZYK0P7RTS4QNFTN4FVQD%24deviceAppType%3ADESKTOP%24ipAddress%3A10.162.117.170%24browseNodes%3A154606011%24userAgent%3AMozilla%2F5.0+%28Macintosh%3B+Intel+Mac+OS+X+10_15_7%29+AppleWebKit%2F537.36+%28KHTML%2C+like+Gecko%29+Chrome%2F114.0.0.0+Safari%2F537.36%24cardSurfaceType%3Adesktop%24cardMobileOS%3AUnknown%24deviceSurfaceType%3Adesktop&storeType=ebooks&widgetId=unified-ebooks-storefront-default_TopSellersStrategy&sourceAsin=&content-id=amzn1.sym.bb33addf-488a-4e99-909f-3acc87146400&refTagFromService=ts&title=Best+sellers+&pf_rd_p=bb33addf-488a-4e99-909f-3acc87146400&sourceType=recs&pf_rd_r=ZYK0P7RTS4QNFTN4FVQD&pd_rd_wg=zphWA&ref_=dbs_f_def_rwt_wigo_ts_recs_wigo&SkipDeviceExclusion=true&pd_rd_w=6nYAH&nodeId=154606011&pd_rd_r=dae2466c-6d6d-4195-a48f-6bde8a306b42&page={{}}"

    all_titles = []
    all_prices = []
    all_ratings = []
    all_purchases = []

    for page_number in range(start_page, end_page + 1):
        url = base_url.format(page_number)
        titles = scrape_titles(url)
        prices = scrape_prices(url)
        ratings = scrape_rating(url)
        purchases = scrape_total_sells(url)

        all_titles.extend(titles)
        all_prices.extend(prices)
        all_ratings.extend(ratings)
        all_purchases.extend(purchases)
    # Store the data in a CSV file
    header = ['Title', 'Price', 'Rating', 'Total Purchases']
    with open('best_sellers_books_multiple.csv', 'w', newline='', encoding='UTF-8') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        for i in range(len(all_titles)):
            row = [all_titles[i], all_prices[i], all_ratings[i], all_purchases[i]]
            writer.writerow(row)


# Scrape pages 1 to 4
scrape_multiple_pages(1, 4)


pd.set_option('display.max.columns', None)
df = pd.read_csv(r'/Users/imac/PycharmProjects/pythonProject/best_sellers_books_multiple.csv')

print(df)

















