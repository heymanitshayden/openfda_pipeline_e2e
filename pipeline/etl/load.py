import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()

DB_CONFIG = {
    "dbname": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "host": os.getenv("POSTGRES_HOST"),
    "port": os.getenv("POSTGRES_PORT")
}

def _get_or_create_row_id(cur, table, value):
    cur.execute(f"SELECT id FROM {table} WHERE name = %s", (value,))
    result = cur.fetchone()
    if result:
        return result[0]
    cur.execute(f"INSERT INTO {table} (name) VALUES (%s) RETURNING id", (value,))
    return cur.fetchone()[0]

def _insert_adverse_event(cur, event):
    return None

def _link_event_to_dimensions(cur, event):
    return None

def load_new_records(records):
    conn = psycopg2.connect(**DB_CONFIG)
    try:
        with conn:
            with conn.cursor() as cur:
                for event, drugs, reactions in records:
                    _insert_adverse_event(cur, event)
                    _link_event_to_dimensions(cur, event["safetyreportid"], drugs, reactions)
    except Exception as e:
        print(f"An error occurred while loading records into Postgres: {e}")
    finally:
        conn.close()

