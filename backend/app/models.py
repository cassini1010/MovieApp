from typing import Annotated

from sqlmodel import Field, Relationship, SQLModel


class MovieResponse(SQLModel):
    title: str
    releaseYear: int
    summary: str | None
    director: "Director"
    actors: list["Actor"]
    genres: list["Genre"]
    thumbnail: str | None


class MovieCreate(SQLModel):
    title: str
    director: str
    releaseYear: int
    summary: str | None = None
    actors: list[str]
    genres: list[str]


class Moive_actors_link(SQLModel, table=True):
    id: Annotated[int | None, Field(default=None, primary_key=True)]
    movie_id: Annotated[
        int | None, Field(default=None, foreign_key="movie.id", ondelete="CASCADE")
    ]
    actor_id: Annotated[
        int | None, Field(default=None, foreign_key="actor.id", ondelete="CASCADE")
    ]


class Movie_genre_link(SQLModel, table=True):
    id: Annotated[int | None, Field(default=None, primary_key=True)]
    movie_id: Annotated[
        int | None, Field(default=None, foreign_key="movie.id", ondelete="CASCADE")
    ]
    genre_id: Annotated[
        int | None, Field(default=None, foreign_key="genre.id", ondelete="CASCADE")
    ]


class Genre(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    genre_type: str

    # Relations
    movies: list["Movie"] = Relationship(
        back_populates="genres", link_model=Movie_genre_link
    )


class Actor(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str

    # Relations
    movies: list["Movie"] = Relationship(
        back_populates="actors", link_model=Moive_actors_link
    )


class Director(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str

    # Relations
    movies: list["Movie"] = Relationship(back_populates="director")


class Movie(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    director_id: int | None = Field(default=None, foreign_key="director.id")
    releaseYear: int
    summary: str | None = Field(default=None)
    thumbnail: str | None = Field(default=None)

    # Relations
    actors: list[Actor] = Relationship(
        back_populates="movies", link_model=Moive_actors_link
    )
    director: Director = Relationship(back_populates="movies")
    genres: list[Genre] = Relationship(
        back_populates="movies", link_model=Movie_genre_link
    )


class UserBase(SQLModel):
    username: str
    password: str


class User(SQLModel, table=True):
    id: Annotated[int | None, Field(default=None, primary_key=True)]
    username: str
    hashed_password: str


class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"
