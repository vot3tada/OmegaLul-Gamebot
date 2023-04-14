DROP TABLE inventory;

CREATE TABLE inventory(
    id SERIAL PRIMARY KEY,
    count integer,
    item_id integer REFERENCES item(id),
    person_chat_id integer,
    person_user_id integer,
    FOREIGN KEY (person_chat_id, person_user_id) REFERENCES person(chat_id, user_id)
);