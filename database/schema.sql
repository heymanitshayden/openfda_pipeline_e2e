-- Main table for adverse event reports
CREATE TABLE IF NOT EXISTS adverse_events (
    safetyreportid TEXT PRIMARY KEY,
    receivedate DATE,
    serious INTEGER,
    seriousnessdeath INTEGER,
    seriousnesshospitalization INTEGER
);

-- Reactions table: one-to-many with adverse_events
CREATE TABLE IF NOT EXISTS reactions (
    id SERIAL PRIMARY KEY,
    safetyreportid TEXT REFERENCES adverse_events(safetyreportid) ON DELETE CASCADE,
    reaction TEXT
);

-- Drugs table: one-to-many with adverse_events
CREATE TABLE IF NOT EXISTS drugs (
    id SERIAL PRIMARY KEY,
    safetyreportid TEXT REFERENCES adverse_events(safetyreportid) ON DELETE CASCADE,
    medicinalproduct TEXT
);
