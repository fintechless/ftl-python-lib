# ftl-python-lib

Fintechless Platform - Python Library

## Local development

### Virtual environment

You'll need [poetry](https://python-poetry.org/docs/#installation). This Python repository uses `Poetry` for managing its packages and dependencies.
Exit from your current virtual environment, if activated. Execute the following command in order to install `Poetry`:

```shell
pip install poetry
```

It is recommended you create a separate virtual environment (Python >=3.10) using `venv`. In order to create
a new virtual environment, execute the following command:

```shell
poetry shell
```

### Dependencies

In order to install the dependencies execute the following command in your shell:

```shell
poetry install
```

If you need to add a new dependency for development, you can execute the following command in your shell:

```shell
poetry add <NAME> --dev
```

If you need to add a new required dependency, you can execute the following command in your shell:

```shell
poetry add <NAME>
```

### Tests

Before running the tests, spin up Kafka on your local machine.
In order to do so, execute the following:

```shell
docker compose -f docker-compose.yml up -d
```

Once Kafka is up and running, you can run the tests by executing the following command in your shell:

```shell
poetry run tests
```

To stop Kafka, please execute the following command:

```shell
docker compose -f docker-compose.yml stop
```

## Code formatting

This library uses `black` in order to format the code using the PEP8 style guide. Execute the following command
to format the code (make sure to install all the dependencies with `Poetry`):

```shell
poetry run format
```

## Code linting

This library uses `pylint` to analyze the code in order to ensure that it's PEP8 compliant. Execute the following command
to analyze the code (make sure to install all the dependencies with `Poetry`):

```shell
poetry run lint
```
