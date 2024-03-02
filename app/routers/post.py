from fastapi import Response, status, HTTPException, Depends, APIRouter
from fastapi.params import Body

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func


from .. import models, schemas, oauth2

# sqlalchemy db initialization
from ..database import get_db


# in memory data
my_posts = [
    {"title": "title of post 1", "content": "content of post 1", "id": 1},
    {"title": "favorite foods", "content": "pizza", "id": 2},
]

router = APIRouter(prefix="/posts", tags=["Posts"])


# @router.get("/")
# def hello_world():
#     return {"message": "Hello World!"}


@router.get("/", response_model=List[schemas.Post])
def get_posts(
    db: Session = Depends(get_db),
    limit: int = 10,
    skip: int = 1,
    search: Optional[str] = "",
):
    print("parameters")
    print(f"skip: {skip}")
    print(f"limit: {limit}")
    print(f"search: {search}")
    # DB version
    # cursor.execute("""SELECT * FROM posts """)
    # posts = cursor.fetchall()

    # alchemy
    # the bellow returns a sql statement
    # equivalent to select * from posts
    # posts = db.query(models.Post)

    # simple query with alchemy
    posts = db.query(models.Post).limit(limit)
    for post in posts:
        print(post.__dict__)

    # join example
    # left inner join with group_by
    db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Post.id == models.Vote.post_id, isouter=True
    ).group_by(models.Post.id)

    return posts


def get_post_with(id):
    for post in my_posts:
        if post["id"] == id:
            print(post)
            return post


# the param in url is a type of a string
# also validation takes place if the type is specified
@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    # if you want to compare the id with int id, use int(id)
    # retrieved_post = get_post_with(id)

    # DB version
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))
    # db_post = cursor.fetchone()

    # Alchemy version
    post = db.query(models.Post).filter(models.Post.id == id).first()
    print(f"post found {post}")
    if post is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail=f"couldn't find the post with id {id}"
        )
    return post


# the param in url is a type of a string
# also validation takes place if the type is specified
@router.get("/{id}")
def get_post_without_exception(id: int, response: Response):
    # if you want to compare the id with int id, use int(id)
    post = get_post_with(id)
    if post is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": f"couldn't find the post with id {id}"}
    return post


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    # In memory version
    # receive_post = post.model_dump()
    # receive_post["id"] = randrange(0, 1000000000000)
    # my_posts.append(receive_post)

    # DB version
    # don't forget top commit
    # cursor.execute(
    #     """INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
    #     (post.title, post.content, post.published),
    # )
    # new_post = cursor.fetchone()
    # conn.commit()

    # Alchemy versions
    # foreign key is required as well
    # fetched through the authentication process
    dict_post = post.model_dump()

    # double start, unpacks all the dict
    new_post = models.Post(current_user.id, **dict_post)
    # new_post = models.Post(
    #     title=post.content, content=post.content, published=post.published
    # )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i
    return -1


# we don't want to send data back when we delete something, just 204
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    # DB version
    # cursor.execute(
    #     """DELETE FROM posts WHERE id = %s  RETURNING *""",
    #     (str(id)),
    # )
    # deleted_post = cursor.fetchone()
    # conn.commit()

    # Alchemy version
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    # in memory version
    # post_index = find_index_post(id)
    if post_query.first() is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail=f"couldn't find the post with id {id}"
        )
    # in memory version
    # my_posts.pop(post_index)

    # if there is a mismatch between the user id on the requested
    # and the user id that owns the post return an error
    if post.user_id != current_user.id:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            detail=f"the current user is not the owner of the post",
        )

    # Alchemy version
    # if there is a post delete it and commit the change
    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# we don't want to send data back when we delete something, just 204
@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.Post)
def update_post_title(
  
    updated_post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    # DB version
    # cursor.execute(
    #     """UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """,
    #     post.title,
    #     post.content,
    #     post.published,
    #     str(id),
    # )
    # updated_post = cursor.fetchone()
    # conn.commit()

    print(current_user.email)
    # Alchemy version
    # DML ops, always we need to check if there the value is present
    query_post = db.query(models.Post).filter(models.Post.id == id)
    post = query_post.first()
    if post is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail=f"couldn't find the post with id {id}"
        )

    # in memory version
    # my_posts[post_index]["title"] = post.title
    # print(my_posts)

    # if there is a mismatch between the user id on the requested
    # and the user id that owns the post return an error
    print(f"post.user_id {post.user_id}")
    print(f"current_user.id {current_user.id}")
    if post.user_id != current_user.id:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            detail=f"the current user is not the owner of the post",
        )

    # Alchemy version
    # query_post.update({"title": post.title, "content": post.content}, synchronize_session=False)
    query_post.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()

    return query_post.first()
