CREATE TABLE work(
    id integer PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    name varchar(255),
    level_required integer,
    exp_reward integer,
    money_reward integer
)