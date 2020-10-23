# simple_rest

```sh
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
$ chmod +x ./app.py 
$ ./app.py
```

### Actions

Для добавления новых действий надо добавить модуль в пакет actions и его функции станут доступны.

### ICQ bot

Для использования ICQ bot необходимо экспортировать переменную
```sh
$ export icqbot_[name]=[token]
```

### Docker

```sh
$ docker build -t simple_rest .
$ docker run --restart=unless-stopped \
--name simple_rest_1 -d -p 8800:8800 \
-e icqbot_[name]=[token] \
-e icqbot_[name]=[token] \
simple_rest
```
