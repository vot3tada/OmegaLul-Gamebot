CREATE TABLE inventory(
    item_id integer REFERENCES item(id) ON DELETE CASCADE,
    person_id_chatId integer not null,
    person_id_userId integer not null,
    FOREIGN KEY (person_id_userId, person_id_chatId) REFERENCES person(user_id, chat_id) ON DELETE CASCADE
);

CREATE TABLE status(
    item_id integer REFERENCES item(id) ON DELETE CASCADE,
    person_id_chatId integer not null,
    person_id_userId integer not null,
    FOREIGN KEY (person_id_userId, person_id_chatId) REFERENCES person(user_id, chat_id) ON DELETE CASCADE
);