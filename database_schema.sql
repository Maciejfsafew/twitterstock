SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;


CREATE TABLE "Companies" (
    company_id serial primary key,
    company_symbol VARCHAR(10),
    company_name VARCHAR(50)
);


ALTER TABLE "Companies" OWNER TO "user";

CREATE TABLE "MetricTypes" (
    metric_type_id serial primary key,
    metric_type_name text
);


ALTER TABLE "MetricTypes" OWNER TO "user";

CREATE TABLE "Metrics" (
    metric_id serial primary key,
    tweet_id integer,
    metric_type_id integer,
    metric_value double precision
);


ALTER TABLE "Metrics" OWNER TO "user";

CREATE TABLE "Quotes" (
    quote_id serial primary key,
    company_id integer,
    ask double precision,
    volume integer,
    "time" timestamp without time zone
);

ALTER TABLE "Quotes" OWNER TO "user";


CREATE TABLE "Tweets" (
    tweet_id serial primary key,
    company_id integer,
    "time" timestamp without time zone,
    text text
);


ALTER TABLE "Tweets" OWNER TO "user";


CREATE INDEX fki_company_id_fk ON "Quotes" USING btree (company_id);

CREATE INDEX fki_metric_type_id_metrics_fk ON "Metrics" USING btree (metric_type_id);


ALTER TABLE ONLY "Quotes"
    ADD CONSTRAINT company_id_quotes_fk FOREIGN KEY (company_id) REFERENCES "Companies"(company_id);

ALTER TABLE ONLY "Tweets"
    ADD CONSTRAINT company_id_tweets_fk FOREIGN KEY (company_id) REFERENCES "Companies"(company_id);

ALTER TABLE ONLY "Metrics"
    ADD CONSTRAINT metric_type_id_metrics_fk FOREIGN KEY (metric_type_id) REFERENCES "MetricTypes"(metric_type_id);

ALTER TABLE ONLY "Metrics"
    ADD CONSTRAINT tweet_id_metrics FOREIGN KEY (tweet_id) REFERENCES "Tweets"(tweet_id);

