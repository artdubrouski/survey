# Authentication

Authentication is available to administrators only.<br>


To authenticate,  include the token key in the Authorization HTTP header.<br>
Prefix it by the **"Token "** string, for example:<br>

```
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

A **curl** request with Authorization header example:

```bash
curl -X GET http://127.0.0.1:8000/api/v1/surveys/ -H 'Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b'
```

Unauthenticated requests to protected resources will result in an HTTP **`401 Unauthorized`** response.

## Retrieving Tokens

First, create superuser:

```bash
docker-compose run --rm web ./manage.py createsuperuser
```

Make a **Request**:

`POST` `/api-token-auth/`

Parameters:

Name     | Type   | Description
---------|--------|--------
username | str    | Admin's username
password | str    | Admin's password

Request data example:

```json
{ 
    "username" : "oleg",
    "password": "t65#4$9)W!" 
}
```

**Response**:

```json
{ 
    "token" : "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b" 
}
```
