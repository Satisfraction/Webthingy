# Webthingy

Webthingy is a desktop application built with PyQt5 and BeautifulSoup libraries for scraping website data. The user can enter a website URL and select an HTML tag to scrape data from. The scraped data is displayed in the output textbox and can be saved to a CSV or PDF file.

To use the application, follow these steps:

1. Enter the website URL in the URL textbox.
2. Select an HTML tag from the dropdown list.
3. Click on the "Scrape" button to retrieve data from the website.
4. The scraped data will be displayed in the output textbox.
5. Click on the "Save CSV" button to save the data to a CSV file.
6. Click on the "Save PDF" button to save the data to a PDF file.

!!! Note: The URL must start with "http" or "https" to be considered valid. !!!

Changes made to the original code:

- Fixed error handling for invalid URLs / HTML tags
- Minor style changes

To run the program, you need to have Python and the following libraries installed:

PyQt5
requests
BeautifulSoup4
To install the required libraries, run the following command in your terminal:
pip install PyQt5 requests beautifulsoup4

To launch the program, run the following command in your terminal:
python webthingy.py

Author: Satisfraction 

Lizenz:
This program is licensed under the MIT License. See the LICENSE file for more information.