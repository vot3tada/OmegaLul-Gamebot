CREATE TABLE quiz(
    id SERIAL PRIMARY KEY,
    name varchar(255),
    photo text
);

CREATE TABLE question(
    id SERIAL PRIMARY KEY,
    text text,
    answer text,
    photo text,
    quiz_id integer REFERENCES quiz(id)
);