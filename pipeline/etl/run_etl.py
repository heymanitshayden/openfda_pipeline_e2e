from fetch import fetch_adverse_events
from transform import transform_record
from load import load_new_records

def main():
    for batch in fetch_adverse_events(total=500):  # You can adjust total as needed
        transformed_records = [transform_record(record) for record in batch]
        load_new_records(transformed_records)

if __name__ == "__main__":
    main()