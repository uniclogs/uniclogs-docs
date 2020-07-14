CREATE TABLE requests
(
    user_token text NOT NULL,
    is_approved boolean,
    is_sent boolean,
    pass_uid integer,
    created_date timestamp without time zone,
    observation_type integer,
    CONSTRAINT requests_pkey PRIMARY KEY (user_token),
    CONSTRAINT pass_fk FOREIGN KEY (pass_uid)
        REFERENCES public.pass (uid) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
);
