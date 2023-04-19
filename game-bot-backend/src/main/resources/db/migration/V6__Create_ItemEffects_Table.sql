ALTER TABLE effect
DROP item_id;

CREATE TABLE item_effects(
    effect_id integer REFERENCES effect(id),
    item_id integer REFERENCES item(id)
);