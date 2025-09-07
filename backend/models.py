from typing import Annotated
from fastapi import Body
from sqlmodel import Field, Relationship, SQLModel


class Moive_actors_link(SQLModel, table=True):
    id: Annotated[int | None, Field(default=None, primary_key=True)]
    movie_id: Annotated[int|None, Field(default=None, foreign_key="movie.id")]
    actor_id: Annotated[int|None, Field(default=None, foreign_key="actor.id")]


class Movie_genre_link(SQLModel, table=True):
    id: Annotated[int | None, Field(default=None, primary_key=True)]
    movie_id: Annotated[int|None, Field(default=None, foreign_key="movie.id")]
    genre_id: Annotated[int|None, Field(default=None, foreign_key="genre.id")]
    

class Genre(SQLModel, table=True):
    id: Annotated[int | None, Field(default=None, primary_key=True)]
    genre_type: str

    # Relations
    movies: list["Movie"] = Relationship(back_populates="genres")


class Actor(SQLModel, table=True):
    id: Annotated[int | None, Field(default=None, primary_key=True)]
    name: str

    # Relations
    movies: list["Movie"] = Relationship(back_populates="actors")


class Director(SQLModel, table=True):
    id: Annotated[int | None, Field(default=None, primary_key=True)]
    name: str

    # Relations
    movies: list["Movie"] = Relationship(back_populates="director")


class Movie(SQLModel, table=True):
    id: Annotated[int | None, Field(default=None, primary_key=True)]
    title: str
    director_id: Annotated[int | None, Field(default=None, foreign_key="director.id")]
    releaseYear: int
    summary: Annotated[str | None, Field(default=None)]

    # Relations
    actors: list[Actor] = Relationship(back_populates="movies")
    director: Director = Relationship(back_populates="movies")
    genres: list[Genre] = Relationship(back_populates="movies")

class UserBase(SQLModel):
    username: str
    password: str

class User(SQLModel, table=True):
    id: Annotated[int | None, Field(default=None, primary_key=True)]
    username: str
    hashed_password: str
