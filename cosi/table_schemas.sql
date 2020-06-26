CREATE TABLE tles
(
    id integer NOT NULL,
    header_text text,
    first_line text,
    second_line text,
    time_added timestamp without time zone NOT NULL,
    PRIMARY KEY (id),
    CONSTRAINT pass_uk UNIQUE (header_text, time_added)
);

CREATE TABLE pass
(
    uid integer NOT NULL,
    latitude double precision NOT NULL,
    longtitude double precision NOT NULL,
    start_time timestamp without time zone NOT NULL,
    end_time time without time zone NOT NULL,
    azimuth integer,
    altitude integer,
    PRIMARY KEY (uid),
    CONSTRAINT pass_def UNIQUE (longtitude, latitude, start_time)
);


CREATE TABLE requests
(
    user_token text NOT NULL,
    approved boolean,
    sent boolean,
    PRIMARY KEY (user_token)
);

/*
	A pass doesnt exist without a request
	every request has a 1-to-1 relationship defined with a 'pass' 
	A pass has many-to-1 relationship with requests
*/

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

