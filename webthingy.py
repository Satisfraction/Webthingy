import csv
import sys
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QTextEdit, QPushButton, QComboBox, QFileDialog
from PyQt5.QtGui import QIcon, QFont, QTextDocument, QPixmap
from PyQt5.QtCore import Qt, QIODevice, QFile, QUrl
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog


class Webthingy(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set window title, icon and background color
        self.setWindowTitle('Webthingy - the Web Scraper Tool')
        self.setWindowIcon(QIcon('icon.png'))
        self.setStyleSheet("background-color: #1c1c1c; color: #ffffff;")

        # Create widgets and set their properties
        font = QFont('Roboto', 12)

        self.url_label = QLabel('Enter website URL:')
        self.url_label.setFont(font)

        self.url_textbox = QLineEdit()
        self.url_textbox.setFont(font)
        self.url_textbox.setStyleSheet("background-color: #252525; color: #ffffff;")

        self.tag_label = QLabel('Select HTML tag:')
        self.tag_label.setFont(font)

        self.tag_combobox = QComboBox()
        self.tag_combobox.setFont(font)
        self.tag_combobox.setStyleSheet("background-color: #252525; color: #ffffff;")
        self.tag_combobox.addItems(['p', 'a', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'img'])

        self.scrape_button = QPushButton('Scrape')
        self.scrape_button.setFont(font)
        self.scrape_button.setStyleSheet("background-color: #d35400; color: #ffffff;")
        self.scrape_button.clicked.connect(self.scrape_website)

        self.save_csv_button = QPushButton('Save CSV')
        self.save_csv_button.setFont(font)
        self.save_csv_button.setStyleSheet("background-color: #2980b9; color: #ffffff;")
        self.save_csv_button.setEnabled(False)
        self.save_csv_button.clicked.connect(self.save_to_csv)

        self.save_pdf_button = QPushButton('Save PDF')
        self.save_pdf_button.setFont(font)
        self.save_pdf_button.setStyleSheet("background-color: #27ae60; color: #ffffff;")
        self.save_pdf_button.setEnabled(False)
        self.save_pdf_button.clicked.connect(self.save_to_pdf)

        self.output_label = QLabel('Output:')
        self.output_label.setFont(font)

        self.output_textbox = QTextEdit()
        self.output_textbox.setFont(font)
        self.output_textbox.setStyleSheet("background-color: #252525; color: #ffffff;")
        self.output_textbox.setReadOnly(True)

        # Create layout and add widgets to it
        layout = QVBoxLayout()

        url_layout = QHBoxLayout()
        url_layout.addWidget(self.url_label)
        url_layout.addWidget(self.url_textbox)
        layout.addLayout(url_layout)

        tag_layout = QHBoxLayout()
        tag_layout.addWidget(self.tag_label)
        tag_layout.addWidget(self.tag_combobox)
        layout.addLayout(tag_layout)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.scrape_button)
        button_layout.addWidget(self.save_csv_button)
        button_layout.addWidget(self.save_pdf_button)
        layout.addLayout(button_layout)

        layout.addWidget(self.output_label)
        layout.addWidget(self.output_textbox)

        main_widget = QWidget()
        main_widget.setLayout(layout)
        main_widget.setStyleSheet("padding: 20px;")
        self.setCentralWidget(main_widget)

        # Initialize data containers
        self.csv_data = None
        self.pdf_data = None

        # Initialize session object
        self.session = requests.Session()



    def scrape_website(self):
        # Get website URL and selected HTML tag from the UI
        url = self.url_textbox.text()
        tag = self.tag_combobox.currentText()

        # Check if website URL is valid
        if not url.startswith('http'):
            self.output_textbox.append('Error: Invalid website URL.')
            return

        try:
            # Send GET request to website URL and get response object
            response = self.session.get(url)

            # Create BeautifulSoup object and find all tags matching the selected HTML tag
            soup = BeautifulSoup(response.text, 'html.parser')
            tag_list = soup.find_all(tag)

            # Use a thread pool to parallelize the scraping process
            with ThreadPoolExecutor() as executor:
                # Define a function to process each tag
                def process_tag(tag):
                    if tag.name == 'img':
                        img_src = tag['src']
                        self.output_textbox.append(img_src)
                        return [url, tag.name, img_src]
                    else:
                        tag_text = tag.text.strip()
                        self.output_textbox.append(tag_text)
                        return [url, tag.name, tag_text]

                # Process tags in parallel and collect the results
                results = list(executor.map(process_tag, tag_list))
                self.csv_data = [['URL', 'Tag', 'Text']] + results
                self.save_csv_button.setEnabled(True)
                self.pdf_data = '<br>'.join((f"{result[1]}: {result[2]}" for result in results))
                self.save_pdf_button.setEnabled(True)

        except requests.exceptions.RequestException as e:
            # Handle request exception
            self.output_textbox.append(f'Error: {e}')

    def save_to_csv(self):
        # Get file path to save CSV
        filepath, _ = QFileDialog.getSaveFileName(self, 'Save CSV', '', 'CSV Files (*.csv)')

        # Check if file path is valid
        if not filepath:
            return

        # Open file for writing and write CSV data
        with open(filepath, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(self.csv_data)

        self.output_textbox.append(f'CSV saved to {filepath}.')

    def save_to_pdf(self):
        # Get file path to save PDF
        filepath, _ = QFileDialog.getSaveFileName(self, 'Save PDF', '', 'PDF Files (*.pdf)')

        # Check if file path is valid
        if not filepath:
            return

        # Create PDF document and add data
        document = QTextDocument()
        document.setHtml(self.pdf_data)

        # Create printer and print dialog
        printer = QPrinter()
        printer.setOutputFormat(QPrinter.PdfFormat)
        printer.setOutputFileName(filepath)
        dialog = QPrintDialog(printer)

        # If dialog is accepted, print document to printer
        if dialog.exec() == QPrintDialog.Accepted:
            document.print_(printer)

        self.output_textbox.append(f'PDF saved to {filepath}.')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = Webthingy()
    gui.show()
    sys.exit(app.exec_())
