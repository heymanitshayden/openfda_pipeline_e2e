import streamlit as st
import pandas as pd
import psycopg2
from dotenv import load_dotenv
import os

# Load env vars for DB
load_dotenv()

DB_CONFIG = {
    "dbname": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "host": os.getenv("POSTGRES_HOST"),
    "port": os.getenv("POSTGRES_PORT")
}

# Function to run query and return DataFrame
@st.cache_data
def run_query(query, params=None):
    conn = psycopg2.connect(**DB_CONFIG)
    try:
        return pd.read_sql_query(query, conn, params=params)
    finally:
        conn.close()

# Page title
st.title("OpenFDA Adverse Events Explorer")

# Load summary stats
event_count = run_query("SELECT COUNT(*) FROM adverse_events").iloc[0, 0]
drug_count = run_query("SELECT COUNT(*) FROM drugs").iloc[0, 0]
reaction_count = run_query("SELECT COUNT(*) FROM reactions").iloc[0, 0]

st.metric("Total Adverse Events", event_count)
st.metric("Unique Drugs", drug_count)
st.metric("Unique Reactions", reaction_count)

st.divider()

# Filter for recent events
recent_events = run_query("""
    SELECT * FROM adverse_events
    ORDER BY receive_date DESC
    LIMIT 100
""")

st.subheader("Recent Adverse Events")
st.dataframe(recent_events)

# Visualize top 10 reactions
top_reactions = run_query("""
    SELECT r.name, COUNT(er.reaction_id) AS count
    FROM event_reaction er
    JOIN reactions r ON er.reaction_id = r.id
    GROUP BY r.name
    ORDER BY count DESC
    LIMIT 10
""")

st.subheader("Top 10 Reactions")
st.bar_chart(top_reactions.set_index("name"))

# Visualize top 10 drugs
top_drugs = run_query("""
    SELECT d.name, COUNT(ed.drug_id) AS count
    FROM event_drug ed
    JOIN drugs d ON ed.drug_id = d.id
    GROUP BY d.name
    ORDER BY count DESC
    LIMIT 10
""")

st.subheader("Top 10 Drugs")
st.bar_chart(top_drugs.set_index("name"))
