# Solution for NEXU-BACKEND-TEST of Rodrigo Plauchu

In this Solution I decided to use python as coding language, Postgres as the SQL database and Flask as the framework for definning endpoints

## Database

I decided to create two tables (MODELS and BRANDS) because it seemed just obvious from the first approach and to make less complex queries to the database, so in this implementation is scalable and easy to change the design for the tables or database 

Under the carpet /db you will be able to find the handler.py that creates the tables and populates them with the models.json included for the test. 

For running this file if you have never worked with Postgres you can be refer to the section of instalation

## Enpoints

As the nature of the framework Flask it makes it more intuitive and scalable the definition of routes or endpoints, I included the rules requested with the small logic inside each method. 

## Instalation 

You can create a virtual env and run the cmd 

```python
pip install -r requirements.txt
```

This will install all the packages needed for this test

To create the database you need to download the UI client from their [website](https://www.postgresql.org/) and add your credentials to the connection string. After that create manually the db with:

```sql
CREATE DATABASE NEXU
```

After that is done you will be able to run the handler and it will create and populate the database

## Test 

Once you have the database created you can you to /endpoints and run the routes.py file with the Flask routes, this will initiate the service in debug mode in your terminal and will indicate the host and port it was initialized, usually 127.0.0.1:5000

For the test you can either access the endpoints directly in the browser, for example:

```
http://127.0.0.1:5000/brands

http://127.0.0.1:5000/brands/2/models

http://127.0.0.1:5000/models
```

Or as I tested, which was inside a new terminal (with still the previous one running) with curl cmds listed here:

Test 1: Get all models 

```shell
curl http://127.0.0.1:5000/models
```

Test 2: Get specific brand models

```shell
curl http://127.0.0.1:5000/brands/2/models
```

Test 3: Create a new brand (success)

```shell
curl -X POST http://127.0.0.1:5000/brands -H "Content-Type: application/json" -d '{"name": "Test Brand"}'
```

Test 4: Create a new brand (failure)

```shell
curl -X POST http://127.0.0.1:5000/brands -H "Content-Type: application/json" -d '{}'
```

Test 5: Create a new model for a brand (success)

```shell
curl -X POST http://127.0.0.1:5000/brands/1/models -H "Content-Type: application/json" -d '{"name": "Test Model", "average_price": 150000}'
```

Test 6: Create a new model for a brand (failure)

```shell
curl -X POST http://127.0.0.1:5000/brands/100/models -H "Content-Type: application/json" -d '{"name": "Test Model", "average_price": 150000}'
```

Test 7: Update an existing model (success)

```shell
curl -X PUT http://127.0.0.1:5000/models/1 -H "Content-Type: application/json" -d '{"average_price": 200000}'
```

Test 8: Update an existing model (failure)
```shell
curl -X PUT http://127.0.0.1:5000/models/1 -H "Content-Type: application/json" -d '{}'
```

Test 9: Get models with price between a range
```shell
curl http://127.0.0.1:5000/models?greater=380000&lower=400000
```

## Improvements

I would love more time to create a frontend with real scenarios of the interactions, create a better model for the database and take into consideration the tools that Nexu actually uses.