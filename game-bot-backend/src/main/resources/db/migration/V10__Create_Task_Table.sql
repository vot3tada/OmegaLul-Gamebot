CREATE TABLE task(
    id SERIAL PRIMARY KEY,
    name text,
    money integer,
    duration bigint,
    worker_user_id integer,
    deadline timestamp,
    person_chat_id integer,
    person_owner_user_id integer,
    FOREIGN KEY (person_chat_id, person_owner_user_id) REFERENCES person(chat_id, user_id)
);