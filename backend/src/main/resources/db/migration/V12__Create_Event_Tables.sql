CREATE TABLE event(
    id SERIAL PRIMARY KEY,
    name varchar(100),
    started_at timestamp
);

CREATE TABLE person_events(
    id SERIAL PRIMARY KEY,
    creator boolean,
    person_chat_id integer,
    person_user_id integer,
    event_id integer REFERENCES event(id),
    FOREIGN KEY (person_chat_id, person_user_id) REFERENCES person(chat_id, user_id)
);