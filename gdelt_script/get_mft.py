from pathlib import Path
import requests
from bs4 import BeautifulSoup

Path("./data").mkdir(parents=True, exist_ok=True)

url = "http://data.gdeltproject.org/gdeltv2/masterfilelist.txt"

response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, "html.parser")

    with open("./data/01events.txt", "w") as file:
        file.write(soup.prettify())
else:
    print(f"Failed to retrieve gdelt data /w code: {response.status_code}")
