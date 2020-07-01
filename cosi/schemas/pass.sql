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
