# Amazon_Web_Scraping
 Scraping Best Sellers books info from amazon.com
 
**Amazon Best Sellers Data Scraper**
 
This Python script allows you to scrape data from the Amazon Best Sellers page for Kindle eBooks. It collects information such as book titles, prices, ratings, and total purchases from multiple pages and saves the data into a CSV file for further analysis.

**Libraries Used:**

 -requests: Used to send HTTP requests to the Amazon website and fetch the HTML content of the pages.

 -BeautifulSoup: Used for parsing the HTML content and extracting relevant information from the web pages.

 -csv: Used for reading and writing data to CSV files.

 -pandas: Used for data manipulation and analysis. It is used to read the data from the CSV file and create a DataFrame for easy data handling.

 -unittest: Used for writing and running test cases to ensure the correctness of the scraping functions.

 -fake_user_agent: Used to generate a fake user agent for the requests headers to avoid being blocked by Amazon's anti-scraping measures.


**Testing**

 The script also includes test functions to check if the scraping functions are working correctly. 

**Contribution**

 Contributions to this project are welcome. If you find any issues or have suggestions for improvements, feel free to create a pull request or open an issue.
