import json
import os
import requests


with open("gdelt_frontend/src/assets/countries.json") as f:
    countries = json.load(f)
    isos = {
        feature["properties"]["ISO_A3"]: feature["properties"]["ADMIN"]
        for feature in countries["features"]
    }
    other_cc = requests.get(
        url=r"https://gdelt-api-staging.filipovski.net/api/v1/relations/",
        headers={
            "x-key": os.getenv("API_KEY")
        },
        params={"date_from": "2019-01-01", "date_to": "2020-01-01"},
    ).content
    other_cc = json.loads(other_cc)
    s1 = {oc["country_code_a"] for oc in other_cc}
    s2 = {oc["country_code_b"] for oc in other_cc}
    mentioned = s1.union(s2)
    unmentioned = {k: v for k, v in isos.items() if k not in mentioned}
    nopandan = [m for m in mentioned if m not in isos]
    with open("unmentioned.json", "w") as f:
        json.dump(unmentioned, f, indent=2)
    with open("nopandan.json", "w") as f:
        json.dump(nopandan, f, indent=2)
    pass
