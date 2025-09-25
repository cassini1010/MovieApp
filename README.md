# MovieApp

This is a movie explorer application build with fastapi, sqlmodel and vuejs.



## How to build a fullstack systematically

### Project setup

#### **Step 1: Create a GitHub Repository and Initial Setup**

1. Start by creating a new GitHub repository for your project.
2. In the repository, create a `README.md` file to introduce your project and provide information about how to get started.
3. Add a license to protect your intellectual property.
4. Create a `.gitignore` file to specify which files should be ignored during Git operations.

#### **Step 2: Clone the Repository to Your Local System**

1. Open a terminal or command prompt and navigate to the directory where you want to clone the repository.
2. Use the command `git clone https://github.com/your-username/repository-name.git` to clone the repository from GitHub.

#### **Step 3: Initialize the Backend Project with Uvicorn**

1. Create a new directory called `.backend` in the root of your project.
2. Open the terminal and navigate into the `.backend` directory.
3. Run the command `uv init --app backend` to create a new project structure for your backend application.

#### **Step 4: Create a FastAPI HelloWorld Project**

1. In the `.backend` directory, create a new file called `main.py`.
2. Write a simple FastAPI hello world project in the `main.py` file using the following code as a starting point:

```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}
```

#### **Step 5: Add a Dockerfile and docker-compose.yml**

1. In the `.backend` directory, create a new file called `Dockerfile`. Copy the following code into the file. It is important to use `fastapi dev` as this dockerfile is for the development stage.

```dockerfile
# Install uv
FROM python:3.13-slim
COPY --from=ghcr.io/astral-sh/uv:0.7.3 /uv /uvx /bin/

# Install the project into `/app`
WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy from the cache instead of linking since it's a mounted volume
ENV UV_LINK_MODE=copy

# Ensure installed tools can be executed out of the box
ENV UV_TOOL_BIN_DIR=/usr/local/bin

# Install the project's dependencies using the lockfile and settings
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --no-dev

# Then, add the rest of the project source code and install it
# Installing separately from its dependencies allows optimal layer caching
COPY . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"

# Reset the entrypoint, don't invoke `uv`
ENTRYPOINT []
EXPOSE 8000
# Run the FastAPI application by default
# Uses `fastapi dev` to enable hot-reloading when the `watch` sync occurs
# Uses `--host 0.0.0.0` to allow access from outside the container
CMD ["fastapi", "dev", "main.py", "--port", "8000", "--host", "0.0.0.0"]
```

2. Create a new file called `docker-compose.yml` in the root of your project directory. Add the following code to the file:

```dockerfile
services:
  web:
    # Build the image from the Dockerfile in the current directory
    build: ./backend

    # Host the FastAPI application on port 8000
    ports:
      - "8000:8000"

    develop:
      # Create a `watch` configuration to update the app
      # https://docs.docker.com/compose/file-watch/#compose-watch-versus-bind-mounts
      watch:
        # Sync the working directory with the `/app` directory in the container
        - action: sync
          path: ./backend
          target: /app
          # Exclude the project virtual environment — it could be for a
          # different platform in the container
          ignore:
            - ./backend/.venv

        # Rebuild the image if dependencies change by checking uv.lock
        - action: rebuild
          path: ./backend/uv.lock
        
        - action: rebuild
          path: ./backend/Dockerfile
```

### DB setup

#### **Step 1: Add Postgres and Adminer to Docker Compose**

Update the `docker-compose.yml` file to include Postgres and Adminer:

```yml
version: "3"

services:
  db:
    image: postgres
    restart: always
    # set shared memory limit when using docker \
    shm_size: 128mb
    ports:
      - 5432:5432
    env_file:
      - .env
    # environment:
    #   - POSTGRES_USER=${DB_USER}
    #   - POSTGRES_PASSWORD=${DB_USER_PASSWORD}
    volumes: 
      - db:/var/lib/postgresql/data

  adminer:
    image: adminer
    restart: always
    ports:
      - 8080:8080 
volumes:
  db:
```

#### **Step 2: Start Compose Services**

Run the following command to start the services:

```bash
docker-compose up -d
```

This will start all the containers in detached mode.

#### **Step 3: Install Alembic and Create Models**

Install Alembic as a dependency:

```bash
pip install alembic
```

Create a new file called `models.py` to define your database models using SQLModel ORM:

```python
from sqlmodel import SQLModel, Field

class User(SQLModel, table=True):
    id: int = Field primary_key=True
    name: str
    email: str
```

Run the following command to initialize Alembic migrations:

```bash
alembic init migrations
```

This will create a new directory called `migrations` and an `alembic.ini` file.

#### **Step 4: Modify Alembic.ini and Generate Migrations**

Modify the `sqlalchemy.url` parameter in `alembic.ini` to match your Postgres database:

```ini
sqlalchemy.url = postgresql://username:password@localhost:5432/database_name
```

Run the following command to generate the initial migrations:

```bash
alembic revision --autogenerate -m "first commit message"
```

This will create a new directory called `versions` with the initial migration.

#### **Step 5: Upgrade to Latest Migration and Verify Tables**

Run the following command to upgrade to the latest migration:

```bash
alembic upgrade head
```

This will create all the tables in your database.

Login to Postgres via Adminer to verify that the tables have been created:

1. Open a web browser and navigate to `http://localhost:8080`.
2. Enter the username as "myuser" and password as "myuser".
3. Connect to the database "mydatabase".
