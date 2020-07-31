CREATE SEQUENCE requests_seq start 1 increment 1;

CREATE TABLE requests
(
    uid integer NOT NULL DEFAULT nextval('requests_seq'),
    user_token text NOT NULL,
    is_approved boolean,
    is_sent boolean,
    pass_uid integer,
    created_date timestamp without time zone,
    updated_date timestamp without time zone,
    observation_type character varying(120), --uniclogs, oresat live, CFC”
    CONSTRAINT requests_pkey PRIMARY KEY (uid),
    CONSTRAINT user_token_uq UNIQUE (user_token),
    CONSTRAINT pass_fk FOREIGN KEY (pass_uid)
        REFERENCES public.pass (uid) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
);
