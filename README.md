# General Purpose Accounting (GPA) System

## Requirements
Python <= 3.11
Postgresql <= 15.1


## Setup
1. Download and install postgres locally 
2. Create `.env` file with the variables found in `.env.example`
3. Run `python manage.py makemigrations` and `python manage.py migrate`  
4. Run `python manage.py runserver` to start the api server.

## Useful commands:
```shell
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
python -m black .
```
