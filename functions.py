import csv
import requests
from bs4 import BeautifulSoup
from PyQt5.QtCore import QThread, pyqtSignal


class ScraperThread(QThread):
    success = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, url, selector=None):
        super().__init__()
        self.url = url
        self.selector = selector

    def run(self):
        try:
            response = requests.get(self.url)
            if response.status_code != 200:
                self.error.emit("Error: Invalid URL")
                return

            html = response.text
            if self.selector is not None:
                soup = BeautifulSoup(html, 'html.parser')
                html = str(soup.select_one(self.selector))

            self.success.emit(html)
        except Exception as e:
            self.error.emit(f"Error: {str(e)}")


def save_output(output_edit):
    filename, _ = QFileDialog.getSaveFileName(None, "Save Output", "", "CSV Files (*.csv)")
    if filename:
        with open(filename, "w", newline="") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["Headlines"])
            for line in output_edit.toPlainText().split("\n"):
                writer.writerow([line])
        output_edit.clear()
        

