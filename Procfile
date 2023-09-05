web: gunicorn family_book.wsgi:application --timeout 0

release: django-admin migrate --no-input && django-admin collectstatic --no-input
