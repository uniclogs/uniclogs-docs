CREATE TABLE requests
(
    user_token text NOT NULL,
    approved boolean,
    sent boolean,
    PRIMARY KEY (user_token)
);
