## Hasker
Проект для изучения возможностей django.
Аналог stackoverflow

### Функционал

#### Пользователи
 - Регистрация/Логин/Изменение профиля/логаут
 - Возможность залить аватарку
 
#### Вопросы
 - Возможность задать вопрос с указанием тегов
 - Список вопросов с пагинаций
 - Сортировка по рейтингу и дате публикации
 - Поиск по тегам
 - Поиск по заголовку и содержанию ответов
 - Блок самых популярных вопросов
 - Возможность голосовать за вопросы
 
#### Ответы
 - Возможность написать ответ на вопрос
 - Список ответов с пагинацией c сортировкой по рейтингу и дате публикации
 - Возможность голосовать на ответы
 - Автор вопроса может пометить ответ как правильный
 - Автор вопроса получает емейл при публикации нового ответа
 
### СI
Наcтроена интерация с Travis CI.
Тесты запускаются автоматически на каждый коммит


#### Local Tests
```
python manage.py test --settings=hasker.settings.local --verbosity=2
```

#### Prod Tests
```
python manage.py test --settings=hasker.settings.production --verbosity=2
```

### Deploy
Настроена интеграция с Heroku.
Деплой происходит после успешного прохождения тестов
Отправка емейлов работает через sendgrid

#### Local Run
```
python manage.py migrate
python manage.py runserver --settings.hasker.local
```
