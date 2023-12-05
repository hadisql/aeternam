web: gunicorn aeternam.wsgi:application

release: django-admin migrate --no-input && django-admin collectstatic --no-input && npm run tailwind-build
