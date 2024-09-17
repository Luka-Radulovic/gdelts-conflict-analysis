import os
import json
import requests
import zipfile
import pandas as pd
import re
import jq
import numpy as np
import datetime
import time
from tqdm import tqdm
from names import col_names, mentions_col_names

country_codes: dict[str, str] = {}

with open(r"./data/06country_codes.txt", "r") as file:
    for line in file:
        code, *country = line.strip().split()
        country = " ".join(country)
        country_codes[code] = country

country_codes.pop("CODE")

country_codes["ROU"] = "Romania"

event_codes: dict[str, str] = {}

with open(r"./data/07event_codes.txt", "r") as file:
    for line in file:
        code, *event_description = line.strip().split()
        event_description = " ".join(event_description)
        event_codes[code] = event_description

event_codes.pop("CAMEOEVENTCODE")


def is_valid_country_code(code: str) -> bool:
    codes = country_codes.keys()
    return pd.notnull(code) and any([code in ccode for ccode in codes])


def format_time_yyyymmddhhmmss_to_str(
    year: str | int,
    month: str | int,
    day: str | int,
    hours: str | int,
    minutes: str | int = "00",
    seconds: str | int = "00",
) -> str:
    """
    Transform given date time to string.
    """
    times = list(map(str, [year, month, day, hours, minutes, seconds]))
    for i in range(len(times)):
        if len(times[i]) == 1:
            times[i] = "0" + times[i]

    return "".join(times)


def format_time_yyyymmdd_to_str(
    year: str | int, month: str | int, day: str | int
) -> str:
    """
    Transform given date to string.
    """
    times = list(map(str, [year, month, day]))
    for i in range(len(times)):
        if len(times[i]) == 1:
            times[i] = "0" + times[i]

    return "".join(times)


def format_str_yyyymmdd_to_time_str(x: str) -> str:
    return str(datetime.date(int(str(x)[:4]), int(str(x)[4:6]), int(str(x)[6:8])))


