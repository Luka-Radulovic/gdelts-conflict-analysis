import os
import json
import requests
import datetime
import time
from tqdm import tqdm

from utils import (
    custom_sigmoid,
    format_str_yyyymmdd_to_time_str,
    load_gdelt_by_yyyymmdd,
)


def execute_script():
    # Global configuration
    config = {}
    with open("config.cfg") as file:
        config = json.load(file)

    RECORD_RESPONSES = config["record"]
    if RECORD_RESPONSES:
        print(
            "WARNING: You are now only recording events! Results from processing won't be posted to API!"
        )

    start_date = datetime.datetime.fromisoformat(config["from"])
    end_date = datetime.datetime.fromisoformat(config["to"])

    current_date = start_date
    error_date = None
    exponential_wait_time = 1

    total_days = (end_date - start_date).days + 1

    with tqdm(total=total_days) as pbar:

        while current_date <= end_date:
            config["from"] = current_date.isoformat()
            with open("config.cfg", "w") as file:
                json.dump(config, file)
            times = [current_date.year, current_date.month, current_date.day]
            try:
                current_data = load_gdelt_by_yyyymmdd(*times, RECORD_RESPONSES)
            except ValueError as e:
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
                    tuple(
                        sorted([x["Actor_1_Country_ABBR"], x["Actor_2_Country_ABBR"]])
                    )
                ),
                axis=1,
            )

            current_data["Event_Score"] = current_data[
                "Goldstein_Scale"
            ] * current_data["Confidence"].apply(lambda x: custom_sigmoid(x))

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

            if not RECORD_RESPONSES:
                BATCH_SIZE = 1000
                for i in range(0, current_data.shape[0], BATCH_SIZE):
                    response = requests.post(
                        url=r"http://localhost:8000/api/v1/relations/",
                        data=current_data.loc[i : i + BATCH_SIZE - 1].to_json(
                            orient="records"
                        ),
                        headers={"x-key": os.getenv("API_KEY")},
                    )

            pbar.update(1)
            current_date += datetime.timedelta(days=1)
