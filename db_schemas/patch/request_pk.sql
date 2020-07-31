ALTER TABLE requests DROP CONSTRAINT requests_pkey CASCADE;	
ALTER TABLE requests ADD COLUMN uid INTEGER;
CREATE SEQUENCE requests_seq OWNED BY requests.uid;

ALTER TABLE requests ALTER COLUMN uid SET DEFAULT nextval('requests_seq');
UPDATE requests SET uid = nextval('requests_seq');
ALTER TABLE requests ADD PRIMARY KEY (uid);
ALTER TABLE requests ADD CONSTRAINT user_token_uq UNIQUE (user_token);

ALTER TABLE pass_requests
ADD CONSTRAINT pass_fk FOREIGN KEY (pass_id)
        REFERENCES pass (uid) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
;

  
ALTER TABLE user_tokens
ADD CONSTRAINT user_token_token_fkey FOREIGN KEY (token)
        REFERENCES public.requests (user_token) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
;
