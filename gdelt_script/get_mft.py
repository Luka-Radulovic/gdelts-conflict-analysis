import json
import os
from pathlib import Path
import re
import pandas as pd
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

pattern = r"http:\/\/data.gdeltproject.org\/gdeltv2\/(.*?)\.export\.CSV\.zip"
last_date_time = None

with (
    open("./data/01events.txt", "r") as in_file,
    open("./data/02relevant_events.json", "w") as out_file,
):
    out_file.write("{\n")

    for line in in_file:
        try:
            line_url = line.strip().split()[2]
            if not line_url.__contains__("export"):
                continue  # We skip mentions and gkg's

            match = re.search(pattern, line_url)

            if not match:
                print("Failed to match regex.")
                continue

            date_time = match.group(1)

            if not last_date_time:  # We write a temporary JSON file
                out_file.write('"' + date_time[:8] + '":[\n')
                out_file.write('{"' + date_time[8:12] + '":"' + line_url + '"}')

            elif date_time[:8] != last_date_time:
                out_file.write("\n],\n")
                out_file.write('"' + date_time[:8] + '":[\n')
                out_file.write('{"' + date_time[8:12] + '":"' + line_url + '"}')

            else:
                out_file.write(",\n")
                out_file.write('{"' + date_time[8:12] + '":"' + line_url + '"}')

            last_date_time = date_time[:8]
        except (
            Exception
        ):  # The line of data retrieved from the webpage is irregular and can be skipped
            # print(f'Corrupt line in 01events.txt containing the following line: {line}')
            continue

    out_file.write("]\n}\n")


def multidict(ordered_pairs):
    data = {}

    for key, value in ordered_pairs:
        if len(key) == 4:
            data[key] = value
            continue

        if not data.get(key):
            data[key] = []
        data[key].extend(value)

    return data


with (
    open("./data/02relevant_events.json", "r") as in_file,
    open("./data/03cleaned_events.json", "w") as out_file,
):
    data = json.load(in_file, object_pairs_hook=multidict)
    json.dump(data, out_file, indent=1)

if not os.path.exists(r"./data/03cleaned_events.json"):
    raise Exception(
        "There is no data to preprocess. Please run the cells in the Data Retrieval section."
    )

pd.set_option("display.max_columns", None)


url = "https://www.gdeltproject.org/data/lookups/CAMEO.country.txt"

response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, "html.parser")

    with open(r"./data/06country_codes.txt", "w") as file:
        file.write(soup.prettify())
else:
    print(
        f"Failed to retrieve gdelt country codes. Status code: {response.status_code}"
    )

url = "https://www.gdeltproject.org/data/lookups/CAMEO.eventcodes.txt"

response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, "html.parser")

    with open(r"./data/07event_codes.txt", "w") as file:
        file.write(soup.prettify())
else:
    print(f"Failed to retrieve gdelt event codes. Status code: {response.status_code}")
