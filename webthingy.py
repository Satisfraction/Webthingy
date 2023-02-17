import requests
from bs4 import BeautifulSoup
import csv

url = "https://www.cnn.com"
response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")

# Find all article headlines
headlines = soup.find_all("h3", class_="cd__headline")

# Write headlines to CSV file
with open("headlines.csv", "w", newline="") as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["Headlines"])
    for headline in headlines:
        writer.writerow([headline.get_text()])
