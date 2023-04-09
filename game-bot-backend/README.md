# Person

**Все поля в json писать camelCase`ом см. пример ниже**

1. Получение списка всех person`ов: GET: **localhost:8080/api/person/all**
    >Success: Status 200 
   
2. Получение списка person`ов в конкретном чате: GET: **localhost:8080/api/person/{chatId}**
    >Success: Status 200

   > Fail: Status 404
3. Создание person`a: POST: **localhost:8080/api/person/create**

    Поля необходимые для создания: userId, chatId, name, photo (остальные поля по желанию, но может не сработать, потестите :) )
    >Success: Status 201

    >Fail: Status 400,500
4. Апдейт person`a: PUT: **localhost:8080/api/person/update?userId=1&chatId=1**

    Отправляйте пожалуйста всего персона кроме айдишников.
    >Success: Status 204

   >Fail: Status 400,404,500
   
5. Удаление всех пользователей в определенном чате: **localhost:8080/api/person/delete/{chatId}**
   >Success: Status 204

   >Fail: Status 400,404,500
### Пример
Body выглядит следующим образом, обратите внимание как вводится первичный ключ при добавлении персона.

        {
         "name": "aboba1",
         "experience": null,
         "experienceMultiply": 3,
         "money": 22,
         "photo": "qwert",
         "luck": 1.0,
         "luckMultiply": 2,
         "hp": 100,
         "damage": 200,
         "damageMultiply": 10,
         "personPk": {
            "chatId": 3,
            "userId": 3
        }

## !!!ВАЖНО!!!
После каждого git pull репы, запуск контейнера будет таким: docker compose up -d --build

Последующие запуски просто: docker compose up

Также следите за тем, чтобы контейнер был выключен когда вы им не пользуетесь, так как он юзает 8080 порт))