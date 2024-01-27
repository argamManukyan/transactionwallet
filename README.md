**Task description**

Task: Develop REST API server using django-rest-framework with pagination, sorting and filtering for two models:
* Transaction (id, wallet_id (fk), txid, amount);
* Wallet (id, label, balance);
Where txid is required unique string field, amount is a number with 18-digits precision, label is a string field, balance is a summary of all transactions’s amounts.
Tech Stack:
* Python – 3.10;
* Database – mysql
API specification – JSON:API — A specification for building APIs in JSON (you are free to use plugin https://django-rest-framework-json-api.readthedocs.io/en/stable/)
Will be your advantage:
* Test coverage;
* SQLAlchemy migrations;
* DB transactions.
* [execution time limit] 4 seconds (py3)
* [memory limit] 1 GB

_**RUNNING**_

Make sure do you have installed Docker and docker-compose 

`docker-compose up --build`