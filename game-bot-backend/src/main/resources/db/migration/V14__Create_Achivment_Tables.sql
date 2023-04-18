CREATE TABLE achievement(
    id varchar(255) PRIMARY KEY,
    name varchar(255),
    photo varchar(255),
    condition integer,
    description text
);

CREATE TABLE person_achievement(
    achievement_id varchar(255) REFERENCES achievement(id),
    person_chat_id integer,
    person_user_id integer,
    FOREIGN KEY (person_chat_id, person_user_id) REFERENCES person(chat_id, user_id)
);

INSERT INTO achievement(id,name, photo, condition, description)
VALUES ('totalMoney','Пончик','totalMoney.jpg',100000,'Своим трудом заработать 100000 денег'),
       ('totalExp','Старец','totalExp.jpg',100000,'Заработать 100000 опыта'),
       ('totalQuestions','Крутите барабан','totalQuestions.jpg',100,'Ответить на 100 вопросов'),
       ('totalFights','Ты знаешь Тайлера?','totalFights.jpg',100,'Поучавствовать в 100 битвах'),
       ('totalWinFights','Баки','totalWinFights.jpg',100,'Победить в 100 битвах'),
       ('totalWinBoss','Искатель приключений','totalWinBoss.jpg',1,'Победить босса'),
       ('totalItem','Барахольщик','totalItem.jpg',100,'Купить 100 предметов'),
       ('totalTakenTasks','Ривийский акцент','totalTakenTasks.jpg',100,'Взять 100 заданий с доски'),
       ('totalEndedTasks','Миска риса','totalEndedTasks.jpg',10,'Выполнить 10 заданий с доски'),
       ('totalFallTasks','Шляпа','totalFallTasks.jpg',10,'Прошляпить выполнение 10 заданий с доски'),
       ('totalWinCollector','Коллектор-звонилка','totalWinCollector.jpg',1,'Победить коллектора'),
       ('totalCreateEvent','Тамада','totalCreateEvent.jpg',10,'Провести 10 мероприятий'),
       ('totalEnterEvent','Таксист','totalEnterEvent.jpg',10,'Посетить 10 мероприятий'),
       ('totalKickEvent','Футболист','totalKickEvent.jpg',10,'Выгнать 10 посетителей'),
       ('totalLeaveFights','Сопляк','totalLeaveFights.jpg',1,'Сбежать с битвы');