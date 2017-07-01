CREATE TABLE "user" (
    id serial PRIMARY KEY,
    username varchar(255) NOT NULL,
    password varchar(255) NOT NULL
);

CREATE TABLE "planet_votes" (
    id serial PRIMARY KEY,
    planet_id int NOT NULL,
    planet_name varchar(255) NOT NULL,
    user_id int REFERENCES "user"(id),
    submission_time timestamp without time zone DEFAULT date_trunc('second'::text, now())
);