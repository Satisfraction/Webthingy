# Webthingy - Web Scraper Tool Documentation

## Description
This is a PyQt5 GUI application for web scraping. The application imports necessary modules such as csv, sys, requests, BeautifulSoup, and ThreadPoolExecutor. The GUI contains a main window (Webthingy) with several widgets such as labels, text boxes, buttons, and a text editor for displaying output.

## Usage

1. Enter the website URL in the URL textbox.
2. Select an HTML tag from the dropdown list.
3. Click on the "Scrape" button to retrieve data from the website.
4. The scraped data will be displayed in the output textbox.
5. Click on the "Save CSV" button to save the data to a CSV file.
6. Click on the "Save PDF" button to save the data to a PDF file.

## Methods

### scrape_website(self)
The `scrape_website()` method is called when the "Scrape" button is clicked. It retrieves the URL and HTML tag selected by the user from the corresponding widgets. It then uses the requests module to get the webpage content and the BeautifulSoup module to parse the HTML. It finds all the HTML tags matching the selected tag and processes them using a ThreadPoolExecutor. The results are stored in a list and used to populate the CSV and PDF data for saving. 

### save_to_csv(self)
The `save_to_csv()` method is called when the "Save CSV" button is clicked. It opens a file dialog to choose the file path and saves the CSV data in the selected format.

### save_to_pdf(self)
The `save_to_pdf()` method is called when the "Save PDF" button is clicked. It opens a file dialog to choose the file path and saves the PDF data in the selected format.

## Widgets
The following widgets are present in the main window:

- `url_label`: QLabel widget for displaying "Enter website URL:" text.
- `url_textbox`: QLineEdit widget for entering the website URL.
- `tag_label`: QLabel widget for displaying "Select HTML tag:" text.
- `tag_combobox`: QComboBox widget for selecting the HTML tag.
- `scrape_button`: QPushButton widget for triggering web scraping.
- `save_csv_button`: QPushButton widget for saving the data as CSV.
- `save_pdf_button`: QPushButton widget for saving the data as PDF.
- `output_label`: QLabel widget for displaying "Output:" text.
- `output_textbox`: QTextEdit widget for displaying the scraped data.

## Dependencies
- csv
- sys
- requests
- BeautifulSoup
- ThreadPoolExecutor
- PyQt5
- PyQt5.QtWidgets
- PyQt5.QtGui
- PyQt5.QtCore
- PyQt5.QtPrintSupport

## Author: 

Satisfraction

## License: 

This program is licensed under the MIT License. See the LICENSE file for more information.
