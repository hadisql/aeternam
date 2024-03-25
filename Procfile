web: gunicorn aeternam.wsgi:application

predeploy: npm run tailwind-build

release: django-admin migrate --no-input && django-admin collectstatic --no-input
