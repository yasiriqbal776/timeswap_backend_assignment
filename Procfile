release: python manage.py migrate
web: gunicorn assignment.wsgi:application --log-file -
worker: celery -A assignment worker --loglevel=debug
beat: celery -A assignment beat --loglevel=debug --scheduler django_celery_beat.schedulers:DatabaseScheduler
