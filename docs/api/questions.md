# Questions
Supports adding, retrieving, updating and deleting questions.

*Note:*

- Authorization required.

## POST a new question

**Request**:

`POST` `/api/v1/questions/`

Parameters:

Name            | Type     | Required | Description
----------------|----------|----------|------------
title           | str      | Yes      | The title for the new question.
survey          | int      | Yes      | Related survey id.
question_type   | text     | No       | Available options: 'text', 'select', 'select multiple'. <br> **Default**: 'text'.
response_options| List[int]| Depends  | Nested [response options](response-options.md) for the new question. <br> **Not required** if question_type is 'text', otherwise **required**

Request data example:

```json
{
	"title": "What linter plugins/features have you used?",
	"survey": 1,
    "question_type": "select",
    "response_options": [
        {
            "title": "Cognitive complexity check"
        },
        {
            "title": "Variable names checker"
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
    "survey": 1,
    "survey_title": "Dev Survey",
    "title": "What linter plugins/features have you used?",
    "question_type": "select",
    "response_options": [
        {
            "id": 3,
            "title": "Cognitive complexity check",
            "question": 2
        },
        {
            "id": 4,
            "title": "Variable names checker",
            "question": 2
        }
    ]
}
```

## List all questions

**Request**:

`GET` `/api/v1/questions/`

**Response**

```json
Content-Type application/json
200 OK

{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        # question details
    ]
```


## GET question detail

`GET` `/api/v1/questions/{question_id}/`

**Response**

```json
Content-Type application/json
200 OK

{
    # question details
}
```

## PATCH a question

**Request**:

`PATCH` `/api/v1/questions/{questions_id}/`

**Response**

```json
Content-Type application/json
200 OK

{
    # survey details
}
```

## DELETE a question

**Request**:

`DELETE` `/api/v1/questions/{questions_id}/`

**Response**:

```json
Content-Type application/json
204 No Content
```