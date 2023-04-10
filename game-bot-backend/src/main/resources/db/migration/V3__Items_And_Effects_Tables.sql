CREATE TABLE item(
    id integer PRIMARY KEY,
    name varchar(30),
    price integer,
    description varchar (255),
    duration  integer
);

CREATE TABLE effect(
    id integer PRIMARY KEY,
    property varchar(20),
    value integer,
    item_id integer REFERENCES item(id) ON DELETE CASCADE
);