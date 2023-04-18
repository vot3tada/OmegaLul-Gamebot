**Все поля в json (нужно установить хедар application/json), писать camelCase`ом см. примеры ниже**

# Person

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
   
5. Удаление всех пользователей в определенном чате: DELETE: **localhost:8080/api/person/delete/{chatId}**
   >Success: Status 204

   >Fail: Status 400,404,500
### Пример
Body выглядит следующим образом, обратите внимание как вводится первичный ключ при добавлении персонажа.

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
      }

# Items and effects

1. Получение всех итемов и их эфектов: GET: **localhost:8080/api/item/all**

   >Success: Status 200

   >Fail: Status 500 (но это врятли)

2. Получение предмета и его свойств по id: GET: **localhost:8080/api/item/id/{id}**

   >Success: Status 200

   >Fail: Status 404,500

3. Добавление предмета и его свойств: POST: **localhost:8080/api/item/create**

   >Success: Status 201

   >Fail: Status 400,500

4. Удаление предмета и всех его свойств по id: DELETE: **localhost:8080/api/item/delete/{id}**

   >Success: Status 204

   >Fail: Status 400,404,500

### Пример
Body выглядит следующим образом, обратите внимание как вводятся свойства предмета.

    {
        "name":"aboba",
        "price":12,
        "description":"rgdfgfdg",
        "duration":12,
        "effects":[{
            "property":"hp",
            "value":443
        }]
    }

# Inventory

1. Получение всего инвентаря пользователя: GET: **localhost:8080/api/inventory/id/{chatId}/{userId}**

   >Success: Status 200

   >Fail: Status 400, 500 (но это врятли)

2. Добавление предмета в инвентарь(поставил метод PUT вроде подходит): PUT:**localhost:8080/api/inventory/update** (см. пример ввода body)

   >Success: Status 204

   >Fail: Status 400,404,500

3. Удаление предмета из инвентаря по айдишнику предмета: DELETE: **localhost:8080/api/inventory/delete** (itemId, userId, chatId в body)

   >Success: Status 204

   >Fail: Status 400,404,500

### Пример


        {
            "itemId":2,
            "count":3,
            "chatId":4,
            "userId":3
        }

# Work 

1. Получение всего списка работ: GET: **localhost:8080/api/work/all**

   >Success: Status 200

   >Fail: Status 400, 500 (но это врятли)

2. Добавление работы: POST: **localhost:8080/api/work/create** (см. пример ввода body)

   >Success: Status 204

   >Fail: Status 400,404,500

3. Удаление работы по айдишнику: DELETE: **localhost:8080/api/work/delete/{id}**

   >Success: Status 204

   >Fail: Status 400,404,500

### Пример


      {
         "name":"aboba",
         "levelRequired":2,
         "expReward":2,
         "moneyReward":2
      }

# Task
1. Получение всех тасков: GET: **localhost:8080/api/task/all** 
   >Success: Status 200

   >Fail: Status 400, 500 (но это врятли)
2. Получение свободных тасков: GET: **localhost:8080/api/task/free**
   >Success: Status 200

   >Fail: Status 400, 500 (но это врятли)
3. Получение тасков, взятых пользователем: GET: **localhost:8080/api/task/taken/{workerUserId}/{chatId}**
   >Success: Status 200

   >Fail: Status 400, 500 (но это врятли)
4. Получение тасков, созданных пользователем: GET: **localhost:8080/api/task/person/{ownerUserId}/{chatId}**
   >Success: Status 200

   >Fail: Status 400, 500 (но это врятли)
5. Обновление таска в обе стороны(см. пример): PUT: **localhost:8080/api/task/update**
   >Success: Status 204

   >Fail: Status 400, 404, 500 
6. Добавление таска(см. пример): POST: **localhost:8080/api/task/create**
   >Success: Status 201

   >Fail: Status 400, 404, 500 
7. Удаление таска по айдишнику: DELETE: **localhost:8080/api/task/delete/{id}**
   >Success: Status 204

   >Fail: Status 400, 404, 500 

### Пример
Обратите внимание на ввод дедлайна(yyyy-MM-dd HH:mm:ss)

**Добавление таска**

      {
      "name":"aboba",
      "money":2,
      "duration":2,
      "chatId":3,
      "ownerUserId":3
      }

**Апдейта таска(принять таск)**

      {
      "id:2,
      "workerUserId":2,
      "deadline":"2023-12-12 20:20:20"
      }

**Апдейт таска(отказаться от таска)**

      {
      "id:2,
      "workerUserId":null,
      "deadline":null
      }

# History
1. Получение истории по чат-юзер айдишнику: GET **localhost:8080/api/history/id/{chatId}/{userId}**
   >Success: Status 200

   >Fail: Status 400, 404, 500(но это врятли)

2. Апдейт истории(см. пример): PUT: **localhost:8080/api/history/update**
   >Success: Status 204

   >Fail: Status 400, 404, 500

### Пример 

          {
            "chatId": 8,
            "userId": 8,
            "totalMoney": 200,
            "totalExp": 200,
            "totalQuestions": 200,
            "totalFights": 200,
            "totalWinFights": 200,
            "totalWinBoss": 200,
            "totalItem": 200,
            "totalTakenTasks": 200,
            "totalEndedTasks": 200,
            "totalFallTasks": 200,
            "totalWinCollector": 200,
            "totalCreateEvent": 200,
            "totalEnterEvent": 200,
            "totalKickEvent": 200,
            "totalLeaveFights": 200
         }

# Event
1. Получить евент по айди: GET: **localhost:8080/api/event/id/{id}**
   >Success: Status 200

   >Fail: Status 400, 404, 500
2. Получить все евенты в чате: GET: **localhost:8080/api/event/chat/{chatId}**
   >Success: Status 200

   >Fail: Status 400, 404, 500
3. Создать евент(см. пример): POST: **localhost:8080/api/event/create**
   >Success: Status 201

   >Fail: Status 400, 404, 500
4. Добавить участника на евент(см. пример): POST: **localhost:8080/api/event/add-member**
   >Success: Status 201

   >Fail: Status 400, 404, 500

5. Кикнуть участника из евента(см. пример): DELETE: **localhost:8080/api/event/delete-member**
   >Success: Status 204

   >Fail: Status 400, 404, 500
### Пример
Обратите внимание на ввод даты(yyyy-MM-dd HH:mm:ss)

**Создание ивента:**

      {
      "name":"boba",
      "startedAt": "2023-12-12 20:20:20",
      "chatId":3,
      "userId":4
      }

**Добавление мембера и удаление:**

      {
      "id":1,//айди евента
      "chatId":3,
      "userId":4
      }

**Так выглядит json /id/{id} реквеста:**

      {
       "id": 2,
       "name": "vfff",
       "startedAt": "2023-12-12 20:20:20",
       "members": [
           {
               "creator": true,
               "chatId": 3,
               "userId": 3
           },
           {
               "creator": false,
               "chatId": 3,
               "userId": 4
           }
       ]
      }

# Quiz
1. Получение всех квизов: GET: **localhost:8080/api/quiz/all**
   >Success: Status 200

   >Fail: Status 400, 404, 500

2. Получение квиза по айди и всех его вопросов: GET: **localhost:8080/api/quiz/id/{id}**
   >Success: Status 200

   >Fail: Status 400, 404, 500
3. Добавление квиза(см. пример): POST: **localhost:8080/api/quiz/create**
   >Success: Status 201

   >Fail: Status 400, 404, 500
4. Добавление вопроса к квизу(см. пример): POST: **localhost:8080/api/quiz/add/question**
   >Success: Status 201

   >Fail: Status 400, 404, 500
5. Удаление квиза по айди и всех его вопросов: DELETE: **localhost:8080/api/quiz/delete/{id}**
   >Success: Status 204

   >Fail: Status 400, 404, 500

### Пример
**Как выглядит json при получении всех квизов:**

      [
         {
         "id": 2,
         "name": "aboba",
         "photo": "dgdf"
         },
         {
         "id": 4,
         "name": "aboba",
         "photo": "dgdf"
         }
      ]

**Как выглядит json когда при получении квиза и его вопросов:**

      {
      "id": 4,
      "name": "aboba",
      "photo": "dgdf",
      "questions": [
         {
            "id": 4,
            "text": "aboba",
            "answer": "ddfgf",
            "photo": "dgdf",
            "quizId": 4
         }
         ]
      }

**Json при добавление квиза:**
      
      {
        "name": "aboba",
        "photo": "dgdf"
      }

**Json при добавлении вопроса к квизу:**

      {
        "text": "aboba",
        "photo": "dgdf",
        "answer":"fsddfg",
        "quizId":12
      }
## !!!ВАЖНО!!!
После каждого git pull репы, запуск контейнера будет таким: docker compose up -d --build

Последующие запуски просто: docker compose up

Также следите за тем, чтобы контейнер был выключен когда вы им не пользуетесь, так как он юзает 8080 порт))