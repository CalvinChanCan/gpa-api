# General Purpose Accounting (GPA) System

## Requirements
Python <= 3.11
Postgresql <= 15.1


## Setup
1. Download and install postgres locally. 
   a. Create a new database `gpa`
2. Clone this repository and run `pip install -r requirements.txt`.
3. Create `.env` file with the variables found in `.env.example`
4. Run `python manage.py makemigrations` and `python manage.py migrate`  
5. Run `python manage.py runserver` to start the api server.
6. Run `python manage.py createsuperuser` to create a superuser
7. Login to `127.0.0.1:8000/admin` as the superuser to create some sample accounts and transactions.

## Useful commands:
```shell
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
python -m black .
```
