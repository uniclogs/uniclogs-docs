CREATE SEQUENCE telemetry_id_seq start 1 increment 1;

CREATE TABLE telemetry (
  id integer NOT NULL DEFAULT nextval('telemetry_id_seq'),
  received_at timestamp without time zone NOT NULL,
  invalid_count integer,
  sensor_used integer,
  vector_body_1 integer,
  vector_body_2 integer,
  vector_body_3 integer,
  vector_valid integer,
  CONSTRAINT telemetry_pkey PRIMARY KEY (id)
);
