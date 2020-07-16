# Surveys
Supports adding, retrieving, updating and deleting surveys.

Survey is basically a **questionnare sheet**, a list of [questions](questions.md), some of which provide [response options](response-options.md).

## POST a new survey

Authorization header shoud be included for this request.

**Request**:

`POST` `/api/v1/surveys/`

Parameters:

Name        | Type     | Required | Description
------------|----------|----------|------------
title       | str      | Yes      | The title for the new survey.
start_date  | datetime | Yes      | The start date of the new survey. <br> Example: **`2020-01-01T12:00:00`**
end_date    | datetime | Yes      | The end date of the new survey.
description | str      | No       | The description for the new survey.
questions   | array    | Yes      | The nested [questions](questions.md) for the new survey.

**Request data** example:

```json
{
    "title": "Dev Survey",
    "start_date": "2020-06-16T17:51:17",
    "end_date": "2020-09-16T17:51:17",
    "description": "This survey is about linting.",
    "questions": [
        {
            "title": "Favourite linter?",
            "question_type": "select",
            "response_options": [
                {
                    "title": "flake8"
                },
                {
                    "title": "pylint"
                }
            ]
        }
    ]
}
```

**Response**:

```json
Content-Type application/json
201 Created

{
    "pk": 1,
    "title": "Dev Survey",
    "start_date": "2020-06-16T17:51:17",
    "end_date": "2020-09-16T17:51:17",
    "description": "This survey is about linting.",
    "questions": [
        {
            "pk": 1,
            "survey": 1,
            "survey_title": "Test Survey",
            "title": "Favourite linter?",
            "question_type": "select",
            "response_options": [
                {
                    "id": 1,
                    "title": "flake8",
                    "question": 1
                },
                {
                    "id": 2,
                    "title": "pylint",
                    "question": 1
                }
            ]
        }
    ]
}
```

## List all surveys

+ If user is authorized as admin, all surveys are listed.
+ If user is an AnonymousUser, only active surveys are listed.

**Request**:

`GET` `/api/v1/surveys/`

**Response**

```json
Content-Type application/json
200 OK

{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "pk": 1,
            "title": "Dev Survey",
            "start_date": "2020-06-16T17:51:17",
            "end_date": "2020-09-16T17:51:17",
            "description": "This survey is about linting.",
            "questions": [
                {
                    "pk": 1,
                    "survey": 1,
                    "survey_title": "Dev Survey",
                    "title": "Favourite linter?",
                    "question_type": "select",
                    "response_options": [
                        {
                            "id": 1,
                            "title": "flake8",
                            "question": 1
                        },
                        {
                            "id": 2,
                            "title": "pylint",
                            "question": 1
                        }
                    ]
                }
            ]
        }
    ]
}
```

## GET survey detail

**Request**:

`GET` `/api/v1/surveys/{survey_id}/`

**Response**

```json
Content-Type application/json
200 OK

{
    # survey details
}
```

## PATCH a survey

**Request**:

`PATCH` `/api/v1/surveys/{survey_id}/`

All the survey fields can be individually updated.

*Notes:*

- start_date can't be changed
- to [update a specific question](questions.md#patch-a-question) from multiple survey questions use [questions endpoint](questions.md#patch-a-question)
- to [add a specific question](questions.md#post-a-question) to the survey questions list use [questions endpoint](questions.md#post-a-question)
- to [delete a specific question](questions.md#delete-a-question) from the survey questions list use [questions endpoint](questions.md#delete-a-question)

**Response**

```json
Content-Type application/json
200 OK

{
    # survey details
}
```


## DELETE a survey

`DELETE` `/api/v1/surveys/{survey_id}/`

**Response**:

```json
Content-Type application/json
204 No Content
```