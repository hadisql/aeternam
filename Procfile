web: gunicorn aeternam.wsgi:application

predeploy: echo "echoing pwd ->" && pwd && cd jstoolchain && npm run tailwind-build

release: django-admin migrate --no-input && django-admin collectstatic --no-input
