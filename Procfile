web: gunicorn aeternam.wsgi:application

release: django-admin migrate --no-input && django-admin collectstatic --no-input && python manage.py thumbnail cleanup
