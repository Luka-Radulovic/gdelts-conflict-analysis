import matplotlib as plt
import pandas as pd
import requests

days = requests.get(
    "http://localhost:8000/api/v1/relations",
    params={"country_code_a": "USA", "country_code_b": "RUS"},
).json()

df = pd.DataFrame(days)
df = df[df["date"] > "2022-01-01"]
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date")
df["summary"] = (
    df["num_verbal_coop"]
    + df["num_material_coop"]
    + df["num_verbal_conf"]
    + df["num_material_conf"]
)
print(df)
