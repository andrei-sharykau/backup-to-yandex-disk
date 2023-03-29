# Бэкап MySQL и файлов с загрузкой на Yandex Disk

## Параметры скрипта 

```
ACTIONS = {
    'sites_backup': True,
    'databases_backup': True
}
```
* **sites_backup** - делать бэкап фалов (True -да, False - нет)
* **databases_backup** - делать бэкап базы MySQL (True -да, False - нет)

```
YANDEX_CONFIG = {
    'yandex_url' : "https://cloud-api.yandex.net/v1/disk/resources",
    'yandex_token' : "yandex_token",
    'yandex_backup_folder' : "/backup/",
}
```
* **yandex_url** - путь к YandexApi (по умолчанию 'https://cloud-api.yandex.net/v1/disk/resources')
* **yandex_token** - токен Вашего приложения в Yandex
* **yandex_backup_folder** - каталог на Yandex Disk для бэкапа (нужно создать руками)

```
TEMP_PATH = '/tmp/backup/'
```
Путь к временной папке

```
SITES = [
    {"path": "/path/your/file", "arch_name": "arch_name"},
]
```
Каталоги которые нужно бэкапить
* **path** - путь к каталогу
* **arch_name** - имя архива

```
DATABASES = [
    {"db_name": "database_name", "login-path": "login-path"},
]
```
Базы данных MySQL которые нужно бэкапить
* **db_name** - имя базы даныых
* **login-path** - шаблон имя_пользователя/пароль для подключения к базе данных, используется чтобы не использоватьв открытую пароль (https://dev.mysql.com/doc/refman/8.0/en/mysql-config-editor.html)
