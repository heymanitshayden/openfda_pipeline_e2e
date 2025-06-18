import requests
import json

OPENFDA_ENDPOINT = "https://api.fda.gov/drug/event.json"
DEFAULT_LIMIT = 100


def fetch_adverse_events(limit=DEFAULT_LIMIT, skip=0, save_raw=False):
    params = {
        "limit": limit,
        "skip": skip
    }
    try:
        response = requests.get(OPENFDA_ENDPOINT, params=params)
        response.raise_for_status()
        data = response.json()

        if save_raw:
            with open(f"openfda_raw_{skip}.json", "w") as f:
                json.dump(data, f, indent=2)

        return data.get("results", [])

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from OpenFDA: {e}")
        return []


if __name__ == "__main__":
    records = fetch_adverse_events(limit=100, save_raw=True)
    print(f"Fetched {len(records)} records.")