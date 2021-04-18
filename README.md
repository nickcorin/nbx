# NBX Users Service

## Prerequisites

- Docker: https://docs.docker.com/install/
- MariaDB https://mariadb.com

### Setting up MariaDB

This project uses a MariaDB database to store its data.

MariaDB can be installed using `homebrew` on MacOS or `apt` on most Ubuntu-based distributions.

Once you have MariaDB installed, we can now set up your local schema.

From within the project, run the following commands:

- `echo -n "create database nbx" | mysql -uroot`

(I have assumed a blank root password. If you set one, please use it with the `-p` flag.)
## Testing

The unit tests for this project depend on having `mariadb` installed locally, and having your `nbx` database created.

Please make sure to set up your environment correctly before attempting to run the tests.

### Setup your Virtual Environment

From within the project, run:
- `python3 -m venv env`.
- `source ./env/bin/activate`

### Install the dependencies.

- `pip3 install -r requirements.txt`

### Run the tests.

- `python3 -m unittest discover -v -s tests`

## How to run the project

### Build

From within the project, run `docker-compose build`

### Run

From within the project, run `docker-compose up -d`

### View logs

From within the project, run `docker-compose logs -f users`

### Endpoints

- health: `GET /` - this is just an endpoint that returns the service name.
- list users: `GET /users` - return the list of users
  - Response Body:

    ```json
    [{
        "id": "uuid",
        "name": "string",
        "email": "string"
    }]
    ```

- create user: `POST /users` - create a user with the given request payload
  - Request Body:

    ```json
    {
        "name": "string",
        "email": "string"
    }
    ```

  - Response Body:

    ```json
    {
        "id": "uuid",
        "name": "string",
        "email": "string"
    }
    ```

- get user by id: `GET /users/{user_id}` - return the user with the ID from the url, or 404 if not found
  - Response Body:

    ```json
    {
        "id": "uuid",
        "name": "string",
        "email": "string"
    }
    ```

- update a user: `PUT /users/{user_id}` - update the user with the provided ID with the request payload, or 404 if not found
  - Request Body:

    ```json
    {
        "id": "uuid",
        "name": "string",
        "email": "string"
    }
    ```

  - Response Body:

    ```json
    {
        "id": "uuid",
        "name": "string",
        "email": "string"
    }
    ```

- delete a user: `DELETE /users/{user_id}` - delete the user with the given ID
  - Response: 204 No Content


