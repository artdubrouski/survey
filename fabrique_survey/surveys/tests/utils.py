from typing import Dict, List, NamedTuple

from django.db.models import Q

from fabrique_survey.surveys.models import Question, ResponseOption


def get_questions_ids(survey_pk: int) -> NamedTuple:
	"""Returns relevant to survey question ids."""
	Qid = NamedTuple(
		'Qid',
		[
			('txt_pk', int),  # pk of a related question with question type 'text'
			('sel_pk', int),  # ... same of 'select'
			('selmult_pk', int),  # ... same of 'select multiple'
		]
	)
	Qid.txt_pk = Question.objects.get(
		Q(survey=survey_pk) & Q(title='Question Text')).pk
	Qid.sel_pk = Question.objects.get(
		Q(survey=survey_pk) & Q(title='Question Select')).pk
	Qid.selmult_pk = Question.objects.get(
		Q(survey=survey_pk) & Q(title='Question Select Multiple')).pk
	return Qid


def get_response_options_ids(survey_pk: int, sel_pk: int, selmult_pk: int) -> NamedTuple:
	"""Returns relevant to survey response options ids."""
	Rid = NamedTuple(
		'Rid',
		[
			# pks of related response options to a question with question type 'select'
			('sel_pks', List[int]),
			('sel_mult_pks', List[int]),  # ... same of 'select multiple'
		]
	)
	Rid.sel_pks = tuple(
		(r.pk for r in ResponseOption.objects.filter(question=sel_pk)),
	)
	Rid.sel_mult_pks = tuple(
		(r.pk for r in ResponseOption.objects.filter(question=selmult_pk)),
	)
	return Rid


def get_survey_response(survey_pk: int) -> Dict:
	"""Returns a valid survey response"""
	Qid = get_questions_ids(survey_pk)
	Rid = get_response_options_ids(survey_pk, Qid.sel_pk, Qid.selmult_pk)

	survey_response = {
		"survey": survey_pk,
		"responses": [
			{
				"question": Qid.txt_pk,
				"response_text": "textt",
			},
			{
				"question": Qid.sel_pk,
				"response_select": Rid.sel_pks[1],
			},
			{
				"question": Qid.selmult_pk,
				"response_select": [Rid.sel_mult_pks[0], Rid.sel_mult_pks[2]],
			},
		],
	}
	return survey_response


def get_another_survey_resp(survey_pk: int) -> Dict:
	"""Returns another valid survey response"""
	Qid = get_questions_ids(survey_pk)
	Rid = get_response_options_ids(survey_pk, Qid.sel_pk, Qid.selmult_pk)

	survey_response = {
		"survey": survey_pk,
		"responses": [
			{
				"question": Qid.txt_pk,
				"response_text": "text2",
			},
			{
				"question": Qid.sel_pk,
				"response_select": Rid.sel_pks[0],
			},
			{
				"question": Qid.selmult_pk,
				"response_select": [Rid.sel_mult_pks[1], Rid.sel_mult_pks[2]],
			},
		],
	}
	return survey_response


def get_surv_resp_with_select_for_text(survey_pk: int) -> Dict:
	"""
	Returns a valid survey response,
	but with redundant response_select option for text question type.
	"""
	Qid = get_questions_ids(survey_pk)
	Rid = get_response_options_ids(survey_pk, Qid.sel_pk, Qid.selmult_pk)

	survey_response = {
		"survey": survey_pk,
		"responses": [
			{
				"question": Qid.txt_pk,
				"response_text": "textt",
				"response_select": Rid.sel_pks[0]},  # redundant
			{
				"question": Qid.sel_pk,
				"response_select": Rid.sel_pks[1],
			},
			{
				"question": Qid.selmult_pk,
				"response_select": [Rid.sel_mult_pks[0], Rid.sel_mult_pks[2]],
			},
		],
	}
	return survey_response


