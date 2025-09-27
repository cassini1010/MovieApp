import uuid
from pathlib import Path
from typing import Annotated

from app.config import settings
from app.database import get_db_session
from app.models import Actor, Director, Genre, Movie, MovieResponse
from fastapi import APIRouter, Depends, Form, HTTPException, Query, UploadFile
from sqlalchemy.exc import NoResultFound
from sqlmodel import Session, select

router = APIRouter(prefix="/movie", tags=["movies"])


@router.post("/")
async def add_movie(
    session: Annotated[Session, Depends(get_db_session)],
    # current_user: Annotated[User, Depends(get_current_user)],
    title: Annotated[str, Form()],
    director: Annotated[str, Form()],
    releaseYear: Annotated[int, Form()],
    actors: Annotated[list[str], Form()],
    genres: Annotated[list[str], Form()],
    summary: str | None = Form(default=None),
    thumbnail: UploadFile | None = None,
):
    if session.exec(select(Movie).where(Movie.title == title)).first():
        raise HTTPException(
            status_code=400,
            detail="The movie with this name already exists in the system.",
        )
    new_director = session.exec(
        select(Director).where(Director.name == director)
    ).first()
    if not new_director:
        new_director = Director(name=director)

    new_movie = Movie(
        title=title,
        releaseYear=releaseYear,
        summary=summary,
        director=new_director,
    )

    for actor in actors:
        existing_actor = session.exec(select(Actor).where(Actor.name == actor)).first()
        if not existing_actor:
            existing_actor = Actor(name=actor)
        new_movie.actors.append(existing_actor)

    for genre in genres:
        existing_genre = session.exec(
            select(Genre).where(Genre.genre_type == genre)
        ).first()
        if not existing_genre:
            existing_genre = Genre(genre_type=genre)
        new_movie.genres.append(existing_genre)

    if thumbnail:
        filename = thumbnail.filename
        if filename.endswith(("jpg", "jpeg", "png")):
            save_path = settings.STATIC_DIRECTORY.joinpath(
                str(uuid.uuid4()) + Path(filename).suffix
            )
            with open(save_path, "wb") as fp:
                fp.write(await thumbnail.read())
            new_movie.thumbnail = save_path.name
        else:
            raise HTTPException(
                status_code=400,
                detail="Wrong file type",
            )
    session.add(new_movie)
    session.commit()

    return new_movie


@router.delete("/{movie_id}")
def delete_movie(
    movie_id: int,
    # current_user: Annotated[User, Depends(get_current_user)],
    session: Annotated[Session, Depends(get_db_session)],
):
    try:
        movie = session.exec(select(Movie).where(Movie.id == movie_id)).one()
        session.delete(movie)
        session.commit()
    except NoResultFound:
        raise HTTPException(status_code=400, detail="Invalid Movie ID") from None


@router.get("/", response_model=list[MovieResponse])
def get_movie(
    session: Annotated[Session, Depends(get_db_session)],
    limit: int = Query(default=10, ge=0),
    offset: int = Query(default=0, ge=0),
):
    movie = session.exec(select(Movie).offset(offset).limit(limit)).all()
    return movie


# @router.put("/{movie_id}")
# async def update_movie(
#     session: Annotated[Session, Depends(get_db_session)],
#     movie_id: int,
#     thumbnail: UploadFile | None = None,
# ):
#     try:
#         movie = session.exec(select(Movie).where(Movie.id == movie_id)).one()
#         if thumbnail:
#             filename = thumbnail.filename
#             if filename.endswith(("jpg", "jpeg", "png")):
#                 with open(
#                     r".static\{}.jpg".format(thumbnail_name := uuid.uuid4()), "wb"
#                 ) as fp:
#                     fp.write(await thumbnail.read())
#                 movie.thumbnail = str(thumbnail_name) + ".{}".format(
#                     thumbnail.filename.split(".")[-1]
#                 )
#             else:
#                 raise HTTPException(
#                     status_code=400,
#                     detail="Wrong file type",
#                 )
#             session.add(movie)
#             session.commit()

#     except NoResultFound:
#         raise HTTPException(status_code=400, detail="Invalid Movie ID") from None
