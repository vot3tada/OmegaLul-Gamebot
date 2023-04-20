INSERT INTO item(name,price,description,duration, type)
VALUES
    ('Дизель Барное', 70 ,'Заправься под завязку! Хиляет на 50 хп.',0,'shop'),
    ('Гаечный ключ на 9', 250 ,'Фирменный ключ дяди Богдана, увеличивает силу.',7200,'shop'),
    ('Болгарка',600,'Доктор одобряет, сильно увеличивает силу.',7200,'shop'),
    ('Крестик',250,'Альтернативный способ спасения, увеличивает удачу.',7200,'shop'),
    ('Каска',600,'Более надежный способ спаения, сильно увеличивает удачу.',7200,'shop');

INSERT INTO effect(property,value)
VALUES
    ('hp',50),
    ('damageMultiply',0.4),
    ('damageMultiply',0.60),
    ('luckMultiply',0.4),
    ('luckMultiply',0.60);

INSERT INTO item_effects(item_id,effect_id)
VALUES 
    (28,28),
    (29,29),
    (30,30),
    (31,31),
    (32,32);




INSERT INTO item(name,price,description,duration, type)
VALUES
    ('Список должников', 0 ,'Позволяет выбить деньги вместо коллектора.',0,'boss'),
    ('МеханоГлаз', 0 ,'Глаз механического кота, позволяет предвидеть угрозу.',259200,'boss'),
    ('Жыбий рыр', 0 , 'Средство смазки шестеренок внутри тебя. Увеличивает силу и удачу',259200,'boss'),
    ('Глаз Каламита', 0, 'Око, видевшее много... Мощно увеличивает получаеммый опыт.',259200,'boss');

INSERT INTO effect(property,value)
VALUES
    ('money',600),
    ('luckMultiply',0.7),
    ('damage',20),
    ('luck',0.1),
    ('experienceMultiply', 1);

INSERT INTO item_effects(item_id,effect_id)
VALUES 
    (33,33),
    (34,34),
    (35,35),
    (35,36),
    (36,37);


