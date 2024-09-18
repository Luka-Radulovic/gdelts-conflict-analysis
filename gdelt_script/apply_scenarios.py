import json
import os

import requests

from main import execute_script


scenarios = [
    {
        "name": "Vtora vojna vo Nagorno-Karabah (Prelude)",
        "from": "2020-09-24",
        "to": "2020-09-29",
    },
    {
        "name": "Vtora vojna vo Nagorno-Karabah (Aftermath)",
        "from": "2020-11-10",
        "to": "2020-11-15",
    },
    {
        "name": "Kirgistansko-tadzikistanski sudiri",
        "from": "2021-04-25",
        "to": "2021-05-03",
    },
    {
        "name": "Vojna vo Gaza, 2021 (Prelude)",
        "from": "2021-05-01",
        "to": "2021-05-10",
    },
    {
        "name": "Vojna vo Gaza, 2021 (Aftermath)",
        "from": "2021-05-20",
        "to": "2021-05-25",
    },
    {"name": "Ruska invazija na Ukraina", "from": "2022-02-20", "to": "2022-02-28"},
    {"name": "Vojna vo Gaza, 2023", "from": "2023-10-04", "to": "2023-10-10"},
]


for scenario in scenarios:
    scenario["record"] = False
    with open("config.cfg", "w") as f:
        json.dump(scenario, f)
    requests.delete(
        "http://localhost:8000/api/v1/relations",
        params={"date_from": scenario["from"], "date_to": scenario["to"]},
        headers={"x-key": os.getenv("API_KEY")},
    )
    execute_script()
