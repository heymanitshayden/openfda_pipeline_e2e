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
if not all(DB_CONFIG.values()):
    raise EnvironmentError("Missing one or more required database environment variables.")


def _get_or_create_row_id(cur, table, value):
    cur.execute(f"SELECT id FROM {table} WHERE name = %s", (value,))
    result = cur.fetchone()
    if result:
        return result[0]
    cur.execute(f"INSERT INTO {table} (name) VALUES (%s) RETURNING id", (value,))
    return cur.fetchone()[0]

def _insert_adverse_event(cur, event):
    sql = """
        INSERT INTO adverse_events (safety_report_id, receive_date, serious, seriousness_death, seriousness_hospitalization)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (safety_report_id) DO NOTHING
    """
    cur.execute(sql, (
        event["safetyreportid"],
        event["receivedate"],
        event["serious"],
        event["seriousnessdeath"],
        event["seriousnesshospitalization"],
    ))

def _link_event_to_dimensions(cur, safety_report_id, drugs, reactions):
    EVENT_DRUG_SQL = """
        INSERT INTO event_drug(safety_report_id, drug_id)
        VALUES (%s, %s)
        ON CONFLICT DO NOTHING
    """
    EVENT_REACTIONS_SQL = """
        INSERT INTO event_reactions(safety_report_id, reaction_id)
        VALUES (%s, %s)
        ON CONFLICT DO NOTHING
    """
    
    for drug in drugs:
        drug_id = _get_or_create_row_id(cur, "drugs", drug)
        cur.execute(EVENT_DRUG_SQL, (safety_report_id, drug_id))

    for reaction in reactions:
        reaction_id = _get_or_create_row_id(cur, "reactions", reaction)
        cur.execute(EVENT_REACTIONS_SQL, (safety_report_id, reaction_id))
    
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

