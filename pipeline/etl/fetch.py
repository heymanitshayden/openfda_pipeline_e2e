import requests
import json
import time
from pathlib import Path

OPENFDA_ENDPOINT = "https://api.fda.gov/drug/event.json"
RATE_LIMIT_DELAY = 0.3
DEFAULT_LIMIT = 100
DEFAULT_TOTAL = 1000
DEFAULT_OUTPUT_DIR = "data"

def fetch_adverse_events(limit=DEFAULT_LIMIT, total=DEFAULT_TOTAL, output_dir=DEFAULT_OUTPUT_DIR, save_raw=False):
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    for skip in range(0, total, limit):
        print(f"Fetching records {skip} to {skip + limit}")
        try:
            params = {"limit": limit, "skip": skip}
            response = requests.get(OPENFDA_ENDPOINT, params=params)
            response.raise_for_status()
            data = response.json()
            results = data.get("results", [])

            if not results:
                print("No more results returned.")
                break

            if save_raw:
                with open(f"{output_dir}/openfda_raw_{skip}.json", "w") as f:
                    json.dump(data, f, indent=2)

            yield results

        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            break

        time.sleep(RATE_LIMIT_DELAY)
