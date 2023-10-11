FROM python:3.10-alpine as python-base

ENV POETRY_VERSION=1.6.1
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv

ENV POETRY_CACHE_DIR=/opt/.cache

FROM python-base as poetry-base

# Creating a virtual environment just for poetry and install it with pip
RUN python3 -m venv $POETRY_VENV \
	&& $POETRY_VENV/bin/pip install -U pip setuptools \
	&& $POETRY_VENV/bin/pip install poetry==${POETRY_VERSION}

FROM python-base as example-app

# Copy Poetry to app image
COPY --from=poetry-base ${POETRY_VENV} ${POETRY_VENV}

# Add Poetry to PATH
ENV PATH="${PATH}:${POETRY_VENV}/bin"

WORKDIR /app

COPY poetry.lock pyproject.toml ./

RUN touch README.md

# [OPTIONAL] Validate the project is properly configured
RUN poetry check

# Install Dependencies
RUN poetry install --no-interaction --no-cache

# Copy Application
COPY . /app

# Run Application
EXPOSE 5001

#RUN pip install

#ENV POETRY_NO_INTERACTION=1 \
#    POETRY_VIRTUALENVS_IN_PROJECT=1 \
#    POETRY_VIRTUALENVS_CREATE=1 \
#    POETRY_CACHE_DIR=/tmp/poetry_cache

#WORKDIR /app

#COPY pyproject.toml poetry.lock ./
#COPY src ./src
#RUN touch README.md

#RUN poetry install --no-root && rm -rf $POETRY_CACHE_DIR

#COPY . /app

#RUN poetry install

#EXPOSE 5001

CMD ["poetry", "run", "flask", "--debug", "run" , "--port", "5001", "--host=0.0.0.0"]