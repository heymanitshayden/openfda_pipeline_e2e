-- Main table for adverse event reports
CREATE TABLE IF NOT EXISTS adverse_events (
    safety_report_id TEXT PRIMARY KEY,
    receive_date DATE,
    serious INTEGER,
    seriousness_death INTEGER,
    seriousness_hospitalization INTEGER
);

-- Dimension: unique adverse drug reactions
CREATE TABLE IF NOT EXISTS reactions (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL
);

-- Dimension: unique drug names
CREATE TABLE IF NOT EXISTS drugs (
    id SERIAL PRIMARY KEY,
    name TEXT unique NOT NULL
);

-- Bridge: adverse events and drugs
CREATE TABLE event_drug (
    safety_report_id TEXT REFERENCES adverse_events(safety_report_id) ON DELETE CASCADE,
    drug_id INTEGER REFERENCES drugs(id) ON DELETE CASCADE,
    PRIMARY KEY (safety_report_id, drug_id)
);

-- Bridge: adverse events and reactions
CREATE TABLE event_reaction (
    safety_report_id TEXT REFERENCES adverse_events(safety_report_id) ON DELETE CASCADE,
    reaction_id INTEGER REFERENCES reactions(id) ON DELETE CASCADE,
    PRIMARY KEY (safety_report_id, reaction_id)
);