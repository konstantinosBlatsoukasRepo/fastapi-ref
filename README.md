## Table of Contents
1. [Creation and activation of virtual environments](#creation-and-activation-of-virtual-environments)
2. [Fast api installation](#fast-api-installation)
3. [Validation with pydantic](#validation-with-pydantic)
4. [Rest endpoints](#rest-endpoints)

## 1. Creation and activation of virtual environments

### 1.1 Virtual environment creation
This is a tool for creating "virtual environments" with dedicated packages per project.
This is useful, when you work with multiple python projects and each project requires
different package versions.

- Example, the bellow command creates a virtual environment in the directory named *new_venv*:
```python
py -3 -m venv new_venv
```

### 1.2 Virtual environment activation

- Example, activation of a virtual environment called new_venv *(windows version)*:
```sh
.\new_venv\Scripts\activate.bat
```

### 1.3 Run uvicorn server

- Example, the main file is located under the module app and it's called main.py
```sh
.\new_venv\Scripts\uvicorn app.main:app --reload
```

## 2. Fast api installation

- pip command:
```sh
pip install fastapi[all]
```

### 2.1 Get all installed packages

- pip command:
```sh
pip freeze
```



- order of the url matters!
- schema validation: pydantic

/posts
/posts/:id
/posts

- how to set default http status
```python 
@app.post("/pydantic/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
```

- in order to create a package to the following:

1. create a new folder
2. in the new folder, create a file named "__init__.py"



```sql
SELECT name FROM products;
SELECT name, id FROM products;
SELECT name, id AS produt_id FROM products;

-- operators
SELECT name, id AS produt_id FROM products WHERE id = 2;
SELECT name, id AS produt_id FROM products WHERE id = 2 or id = 4;
SELECT name, id AS produt_id FROM products WHERE id >= 2;
SELECT name, id AS produt_id FROM products WHERE id != 2;

-- logical ops
SELECT name, id AS produt_id FROM products WHERE id != 2 AND id > 0;
SELECT name, id AS produt_id FROM products WHERE id != 2 OR id > 0;

-- IN op
SELECT name, id AS produt_id FROM products WHERE id IN (1, 2, 4);

-- LIKE op
SELECT *  FROM products WHERE name LIKE 'TV%';
SELECT *  FROM products WHERE name NOT LIKE 'TV%';

-- ORDER BY
SELECT *  FROM products ORDER BY price ASC;
SELECT *  FROM products ORDER BY price DESC;

-- LIMIT
SELECT *  FROM products LIMIT 10;

-- SKIPS THE FIRST 20
SELECT * FROM customers LIMIT 10 OFFSET 20;

-- INSERT
INSERT INTO products (name, price, inventory) VALUES ('tortilla', 4, 1000);

-- INSERT with returning values
INSERT INTO products (name, price, inventory) VALUES ('car', 4, 10002), ('laptop', 3, 500) returning id;

-- DELETE
DELETE FROM products WHERE ....

-- UPDATE
UPDATE products SET name = 'flour tortilla', price = 40 WHERE id = 2

-- BATCH UPDATE
UPDATE products SET name = 'flour tortilla', price = 40

```

## 3. Validation with pydantic

### 3.1 Schema definition

The object that you create is validated against a schema object.
A schema object defines the expected types that the request/object must have, otherwise
a validation error is raised.

- Example, schema object:

```python
from typing import Optional
from pydantic import BaseModel, EmailStr

class UserLogin(BaseModel):
    email: EmailStr
    password: str

```
The above object requires two fields email and password:

- email is a required field and must looks like a valid email
- the password is a required field and must be a string

### 3.2 Schema definition with optional field

- Example, schema object:
```python
class TokenData(BaseModel):
    id: Optional[int] = None
```

### 3.3 Schema definition that validates sqlalchemy object

- Example, schema object:
```python
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    # converts properly an orm object
    class Config:
        from_attributes = True
```

## 4. Rest endpoints

### 4.1 __Get__

Example:

```python
from fastapi import FastAPI

@app.get("/")
async def hello_world():
    return {"message": "Hello World!"}
```

### 4.2 __Post__ that accepts a specific json object (validated with pydantic)

Endpoint that accepts a certain json (validated by pydantic)

- In this case the json looks like:
```json
{
    "title": "Fullmetal",
    "content": "Manga",
    "published": true
}
```

- the schema object (pydantic):
```python
# under the module schemas.py
from pydantic import BaseModel

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
```

- rest end point:
```python
@app.post("/")
def create_post(
    post: schemas.PostCreate,
):
    # the json request is validated based on the object PostBase
    # python logic...
```

### 4.3 __Delete__ operation with status code specification

```python
# this is a delete operation, is used for deleting something
@app.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    # params
):
    # if the logic and the validation passes
    # the returned http request will have http status code 204
```

### 4.3 __Update__ with parameter specified

```python
# this is a update operation, is used for updating a resource
# for example, in this case the id must be an int
# PUT http://whatever/posts/2, the var id in this case has the value of 2
@app.put("/{id}", status_code=status.HTTP_200_OK)
def update_post_title(id: int):
    # if the logic and the validation passes
    # the returned http request will have http status code 200
```

### 4.4 Response validation using pydantic

```python
from typing import List

# The output of the endpoint must comply with the object that is assigned
# to response_model, in this case a list of Post objects
@app.get("/", response_model=List[schemas.Post])
def get_posts():
    pass

# schema.Post
from pydantic import BaseModel

class Post(PostBase):
    id: int
    created_at: datetime
    user_id: int
```

### 4.5 Run depended code before the logic execution (Depends)

```python
# the get_db function is executed before the endpoint logic execution
@app.get("/", response_model=List[schemas.Post])
def get_posts(
    db: Session = Depends(get_db),
    limit: int = 10,
    skip: int = 1,
    search: Optional[str] = "",
):
    pass
```

### 4.5 Endpoints/resources organization 



# Alembic: to

# differences between 


# passlib[bcrypt]
```python
pip install passlib[bcrypt]
```

# JWT token authentication

1. /login (usr + pwd)

```python
pip install python-jose[cryptography]
```

cascade action on FK:

%20 is a single space on the url

# environment vars

how to access them, using fastApi:

```python
import os
path = os.getenv("Path")
```

- environment file to the rescue!

- validate environment vars
```python

from pydantic import BaseSettings

# the environment vars are actually properties if the class
# keep in mind, that the attributes are case insensitive
class Settings(BaseSettings):
    database_password: str = ""
    database_host: str = ""
    ...

settings = Settings()
print(settings.database_password)
...
...
```

```cmd
pip install pydantic-settings
```

## left join
```sql
select * from posts LEFT JOIN users ON posts.user_id = users.id;
select content, email, title from posts LEFT JOIN users ON posts.user_id = users.id;

-- where is ambiguity, use the table in front
SELECT post.id, users.emai
FROM posts -- the left table
LEFT JOIN users -- the right table
ON posts.user_id = users.id;
```

## right join
```sql
select * from posts RIGHT JOIN users ON posts.user_id = users.id;
select content, email, title from posts RIGHT JOIN users ON posts.user_id = users.id;

-- where is ambiguity, use the table in front
SELECT post.id, users.emai
FROM posts -- the left table
RIGHT JOIN users -- the right table
ON posts.user_id = users.id;
```

## group by
```sql
SELECT users.id, COUNT(*)
FROM posts -- the left table
LEFT JOIN users -- the right table
ON posts.user_id = users.id
group by users.id;


SELECT users.id, COUNT(posts.id)
FROM posts
RIGHT JOIN users
ON posts.user_id = users.id
group by users.id;
```


## join
```sql
SELECT posts.id, COUNT(votes.id) as likes
FROM posts
LEFT JOIN votes
ON posts.id = votes.post_id;
GROUP BY posts.id

```

- Alembic, DB migration tool
# keep track incremental changes on DB

```sh
pip install alembic

alembic init alembic
# creates a file with the sql statements that we want to apply
alembic revision -m "create post table"+

alembic revision <my_revision>
alembic downgrade -1
alembic upgrade 


```

# requirements dump and install

## requirements dump
pip freeze > requirements.txt

## requirements install
pip install -r requirements.txt

# Docker


## Dockerfile

```Dockerfile
FROM python:3.9.7

WORKDIR /usr/src/app
COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . . 

CMD ["uvicorn". "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```sh
docker build -t fastapi .
```

# docker-compose.yml

```yml
version: "3"
services:
    api:
        build: .
        depends_on:
         - postgres
        ports: 
            - 4000:8000
        # env_file:
        #     - ./.env
        environment:
            - DATABASE_HOSTNAME=postgres
        # app synchronization, reload
        volumes:
            - ./:/user/src/app:ro
        command: uvicorn app.maiLapp --host 0.0.0.0 --port 800 --reload
            ....
    postgres:
        image: postgres
        environment:
            - POSTGRES_PASSWORD=postgres
            - POSTGRES_DB=postgres
        volumes: 
            - postgres-db:/var/lib/postgresql/data

volumes: 
    - postgres-db:

```

```sh
docker compose up
docker compose down
docker exec -it fastapi_api bash
```



```sh
pip install pytest
```


# pytest

- auto-discovery
  - test_calculations.py

running on verbose mode
```sh
pytest -v
```

- print statements are visible, -s option

```sh
pytest -v -s 
```

- fixtures, you can avoid repetitive code

- test specific tests
```sh
pytest -v -s tests/test_users.py
```

stop at the first failure
```sh
pytest -x
```

- fixture scopes! are run for each function, runs for each function

- whatever fixture is in the conftest.py is automatically available to all modules,
  no need to import explicitly