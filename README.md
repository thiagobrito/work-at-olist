[![CircleCI](https://circleci.com/gh/thiagobrito/work-at-olist/tree/master.svg?style=svg)](https://circleci.com/gh/thiagobrito/work-at-olist/tree/master)

# Work at Olist Problem Solved

[Olist](https://olist.com/) is a company that offers an integration platform
for sellers and marketplaces allowing them to sell their products across
multiple channels.

This repository contains a solved problem to evaluate the candidate skills.

[You can access the published APP at Heroku here.](https://thiago-olist-challenge.herokuapp.com/)


## How to build this APP

1. Clone this repository from Github;
2. Create virtualenv, activate and install requirements:
   ```
   virtualenv .venv
   .venv\scripts\activate
   pip install -r requirements.txt
   ``` 
3. Create application database
   ```
   python manage.py makemigrations core
   python manage.py migrate
   ```
4. Run tests and application
   ```
   python manage.py test
   python manage.py runserver   
   ```
5. Access local running locally at [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## Implementation details

This is a Django 2.1 application using Django Rest Framework 3.9 as backend. 

At front-end, I used Django Rest Framework Docs that was migrated to run at 
Django 2.0 from [this respository](https://github.com/jasperlittle/django-rest-framework-docs.git)   

### Project structure

* Django Application called core that runs all API
* We have only two models
  * *Call* that contains all Phone Calls information
  * *Billing* that contains all information related with billing report
* When a "start" call and "end" call with the same Call-ID are created, the system 
  automatically creates new information at the "Billing" table with all the information that's necessary for billing purposes
. [This logic is implemented here.](https://github.com/thiagobrito/work-at-olist/blob/master/phone_calls/core/services/billing.py)
* I created tests for everything :-)
* You can access live API documentation and also an interface for testing purposes [here](https://thiago-olist-challenge.herokuapp.com/)


# Todo list

- [x] Create first structure of project (1)
- [x] Setup Continous Integration using CircleCI (2)
- [x] Setup Django Rest Framework (1)
- [x] Receive telephone call detail reports through Rest API (5)
- [x] Get telephone bill through Rest API (3)
- [ ] EXTRA: Provide an API to change the charge price and free period (2)
- [x] Publish at heroku (2)
- [x] Fill database with sample data (1)
- [x] Finish documentation (2)
