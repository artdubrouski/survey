# Responses

Only accessible via [survey responses](survey-responses.md).

## Response Types
**- str** if related question_type is 'text'.<br> 
**- int** if related question_type is 'select'.<br> 
**- List[int]** if related question_type is 'select multiple'.<br> 

## Parameters

Name            | Type            | Required | Description
----------------|-----------------|----------|------------
question        | int             | No       | Related [question](questions.md) ID, auto added on creating survey response.
response_text   | str             | Depends  | Required only if related question_type is 'text'.
response_select | List[int]       | Depends  | Required only if related question_type is 'select' or 'select multiple'.<br> **NOTE:**<br>If related question_type is 'select', **int** type is prefered for selecting single response option ID.