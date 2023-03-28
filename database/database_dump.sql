--
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
-- Name: cache; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.cache (
    id integer NOT NULL,
    primary_result integer NOT NULL,
    all_results integer[] NOT NULL,
    recorded_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);


ALTER TABLE public.cache OWNER TO postgres;

--
-- Name: task_state; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.task_state (
    id integer NOT NULL,
    task_id text NOT NULL,
    cache_id integer
);


ALTER TABLE public.task_state OWNER TO postgres;

--
-- Name: cache_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
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
-- Name: cache_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.cache_id_seq OWNED BY public.task_state.id;


--
-- Name: cache_id_seq1; Type: SEQUENCE; Schema: public; Owner: postgres
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
-- Name: cache_id_seq1; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.cache_id_seq1 OWNED BY public.cache.id;


--
-- Name: mal_tokens; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mal_tokens (
    user_id integer NOT NULL,
    access_token text NOT NULL,
    refresh_token text NOT NULL
);


ALTER TABLE public.mal_tokens OWNER TO postgres;

--
-- Name: sessions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.sessions (
    id integer NOT NULL,
    expires_in integer NOT NULL,
    token text NOT NULL,
    user_id bigint NOT NULL
);


ALTER TABLE public.sessions OWNER TO postgres;

--
-- Name: sessions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.sessions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.sessions_id_seq OWNER TO postgres;

--
-- Name: sessions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.sessions_id_seq OWNED BY public.sessions.id;


--
-- Name: cache id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cache ALTER COLUMN id SET DEFAULT nextval('public.cache_id_seq1'::regclass);


--
-- Name: sessions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sessions ALTER COLUMN id SET DEFAULT nextval('public.sessions_id_seq'::regclass);


--
-- Name: task_state id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.task_state ALTER COLUMN id SET DEFAULT nextval('public.cache_id_seq'::regclass);


--
-- Data for Name: cache; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.cache (id, primary_result, all_results, recorded_at) VALUES (11, 47917, '{35180,33352,47917,1575}', '2023-03-15 13:25:28.655324');
INSERT INTO public.cache (id, primary_result, all_results, recorded_at) VALUES (44, 47917, '{35180,33352,47917,1575}', '2023-03-17 12:49:46.362697');
INSERT INTO public.cache (id, primary_result, all_results, recorded_at) VALUES (45, 35180, '{35180,33352,47917,1575}', '2023-03-17 14:50:46.687813');
INSERT INTO public.cache (id, primary_result, all_results, recorded_at) VALUES (46, 33352, '{35180,33352,47917,1575}', '2023-03-17 14:51:32.791345');
INSERT INTO public.cache (id, primary_result, all_results, recorded_at) VALUES (48, 1575, '{35180,33352,47917,1575}', '2023-03-19 11:07:54.123124');
INSERT INTO public.cache (id, primary_result, all_results, recorded_at) VALUES (49, 1575, '{35180,33352,47917,1575}', '2023-03-19 11:08:08.029392');
INSERT INTO public.cache (id, primary_result, all_results, recorded_at) VALUES (50, 47917, '{35180,33352,47917,1575}', '2023-03-19 13:11:58.428965');
INSERT INTO public.cache (id, primary_result, all_results, recorded_at) VALUES (51, 47917, '{35180,33352,47917,1575}', '2023-03-20 11:59:42.208971');
INSERT INTO public.cache (id, primary_result, all_results, recorded_at) VALUES (52, 33352, '{35180,33352,47917,1575}', '2023-03-20 12:05:20.699061');
INSERT INTO public.cache (id, primary_result, all_results, recorded_at) VALUES (53, 1575, '{35180,33352,47917,1575}', '2023-03-20 12:09:18.696681');
INSERT INTO public.cache (id, primary_result, all_results, recorded_at) VALUES (54, 47917, '{35180,33352,47917,1575}', '2023-03-20 12:11:09.479849');
INSERT INTO public.cache (id, primary_result, all_results, recorded_at) VALUES (56, 1575, '{35180,33352,47917,1575}', '2023-03-20 12:14:17.818289');
INSERT INTO public.cache (id, primary_result, all_results, recorded_at) VALUES (57, 35180, '{35180,33352,47917,1575}', '2023-03-21 09:52:37.739465');


