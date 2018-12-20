release: python manage.py makemigrations core
release: python manage.py migrate core
web: gunicorn phone_calls.wsgi --log-file -
