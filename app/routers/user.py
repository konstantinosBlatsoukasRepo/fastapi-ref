from fastapi import Response, status, HTTPException, Depends, APIRouter
from fastapi.params import Body

from sqlalchemy.orm import Session


from .. import models, schemas, utils

# sqlalchemy db initialization
from ..database import get_db

router = APIRouter(prefix="/users", tags=['Users'])


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.UserOut,
)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # hash password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    # Alchemy version
    # double start, unpacks all the dict
    new_user = models.User(**user.model_dump())

    # old fashioned way
    # new_post = models.Post(
    #     title=post.content, content=post.content, published=post.published
    # )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/{id}", response_model=schemas.UserOut)
def gat_user(id: int, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == id).first()
    if user is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail=f"couldn't find the user with id {id}"
        )
    return user
