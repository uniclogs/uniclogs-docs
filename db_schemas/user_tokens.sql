CREATE TABLE user_tokens
(
    token text NOT NULL,
    user_id character varying(155),
    CONSTRAINT user_token_token_fkey FOREIGN KEY (token)
        REFERENCES requests (user_token) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
);
