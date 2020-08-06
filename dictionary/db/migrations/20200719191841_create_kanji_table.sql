-- migrate:up
CREATE TABLE kanji (
    literal CHAR(1) PRIMARY KEY,
    grade INTEGER,
    stroke_count INTEGER,
    frequency INTEGER,
    radical_name VARCHAR(16),
    jlpt_old INTEGER
);
CREATE TABLE kanji_codepoint (
    id SERIAL PRIMARY KEY,
    cp_value VARCHAR(32),
    cp_type VARCHAR(32),
    kanji CHAR(1) REFERENCES kanji (literal)
);
CREATE TABLE kanji_radical (
    id SERIAL PRIMARY KEY,
    rad_type VARCHAR(32),
    rad_value INTEGER
);
CREATE TABLE kanji_to_radical (
    id SERIAL PRIMARY KEY,
    kanji CHAR(1) REFERENCES kanji (literal),
    radical INTEGER REFERENCES kanji_radical
);
CREATE TABLE kanji_stroke_miscount (
    id SERIAL PRIMARY KEY,
    kanji CHAR(1) REFERENCES kanji (literal),
    stroke_count INTEGER NOT NULL
);
CREATE TABLE kanji_variant (
    id SERIAL PRIMARY KEY,
    var_value VARCHAR(32),
    var_type VARCHAR(32),
    kanji CHAR(1) REFERENCES kanji (literal)
);
CREATE TABLE kanji_reference_index (
    id SERIAL PRIMARY KEY,
    index_number VARCHAR(32) NOT NULL,
    reference VARCHAR(32) NOT NULL,
    kanji CHAR(1) REFERENCES kanji (literal)
);
CREATE TABLE kanji_reference_daikanwajiten (
    id SERIAL PRIMARY KEY,
    volume VARCHAR(32),
    "page" VARCHAR(32),
    kanji_reference_index_id INTEGER REFERENCES kanji_reference_index (id)
);
CREATE TABLE kanji_query_code (
    id SERIAL PRIMARY KEY,
    qc_type VARCHAR(32),
    qc_value VARCHAR(32),
    skip_misclass VARCHAR(32),
    kanji CHAR(1) REFERENCES kanji (literal)
);
CREATE TABLE kanji_reading (
    id SERIAL PRIMARY KEY,
    reading_type VARCHAR(32),
    reading VARCHAR(32),
    kanji CHAR(1) REFERENCES kanji (literal)
);
CREATE TABLE kanji_meaning (
    id SERIAL PRIMARY KEY,
    lang VARCHAR(16),
    meaning VARCHAR(128),
    kanji CHAR(1) REFERENCES kanji (literal)
);
-- migrate:down
DROP TABLE IF EXISTS kanji_to_radical;
DROP TABLE IF EXISTS kanji_radical;
DROP TABLE IF EXISTS kanji_codepoint;
DROP TABLE IF EXISTS kanji_stroke_miscount;
DROP TABLE IF EXISTS kanji_variant;
DROP TABLE IF EXISTS kanji_reference_daikanwajiten;
DROP TABLE IF EXISTS kanji_reference_index;
DROP TABLE IF EXISTS kanji_query_code;
DROP TABLE IF EXISTS kanji_reading;
DROP TABLE IF EXISTS kanji_meaning;
DROP TABLE IF EXISTS kanji;
