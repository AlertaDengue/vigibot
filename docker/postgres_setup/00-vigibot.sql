--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.13
-- Dumped by pg_dump version 11.3 (Ubuntu 11.3-1.pgdg14.04+1)

-- Name: vigibot; Type: DATABASE; Schema: -; Owner: dengueadmin
--

CREATE DATABASE "dengue" WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE = 'en_US.utf8';
ALTER DATABASE "dengue" OWNER TO dengueadmin;

CREATE DATABASE "vigibot" WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE = 'en_US.utf8';
ALTER DATABASE "vigibot" OWNER TO dengueadmin;

-- Name: statement;
--

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

SET default_with_oids = false;

--
-- Roles
--

-- CREATE ROLE dengueadmin;
-- ALTER ROLE dengueadmin WITH SUPERUSER INHERIT CREATEROLE CREATEDB LOGIN NOREPLICATION NOBYPASSRLS PASSWORD NULL VALID UNTIL 'infinity';

CREATE ROLE administrador;
ALTER ROLE administrador WITH SUPERUSER INHERIT CREATEROLE CREATEDB LOGIN NOREPLICATION NOBYPASSRLS PASSWORD NULL;

-- Table: "Municipio"."Historico_alerta"

\connect "dengue"

--
-- Name: TABLE "Municipio"; Type: ACL; Schema: Municipio; Owner: administrador
--
CREATE SCHEMA IF NOT EXISTS "Dengue_global";

CREATE TABLE IF NOT EXISTS "Dengue_global"."Municipio"
(
  geocodigo integer NOT NULL,
  nome character varying(128) NOT NULL,
  geojson text NOT NULL,
  populacao bigint NOT NULL,
  uf character varying(20) NOT NULL,
  CONSTRAINT "Municipio_pk" PRIMARY KEY (geocodigo)
);

--
-- Name: TABLE "Historico_alerta"; Type: ACL; Schema: Municipio; Owner: administrador
--

CREATE SCHEMA IF NOT EXISTS "Municipio";

CREATE TABLE IF NOT EXISTS "Municipio"."Historico_alerta"
(
  "data_iniSE" date NOT NULL,
  "SE" integer NOT NULL,
  casos_est real,
  casos_est_min integer,
  casos_est_max integer,
  casos integer,
  municipio_geocodigo integer NOT NULL,
  p_rt1 real,
  p_inc100k real,
  "Localidade_id" integer,
  nivel smallint,
  id bigserial NOT NULL,
  versao_modelo character varying(40),
  municipio_nome character varying(128),
  CONSTRAINT "Historico_alerta_zika_pk" PRIMARY KEY (id),
  CONSTRAINT alertas_unicos_zika UNIQUE ("SE", municipio_geocodigo, "Localidade_id")
);

\connect "vigibot"

--
-- Name: bot_users; Type: TABLE; Schema: public; Owner: dengueadmin
--

CREATE TABLE public.bot_users (
    id integer NOT NULL,
    telegram_uid bigint,
    first_name text,
    last_name text,
    latitude real,
    longitude real
);


ALTER TABLE public.bot_users OWNER TO dengueadmin;

--
-- Name: bot_users_id_seq; Type: SEQUENCE; Schema: public; Owner: dengueadmin
--

CREATE SEQUENCE public.bot_users_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.bot_users_id_seq OWNER TO dengueadmin;

--
-- Name: bot_users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dengueadmin
--

ALTER SEQUENCE public.bot_users_id_seq OWNED BY public.bot_users.id;


--
-- Name: pergunta; Type: TABLE; Schema: public; Owner: administrador
--

CREATE TABLE public.pergunta (
    id bigint NOT NULL,
    username character varying(32) NOT NULL,
    network character varying(16) NOT NULL,
    pergunta text NOT NULL,
    datetime timestamp without time zone DEFAULT now() NOT NULL,
    msgid bigint
);


ALTER TABLE public.pergunta OWNER TO administrador;

--
-- Name: pergunta_id_seq; Type: SEQUENCE; Schema: public; Owner: administrador
--

CREATE SEQUENCE public.pergunta_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.pergunta_id_seq OWNER TO administrador;

--
-- Name: pergunta_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: administrador
--

ALTER SEQUENCE public.pergunta_id_seq OWNED BY public.pergunta.id;


--
-- Name: bot_users id; Type: DEFAULT; Schema: public; Owner: dengueadmin
--

ALTER TABLE ONLY public.bot_users ALTER COLUMN id SET DEFAULT nextval('public.bot_users_id_seq'::regclass);


--
-- Name: pergunta id; Type: DEFAULT; Schema: public; Owner: administrador
--

ALTER TABLE ONLY public.pergunta ALTER COLUMN id SET DEFAULT nextval('public.pergunta_id_seq'::regclass);


