--
-- PostgreSQL database dump
--

-- Dumped from database version 10.9
-- Dumped by pg_dump version 11.5

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
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: anuj
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO anuj;

--
-- Name: device_info; Type: TABLE; Schema: public; Owner: anuj
--

CREATE TABLE public.device_info (
    id character varying NOT NULL,
    device_name character varying NOT NULL,
    created_on double precision,
    is_free boolean,
    employee_id character varying,
    model_name character varying,
    device_code character varying
);


ALTER TABLE public.device_info OWNER TO anuj;

--
-- Name: employee_info; Type: TABLE; Schema: public; Owner: anuj
--

CREATE TABLE public.employee_info (
    id character varying NOT NULL,
    first_name character varying,
    last_name character varying,
    created_on double precision,
    mobile_number character varying,
    email character varying NOT NULL,
    employee_code character varying
);


ALTER TABLE public.employee_info OWNER TO anuj;

--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: anuj
--

COPY public.alembic_version (version_num) FROM stdin;
cb9cbdb10136
\.


--
-- Data for Name: device_info; Type: TABLE DATA; Schema: public; Owner: anuj
--

COPY public.device_info (id, device_name, created_on, is_free, employee_id, model_name, device_code) FROM stdin;
d92d572a-b4b7-4f30-b1dc-cb8a4e15409a	abcde	1576572159865	t	\N	galaxy	959954
93c35d06-e30c-49b1-8b8a-eb7ee1dfd872	abc	1576571063667	f	d3fd96f2-760c-4950-8830-38f17aba263e	galaxy 1	113243
\.


--
-- Data for Name: employee_info; Type: TABLE DATA; Schema: public; Owner: anuj
--

COPY public.employee_info (id, first_name, last_name, created_on, mobile_number, email, employee_code) FROM stdin;
03fa07a9-048d-44e2-9d4b-e34aa40653b7	Anuj	Sri	1576569569865	1234567891	anuj123@gmail.com	668872
d3fd96f2-760c-4950-8830-38f17aba263e	Anuj	Kumar	1576571129985	1234567891	anuj96sri@gmail.com	839107
\.


--
-- Name: device_info device_info_device_code_key; Type: CONSTRAINT; Schema: public; Owner: anuj
--

ALTER TABLE ONLY public.device_info
    ADD CONSTRAINT device_info_device_code_key UNIQUE (device_code);


--
-- Name: device_info device_info_device_name_key; Type: CONSTRAINT; Schema: public; Owner: anuj
--

ALTER TABLE ONLY public.device_info
    ADD CONSTRAINT device_info_device_name_key UNIQUE (device_name);


--
-- Name: device_info device_info_pkey; Type: CONSTRAINT; Schema: public; Owner: anuj
--

ALTER TABLE ONLY public.device_info
    ADD CONSTRAINT device_info_pkey PRIMARY KEY (id);


--
-- Name: employee_info employee_info_email_key; Type: CONSTRAINT; Schema: public; Owner: anuj
--

ALTER TABLE ONLY public.employee_info
    ADD CONSTRAINT employee_info_email_key UNIQUE (email);


--
-- Name: employee_info employee_info_employee_code_key; Type: CONSTRAINT; Schema: public; Owner: anuj
--

ALTER TABLE ONLY public.employee_info
    ADD CONSTRAINT employee_info_employee_code_key UNIQUE (employee_code);


--
-- Name: employee_info employee_info_pkey; Type: CONSTRAINT; Schema: public; Owner: anuj
--

ALTER TABLE ONLY public.employee_info
    ADD CONSTRAINT employee_info_pkey PRIMARY KEY (id);


--
-- Name: device_info device_info_employee_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: anuj
--

ALTER TABLE ONLY public.device_info
    ADD CONSTRAINT device_info_employee_id_fkey FOREIGN KEY (employee_id) REFERENCES public.employee_info(id);


--
-- PostgreSQL database dump complete
--

