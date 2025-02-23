import datetime
import os
from pathlib import Path
import re
import zipfile
import numpy as np
import pandas as pd
import requests
from names import col_names, mentions_col_names

country_codes: dict[str, str] = {}

with open(r"./data/06country_codes.txt", "r") as file:
    for line in file:
        code, *country = line.strip().split()
        country = " ".join(country)
        country_codes[code] = country

country_codes.pop("CODE")

country_codes["ROU"] = "Romania"
country_codes["MNE"] = "Montenegro"

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


def load_gdelt_from_url(url: str, RECORD_RESPONSES: bool) -> pd.DataFrame | None:
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
    # TODO: Check if removing this step fixes anything.
    # data = data[
    #     data[["Actor_1_Country_ABBR", "Actor_2_Country_ABBR"]]
    #     .map(is_valid_country_code)
    #     .all(axis=1)
    # ]

    if not RECORD_RESPONSES:
        # Get only the relevant columns of the data
        data = data[
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

    data = data[data["Day"] == int(date_time[:8])].reset_index(drop=True)

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
    RECORD_RESPONSES: bool,
    seconds: str | int = "00",
) -> pd.DataFrame | None:
    """
    Load the gdelt events dataset logged on given date time.
    """
    date_time = format_time_yyyymmddhhmmss_to_str(year, month, day, hours, minutes)

    url = r"http://data.gdeltproject.org/gdeltv2/" + date_time + r".export.CSV.zip"

    return load_gdelt_from_url(url, RECORD_RESPONSES)


def load_gdelt_by_yyyymmdd(
    year: str | int, month: str | int, day: str | int, RECORD_RESPONSES: bool
) -> pd.DataFrame | None:
    """
    Load the gdelt events dataset logged on given date.
    Equivalent to getting all 96 15-minute interval datasets on given date.
    """
    hours_list = list(range(24))
    minutes_list = list(range(0, 60, 15))

    RECORD_PATH = Path(f"{Path(__file__).parent}/scenarios")
    RECORD_PATH.mkdir(exist_ok=True, parents=True)
    filename = format_time_yyyymmdd_to_str(year, month, day) + ".csv"
    file_path = Path(f"{RECORD_PATH}/{filename}")

    if Path.exists(file_path):
        return pd.read_csv(file_path)

    data_frames = []
    for hours in hours_list:
        for minutes in minutes_list:
            data = load_gdelt_by_yyyymmddhhmmss(year, month, day, hours, minutes, RECORD_RESPONSES)
            if data is not None:
                data_frames.append(data)

    result = pd.concat(data_frames, ignore_index=True)
    if RECORD_RESPONSES:
        result.to_csv(file_path)

    return result


def custom_sigmoid(n: int) -> float:
    return 1 / (1 + 1 / (np.e ** ((n - 50) / 10)))
