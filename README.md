
## Адрес приложения
Проект доступен по [адресу](https://foodgramsn.ddns.net/recipes)

Логин admin@mail.ru, pass 1234

**Foodgram** - сервис публикации кулинарных рецептов. Позволяет публиковать рецепты, сохранять избранные, а также формировать список покупок для выбранных рецептов. Можно подписываться на любимых авторов.

## Технологии
Python 3.9
Django 3.2.3
Django REST framework 3.12.4
Nginx
Docker
Postgres

## Установка
* Клонируете репозиторий:
`git@github.com:SergeiN25/foodgram-project-react.git`

* Установите на сервере Docker, Docker Compose:
```
sudo apt install docker.io
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo apt-get install docker-compose-plugin
```

* Локально отредактируйте файл infra/nginx.conf и в строке server_name впишите свой IP

* Скопируйте файлы docker-compose.yml и nginx.conf из директории infra на сервер:
```
scp docker-compose.yml <username>@<host>:/home/<username>/docker-compose.yml
scp nginx.conf <username>@<host>:/home/<username>/nginx.conf
```

* Cоздайте .env файл и впишите:
```
    DB_ENGINE=django.db.backends.postgresql
    DB_NAME=<имя базы данных postgres>
    DB_USER=<пользователь бд>
    DB_PASSWORD=<пароль>
    DB_HOST=db
    DB_PORT=5432
    SECRET_KEY=<секретный ключ проекта django>
```
* На сервере соберите docker-compose:
`sudo docker-compose up -d --build`

* После успешной сборки на сервере выполните команды (только после первого деплоя)
```
sudo docker-compose exec backend python manage.py migrate
sudo docker-compose exec backend python manage.py collectstatic
sudo docker compose -f docker-compose.yml exec backend cp -r /app/static/. /backend_static/static/
sudo docker-compose exec backend python manage.py load_ingredients <Название файла из директории data>
```
* Для работы с Workflow добавьте в Secrets GitHub переменные окружения для работы

## Примеры запросов:
**POST | Создание рецепта: http://127.0.0.1:8000/api/recipes/**

Request:
```
{
  "ingredients": [
    {
      "id": 1123,
      "amount": 10
    }
  ],
  "tags": [
    1,
    2
  ],
  "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
  "name": "string",
  "text": "string",
  "cooking_time": 1
}
```

Response:
```
{
  "id": 0,
  "tags": [
    {
      "id": 0,
      "name": "Завтрак",
      "color": "#E26C2D",
      "slug": "breakfast"
    }
  ],
  "author": {
    "email": "user@example.com",
    "id": 0,
    "username": "string",
    "first_name": "Вася",
    "last_name": "Пупкин",
    "is_subscribed": false
  },
  "ingredients": [
    {
      "id": 0,
      "name": "Картофель отварной",
      "measurement_unit": "г",
      "amount": 1
    }
  ],
  "is_favorited": true,
  "is_in_shopping_cart": true,
  "name": "string",
  "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
  "text": "string",
  "cooking_time": 1
}
```

**`POST` | Подписаться на пользователя: `http://127.0.0.1:8000/api/users/{id}/subscribe/`**

Response:
```
{
  "email": "user@example.com",
  "id": 0,
  "username": "string",
  "first_name": "Вася",
  "last_name": "Пупкин",
  "is_subscribed": true,
  "recipes": [
    {
      "id": 0,
      "name": "string",
      "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
      "cooking_time": 1
    }
  ],
  "recipes_count": 0
}
```
