-- Main table for adverse event reports
CREATE TABLE IF NOT EXISTS adverse_events (
    safetyreportid TEXT PRIMARY KEY,
    receivedate DATE,
    serious INTEGER,
    seriousnessdeath INTEGER,
    seriousnesshospitalization INTEGER
);

-- Dimension: unique adverse drug reactions
CREATE TABLE IF NOT EXISTS reactions (
    id SERIAL PRIMARY KEY,
    reaction TEXT UNIQUE NOT NULL
);

-- Dimension: unique drug names
CREATE TABLE IF NOT EXISTS drugs (
    id SERIAL PRIMARY KEY,
    drug_name TEXT unique NOT NULL
);

-- Bridge: adverse events and drugs
CREATE TABLE event_drug (
    safetyreportid TEXT REFERENCES adverse_events(safetyreportid) ON DELETE CASCADE,
    drug_id INTEGER REFERENCES drug(id) ON DELETE CASCADE,
    PRIMARY KEY (safetyreportid, drug_id)
);

-- Bridge: adverse events and reactions
CREATE TABLE event_reaction (
    safetyreportid TEXT REFERENCES adverse_events(safetyreportid) ON DELETE CASCADE,
    reaction_id INTEGER REFERENCES reaction(id) ON DELETE CASCADE,
    PRIMARY KEY (safetyreportid, reaction_id)
);