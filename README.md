[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-380/)

# Password Generator API

This app is responsible to generate random passwords based on parameters that the user can chose. The user can chose what type of characters the generated password can have. For now, the available characters can be numbers, lowercase chars and uppercase chars and special characters. The user also can chose the lenght of the password. If the user decided to not pass some of the parameters in the request, those parameters will be replaced by default ones that can be configurable by an user.

## How to run

You can run the application with Docker compose or with the recommended way (virtual environment). But before that, you have to create a `.env` file with some environment variables. You can check the template example on the `.env_template` file.

### Docker compose

With docker compose, you just need to run the following command:
```bash
docker-compose up --build
```

### Virtual environment
Make sure you have [pipenv](https://pypi.org/project/pipenv/) installed in your computer. Then, you have to run the following commands:
```bash
pipenv install
pipenv run uvicorn app.main:app
```

## Tests

Tests are run with [pytest](https://docs.pytest.org/en/7.1.x/). To run the tests, you can run the following command:
```bash
pipenv run pytest .
```

## Implementation details

### overview

This app was designed to generate random passwords based on parameters that users can chose. If a parameter is not been passed on the request, the system will get the default value for that parameter. This default parameter is saved on a database (PostgreSQL) in a table named `configuration`, which contains all the default values. This configuration must be active, otherwise the API will raise an exception. Only the registered admin users can add/read/update/delete configurations. These default values could be saved in simple environment variables, but being stored in a database offers more advantages, e.g. the admin can add or update a default configuration without having to re-deploy the app with the new environment variables.

In the following images are present two flows, the first one is regarding the creation of a configuration and the second one is regarding the generation of a password.

![Captura de ecrã 2022-10-12, às 08 45 47](https://user-images.githubusercontent.com/70910909/195272373-54bc8561-aad8-4098-b47d-17c3252c50cf.png)

### Structure

For the structure, it was followed the recommended structure by the FastAPI's official [documentation](https://fastapi.tiangolo.com/tutorial/bigger-applications/).

### Patterns

The main pattern followed was to separate the business logic code from the rest. All the code regarding third-party libraries was put on the `utils` folder and the business logic was put outside. This is a good practice with the advantage of, if we need to change, in the future, let's say, the database for another one that is not supported by Sqlalchemy, we only need to change what is inside the `utils`, the business logic doesn't need to be changed.

It was also created a data layer on `utils/data_handlers` so we can reuse the methods regarding the models.

For larger classes, it was decided to use one class per file, so that can be easily managed and maintained.

### Future work

As a future work, we intend to improve the authentication service, maybe adding a feature in which only a super user can invite admin users by email or so, because currently any user can create/read/update/delete configurations, they just need to be registered. We also intend to improve the converage of the unit tests.

## Endpoints

### Signup
**You send:**  Your credentials for log in
**You get:** The info about the user created

**Request Example:**
```json
POST api/signup

{
    "email": "example@email.com",
    "password": "password"
}
```
**Successful Response Example:**
```json
Status: 201 Created
{
    "id": 1,
    "email": "example@email.com",
    "is_active": true
}
```
**Failed Response Example:**
```json
Status: 422 Unprocessable Entity
{
    "detail": [
        {
            "loc": [
                "body",
                "email"
            ],
            "msg": "must be a valid email",
            "type": "value_error"
        }
    ]
}
``` 

### Login
**You send:**  Your login credentials
**You get:** An access token with wich you can make further actions

**Request Example:**
```json
POST api/login

{
    "email": "example@email.com",
    "password": "password"
}
```
**Successful Response Example:**
```json
Status: 200 OK
{
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImV4YW1wbGVAZW1haWwuY29tIiwiZXhwIjoxNjY1NTYzMjQ0fQ.O2zUZQMtxuEVpUE6mcTzyTmB70B4ugOQ-TqzIuULU4U"
}
```
**Failed Response Example:**
```json
Status: 422 Unprocessable Entity
{
    "detail": "credentials are incorrect"
}
``` 

### Generate password
**You send:**  Parameters with the options
**You get:** The generated password

**Request Example:**
```json
GET api/random-password?lenght=200&numbers=1&lowercase_chars=1&uppercase_chars=1&special_symbols=1
```
**Successful Response Example:**
```json
Status: 200 OK
{
    "random_password": "|h\"8qy&0m83OOLL.1n<8jd5-UZ9C4\"=C%(8p3890>R40gxi-qO6'p%~s;VmW}<6&c5$PYF4Q~%.7is7o6IV8t'lx7SC3#KwXxW8baSz}S7h*G0ln3\\*tNZs1@/4+;vENyP8MFO.62r)vqnS63W{!D@`P>LZ!XJ0KU-x0.C,>eDtP9Duyr~:{9Ii&28A\\4c6JWDfE2+0#"
}
```
**Failed Response Example:**
```json
Status: 400 Bad Request
{
    "detail": "one of the following parameters must be provided: 'numbers', 'lowercase_chars', 'uppercase_chars' or 'special_symbols'"
}
```

The next endpoints need a `Authorization: Bearer <Token>` header.

### Create Configuration
**You send:**  The configuration with the info
**You get:** The created configuration info

**Request Example:**
```json
POST api/admin/configurations/

{
    "lenght": 10,
    "numbers": false,
    "lowercase_chars": true,
    "uppercase_chars": true,
    "special_symbols": true,
    "is_active": true
}
```
**Successful Response Example:**
```json
Status: 201 Created
{
    "id": 1,
    "lenght": 10,
    "numbers": false,
    "lowercase_chars": true,
    "uppercase_chars": true,
    "special_symbols": true,
    "is_active": true,
    "created_at": "2022-10-12T07:29:28.208504+00:00",
    "updated_at": null,
    "user": {
        "id": 1,
        "email": "example@email.com",
        "is_active": true
    }
}
```
**Failed Response Example:**
```json
Status: 422 Unprocessable Entity
{
    "detail": [
        {
            "loc": [
                "body",
                "uppercase_chars"
            ],
            "msg": "field required",
            "type": "value_error.missing"
        }
    ]
}
``` 

### List Configuration
**You get:** The list of all saved configurations

**Request Example:**
```json
GET api/admin/configurations
```
**Successful Response Example:**
```json
Status: 201 Created
[
  {
      "id": 1,
      "lenght": 10,
      "numbers": false,
      "lowercase_chars": true,
      "uppercase_chars": true,
      "special_symbols": true,
      "is_active": true,
      "created_at": "2022-10-12T07:29:28.208504+00:00",
      "updated_at": null,
      "user": {
          "id": 1,
          "email": "example@email.com",
          "is_active": true
      }
  }
]
```
**Failed Response Example:**
```json
Status: 401 Unauthorized
{
    "detail": "Not authenticated"
}
``` 

### Update Configuration
**You send:**  The info to update a specific configuration
**You get:** The updated configuration info

**Request Example:**
```json
PATCH api/admin/configurations/1/
{
  "lowercase_chars": false
}
```
**Successful Response Example:**
```json
Status: 201 Created

{
    "id": 1,
    "lenght": 10,
    "numbers": false,
    "lowercase_chars": false,
    "uppercase_chars": true,
    "special_symbols": true,
    "is_active": true,
    "created_at": "2022-10-12T07:29:28.208504+00:00",
    "updated_at": null,
    "user": {
        "id": 1,
        "email": "example@email.com",
        "is_active": true
    }
}
```
**Failed Response Example:**
```json
Status: 404 Not Found
{
    "detail": "configuration not found"
}
```

### Delete Configuration

**Request Example:**
```json
DELETE api/admin/configurations/1/
```
**Successful Response Example:**
```json
Status: 204 No Content
```
**Failed Response Example:**
```json
Status: 404 Not Found
{
    "detail": "configuration not found"
}
``` 
