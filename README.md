Развертывание:

1) Создайте окружение python (3.5-3.7) >> python3 -m venv env
2) Активируйте окружение >> source env/bin/activate
3) Установите зависимости >> pip install -r requirements.txt
4) Перейдите в папку проекта
5) Укажите параметры подключения к бд : app/config.py
6) Создайте первую миграцию >> python manager.py db migrate
7) Произведите миграцию >> python manager.py db upgrade
8) Загрузите фикстуры >> python manager.py initial_data app/fixtures/initial.json
9) Создайте первого юзера-админа >> python manager.py create_admin <username> <password>
10) Запустите приложение >> python manage.py run
11) Откройте в браузере http://localhost:5000