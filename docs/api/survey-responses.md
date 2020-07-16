# Survey Responses
Supports adding, retrieving, updating and deleting survey responses.

Survey Response is basically an **response sheet** with responses.

## POST a new survey

When posting a new Survey Response, **user_id** (uuid4) is generated and saved to client cookie file.<br>
This user_id is automatically added to the corresponding survey response instance field.<br>
It is later used to access only user related survey responses.

If user_id is found in user cookies, it is validated and used instead of creating a new one.

**Request**:

`POST` `/api/v1/survey-responses/`

Parameters:

Name            | Type     | Required | Description
----------------|----------|----------|------------
survey          | int      | Yes      | Related survey ID.
responses       | array    | Yes      | Nested [responses](responses.md) for the new survey response.

**For responses parameters check [Response model.](responses.md)**

Survey Response **request data** example:

```json
{
	"survey": 1,
	"responses": [
		{
            "question": 7,
            "response_text": "mypy"
        },
		{
            "question": 6,
            "response_select": 9
        },
		{
            "question": 5,
            "response_select": [7,8]
        }
	]
}
```

**Response**:

```json
Content-Type application/json
201 Created

{
    "pk": 2,
    "user_id": "857402d9-d573-42de-93f5-6e0f66caa528",
    "survey": 1,
    "responses": [
        {
            "question": 7,
            "question_title": "Favourite type checker?",
            "response_text": "mypy",
            "response_select": [],
            "response_select_titles": []
        },
        {
            "question": 6,
            "question_title": "Favourite linter?",
            "response_text": "",
            "response_select": [
                9
            ],
            "response_select_titles": [
                "flake8"
            ]
        },
        {
            "question": 5,
            "question_title": "What linter plugins/features have you used?",
            "response_text": "",
            "response_select": [
                7,
                8
            ],
            "response_select_titles": [
                "Variable names checker",
                "Docstrings check"
            ]
        }
    ]
}

```

## List all surveys

+ If user is authorized as admin, all survey responses are listed.
+ If user is an AnonymousUser, only his survey responses are listed, based on cookies user_id.

**Request**:

`GET` `/api/v1/survey-responses/`

**Response**

```json
Content-Type application/json
200 OK

{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        # survey response results
    ]
}
```

## GET survey response detail

**Request**:

`GET` `/api/v1/survey-responses/{survey_response_id}/`

**Response**

```json
Content-Type application/json
200 OK

{
    # survey response details
}
```


## DELETE survey response

`DELETE` `/api/v1/survey-responses/{survey_response_id}/`

**Response**:

```json
Content-Type application/json
204 No Content
```

**Survey Responses can't be modified.**<br>
`PATCH` method not allowed.
