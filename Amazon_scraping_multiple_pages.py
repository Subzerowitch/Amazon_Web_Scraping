import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
import unittest
import math
from fake_user_agent import user_agent

data_list = []

base_url = "https://www.amazon.com/kindle-dbs/browse/ref=dbs_b_def_rwt_brws_ts_recs_pg_{}?metadata=cardAppType%3ADESKTOP%24deviceTypeID%3AA2Y8LFC259B97P%24clientRequestId%3A%24deviceAppType%3ADESKTOP%24ipAddress%3A%24browseNodes%3A154606011%24userAgent%3A%2F5.0+%28Macintosh%3B+Intel+Mac+OS+X+10_15_7%29+AppleWebKit%2F537.36+%28KHTML%2C+like+Gecko%29+Chrome%2F114.0.0.0+Safari%2F537.36%24cardSurfaceType%3Adesktop%24cardMobileOS%3AUnknown%24deviceSurfaceType%3Adesktop&storeType=ebooks&widgetId=unified-ebooks-storefront-default_TopSellersStrategy&sourceAsin=&content-id=amzn1.sym.bb33addf-488a-4e99-909f-3acc87146400&refTagFromService=ts&title=Best+sellers+&pf_rd_p=bb33addf-488a-4e99-909f-3acc87146400&sourceType=recs&pf_rd_r=ZYK0P7RTS4QNFTN4FVQD&pd_rd_wg=zphWA&ref_=dbs_f_def_rwt_wigo_ts_recs_wigo&SkipDeviceExclusion=true&pd_rd_w=6nYAH&nodeId=154606011&pd_rd_r=dae2466c-6d6d-4195-a48f-6bde8a306b42&page={{}}"


def get_soup(url):
    # getting soup
    user_Agent = user_agent()
    headers = {"User Agent": user_Agent}
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup


def scrape_data_list(url):
    # scrape data to a list
    soup = get_soup(url)
    global data_list
    data_list = []
    data = soup.find_all('li', class_='a-list-normal')
    for data_item in data:
        d = data_item.get_text(strip=True)
        data_list.append(d)
    return data_list


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
        price = data_list[i].replace('to buy', '').strip()
        price_list.append(price if price != '' else None)
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
    # store the data in a CSV file
    header = ['Title', 'Price', 'Rating', 'Total Purchases']
    with open('best_sellers_books_multiple.csv', 'w', newline='', encoding='UTF-8') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        for i in range(len(all_titles)):
            row = [all_titles[i], all_prices[i], all_ratings[i], all_purchases[i]]
            writer.writerow(row)


# scrape pages 1 to 4, uncomment to scrape before test runs
# scrape_multiple_pages(1, 4)

pd.set_option('display.max.columns', None)
df = pd.read_csv(r'/Users/imac/PycharmProjects/pythonProject/best_sellers_books_multiple.csv')

print(df)


class TestScrapingFunctions(unittest.TestCase):

    """
    This function will assert error if there were NaN values scraped and where.
    Uncomment its call under each function to see missing values
    """
    def assert_if_nan_values(self, data, data_title):
        for item in data:
            if isinstance(item, (int, float)):
                self.assertIsNotNone(item, f"Scraped {data_title} should not be None")
                self.assertFalse(math.isnan(item), f'Scraped {data_title} should not be NaN')
            elif isinstance(item, str):
                self.assertNotEqual(item.strip(), '', f'Scraped {data_title} should not be an empty string')
            else:
                self.fail(f"Unexpected data type: {type(item)}")

    def test_scrape_titles(self):
        # test scraping titles
        for page_number in range(1, 5):
            url = base_url.format(page_number)
            titles = scrape_titles(url)
            self.assertTrue(len(titles) > 0)  # check if any titles are scraped
        # self.assert_if_nan_values(titles, "titles")

    def test_scrape_prices(self):
        # test scraping prices
        for page_number in range(1, 5):
            url = base_url.format(page_number)
            prices = scrape_prices(url)
            self.assertTrue(len(prices) > 0)  # check if any prices are scraped
        # self.assert_if_nan_values(prices, "prices")

    def test_scrape_rating(self):
        # test scraping ratings
        for page_number in range(1, 5):
            url = base_url.format(page_number)
            ratings = scrape_rating(url)
            self.assertTrue(len(ratings) > 0)  # check if any ratings are scraped
        # self.assert_if_nan_values(ratings, "ratings")

    def test_scrape_total_sells(self):
        # test scraping total purchases
        for page_number in range(1, 5):
            url = base_url.format(page_number)
            total_sells = scrape_total_sells(url)
            self.assertTrue(len(total_sells) > 0)  # check if any total sells data are scraped
        # self.assert_if_nan_values(total_sells, "total sells")


if __name__ == '__main__':
    unittest.main()
