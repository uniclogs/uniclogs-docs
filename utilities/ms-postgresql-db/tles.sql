CREATE TABLE tles
(
    header_text text NOT NULL,
    first_line text NOT NULL,
    second_line text NOT NULL,
    time_added timestamp without time zone NOT NULL,
    PRIMARY KEY (header_text, time_added),
    CONSTRAINT pass_uk UNIQUE (header_text, time_added)
);
