release: python manage.py migrate
worker: celery -A reddit_django worker
web: gunicorn reddit_django.wsgi
