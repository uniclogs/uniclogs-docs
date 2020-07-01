-- A pass doesnt exist without a request
-- every request has a 1-to-1 relationship defined with a 'pass'
-- A pass has many-to-1 relationship with requests

CREATE TABLE pass_requests
(
    pass_id integer NOT NULL,
    req_token text NOT NULL,
    PRIMARY KEY (pass_id, req_token),
    CONSTRAINT pass_fk FOREIGN KEY (pass_id)
        REFERENCES pass (uid) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID,
    CONSTRAINT req_fk FOREIGN KEY (req_token)
        REFERENCES requests (user_token) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
);
