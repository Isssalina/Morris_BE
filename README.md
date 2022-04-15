# Morris_BE
### Clean Database

```
cd Morris_BE
rm -rf db.sqlite3
rm -rf ./api/migrations
python manage.py makemigrations api
python manage.py migrate
```
### Create Superuser
```
python manage.py createsuperuser
```
