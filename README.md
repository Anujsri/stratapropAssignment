# Employee Management
The use of this application is to manage employee data and assign them devices.
***
## Problem Statement

>Whenever an employee is created he/she is allocated an EMPLOYEE_ID, for the inputs taken as >FIRST_NAME, LAST_NAME, E_MAIL, and MOBILE_NUMBER.
>Each employee can be assigned more that one device that is identified by an DEVICE_ID.
>Create a flask app to replicate CRUD operations:

- Create an Employee
- Update Employee details
- Create Device
- Update Device Details
- Assign a device to an employee
- Whenever a device is assigned or unassigned send out the details of the same to the corresponding employee as an e-mail.
***

> This application is using two model(Schemas)
  - Employee
  - Device
***
### Technology Used
  - Flask-RESTful
  - PostgreSQL
  - SqlAlchemy(ORM)
***  
 ### Installation

>requires Python3 to run.
>Install the dependencies and devDependencies and start the server.
```sh
$ python3 -m venv virtual_environmentr_name
$ source virtual_environmentr_name/bin/activate
$ pip install -r requirements.txt
```
***

### How to run this application
> #1 Create database and database user 
```sh
$ create database assignment;
$ create user anuj with encrypted password 'anuj1234';
$ grant all privileges on database assignment to anuj;
```
>#2 Import some enviromental variable
```sh
export PYTHONPATH=$PROJECT_DIR:$PYTHONPATH
export LANG=en_US.UTF-8
export LC_MESSAGES="C"
export APP_KEY='BYTa4u9d-dsc8GM1LtnQEjs9RZVgZzRGyPQ2bMQw'
export APP_SETTINGS="config.ProductionConfig"
export SECURITY_PASSWORD_HASH='pbkdf2_sha512'
export SECURITY_PASSWORD_SALT='poiuytresdfghjkloiuytrescvbnml;p98765rdcvbnmloiuytr'
export MAIL_USERNAME='your_email'
export MAIL_PASSWORD='your_email_password'
export DATABASE_NAME='assignment'
export DATABASE_USER='anuj'
export DATABASE_PASSWORD='anuj1234'
export DATABASE_HOST='localhost'
export PGPASSWORD=$DATABASE_PASSWORD
export DATABASE_URL="postgresql://anuj:anuj1234@localhost:5432/assignment"
export REDIS_URL='redis://localhost:6379/0'
export AMQP_URL='amqp://au_user:au1234@localhost/localhost'
export APP_SECRET_KEY='\xb5\x1ePn\xc7\n\xcd\x96C\xc6\xa8\x05\xe9\x7fF\x8fz\xa1\x19\x17\x19\x10g\x85'
```

>#3 IMPORT A POSTGRESQL DATABASE (optional), I have provided a sql dump file named dbexport.pgsql 

```sh
$ psql -U anuj assignment < dbexport.pgsql
```
>#4 migrate and upgrade database
```sh
$ python manage.py db init
$ python manage.py db migrate
$ python manage.py db upgrade
```
>#5 run server
```sh
$ python manage.py runserver
```
>#5 run celery in **separate terminal window** to handle asynchronous task like sending mail in our case
```sh
$ celery -A manage.celery worker -l info
```
***
### API Documentation 

To see available REST API for this application please visist 
**https://documenter.getpostman.com/view/7704284/SWEB3baf?version=latest)**

***
<img width="1182" alt="Screenshot 2019-12-17 at 3 47 12 PM" src="https://user-images.githubusercontent.com/25398413/70986777-930daa00-20e4-11ea-9fbe-0aa427caad50.png">

## Thank You !

