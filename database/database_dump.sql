-- PostgreSQL database dump
--

-- Dumped from database version 15.2
-- Dumped by pg_dump version 15.2

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

DROP DATABASE IF EXISTS anime_suggester;
--
-- Name: anime_suggester; Type: DATABASE; Schema: -; Owner: postgres
--

CREATE DATABASE anime_suggester WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'en_US.UTF-8';


ALTER DATABASE anime_suggester OWNER TO postgres;

\connect anime_suggester

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

--
-- Name: anime_suggester_client; Type: Role; Schema -
--

CREATE ROLE anime_suggester_client WITH LOGIN PASSWORD '2137' NOSUPERUSER INHERIT;

--
-- Name: clear_stale_cache_function(); Type: FUNCTION; Schema: public; Owner: gruzin
--

CREATE FUNCTION public.clear_stale_cache_function() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
        DELETE FROM cache WHERE recorded_at < CURRENT_DATE - interval '1 week';
        RETURN NULL;
END;
    $$;


ALTER FUNCTION public.clear_stale_cache_function() OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: cache; Type: TABLE; Schema: public; Owner: gruzin
--

CREATE TABLE public.cache (
    id integer NOT NULL,
    primary_result integer NOT NULL,
    all_results integer[] NOT NULL,
    recorded_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);


ALTER TABLE public.cache OWNER TO postgres;

--
-- Name: task_state; Type: TABLE; Schema: public; Owner: gruzin
--

CREATE TABLE public.task_state (
    id integer NOT NULL,
    task_id text NOT NULL,
    cache_id integer
);


ALTER TABLE public.task_state OWNER TO postgres;

--
-- Name: cache_id_seq; Type: SEQUENCE; Schema: public; Owner: gruzin
--

CREATE SEQUENCE public.cache_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.cache_id_seq OWNER TO postgres;

--
-- Name: cache_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gruzin
--

ALTER SEQUENCE public.cache_id_seq OWNED BY public.task_state.id;


--
-- Name: cache_id_seq1; Type: SEQUENCE; Schema: public; Owner: gruzin
--

CREATE SEQUENCE public.cache_id_seq1
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.cache_id_seq1 OWNER TO postgres;

--
-- Name: cache_id_seq1; Type: SEQUENCE OWNED BY; Schema: public; Owner: gruzin
--

ALTER SEQUENCE public.cache_id_seq1 OWNED BY public.cache.id;


--
-- Name: cache id; Type: DEFAULT; Schema: public; Owner: gruzin
--

ALTER TABLE ONLY public.cache ALTER COLUMN id SET DEFAULT nextval('public.cache_id_seq1'::regclass);


--
-- Name: task_state id; Type: DEFAULT; Schema: public; Owner: gruzin
--

ALTER TABLE ONLY public.task_state ALTER COLUMN id SET DEFAULT nextval('public.cache_id_seq'::regclass);


--
-- Data for Name: cache; Type: TABLE DATA; Schema: public; Owner: gruzin
--

--
-- Data for Name: task_state; Type: TABLE DATA; Schema: public; Owner: gruzin
--


--
-- Name: cache_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gruzin
--

SELECT pg_catalog.setval('public.cache_id_seq', 65, true);


--
-- Name: cache_id_seq1; Type: SEQUENCE SET; Schema: public; Owner: gruzin
--

SELECT pg_catalog.setval('public.cache_id_seq1', 57, true);


--
-- Name: task_state cache_pkey; Type: CONSTRAINT; Schema: public; Owner: gruzin
--

ALTER TABLE ONLY public.task_state
    ADD CONSTRAINT cache_pkey PRIMARY KEY (id);


--
-- Name: cache cache_pkey1; Type: CONSTRAINT; Schema: public; Owner: gruzin
--

ALTER TABLE ONLY public.cache
    ADD CONSTRAINT cache_pkey1 PRIMARY KEY (id);


--
-- Name: task_state cache_task_id_key; Type: CONSTRAINT; Schema: public; Owner: gruzin
--

ALTER TABLE ONLY public.task_state
    ADD CONSTRAINT cache_task_id_key UNIQUE (task_id);


--
-- Name: cache clear_stale_cache; Type: TRIGGER; Schema: public; Owner: gruzin
--

CREATE TRIGGER clear_stale_cache AFTER INSERT ON public.cache FOR EACH STATEMENT EXECUTE FUNCTION public.clear_stale_cache_function();


--
-- Name: task_state fk_cache; Type: FK CONSTRAINT; Schema: public; Owner: gruzin
--

ALTER TABLE ONLY public.task_state
    ADD CONSTRAINT fk_cache FOREIGN KEY (cache_id) REFERENCES public.cache(id) ON DELETE SET NULL;


--
-- Name: FUNCTION clear_stale_cache_function(); Type: ACL; Schema: public; Owner: gruzin
--

GRANT ALL ON FUNCTION public.clear_stale_cache_function() TO anime_suggester_client;


--
-- Name: TABLE cache; Type: ACL; Schema: public; Owner: gruzin
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.cache TO anime_suggester_client;


--
-- Name: TABLE task_state; Type: ACL; Schema: public; Owner: gruzin
--

GRANT SELECT,INSERT,UPDATE ON TABLE public.task_state TO anime_suggester_client;


--
-- Name: SEQUENCE cache_id_seq; Type: ACL; Schema: public; Owner: gruzin
--

GRANT SELECT,USAGE ON SEQUENCE public.cache_id_seq TO anime_suggester_client;


--
-- Name: SEQUENCE cache_id_seq1; Type: ACL; Schema: public; Owner: gruzin
--

GRANT SELECT,USAGE ON SEQUENCE public.cache_id_seq1 TO anime_suggester_client;


--
-- PostgreSQL database dump complete
--

