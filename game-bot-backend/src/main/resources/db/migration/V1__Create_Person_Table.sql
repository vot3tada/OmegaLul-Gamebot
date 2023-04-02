CREATE TABLE person(
    name varchar(255) not null,
    experience integer,
    experience_multiply integer DEFAULT 1,
    money integer,
    photo text not null,
    luck float DEFAULT 0.2,
    luck_multiply integer DEFAULT 1,
    hp integer DEFAULT 100,
    damage integer DEFAULT 20,
    damage_multiply integer DEFAULT 1,
    user_id integer not null,
    chat_id integer not null,
    PRIMARY KEY(user_id, chat_id)
)