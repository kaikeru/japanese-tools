-- migrate:up
CREATE TABLE kanjidict_version (
    id SERIAL PRIMARY KEY ,
    file_version INTEGER,
    database_version VARCHAR(32) UNIQUE,
    date_of_creation DATE,
    created_on TIMESTAMPTZ DEFAULT now()
);
-- migrate:down
DROP TABLE IF EXISTS kanjidict_version;
