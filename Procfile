web: gunicorn norm.wsgi --log-file - --log-level debug
worker: celery -A norm worker -l debug
beat: celery -A norm beat -l debug