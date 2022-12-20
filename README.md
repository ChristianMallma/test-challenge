### Description
This project was developed based on the Hexagonal Architecture

### BD
1. Create a database using Postgres  
After create, you need insert the credentials in your .env into src folder:  
Example:

    *POSTGRES_DATABASE=store*  
*POSTGRES_HOST='127.0.0.1'*  
*POSTGRES_PASSWORD=store*  
*POSTGRES_PORT=5432*  
*POSTGRES_USER=store_user*


2. Create a "Product" table in your database with the following fields:  
Column name (Type)  
================  
- *id (uuid)*  
- *name (character varying(256))*  
- *status (boolean)*  
- *stock (integer)*  
- *description (character varying(256))*  
- *price (double precision)*  
- *created (date)*  
- *updated (date)*

### Virtual Environment
1. Create a virtual environment
2. Open the project with the virtual environment activated
3. Go to src folder using terminal
4. In the terminal execute:  
*pip install -r requirements/requirements.txt*

## Start Project
1. In the terminal execute:  
*uvicorn app.route:app --reload --host 0.0.0.0 --port 8084*

## Observation
1. In your .env add the following:  
*SLEEP_PROCESS=5*  
*TIME_IN_CACHE=300*  

2. For Tests Execution:  
*python -m unittest*

## Open to Swagger
1. Go to the website and type in the search engine:  
*localhost:8084*  

2. For redocs:  
*localhost:8084/api/redocs*
