release: python manage.py migrate
worker: celery -A reddit_django worker -l info
web: gunicorn reddit_django.wsgi
