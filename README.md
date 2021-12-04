# Развёртывание
## А. Сервер оператора:
```
cd operators
pip3 install -r requirements.txt
python3 manage.py migrate
python3 manage.py createsuperuser # создаёте пользователя
python3 manage.py runserver 0.0.0.0:8000
```

## Б. Приложение крана:
`cd flask-app`

выставить в файле app.py `SERVER_URL = 'http://yourserver:8000'`
например: `SERVER_URL = 'http://localhost:8000'`
```
pip3 install -r requirements.txt
sudo apt install memcached
```
Следующие компоненты запустить параллельно, сначала **video_capture.py**. Это можно сделать в разных терминалах или при помощи **tmux**.
```
python3 video_capture.py
python3 app.py
```

# Работа с системой

## Панель крановщика
TODO

...
