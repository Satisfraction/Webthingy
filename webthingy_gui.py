# WebThingy

import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit, QTextEdit, QGridLayout, QComboBox
from functions import ScraperThread, save_output, BeautifulSoup


class WebthingyGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Webthingy")

        # Create GUI elements
        self.url_label = QLabel("URL:")
        self.url_edit = QLineEdit()
        self.run_button = QPushButton("Run")
        self.output_label = QLabel("Output:")
        self.output_edit = QTextEdit()
        self.save_button = QPushButton("Save")
        self.quit_button = QPushButton("Quit")
        self.selector_label = QLabel("CSS Selector:")
        self.selector_dropdown = QComboBox()
        
        # Set layout
        grid = QGridLayout()
        grid.addWidget(self.url_label, 0, 0)
        grid.addWidget(self.url_edit, 0, 1)
        grid.addWidget(self.selector_label, 0, 2)
        grid.addWidget(self.selector_dropdown, 0, 3)
        grid.addWidget(self.run_button, 0, 4)
        grid.addWidget(self.output_label, 1, 0)
        grid.addWidget(self.output_edit, 1, 1, 1, 4)
        grid.addWidget(self.save_button, 2, 3)
        grid.addWidget(self.quit_button, 2, 4)
        self.setLayout(grid)

        # Create scraper thread
        self.scraper_thread = None

        # Connect signals to slots
        self.run_button.clicked.connect(self.start_scraper)
        self.save_button.clicked.connect(lambda: save_output(self.output_edit))
        self.quit_button.clicked.connect(self.close)
        self.selector_dropdown.currentIndexChanged.connect(self.start_scraper)

    def start_scraper(self):
        url = self.url_edit.text()
        if not url:
            return

        selector = self.selector_dropdown.currentText()

        # Disable the Run button while scraping
        self.run_button.setEnabled(False)

        # Create and start scraper thread
        self.scraper_thread = ScraperThread(url, selector)
        self.scraper_thread.success.connect(self.display_output)
        self.scraper_thread.error.connect(self.display_error)
        self.scraper_thread.finished.connect(self.scraper_finished)
        self.scraper_thread.start()

    def display_output(self, output):
        self.output_edit.setText(output)

    def display_error(self, error):
        self.output_edit.setText(str(error))

    def scraper_finished(self):
        # Re-enable the Run button
        self.run_button.setEnabled(True)

    def update_selector_dropdown(self, selectors):
        self.selector_dropdown.clear()
        self.selector_dropdown.addItems(selectors)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = WebthingyGUI()
    gui.show()

    # Find selectors
    url = "https://www.google.com"
    try:
        response = requests.get(url)
        if response.status_code != 200:
            gui.display_error("Error: Invalid URL")
            sys.exit(app.exec_())

        soup = BeautifulSoup(response.text, 'html.parser')
        selectors = [el.name for el in soup.find_all()]
        gui.update_selector_dropdown(selectors)
    except Exception as e:
        gui.display_error(f"Error: {str(e)}")
        sys.exit(app.exec_())

    sys.exit(app.exec_())
