CREATE TABLE pass
(
    uid integer NOT NULL,
    latitude double precision NOT NULL,
    longtitude double precision NOT NULL,
    start_time timestamp without time zone NOT NULL,
    end_time timestamp without time zone NOT NULL,
    azimuth integer,
    altitude integer,
    elevation double precision NOT NULL,
    PRIMARY KEY (uid),
    CONSTRAINT pass_def UNIQUE (longtitude, latitude, start_time)
);
