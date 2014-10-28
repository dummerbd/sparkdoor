web: waitress-serve --port=$PORT sparkdoor.wsgi.heroku:application
celery: celery -A sparkdoor worker
beat: celery -A sparkdoor beat
