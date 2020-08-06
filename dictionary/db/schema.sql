SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: kanji; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.kanji (
    literal character(1) NOT NULL,
    grade integer,
    stroke_count integer,
    frequency integer,
    radical_name character varying(16),
    jlpt_old integer
);


--
-- Name: kanji_codepoint; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.kanji_codepoint (
    id integer NOT NULL,
    cp_value character varying(32),
    cp_type character varying(32),
    kanji character(1)
);


--
-- Name: kanji_codepoint_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.kanji_codepoint_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: kanji_codepoint_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.kanji_codepoint_id_seq OWNED BY public.kanji_codepoint.id;


--
-- Name: kanji_meaning; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.kanji_meaning (
    id integer NOT NULL,
    lang character varying(16),
    meaning character varying(128),
    kanji character(1)
);


--
-- Name: kanji_meaning_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.kanji_meaning_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: kanji_meaning_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.kanji_meaning_id_seq OWNED BY public.kanji_meaning.id;


--
-- Name: kanji_query_code; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.kanji_query_code (
    id integer NOT NULL,
    qc_type character varying(32),
    qc_value character varying(32),
    skip_misclass character varying(32),
    kanji character(1)
);


--
-- Name: kanji_query_code_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.kanji_query_code_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: kanji_query_code_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.kanji_query_code_id_seq OWNED BY public.kanji_query_code.id;


--
-- Name: kanji_radical; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.kanji_radical (
    id integer NOT NULL,
    rad_type character varying(32),
    rad_value integer
);


--
-- Name: kanji_radical_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.kanji_radical_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: kanji_radical_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.kanji_radical_id_seq OWNED BY public.kanji_radical.id;


--
-- Name: kanji_reading; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.kanji_reading (
    id integer NOT NULL,
    reading_type character varying(32),
    reading character varying(32),
    kanji character(1)
);


--
-- Name: kanji_reading_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.kanji_reading_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: kanji_reading_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.kanji_reading_id_seq OWNED BY public.kanji_reading.id;


--
-- Name: kanji_reference_daikanwajiten; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.kanji_reference_daikanwajiten (
    id integer NOT NULL,
    volume character varying(32),
    page character varying(32),
    kanji_reference_index_id integer
);


--
-- Name: kanji_reference_daikanwajiten_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.kanji_reference_daikanwajiten_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: kanji_reference_daikanwajiten_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.kanji_reference_daikanwajiten_id_seq OWNED BY public.kanji_reference_daikanwajiten.id;


--
-- Name: kanji_reference_index; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.kanji_reference_index (
    id integer NOT NULL,
    index_number character varying(32) NOT NULL,
    reference character varying(32) NOT NULL,
    kanji character(1)
);


--
-- Name: kanji_reference_index_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.kanji_reference_index_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: kanji_reference_index_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.kanji_reference_index_id_seq OWNED BY public.kanji_reference_index.id;


--
-- Name: kanji_stroke_miscount; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.kanji_stroke_miscount (
    id integer NOT NULL,
    kanji character(1),
    stroke_count integer NOT NULL
);


--
-- Name: kanji_stroke_miscount_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.kanji_stroke_miscount_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: kanji_stroke_miscount_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.kanji_stroke_miscount_id_seq OWNED BY public.kanji_stroke_miscount.id;


--
-- Name: kanji_to_radical; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.kanji_to_radical (
    id integer NOT NULL,
    kanji character(1),
    radical integer
);


--
-- Name: kanji_to_radical_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.kanji_to_radical_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: kanji_to_radical_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.kanji_to_radical_id_seq OWNED BY public.kanji_to_radical.id;


--
-- Name: kanji_variant; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.kanji_variant (
    id integer NOT NULL,
    var_value character varying(32),
    var_type character varying(32),
    kanji character(1)
);


--
-- Name: kanji_variant_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.kanji_variant_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: kanji_variant_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.kanji_variant_id_seq OWNED BY public.kanji_variant.id;


--
-- Name: kanjidict_version; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.kanjidict_version (
    id integer NOT NULL,
    file_version integer,
    database_version character varying(32),
    date_of_creation date,
    created_on timestamp with time zone DEFAULT now()
);


--
-- Name: kanjidict_version_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.kanjidict_version_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: kanjidict_version_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.kanjidict_version_id_seq OWNED BY public.kanjidict_version.id;


--
-- Name: schema_migrations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.schema_migrations (
    version character varying(255) NOT NULL
);


--
-- Name: kanji_codepoint id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kanji_codepoint ALTER COLUMN id SET DEFAULT nextval('public.kanji_codepoint_id_seq'::regclass);


--
-- Name: kanji_meaning id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kanji_meaning ALTER COLUMN id SET DEFAULT nextval('public.kanji_meaning_id_seq'::regclass);


--
-- Name: kanji_query_code id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kanji_query_code ALTER COLUMN id SET DEFAULT nextval('public.kanji_query_code_id_seq'::regclass);


--
-- Name: kanji_radical id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kanji_radical ALTER COLUMN id SET DEFAULT nextval('public.kanji_radical_id_seq'::regclass);


--
-- Name: kanji_reading id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kanji_reading ALTER COLUMN id SET DEFAULT nextval('public.kanji_reading_id_seq'::regclass);


--
-- Name: kanji_reference_daikanwajiten id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kanji_reference_daikanwajiten ALTER COLUMN id SET DEFAULT nextval('public.kanji_reference_daikanwajiten_id_seq'::regclass);


--
-- Name: kanji_reference_index id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kanji_reference_index ALTER COLUMN id SET DEFAULT nextval('public.kanji_reference_index_id_seq'::regclass);


