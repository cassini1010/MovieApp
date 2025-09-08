from fastapi import APIRouter, Depends, Form, HTTPException
from app.utils import get_current_user
from typing import Annotated
from app.models import (
    User,
    MovieCreate,
    Director,
    Actor,
    Genre,
    Movie,
    Movie_genre_link,
    Moive_actors_link,
)
from app.database import get_db_session
from sqlmodel import Session, select


router = APIRouter(prefix="/movie", tags=["movies"])


@router.post("/")
def add_movie(
    movie: MovieCreate,
    # current_user: Annotated[User, Depends(get_current_user)],
    session: Annotated[Session, Depends(get_db_session)],
):
    director = session.exec(
        select(Director).where(Director.name == movie.director)
    ).first()
    if not director:
        director = Director(name=movie.director)
        session.add(director)
        session.flush()

    db_movie = Movie(
        title=movie.title,
        releaseYear=movie.releaseYear,
        director_id=director.id,
        summary=movie.summary,
    )

    # Handle actors
    for name in movie.actors:
        actor = session.exec(select(Actor).where(Actor.name == name)).first()
        if not actor:
            actor = Actor(name=name)
            session.add(actor)
            session.flush()
        db_movie.actors.append(actor)

    # Handle genres
    for name in movie.genres:
        genre = session.exec(select(Genre).where(Genre.genre_type == name)).first()
        if not genre:
            genre = Genre(genre_type=name)
            session.add(genre)
            session.flush()
        db_movie.genres.append(genre)

    session.add(db_movie)
    session.commit()
    session.refresh(db_movie)
    return movie


@router.delete("/{movie_id}")
def delete_movie(movie_id: int, session: Annotated[Session, Depends(get_db_session)]):
    movie = session.exec(select(Movie).where(Movie.id == movie_id)).first()
    if not movie:
        raise HTTPException(status_code=400, detail="Invalid Movie ID")
    session.delete(movie)
    session.commit()