from django.db.models import Q

from fabrique_survey.surveys.models import Question, ResponseOption


def get_questions_ids(survey_pk):
	q_txt_pk = Question.objects.get(
		Q(survey=survey_pk) & Q(title='Question Text')).pk
	q_sel_pk = Question.objects.get(
		Q(survey=survey_pk) & Q(title='Question Select')).pk
	q_selmult_pk = Question.objects.get(
		Q(survey=survey_pk) & Q(title='Question Select Multiple')).pk
	return q_txt_pk, q_sel_pk, q_selmult_pk


def get_responses_ids(survey_pk, q_sel_pk, q_selmult_pk):
	resp_sel = tuple(
		(r.pk for r in ResponseOption.objects.filter(question=q_sel_pk)),
	)
	resp_selmult = tuple(
		(r.pk for r in ResponseOption.objects.filter(question=q_selmult_pk)),
	)
	return resp_sel, resp_selmult


def get_survey_response(survey_pk):
	q_txt_pk, q_sel_pk, q_selmult_pk = get_questions_ids(survey_pk)
	resp_sel, resp_selmult = get_responses_ids(survey_pk, q_sel_pk, q_selmult_pk)

	survey_response = {
		"survey": survey_pk,
		"responses": [
			{
				"question": q_txt_pk,
				"response_text": "textt",
			},
			{
				"question": q_sel_pk,
				"response_select": resp_sel[1],
			},
			{
				"question": q_selmult_pk,
				"response_select": [resp_selmult[0], resp_selmult[2]],
			},
		],
	}
	return survey_response


def get_another_survey_resp(survey_pk):
	q_txt_pk, q_sel_pk, q_selmult_pk = get_questions_ids(survey_pk)
	resp_sel, resp_selmult = get_responses_ids(survey_pk, q_sel_pk, q_selmult_pk)

	survey_response = {
		"survey": survey_pk,
		"responses": [
			{
				"question": q_txt_pk,
				"response_text": "text2",
			},
			{
				"question": q_sel_pk,
				"response_select": resp_sel[0],
			},
			{
				"question": q_selmult_pk,
				"response_select": [resp_selmult[1], resp_selmult[2]],
			},
		],
	}
	return survey_response


def get_surv_resp_with_select_for_text(survey_pk):
	q_txt_pk, q_sel_pk, q_selmult_pk = get_questions_ids(survey_pk)
	resp_sel, resp_selmult = get_responses_ids(survey_pk, q_sel_pk, q_selmult_pk)

	survey_response = {
		"survey": survey_pk,
		"responses": [
			{
				"question": q_txt_pk,
				"response_text": "textt",
				"response_select": resp_sel[0]},  # invalid
			{
				"question": q_sel_pk,
				"response_select": resp_sel[1],
			},
			{
				"question": q_selmult_pk,
				"response_select": [resp_selmult[0], resp_selmult[2]],
			},
		],
	}
	return survey_response


def get_surv_resp_empty_resp_select_for_select(survey_pk):
	q_txt_pk, q_sel_pk, q_selmult_pk = get_questions_ids(survey_pk)
	resp_sel, resp_selmult = get_responses_ids(survey_pk, q_sel_pk, q_selmult_pk)

	survey_response = {
		"survey": survey_pk,
		"responses": [
			{
				"question": q_txt_pk,
				"response_text": "textt",
			},
			{
				"question": q_sel_pk,  # invalid
			},
			{
				"question": q_selmult_pk,
				"response_select": [resp_selmult[0], resp_selmult[2]],
			},
		],
	}
	return survey_response


def get_survey_response_text_for_select(survey_pk):
	q_txt_pk, q_sel_pk, q_selmult_pk = get_questions_ids(survey_pk)
	resp_sel, resp_selmult = get_responses_ids(survey_pk, q_sel_pk, q_selmult_pk)

	survey_response = {
		"survey": survey_pk,
		"responses": [
			{
				"question": q_txt_pk,
				"response_text": "text",
			},
			{
				"question": q_sel_pk,
				"response_text": "text_sel",  # invalid
				"response_select": resp_sel[1],
			},
			{
				"question": q_selmult_pk,
				"response_text": "text_selmult",
				"response_select": [resp_selmult[0], resp_selmult[2]],
			},
		],
	}
	return survey_response


