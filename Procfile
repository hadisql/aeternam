web: gunicorn aeternam.wsgi:application

release: django-admin migrate --no-input && django-admin collectstatic --no-input

predeploy: echo "predeploy.."
