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