--
-- Data for Name: mal_tokens; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: sessions; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: task_state; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.task_state (id, task_id, cache_id) VALUES (1, 'dd12kd-xda134', NULL);
INSERT INTO public.task_state (id, task_id, cache_id) VALUES (10, '593041c5-51a1-4a40-8d9e-3f0944578eae', 11);
INSERT INTO public.task_state (id, task_id, cache_id) VALUES (43, 'ce58a104-7104-4115-a7a9-fb508efea124', 44);
INSERT INTO public.task_state (id, task_id, cache_id) VALUES (44, 'fe431901-dfd1-475b-b402-577639d2b36b', 45);
INSERT INTO public.task_state (id, task_id, cache_id) VALUES (45, '842c5a51-82f2-4fac-901d-b2b4be5aa9ef', 46);
INSERT INTO public.task_state (id, task_id, cache_id) VALUES (46, '30fb84dd-c682-4293-9c70-c6577a1a80d2', NULL);
INSERT INTO public.task_state (id, task_id, cache_id) VALUES (47, 'aedd66b1-2fc8-4369-bd9a-c77b6c946137', NULL);
INSERT INTO public.task_state (id, task_id, cache_id) VALUES (48, 'c0ef0bb4-9bdd-4de4-aaad-270ae4f2a3a9', NULL);
INSERT INTO public.task_state (id, task_id, cache_id) VALUES (49, '5691ed80-568b-452e-b27b-1f9ae8ff468a', NULL);
INSERT INTO public.task_state (id, task_id, cache_id) VALUES (50, '982e5279-c2d8-476d-93a2-0b5bf2444e12', NULL);
INSERT INTO public.task_state (id, task_id, cache_id) VALUES (51, '5468a690-57bf-41e2-8fdd-284df506ce84', NULL);
INSERT INTO public.task_state (id, task_id, cache_id) VALUES (52, 'aa5744d2-463f-4152-a65c-d5087adb2af9', NULL);
INSERT INTO public.task_state (id, task_id, cache_id) VALUES (53, '4066b8e9-2c35-45cd-ba4f-1bbb223ab54a', NULL);
INSERT INTO public.task_state (id, task_id, cache_id) VALUES (54, '5ecf7520-aa11-450d-b6a6-315f76565e4d', NULL);
INSERT INTO public.task_state (id, task_id, cache_id) VALUES (55, '756cb24b-2e75-4d29-88bd-d7ab145f5902', NULL);
INSERT INTO public.task_state (id, task_id, cache_id) VALUES (56, '10068761-cd8b-4859-a26d-4f7be8d80439', 48);
INSERT INTO public.task_state (id, task_id, cache_id) VALUES (57, '7435c13a-de7a-45ec-8f79-71d36d3b8e99', 49);
INSERT INTO public.task_state (id, task_id, cache_id) VALUES (58, 'a59d9269-21df-44f4-9bc1-9679ca6aa397', 50);
INSERT INTO public.task_state (id, task_id, cache_id) VALUES (59, 'ccfc3fa2-c5d0-4cf6-a537-7e307207e0e1', 51);
INSERT INTO public.task_state (id, task_id, cache_id) VALUES (60, '16067feb-22c1-466c-b291-580e2449566a', 52);
INSERT INTO public.task_state (id, task_id, cache_id) VALUES (61, '664dac98-eeaf-4995-847e-45356f410877', 53);
INSERT INTO public.task_state (id, task_id, cache_id) VALUES (62, 'fcc9f6da-b8a8-4ac1-91d6-4425e777b387', 54);
INSERT INTO public.task_state (id, task_id, cache_id) VALUES (63, '2df183d4-564b-4bb3-8315-357748a913d7', NULL);
INSERT INTO public.task_state (id, task_id, cache_id) VALUES (64, '19d948a9-7e11-4338-a11d-e1cc7d2f3dee', 56);
INSERT INTO public.task_state (id, task_id, cache_id) VALUES (65, '489c0051-756f-422f-91b8-9dc86505f8d2', 57);


--
-- Name: cache_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.cache_id_seq', 65, true);


--
-- Name: cache_id_seq1; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.cache_id_seq1', 57, true);


--
-- Name: sessions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.sessions_id_seq', 1, false);


--
-- Name: task_state cache_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.task_state
    ADD CONSTRAINT cache_pkey PRIMARY KEY (id);


--
-- Name: cache cache_pkey1; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cache
    ADD CONSTRAINT cache_pkey1 PRIMARY KEY (id);


--
-- Name: task_state cache_task_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.task_state
    ADD CONSTRAINT cache_task_id_key UNIQUE (task_id);


--
-- Name: mal_tokens mal_tokens_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mal_tokens
    ADD CONSTRAINT mal_tokens_pk PRIMARY KEY (user_id);


--
-- Name: sessions sessions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sessions
    ADD CONSTRAINT sessions_pkey PRIMARY KEY (id);


--
-- Name: cache clear_stale_cache; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER clear_stale_cache AFTER INSERT ON public.cache FOR EACH STATEMENT EXECUTE FUNCTION public.clear_stale_cache_function();


--
-- Name: task_state fk_cache; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.task_state
    ADD CONSTRAINT fk_cache FOREIGN KEY (cache_id) REFERENCES public.cache(id) ON DELETE SET NULL;


--
-- Name: FUNCTION clear_stale_cache_function(); Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON FUNCTION public.clear_stale_cache_function() TO anime_suggester_client;


--
-- Name: TABLE cache; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.cache TO anime_suggester_client;


--
-- Name: TABLE task_state; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT,INSERT,UPDATE ON TABLE public.task_state TO anime_suggester_client;
GRANT SELECT,INSERT,UPDATE,DELETE ON TABLE public.mal_tokens TO anime_suggester_client;
GRANT SELECT,INSERT,UPDATE,DELETE ON TABLE public.sessions TO anime_suggester_client;


--
-- Name: SEQUENCE cache_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE public.cache_id_seq TO anime_suggester_client;


--
-- Name: SEQUENCE cache_id_seq1; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE public.cache_id_seq1 TO anime_suggester_client;
GRANT SELECT,USAGE ON SEQUENCE public.sessions_id_seq TO anime_suggester_client;


--
-- PostgreSQL database dump complete
--

