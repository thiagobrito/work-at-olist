release: python manage.py makemigrations core
release: python manage.py migrate
web: gunicorn phone_calls.wsgi --log-file -
