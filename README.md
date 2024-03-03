## Table of Contents
1. [Creation and activation of virtual environments](#creation-and-activation-of-virtual-environments)
2. [Fastpi rest endpoints](#fastpi-rest-endpoints)
3. [Validation with pydantic](#validation-with-pydantic)
4. [Rest endpoints](#rest-endpoints)
5. [Reading environmental variables using pydantic settings](#reading-environmental-variables-using-pydantic-settings)
6. [Database](#database)
7. [JWT with fastapi](#jwt-with-fastapi)
8. [Install libs through requirements.txt](#install-libs-through-requirements-txt)
9. [app dockerization](#app-dockerization)
10. [postgres queries examples](#postgres-queries-examples)

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

## 4. Fastpi rest endpoints

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

### 4.6 Endpoints/resources organization

Fastapi uses the notion of routers for structuring the code (resources).
Routers are a combination of packages and use of APIRouter.

Example:You have an app that manages users posts.
So, you want to separate the posts code and the user code into separate
url resources and you don't want to have all the code into a single file.
A solution to this is a combination of packages and fastapi routers.

- Using packages for better code structure (usage of dunder init file):

```sh
.
└── app/
    ├── routers/
    │   ├── __init__.py
    │   ├── post.py
    │   └── user.py
    ├── __init__.py
    └── main.py
```

- Router usage:

```python
from fastapi import APIRouter


# appends to all REST urls the /posts
router = APIRouter(prefix="/posts", tags=["Posts"])

@router.get("/")
def get_posts(...):
    pass

```
Similar code is implemented for the users.

- Router inclusion to fast api app:

```python
from fastapi import FastAPI

app = FastAPI()

# include routes
app.include_router(post.router)
app.include_router(user.router)

```

## 5. Reading environmental variables using pydantic settings

Lib required:
```cmd
pip install pydantic-settings
```

Example, the attributes of Settings class must match the environmental variables (is case insensitive):

```python
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"


settings = Settings()
```

## 6. Database

### 6.1 Get DB connection using psycopg2 and postgres
Get DB connection using psycopg2 and postgres

Example:

```python
from psycopg2.extras import RealDictCursor
import psycopg2
import time

# connect to DB, without alchemy
while True:
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="fastapi",
            user="postgres",
            password="postgres",
            cursor_factory=RealDictCursor,
        )
        cursor = conn.cursor()
        print("Database connection succesfull!")
        break
    except Exception as error:
        print("Database connection failed")
        time.sleep(2)
```

### 6.2 Fastapi DB Queries using psycopg2

- Example, get all posts (select all posts)
```python
@router.get("/", response_model=List[schemas.Post])
def get_posts(
    limit: int = 10,
    skip: int = 1,
    search: Optional[str] = "",
):
    # DB version
    cursor.execute("""SELECT * FROM posts """)
    posts = cursor.fetchall()

```

- Example, get all posts with where condition
```python
@router.get("/", response_model=List[schemas.Post])
def get_posts(
    db: Session = Depends(get_db),
    limit: int = 10,
    skip: int = 1,
    search: Optional[str] = "",
):
    # DB version
    cursor.execute("""SELECT * FROM posts """)
    posts = cursor.fetchall()

```

- Example, insert a post
```python
    cursor.execute(
        """INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
        (post.title, post.content, post.published),
    )
    new_post = cursor.fetchone()
    conn.commit()
```

- Example, delete a post
```python
    # DB version
    cursor.execute(
        """DELETE FROM posts WHERE id = %s  RETURNING *""",
        (str(id)),
    )
    deleted_post = cursor.fetchone()
    conn.commit()
```

- Example, update a post
```python
    # DB version
    cursor.execute(
        """UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """,
        post.title,
        post.content,
        post.published,
        str(id),
    )
    updated_post = cursor.fetchone()
    conn.commit()
```

## 7. JWT with fastapi

- Required lib:

1. Lib for hashing passwords, the hashed password will be stored in the DB
```cmd
pip install passlib[bcrypt]
```

2. Lib for jwt encoding/decoding, used for creation and verification of the token
 ```python
pip install python-jose[cryptography]
```

Access token creation and verification, retrieved by performing a POST on \login resource (username and password):

```python
from app import schemas
from datetime import datetime, timedelta
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from . import database, models, config
from .config import settings

# api that performs the authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


# secret key
# algorithm
# expiration time
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def create_access_token(data: dict):
    # swallow copy
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        # payload decode
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(payload)
        # extract id from the payload
        id: str = payload.get("user_id")

        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception
    return token_data


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()
    return user

```


## 8. install libs through requirements.txt

### 8.1 requirements dump
```cmd
pip freeze > requirements.txt
```

### 8.2 requirements install
```cmd
pip install -r requirements.txt
```

## 9. app dockerization

### 9.1 Dockerfile

Example:

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

### 9.2 docker-compose.yml

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

### 9.3 docker compose useful commands
```sh
docker compose up
docker compose down
docker exec -it fastapi_api bash
```

## 10. postgres queries examples

### left join
```sql
select * from posts LEFT JOIN users ON posts.user_id = users.id;
select content, email, title from posts LEFT JOIN users ON posts.user_id = users.id;

-- where is ambiguity, use the table in front
SELECT post.id, users.emai
FROM posts -- the left table
LEFT JOIN users -- the right table
ON posts.user_id = users.id;
```

### right join
```sql
select * from posts RIGHT JOIN users ON posts.user_id = users.id;
select content, email, title from posts RIGHT JOIN users ON posts.user_id = users.id;

-- where is ambiguity, use the table in front
SELECT post.id, users.emai
FROM posts -- the left table
RIGHT JOIN users -- the right table
ON posts.user_id = users.id;
```

### group by
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


### join



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
pip install pytest
```
# pytest
- auto-discovery
  - test_calculations.py
running on verbose mode
```sh
pytest -v
``
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

```sh
pip install alembic
alembic init alembic
# creates a file with the sql statements that we want to apply
alembic revision -m "create post table"+
alembic revision <my_revision>
alembic downgrade -1
alembic upgrade 
```