def load_gdelt_from_url(url: str) -> pd.DataFrame | None:
    """
    Load gdelt data from url on certain date time.
    """

    response = requests.get(url, stream=True)

    if response.status_code == 200:
        with open(r"./data/04temp_15min_data.zip", "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
    else:
        print(
            f"Failed to retrieve gdelt data for url: {url}. Status code: {response.status_code}"
        )
        return None

    with zipfile.ZipFile(r"./data/04temp_15min_data.zip", "r") as zip_ref:
        zip_ref.extractall(r"./data/")

    pattern = r"gdeltv2\/(.*?)\.export\.CSV\.zip"

    match = re.search(pattern, url)

    if not match:
        print(f"Failed to match regex. {url}")
        return None

    date_time = match.group(1)

    os.rename(r"./data/" + date_time + ".export.CSV", r"./data/05temp_15min_data.CSV")

    data = pd.read_csv(
        r"./data/05temp_15min_data.CSV",
        sep=r"\t",
        engine="python",
        header=None,
        names=col_names,
        dtype={"Event_Code": str},
    )

    os.remove(r"./data/04temp_15min_data.zip")
    os.remove(r"./data/05temp_15min_data.CSV")

    # Handle the cases for Montenegro, Slovenia, and Bosnia and Herzegovina
    mappings = {"MJ": "MNE", "SI": "SVN", "BK": "BIH"}
    data.loc[
        data["Actor_1_Country_ABBR"].isnull()
        & data["Actor_1_Geo_Country_Code"].isin(mappings),
        "Actor_1_Country_ABBR",
    ] = data["Actor_1_Geo_Country_Code"].map(mappings)
    data.loc[
        data["Actor_2_Country_ABBR"].isnull()
        & data["Actor_2_Geo_Country_Code"].isin(mappings),
        "Actor_2_Country_ABBR",
    ] = data["Actor_2_Geo_Country_Code"].map(mappings)

    # Handle the case for Romania
    data.loc[
        data["Actor_1_Country_ABBR"].isnull() & (data["Actor_1_Country_Code"] == "ROU"),
        "Actor_1_Country_ABBR",
    ] = "ROU"
    data.loc[
        data["Actor_2_Country_ABBR"].isnull() & (data["Actor_2_Country_Code"] == "ROU"),
        "Actor_2_Country_ABBR",
    ] = "ROU"

    # Drop the events where a country is absent
    data = data.dropna(subset=["Actor_1_Country_ABBR", "Actor_2_Country_ABBR"])

    # Drop the events where the country codes are equal
    data = data[data["Actor_1_Country_ABBR"] != data["Actor_2_Country_ABBR"]]

    # Filter only the countries/continents
    data = data[
        data[["Actor_1_Country_ABBR", "Actor_2_Country_ABBR"]]
        .map(is_valid_country_code)
        .all(axis=1)
    ]

    data = (
        # Get only the relevant columns of the data
        data[
            [
                "Global_Event_ID",
                "Day",
                "Actor_1_Country_ABBR",
                "Actor_2_Country_ABBR",
                "Event_Code",
                "Quad_Class",
                "Goldstein_Scale",
                "Num_Articles",  # 'AVG_TONE', 'Source_URL'
            ]
        ]
        # Filter only the events that happened in the wanted time-frame
        [data["Day"] == int(date_time[:8])].reset_index(drop=True)
    )

    mentions_url = url.replace("export", "mentions")

    response = requests.get(mentions_url, stream=True)

    if response.status_code == 200:
        with open(r"./data/04temp_15min_data.zip", "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
    else:
        print(
            f"Failed to retrieve gdelt data for url: {mentions_url}. Status code: {response.status_code}"
        )
        exit()

    with zipfile.ZipFile(r"./data/04temp_15min_data.zip", "r") as zip_ref:
        zip_ref.extractall(r"./data/")

    os.rename(r"./data/" + date_time + ".mentions.CSV", r"./data/05temp_15min_data.CSV")

    mentions_data = pd.read_csv(
        r"./data/05temp_15min_data.CSV",
        sep=r"\t",
        engine="python",
        header=None,
        names=mentions_col_names,
    )

    os.remove(r"./data/04temp_15min_data.zip")
    os.remove(r"./data/05temp_15min_data.CSV")

    mentions_data = (
        # Get only the relevant columns of the data
        mentions_data[["Global_Event_ID", "Confidence"]]
        # For the same event, get the confidence score by averaging all scores | WE MIGHT WANT MAX!!
        .groupby(by="Global_Event_ID", as_index=False)
        .aggregate("mean")
        .reset_index(drop=True)
    )

    mentions_data["Confidence"] = mentions_data["Confidence"].astype(int)

    return pd.merge(data, mentions_data, how="left", on="Global_Event_ID")


def load_gdelt_by_yyyymmddhhmmss(
    year: str | int,
    month: str | int,
    day: str | int,
    hours: str | int,
    minutes: str | int,
    seconds: str | int = "00",
) -> pd.DataFrame | None:
    """
    Load the gdelt events dataset logged on given date time.
    """
    date_time = format_time_yyyymmddhhmmss_to_str(year, month, day, hours, minutes)

    url = r"http://data.gdeltproject.org/gdeltv2/" + date_time + r".export.CSV.zip"

    return load_gdelt_from_url(url)


def load_gdelt_by_yyyymmdd(
    year: str | int, month: str | int, day: str | int
) -> pd.DataFrame | None:
    """
    Load the gdelt events dataset logged on given date.
    Equivalent to getting all 96 15-minute interval datasets on given date.
    """
    hours_list = list(range(24))
    minutes_list = list(range(0, 60, 15))

    data_frames = []
    for hours in hours_list:
        for minutes in minutes_list:
            data = load_gdelt_by_yyyymmddhhmmss(year, month, day, hours, minutes)
            if data is not None:
                data_frames.append(data)

    return pd.concat(data_frames, ignore_index=True)


def load_gdelt_from_to_yyyymmdd(
    year_from: str | int,
    month_from: str | int,
    day_from: str | int,
    year_to: str | int,
    month_to: str | int,
    day_to: str | int,
) -> pd.DataFrame | None:
    """
    Load the gdelt events dataset between selected days (inclusive).
    """
    start_date = format_time_yyyymmdd_to_str(year_from, month_from, day_from)
    end_date = format_time_yyyymmdd_to_str(year_to, month_to, day_to)

    with open(r"./data/03cleaned_events.json", "r") as file:
        json_data = json.dumps(json.load(file))

    # JQ query to filter URLs between the given dates
    jq_query = f'. | to_entries | map(select(.key >= "{start_date}" and .key <= "{end_date}")) | .[].value | .[] | .[]'

    urls = jq.compile(jq_query).input(text=json_data).all()

    data_frames = []
    for url in urls:
        data = load_gdelt_from_url(url)
        if data is not None:
            data_frames.append(data)

    return pd.concat(data_frames, ignore_index=True) if len(data_frames) > 0 else None


def custom_sigmoid(n: int) -> float:
    return 1 / (1 + 1 / (np.e ** ((n - 50) / 10)))


dateconfig = {}
with open("config.cfg") as file:
    dateconfig = json.load(file)

start_date = datetime.datetime.fromisoformat(dateconfig["from"])
end_date = datetime.datetime.fromisoformat(dateconfig["to"])

current_date = start_date
error_date = None
exponential_wait_time = 1

total_days = (end_date - start_date).days + 1

with tqdm(total=total_days) as pbar:

    while current_date <= end_date:
        dateconfig["from"] = current_date.isoformat()
        with open("config.cfg", "w") as file:
            json.dump(dateconfig, file)
        times = [current_date.year, current_date.month, current_date.day]
        try:
            current_data = load_gdelt_by_yyyymmdd(*times)
        except Exception as e:
            print(str(e))
            time.sleep(exponential_wait_time)

            if current_date == error_date:
                exponential_wait_time *= 2
            else:
                error_date = current_date
            continue

        exponential_wait_time = 1

        current_data["Country_Pairs"] = current_data.apply(
            lambda x: str(
                tuple(sorted([x["Actor_1_Country_ABBR"], x["Actor_2_Country_ABBR"]]))
            ),
            axis=1,
        )

        current_data["Event_Score"] = current_data["Goldstein_Scale"] * current_data[
            "Confidence"
        ].apply(lambda x: custom_sigmoid(x))

        current_data = (
            current_data.groupby(["Country_Pairs", "Day"])
            .aggregate(
                country_code_a=("Actor_1_Country_ABBR", "first"),
                country_code_b=("Actor_2_Country_ABBR", "first"),
                relations_score=("Event_Score", "mean"),
                num_verbal_coop=("Quad_Class", lambda x: (x == 1).sum()),
                num_material_coop=("Quad_Class", lambda x: (x == 2).sum()),
                num_verbal_conf=("Quad_Class", lambda x: (x == 3).sum()),
                num_material_conf=("Quad_Class", lambda x: (x == 4).sum()),
            )
            .reset_index()
        )

        current_data = current_data.drop(columns="Country_Pairs")
        current_data = current_data.rename(columns={"Day": "date"})
        current_data["date"] = current_data["date"].apply(
            lambda x: format_str_yyyymmdd_to_time_str(str(x))
        )

        current_data.to_csv("process_1day.csv")

        BATCH_SIZE = 1000
        for i in range(0, current_data.shape[0], BATCH_SIZE):
            try:
                response = requests.post(
                    url=r"http://localhost:8000/api/v1/relations/",
                    data=current_data.loc[i:i+BATCH_SIZE-1].to_json(orient='records'),
                    headers={"x-key": os.getenv("API_KEY")},
                )
            except Exception:
                print(response.content)
        # for row in current_data.index:
        #     data_to_post = current_data.iloc[row].to_json()

        #     try:
        #         response = requests.post(
        #             url=r"http://127.0.0.1:8000/api/v1/relations/",
        #             data=data_to_post,
        #             headers={"x-key": os.getenv("API_KEY")},
        #         )

        #     except Exception:
        #         print(response.content)
        #         continue

        #     try:
        #         response = requests.post(
        #             url=r"https://gdelt-api-staging.filipovski.net/api/v1/relations/",
        #             data=data_to_post,
        #             headers={"x-key": os.getenv("API_KEY")},
        #         )

        #     except Exception:
        #         print(response.content)
        #         continue

        pbar.update(1)
        current_date += datetime.timedelta(days=1)
