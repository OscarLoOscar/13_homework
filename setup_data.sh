echo 'Applying Migrations...'
python manage.py makemigrations
python manage.py migrate

echo 'Fetching data from API...'
python manage.py fetch_data

echo 'Starting Server...'
python manage.py runserver