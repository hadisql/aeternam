web: gunicorn aeternam.wsgi:application & npm run tailwind-build & wait -n

release: django-admin migrate --no-input && django-admin collectstatic --no-input

postdeploy: echo "postdeploy.."