def get_sr_empty_resp_opts_for_select(survey_pk: int) -> Dict:
	"""
	Returns an invalid survey response, with
	no requiried response_select option for select question type.
	"""
	Qid = get_questions_ids(survey_pk)
	Rid = get_response_options_ids(survey_pk, Qid.sel_pk, Qid.selmult_pk)

	survey_response = {
		"survey": survey_pk,
		"responses": [
			{
				"question": Qid.txt_pk,
				"response_text": "textt",
			},
			{
				"question": Qid.sel_pk,  # invalid
			},
			{
				"question": Qid.selmult_pk,
				"response_select": [Rid.sel_mult_pks[0], Rid.sel_mult_pks[2]],
			},
		],
	}
	return survey_response


def get_survey_response_text_for_select(survey_pk: int) -> Dict:
	"""
	Returns a valid survey response, but with redundant
	response_text option for select question type.
	"""
	Qid = get_questions_ids(survey_pk)
	Rid = get_response_options_ids(survey_pk, Qid.sel_pk, Qid.selmult_pk)

	survey_response = {
		"survey": survey_pk,
		"responses": [
			{
				"question": Qid.txt_pk,
				"response_text": "text",
			},
			{
				"question": Qid.sel_pk,
				"response_text": "text_sel",  # redundant
				"response_select": Rid.sel_pks[1],
			},
			{
				"question": Qid.selmult_pk,
				"response_text": "text_selmult",
				"response_select": [Rid.sel_mult_pks[0], Rid.sel_mult_pks[2]],
			},
		],
	}
	return survey_response


def get_surv_resp_singleselect_for_selectmutli(survey_pk: int) -> Dict:
	"""
	Returns an invalid survey response, with an integer in
	response_select option for select multiple question type,
	which require a List[int] in response_select field.
	"""
	Qid = get_questions_ids(survey_pk)
	Rid = get_response_options_ids(survey_pk, Qid.sel_pk, Qid.selmult_pk)

	survey_response = {
		"survey": survey_pk,
		"responses": [
			{
				"question": Qid.txt_pk,
				"response_text": "textt",
			},
			{
				"question": Qid.sel_pk,
				"response_text": "textt2",
				"response_select": Rid.sel_mult_pks[1],
			},
			{
				"question": Qid.selmult_pk,
				"response_text": "textt3",
				"response_select": Rid.sel_mult_pks[0],  # invalid
			},
		],
	}
	return survey_response


def get_sr_responses_lt_questions(survey_pk: int) -> Dict:
	"""
	Returns an invalid survey response, with
	num of responses < num of related survey questions.
	"""
	Qid = get_questions_ids(survey_pk)
	Rid = get_response_options_ids(survey_pk, Qid.sel_pk, Qid.selmult_pk)

	survey_response = {
		"survey": survey_pk,
		"responses": [
			{
				"question": Qid.txt_pk,
				"response_text": "text",
			},
			{
				"question": Qid.sel_pk,
				"response_select": Rid.sel_mult_pks[1],
			},
			# invalid - should be one more response
		],
	}
	return survey_response


def get_sr_responses_gt_questions(survey_pk: int) -> Dict:
	"""
	Returns an invalid survey response, with
	num of responses > num of related survey questions.
	"""
	Qid = get_questions_ids(survey_pk)
	Rid = get_response_options_ids(survey_pk, Qid.sel_pk, Qid.selmult_pk)

	survey_response = {
		"survey": survey_pk,
		"responses": [
			{
				"question": Qid.txt_pk,
				"response_text": "textt",
			},
			{
				"question": Qid.sel_pk,
				"response_select": Rid.sel_mult_pks[1],
			},
			{
				"question": Qid.selmult_pk,
				"response_select": [Rid.sel_mult_pks[0], Rid.sel_mult_pks[2]],
			},
			{
				# invalid - duplicated question response
				"question": Qid.txt_pk,
				"response_text": "changed my mind",
			},
		],
	}
	return survey_response


