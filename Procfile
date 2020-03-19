release: python manage.py migrate
web: gunicorn reddit_django.wsgi
worker: celery -A reddit_django worker
