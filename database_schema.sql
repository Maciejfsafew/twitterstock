--
-- PostgreSQL database dump
--

-- Dumped from database version 9.4.1
-- Dumped by pg_dump version 9.4.1
-- Started on 2015-05-11 00:31:52

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- TOC entry 7 (class 2615 OID 16395)
-- Name: database; Type: SCHEMA; Schema: -; Owner: user
--

CREATE SCHEMA database;


ALTER SCHEMA database OWNER TO "user";

--
-- TOC entry 178 (class 3079 OID 11855)
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner:
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- TOC entry 2035 (class 0 OID 0)
-- Dependencies: 178
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner:
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = database, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- TOC entry 173 (class 1259 OID 16396)
-- Name: Companies; Type: TABLE; Schema: database; Owner: user; Tablespace:
--

CREATE TABLE "Companies" (
    company_id integer NOT NULL,
    company_symbol text,
    company_name text
);


ALTER TABLE "Companies" OWNER TO "user";

--
-- TOC entry 177 (class 1259 OID 16440)
-- Name: MetricTypes; Type: TABLE; Schema: database; Owner: user; Tablespace:
--

CREATE TABLE "MetricTypes" (
    metric_type_id integer NOT NULL,
    metric_type_name text
);


ALTER TABLE "MetricTypes" OWNER TO "user";

--
-- TOC entry 176 (class 1259 OID 16430)
-- Name: Metrics; Type: TABLE; Schema: database; Owner: user; Tablespace:
--

CREATE TABLE "Metrics" (
    metric_id integer NOT NULL,
    tweet_id integer,
    metric_type_id integer,
    metric_value double precision
);


ALTER TABLE "Metrics" OWNER TO "user";

--
-- TOC entry 174 (class 1259 OID 16409)
-- Name: Quotes; Type: TABLE; Schema: database; Owner: user; Tablespace:
--

CREATE TABLE "Quotes" (
    quite_id integer NOT NULL,
    company_id integer,
    ask double precision,
    volume integer,
    "time" timestamp without time zone
);


ALTER TABLE "Quotes" OWNER TO "user";

--
-- TOC entry 175 (class 1259 OID 16420)
-- Name: Tweets; Type: TABLE; Schema: database; Owner: user; Tablespace:
--

CREATE TABLE "Tweets" (
    tweet_id integer NOT NULL,
    company_id integer,
    "time" timestamp without time zone
);


ALTER TABLE "Tweets" OWNER TO "user";

--
-- TOC entry 2023 (class 0 OID 16396)
-- Dependencies: 173
-- Data for Name: Companies; Type: TABLE DATA; Schema: database; Owner: user
--

COPY "Companies" (company_id, company_symbol, company_name) FROM stdin;
\.


--
-- TOC entry 2027 (class 0 OID 16440)
-- Dependencies: 177
-- Data for Name: MetricTypes; Type: TABLE DATA; Schema: database; Owner: user
--

COPY "MetricTypes" (metric_type_id, metric_type_name) FROM stdin;
\.


--
-- TOC entry 2026 (class 0 OID 16430)
-- Dependencies: 176
-- Data for Name: Metrics; Type: TABLE DATA; Schema: database; Owner: user
--

COPY "Metrics" (metric_id, tweet_id, metric_type_id, metric_value) FROM stdin;
\.


--
-- TOC entry 2024 (class 0 OID 16409)
-- Dependencies: 174
-- Data for Name: Quotes; Type: TABLE DATA; Schema: database; Owner: user
--

COPY "Quotes" (quite_id, company_id, ask, volume, "time") FROM stdin;
\.


--
-- TOC entry 2025 (class 0 OID 16420)
-- Dependencies: 175
-- Data for Name: Tweets; Type: TABLE DATA; Schema: database; Owner: user
--

COPY "Tweets" (tweet_id, company_id, "time") FROM stdin;
\.


--
-- TOC entry 1899 (class 2606 OID 16403)
-- Name: company_id_pk; Type: CONSTRAINT; Schema: database; Owner: user; Tablespace:
--

ALTER TABLE ONLY "Companies"
    ADD CONSTRAINT company_id_pk PRIMARY KEY (company_id);


--
-- TOC entry 1907 (class 2606 OID 16434)
-- Name: metric_id_pk; Type: CONSTRAINT; Schema: database; Owner: user; Tablespace:
--

ALTER TABLE ONLY "Metrics"
    ADD CONSTRAINT metric_id_pk PRIMARY KEY (metric_id);


--
-- TOC entry 1909 (class 2606 OID 16447)
-- Name: metric_type_id_pk; Type: CONSTRAINT; Schema: database; Owner: user; Tablespace:
--

ALTER TABLE ONLY "MetricTypes"
    ADD CONSTRAINT metric_type_id_pk PRIMARY KEY (metric_type_id);


--
-- TOC entry 1902 (class 2606 OID 16413)
-- Name: quite_id_pk; Type: CONSTRAINT; Schema: database; Owner: user; Tablespace:
--

ALTER TABLE ONLY "Quotes"
    ADD CONSTRAINT quite_id_pk PRIMARY KEY (quite_id);


--
-- TOC entry 1904 (class 2606 OID 16424)
-- Name: tweet_id_pk; Type: CONSTRAINT; Schema: database; Owner: user; Tablespace:
--

ALTER TABLE ONLY "Tweets"
    ADD CONSTRAINT tweet_id_pk PRIMARY KEY (tweet_id);


--
-- TOC entry 1900 (class 1259 OID 16419)
-- Name: fki_company_id_fk; Type: INDEX; Schema: database; Owner: user; Tablespace:
--

CREATE INDEX fki_company_id_fk ON "Quotes" USING btree (company_id);


--
-- TOC entry 1905 (class 1259 OID 16453)
-- Name: fki_metric_type_id_metrics_fk; Type: INDEX; Schema: database; Owner: user; Tablespace:
--

CREATE INDEX fki_metric_type_id_metrics_fk ON "Metrics" USING btree (metric_type_id);


--
-- TOC entry 1910 (class 2606 OID 16414)
-- Name: company_id_quotes_fk; Type: FK CONSTRAINT; Schema: database; Owner: user
--

ALTER TABLE ONLY "Quotes"
    ADD CONSTRAINT company_id_quotes_fk FOREIGN KEY (company_id) REFERENCES "Companies"(company_id);


--
-- TOC entry 1911 (class 2606 OID 16425)
-- Name: company_id_tweets_fk; Type: FK CONSTRAINT; Schema: database; Owner: user
--

ALTER TABLE ONLY "Tweets"
    ADD CONSTRAINT company_id_tweets_fk FOREIGN KEY (company_id) REFERENCES "Companies"(company_id);


--
-- TOC entry 1913 (class 2606 OID 16448)
-- Name: metric_type_id_metrics_fk; Type: FK CONSTRAINT; Schema: database; Owner: user
--

ALTER TABLE ONLY "Metrics"
    ADD CONSTRAINT metric_type_id_metrics_fk FOREIGN KEY (metric_type_id) REFERENCES "MetricTypes"(metric_type_id);


--
-- TOC entry 1912 (class 2606 OID 16435)
-- Name: tweet_id_metrics; Type: FK CONSTRAINT; Schema: database; Owner: user
--

ALTER TABLE ONLY "Metrics"
    ADD CONSTRAINT tweet_id_metrics FOREIGN KEY (tweet_id) REFERENCES "Tweets"(tweet_id);


--
-- TOC entry 2034 (class 0 OID 0)
-- Dependencies: 5
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


-- Completed on 2015-05-11 00:31:52

--
-- PostgreSQL database dump complete
--