def get_sr_mutselect_for_select(survey_pk: int) -> Dict:
	"""
	Returns an invalid survey response, with an List[int] in
	select option for select question type, which require 
	an int or a list with one int in response_select field.
	"""
	Qid = get_questions_ids(survey_pk)
	Rid = get_response_options_ids(survey_pk, Qid.sel_pk, Qid.selmult_pk)

	survey_response = {
		"survey": survey_pk,
		"responses": [
			{
				"question": Qid.txt_pk,
				"response_text": "textt",
			},
			{
				"question": Qid.sel_pk,
				"response_select": [Rid.sel_mult_pks[1], Rid.sel_mult_pks[2]],  # invalid
			},
			{
				"question": Qid.selmult_pk,
				"response_select": [Rid.sel_mult_pks[0], Rid.sel_mult_pks[2]],
			},
		],
	}
	return survey_response


def get_sr_resp_unrelated_questions(survey_pk1: int, survey_pk2: int) -> Dict:
	"""
	Returns an invalid survey response, with responses
	to unrelated questions to the survey.
	"""
	Qid1 = get_questions_ids(survey_pk1)
	Rid1 = get_response_options_ids(survey_pk1, Qid1.sel_pk, Qid1.selmult_pk)
	Qid2 = get_questions_ids(survey_pk2)
	Rid2 = get_response_options_ids(survey_pk2, Qid2.sel_pk, Qid2.selmult_pk)

	survey_response = {
		"survey": survey_pk1,
		"responses": [
			{
				"question": Qid1.txt_pk,
				"response_text": "textt",
			},
			{
				"question": Qid2.sel_pk,  # invalid question id
				"response_select": Rid2.sel_pks[1],
			},
			{
				"question": Qid1.selmult_pk,
				"response_select": [Rid1.sel_mult_pks[0], Rid1.sel_mult_pks[2]],
			},
		],
	}
	return survey_response


def get_sr_unrelated_resp_options(survey_pk1, survey_pk2):
	"""
	Returns an invalid survey response, with response options
	unrelated to the question.
	"""
	Qid1 = get_questions_ids(survey_pk1)
	Rid1 = get_response_options_ids(survey_pk1, Qid1.sel_pk, Qid1.selmult_pk)
	Qid2 = get_questions_ids(survey_pk2)
	Rid2 = get_response_options_ids(survey_pk2, Qid2.sel_pk, Qid2.selmult_pk)

	survey_response = {
		"survey": survey_pk1,
		"responses": [
			{
				"question": Qid1.txt_pk,
				"response_text": "textt",
			},
			{
				"question": Qid1.sel_pk,
				"response_select": Rid2.sel_mult_pks[1],  # invalid response option id
			},
			{
				"question": Qid1.selmult_pk,
				"response_select": [Rid2.sel_mult_pks[0], Rid1.sel_mult_pks[2]],
			},
		],
	}
	return survey_response


"""
# TEST SURVEY
{
	"title": "Dev Survey",
	"start_date": "2020-06-16T17:51:17Z",
	"end_date":"2020-09-16T17:51:17Z",
	"description": "This survey is about linting",
	"questions": [
		{
			"title": "Using linters?"
		},
		{
			"title": "Favourite linter?",
			"question_type": "select",
			"response_options": [
				{"title": "flake8"},
				{"title": "pylint"}
			]
		},
		{
			"title": "What linter plugins/features have you used?",
			"question_type": "select multiple",
			"response_options": [
				{"title": "Cognitive complexity check"},
				{"title": "Variable names checker"},
				{"title": "Docstrings check"}
			]
		}
	]
}


# TEST SURVEY_RESPONSE
{
	"survey": 1,
	"responses": [
		{"question": 1, "response_text": "Yep, from kindergarden"},
		{"question": 2, "response_select": 2},
		{"question": 3, "response_select": [3,5]}
		]
}
"""
