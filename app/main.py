from fastapi import FastAPI


# ORM classes
from . import models

# sqlalchemy db initialization
from .database import engine

# our routers
from .routers import post, user, auth, vote

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# include routes
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
async def hello_world():
    return {"message": "Hello World!"}
