web: gunicorn family_book.wsgi:application

release: django-admin migrate --no-input && django-admin collectstatic --no-input