--
-- Data for Name: bot_users; Type: TABLE DATA; Schema: public; Owner: dengueadmin
--

COPY public.bot_users (id, telegram_uid, first_name, last_name, latitude, longitude) FROM stdin;
10	159627190	Flávio	Coelho	-22.9416409	-43.1800461
14	844782728	Claudia	None	-22.9299259	-43.1895332
15	269187043	Elton Nogueira	Santana	-22.9114208	-43.2244072
16	816116305	@esloch	None	\N	\N
17	329610429	Felipe	Bottega	\N	\N
18	80929548	Marfcg	None	-22.9103031	-43.2238922
20	910394093	Lucas	Bianchi	\N	\N
19	854488804	Iasmim	Almeida	-22.9114208	-43.2244072
22	165204133	Jorge	Fernandes	-22.9114208	-43.2244072
23	202214378	Helio	Schechtman	-22.9114208	-43.2244072
24	690432815	Yan	Britto	\N	\N
25	168247529	Oswaldo	None	\N	\N
21	163441277	Douglas Felipe	None	20.6593246	-11.4062548
26	740540352	Rafael	Pinheiro	-22.9112568	-43.2056084
27	1028821812	Marcelle	Chagas	-22.9416161	-43.1801338
28	1035385935	mr	frouzanpour	\N	\N
29	1187833911	Bina	None	\N	\N
11	1	ze	teste	23	-46.2000008
\.


--
-- Data for Name: pergunta; Type: TABLE DATA; Schema: public; Owner: administrador
--

COPY public.pergunta (id, username, network, pergunta, datetime, msgid) FROM stdin;
32	fccoelho	Twitter	 dengue	2021-02-26 05:43:22.315911	1364927637114793991
33	fccoelho	Telegram	covid19	2021-02-26 06:42:28.109375	259393224
34	fccoelho	Telegram	o que é dengue?	2021-02-26 06:44:25.821346	259393229
35	fccoelho	Telegram	o que é dengue	2021-02-26 09:19:32.734842	259393244
36	clau_codeco	Telegram	o que é dengue?	2021-02-26 09:22:45.722357	259393245
37	clau_codeco	Telegram	como está a dengue no Rio de Janeiro?	2021-02-26 09:28:09.374742	259393259
38	fccoelho	Telegram	o que é dengue?	2021-03-18 11:46:28.165934	259393270
39	fccoelho	Telegram	o que é dengue	2021-04-19 14:30:25.955158	259393301
40	fccoelho	Twitter	Esta pergunta é um teste	2022-05-30 10:50:44.575007	0
41	fccoelho	Twitter	Esta pergunta é um teste	2022-05-30 11:20:11.509477	0
42	fccoelho	Twitter	Esta pergunta é um teste	2022-05-30 11:22:52.953772	0
43	fccoelho	Twitter	Esta pergunta é um teste	2022-05-30 11:24:15.015527	0
44	fccoelho	Twitter	Esta pergunta é um teste	2022-05-30 11:31:31.555524	0
45	fccoelho	Twitter	Esta pergunta é um teste	2022-05-30 11:33:46.421413	0
\.


--
-- Name: bot_users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dengueadmin
--

SELECT pg_catalog.setval('public.bot_users_id_seq', 36, true);


--
-- Name: pergunta_id_seq; Type: SEQUENCE SET; Schema: public; Owner: administrador
--

SELECT pg_catalog.setval('public.pergunta_id_seq', 45, true);


--
-- Name: bot_users bot_users_pkey; Type: CONSTRAINT; Schema: public; Owner: dengueadmin
--

ALTER TABLE ONLY public.bot_users
    ADD CONSTRAINT bot_users_pkey PRIMARY KEY (id);


--
-- Name: bot_users bot_users_telegram_uid_key; Type: CONSTRAINT; Schema: public; Owner: dengueadmin
--

ALTER TABLE ONLY public.bot_users
    ADD CONSTRAINT bot_users_telegram_uid_key UNIQUE (telegram_uid);


--
-- Name: pergunta pergunta_pkey; Type: CONSTRAINT; Schema: public; Owner: administrador
--

ALTER TABLE ONLY public.pergunta
    ADD CONSTRAINT pergunta_pkey PRIMARY KEY (id);


--
-- Name: pergunta_datetime_idx; Type: INDEX; Schema: public; Owner: administrador
--

CREATE INDEX pergunta_datetime_idx ON public.pergunta USING btree (datetime);


--
-- Name: pergunta_network_idx; Type: INDEX; Schema: public; Owner: administrador
--

CREATE INDEX pergunta_network_idx ON public.pergunta USING btree (network);


--
-- PostgreSQL database dump complete
--
