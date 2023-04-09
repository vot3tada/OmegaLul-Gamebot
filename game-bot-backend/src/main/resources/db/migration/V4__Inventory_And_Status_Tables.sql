CREATE TABLE inventory(
    item_id integer REFERENCES item(id),
    person_id_chatId integer not null,
    person_id_userId integer not null,
    FOREIGN KEY (person_id_userId, person_id_chatId) REFERENCES person(user_id, chat_id)
);

CREATE TABLE status(
    item_id integer REFERENCES item(id),
    person_id_chatId integer not null,
    person_id_userId integer not null,
    FOREIGN KEY (person_id_userId, person_id_chatId) REFERENCES person(user_id, chat_id)
);