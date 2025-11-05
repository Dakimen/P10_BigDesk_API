# P10_BigDesk_API

API project

## Launching the API

1. Clone the repository

```
git clone https://github.com/Dakimen/P10_BigDesk_API.git
cd P10_BigDesk_API
```

2. Create and activate a virtual environment

```
python -m venv .venv
.venv\Scripts\Activate
```

3. Install dependencies

```
pip install -r requirements.txt
```

4. Create a .env file in the project root (do not commit it).

In P10_BigDesk_API/SoftDesk/SoftDesk create a .env file containing a variable DJANGO_SECRET_KEY.
This key can be generated using this command:

```
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

The generated value now has to be assigned to this new variable.

5. Run migrations

```
cd SoftDesk
python manage.py makemigrations
python manage.py migrate
```

6. Start the development server.

```
python manage.py runserver
```

Now the API is functional and requests can be sent to the urls defined in the urls.py file
