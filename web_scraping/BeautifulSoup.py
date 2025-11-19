import requests
import json
from bs4 import BeautifulSoup

url = "https://books.toscrape.com/"

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

link_data = []

for link in soup.find_all("a"):
    href = link.get("href")  
    text = link.text.strip()

    if href:
        link_data.append({
            "text": text,
            "url": href
        })

with open("links.json", "w") as f:
    json.dump(link_data, f, indent=4)

print(" Success! All links saved to links.json")