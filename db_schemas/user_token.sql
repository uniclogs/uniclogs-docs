CREATE TABLE user_token
(
    token text NOT NULL,
    "user-id" character varying(155),
    CONSTRAINT user_token_pkey PRIMARY KEY (token),
    CONSTRAINT user_token_token_fkey FOREIGN KEY (token)
        REFERENCES public.requests (user_token) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
);