--
-- Name: kanji_stroke_miscount id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kanji_stroke_miscount ALTER COLUMN id SET DEFAULT nextval('public.kanji_stroke_miscount_id_seq'::regclass);


--
-- Name: kanji_to_radical id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kanji_to_radical ALTER COLUMN id SET DEFAULT nextval('public.kanji_to_radical_id_seq'::regclass);


--
-- Name: kanji_variant id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kanji_variant ALTER COLUMN id SET DEFAULT nextval('public.kanji_variant_id_seq'::regclass);


--
-- Name: kanjidict_version id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kanjidict_version ALTER COLUMN id SET DEFAULT nextval('public.kanjidict_version_id_seq'::regclass);


--
-- Name: kanji_codepoint kanji_codepoint_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kanji_codepoint
    ADD CONSTRAINT kanji_codepoint_pkey PRIMARY KEY (id);


--
-- Name: kanji_meaning kanji_meaning_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kanji_meaning
    ADD CONSTRAINT kanji_meaning_pkey PRIMARY KEY (id);


--
-- Name: kanji kanji_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kanji
    ADD CONSTRAINT kanji_pkey PRIMARY KEY (literal);


--
-- Name: kanji_query_code kanji_query_code_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kanji_query_code
    ADD CONSTRAINT kanji_query_code_pkey PRIMARY KEY (id);


--
-- Name: kanji_radical kanji_radical_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kanji_radical
    ADD CONSTRAINT kanji_radical_pkey PRIMARY KEY (id);


--
-- Name: kanji_reading kanji_reading_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kanji_reading
    ADD CONSTRAINT kanji_reading_pkey PRIMARY KEY (id);


--
-- Name: kanji_reference_daikanwajiten kanji_reference_daikanwajiten_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kanji_reference_daikanwajiten
    ADD CONSTRAINT kanji_reference_daikanwajiten_pkey PRIMARY KEY (id);


--
-- Name: kanji_reference_index kanji_reference_index_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kanji_reference_index
    ADD CONSTRAINT kanji_reference_index_pkey PRIMARY KEY (id);


--
-- Name: kanji_stroke_miscount kanji_stroke_miscount_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kanji_stroke_miscount
    ADD CONSTRAINT kanji_stroke_miscount_pkey PRIMARY KEY (id);


--
-- Name: kanji_to_radical kanji_to_radical_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kanji_to_radical
    ADD CONSTRAINT kanji_to_radical_pkey PRIMARY KEY (id);


--
-- Name: kanji_variant kanji_variant_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kanji_variant
    ADD CONSTRAINT kanji_variant_pkey PRIMARY KEY (id);


--
-- Name: kanjidict_version kanjidict_version_database_version_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kanjidict_version
    ADD CONSTRAINT kanjidict_version_database_version_key UNIQUE (database_version);


--
-- Name: kanjidict_version kanjidict_version_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kanjidict_version
    ADD CONSTRAINT kanjidict_version_pkey PRIMARY KEY (id);


--
-- Name: schema_migrations schema_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.schema_migrations
    ADD CONSTRAINT schema_migrations_pkey PRIMARY KEY (version);


--
-- Name: kanji_codepoint kanji_codepoint_kanji_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kanji_codepoint
    ADD CONSTRAINT kanji_codepoint_kanji_fkey FOREIGN KEY (kanji) REFERENCES public.kanji(literal);


--
-- Name: kanji_meaning kanji_meaning_kanji_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kanji_meaning
    ADD CONSTRAINT kanji_meaning_kanji_fkey FOREIGN KEY (kanji) REFERENCES public.kanji(literal);


--
-- Name: kanji_query_code kanji_query_code_kanji_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kanji_query_code
    ADD CONSTRAINT kanji_query_code_kanji_fkey FOREIGN KEY (kanji) REFERENCES public.kanji(literal);


--
-- Name: kanji_reading kanji_reading_kanji_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kanji_reading
    ADD CONSTRAINT kanji_reading_kanji_fkey FOREIGN KEY (kanji) REFERENCES public.kanji(literal);


--
-- Name: kanji_reference_daikanwajiten kanji_reference_daikanwajiten_kanji_reference_index_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kanji_reference_daikanwajiten
    ADD CONSTRAINT kanji_reference_daikanwajiten_kanji_reference_index_id_fkey FOREIGN KEY (kanji_reference_index_id) REFERENCES public.kanji_reference_index(id);


--
-- Name: kanji_reference_index kanji_reference_index_kanji_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kanji_reference_index
    ADD CONSTRAINT kanji_reference_index_kanji_fkey FOREIGN KEY (kanji) REFERENCES public.kanji(literal);


--
-- Name: kanji_stroke_miscount kanji_stroke_miscount_kanji_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kanji_stroke_miscount
    ADD CONSTRAINT kanji_stroke_miscount_kanji_fkey FOREIGN KEY (kanji) REFERENCES public.kanji(literal);


--
-- Name: kanji_to_radical kanji_to_radical_kanji_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kanji_to_radical
    ADD CONSTRAINT kanji_to_radical_kanji_fkey FOREIGN KEY (kanji) REFERENCES public.kanji(literal);


--
-- Name: kanji_to_radical kanji_to_radical_radical_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kanji_to_radical
    ADD CONSTRAINT kanji_to_radical_radical_fkey FOREIGN KEY (radical) REFERENCES public.kanji_radical(id);


--
-- Name: kanji_variant kanji_variant_kanji_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kanji_variant
    ADD CONSTRAINT kanji_variant_kanji_fkey FOREIGN KEY (kanji) REFERENCES public.kanji(literal);


--
-- PostgreSQL database dump complete
--


--
-- Dbmate schema migrations
--

INSERT INTO public.schema_migrations (version) VALUES
    ('20200717181342'),
    ('20200719191841');