def get_surv_resp_singleselect_for_selectmutli(survey_pk):
	q_txt_pk, q_sel_pk, q_selmult_pk = get_questions_ids(survey_pk)
	resp_sel, resp_selmult = get_responses_ids(survey_pk, q_sel_pk, q_selmult_pk)

	survey_response = {
		"survey": survey_pk,
		"responses": [
			{
				"question": q_txt_pk,
				"response_text": "textt",
			},
			{
				"question": q_sel_pk,
				"response_text": "textt2",
				"response_select": resp_selmult[1],
			},
			{
				"question": q_selmult_pk,
				"response_text": "textt3",
				"response_select": resp_selmult[0],  # invalid
			},
		],
	}
	return survey_response


def get_sr_responses_less_than_questions(survey_pk):
	q_txt_pk, q_sel_pk, q_selmult_pk = get_questions_ids(survey_pk)
	resp_sel, resp_selmult = get_responses_ids(survey_pk, q_sel_pk, q_selmult_pk)

	survey_response = {
		"survey": survey_pk,
		"responses": [
			{
				"question": q_txt_pk,
				"response_text": "text",
			},
			{
				"question": q_sel_pk,
				"response_select": resp_selmult[1],
			},
			# invalid - should be one more response
		],
	}
	return survey_response


def get_sr_responses_more_than_questions(survey_pk):
	q_txt_pk, q_sel_pk, q_selmult_pk = get_questions_ids(survey_pk)
	resp_sel, resp_selmult = get_responses_ids(survey_pk, q_sel_pk, q_selmult_pk)

	survey_response = {
		"survey": survey_pk,
		"responses": [
			{
				"question": q_txt_pk,
				"response_text": "textt",
			},
			{
				"question": q_sel_pk,
				"response_select": resp_selmult[1],
			},
			{
				"question": q_selmult_pk,
				"response_select": [resp_selmult[0], resp_selmult[2]],
			},
			{
				"question": q_txt_pk,
				"response_text": "changed my mind",
			},
		],
	}
	return survey_response


def get_sr_mutselect_for_select(survey_pk):
	q_txt_pk, q_sel_pk, q_selmult_pk = get_questions_ids(survey_pk)
	resp_sel, resp_selmult = get_responses_ids(survey_pk, q_sel_pk, q_selmult_pk)

	survey_response = {
		"survey": survey_pk,
		"responses": [
			{
				"question": q_txt_pk,
				"response_text": "textt",
			},
			{
				"question": q_sel_pk,
				"response_select": [resp_selmult[1], resp_selmult[2]],
			},
			{
				"question": q_selmult_pk,
				"response_select": [resp_selmult[0], resp_selmult[2]],
			},
		],
	}
	return survey_response


def get_sr_responses_on_questions_not_in_survey(survey_pk1, survey_pk2):
	q_txt_pk1, q_sel_pk1, q_selmult_pk1 = get_questions_ids(survey_pk1)
	resp_sel1, resp_selmult1 = get_responses_ids(survey_pk1, q_sel_pk1, q_selmult_pk1)
	q_txt_pk2, q_sel_pk2, q_selmult_pk2 = get_questions_ids(survey_pk2)
	resp_sel2, resp_selmult2 = get_responses_ids(survey_pk2, q_sel_pk2, q_selmult_pk2)

	survey_response = {
		"survey": survey_pk1,
		"responses": [
			{
				"question": q_txt_pk1,
				"response_text": "textt",
			},
			{
				"question": q_sel_pk2,  # invalid question id
				"response_select": resp_sel2[1],
			},
			{
				"question": q_selmult_pk1,
				"response_select": [resp_selmult1[0], resp_selmult1[2]],
			},
		],
	}
	return survey_response


def get_sr_responses_with_unrelated_responseoptions(survey_pk1, survey_pk2):
	q_txt_pk1, q_sel_pk1, q_selmult_pk1 = get_questions_ids(survey_pk1)
	resp_sel1, resp_selmult1 = get_responses_ids(survey_pk1, q_sel_pk1, q_selmult_pk1)
	q_txt_pk2, q_sel_pk2, q_selmult_pk2 = get_questions_ids(survey_pk2)
	resp_sel2, resp_selmult2 = get_responses_ids(survey_pk2, q_sel_pk2, q_selmult_pk2)

	survey_response = {
		"survey": survey_pk1,
		"responses": [
			{
				"question": q_txt_pk1,
				"response_text": "textt",
			},
			{
				"question": q_sel_pk1,
				"response_select": resp_selmult2[1],  # invalid response option id
			},
			{
				"question": q_selmult_pk1,
				"response_select": [resp_selmult2[0], resp_selmult1[2]],
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
