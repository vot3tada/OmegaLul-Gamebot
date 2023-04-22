CREATE TABLE boss(
    id SERIAL PRIMARY KEY,
    name varchar(100),
    photo text,
    hp integer,
    damage integer,
    luck float,
    money_reward integer,
    exp_reward integer,
    ulta_charge integer,
    cleave_rate integer,
    ulta_rate integer,
    item_id integer REFERENCES item(id)
);

INSERT INTO boss(name,photo,hp,damage,luck,money_reward,exp_reward,ulta_charge,cleave_rate,ulta_rate,item_id)
VALUES('Батя Коллектора','father.jpg',750,47,0.3,1000,850,5,0.35,0.5,33),
      ('Кыксик','kiksik.jpg',690,49,0.65,1200,1050,2,0.51,0.1,34),
      ('Жаба','frog.jpg',1200,30,0.1,1500,1300,6,0.7,0.9,35),
      ('Местный Каламит','dragon.jpg',1500,46,0.45,2000,1800,7,0.51,0.4,36);