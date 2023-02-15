Сайт знакомств на Django.

***[Calambug](https://calambug.fun/)*** <em>\- знакомства</em> и общение с интересными людьми по всему миру. Присоединяйся и найди новых друзей уже сегодня.

### TODO

***

* Рефакторинг
* ~~Поиск пользователей~~
* ~~Фильтр пользователей в главном меню~~
* Фотоальбом пользователя
* ~~Лайк/дизлайк пользователя~~
* Стена пользователя
* ~~Превью профиля~~
* ~~Бар-успеха для показа успешности аккаунта по заполненным данным~~

### Установка

***

```
git clone https://github.com/towiron/dating-web-app.git
python3 -m venv virtualenv_name
souce virtualenv_name/bin/activate
pip3 install -r req.txt
```

### Запуск

***

```
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver
```