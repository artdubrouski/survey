from typing import Dict, List, NamedTuple, Tuple, Type

from django.db.models import Q

from fabrique_survey.surveys.models import Question, ResponseOption


QID = NamedTuple(
	'QuestionIDs',
	[
		('txt_pk', int),  # pk of a related question with question type 'text'
		('sel_pk', int),  # ... same of 'select'
		('selmult_pk', int),  # ... same of 'select multiple'
	]
)

RID = NamedTuple(
	'ResponseOptionsIDs',
	[
		# pks of related response options to a question with question type 'select'
		('sel_pks', List[int]),
		('sel_mult_pks', List[int]),  # ... same of 'select multiple'
	]
)


def get_questions_ids(survey_pk: int) -> 'QID':
	"""Returns relevant to survey question ids."""
	txt_pk = Question.objects.get(
		Q(survey=survey_pk) & Q(title='Question Text')).pk
	sel_pk = Question.objects.get(
		Q(survey=survey_pk) & Q(title='Question Select')).pk
	selmult_pk = Question.objects.get(
		Q(survey=survey_pk) & Q(title='Question Select Multiple')).pk
	return QID(txt_pk, sel_pk, selmult_pk)


def get_response_options_ids(survey_pk: int, sel_pk: int, selmult_pk: int) -> 'RID':
	"""Returns relevant to survey response options ids."""
	sel_pks = list(
		(int(r.pk) for r in ResponseOption.objects.filter(question=sel_pk)),
	)
	sel_mult_pks = list(
		(int(r.pk) for r in ResponseOption.objects.filter(question=selmult_pk)),
	)
	return RID(sel_pks, sel_mult_pks)


class CustomSurveyResponse:
	def __init__(self, survey_pk: int) -> None:
		self.survey_pk = survey_pk
		self.Qid = get_questions_ids(survey_pk)
		self.Rid = get_response_options_ids(survey_pk, self.Qid.sel_pk, self.Qid.selmult_pk)
		self.txt_response = {
			"question": self.Qid.txt_pk,
			"response_text": "textt"
		}
		self.sel_response = {
			"question": self.Qid.sel_pk,
			"response_select": self.Rid.sel_pks[1]
		}
		self.selmult_response = {
			"question": self.Qid.selmult_pk,
			"response_select": [self.Rid.sel_mult_pks[0], self.Rid.sel_mult_pks[2]]
		}

	def _generate_survey_response(self) -> Dict:
		"""Returns a survey resonse based on all self.responses."""
		survey_response = {
			"survey": self.survey_pk,
			"responses": [self.txt_response, self.sel_response, self.selmult_response],
		}
		return survey_response

	def _set_self_qid2_self_rid2(self, survey_pk2: int) -> Dict:
		"""Add another question and response ids to self."""
		self.Qid2 = get_questions_ids(survey_pk2)
		self.Rid2 = get_response_options_ids(survey_pk2, self.Qid2.sel_pk, self.Qid2.selmult_pk)

	def get_valid_sr(self) -> Dict:
		"""Returns a valid survey response."""
		return self._generate_survey_response()
	
	def get_another_valid_sr(self) -> Dict:
		"""
		Returns another valid survey response with
		modified responses.
		"""
		self.txt_response['response_text'] = 'text2'
		self.sel_response['response_select'] = self.Rid.sel_pks[0]
		self.selmult_response['response_select'] = [
			self.Rid.sel_mult_pks[1],
			self.Rid.sel_mult_pks[2]
		]
		return self._generate_survey_response()

	def get_invalid_sr_redundant_select_for_text(self) -> Dict:
		"""
		Returns a valid survey response, with
		redundant response_select option for text question type.
		"""
		self.txt_response['response_select'] = self.Rid.sel_pks[0]
		return self._generate_survey_response()

	def get_valid_sr_redundant_text_for_select(self) -> Dict:
		"""
		Returns a valid survey response, but with redundant
		response_text option for select question type.
		"""
		self.sel_response['response_text'] = 'text_sel'
		return self._generate_survey_response()

	def get_invalid_sr_empty_resp_opts_for_select(self) -> Dict:
		"""
		Returns an invalid survey response, with
		no requiried response_select option for select question type.
		"""
		self.sel_response.pop('response_select')
		return self._generate_survey_response()

	def get_invalid_sr_singleselect_for_selectmult(self) -> Dict:
		"""
		Returns an invalid survey response, with an integer in
		response_select option for select multiple question type,
		which require a List[int] in response_select field.
		"""
		self.selmult_response['response_select'] = self.Rid.sel_mult_pks[0]
		return self._generate_survey_response()

	def get_invalid_sr_mutselect_for_select(self) -> Dict:
		"""
		Returns an invalid survey response, with an List[int] in
		select option for select question type, which require 
		an int or a list with one int in response_select field.
		"""
		self.sel_response['response_select'] = [
			self.Rid.sel_mult_pks[1],self.Rid.sel_mult_pks[2],
		]
		return self._generate_survey_response()
	
	def get_invalid_sr_responses_lt_questions(self) -> Dict:
		"""
		Returns an invalid survey response, with
		num of responses < num of related survey questions.
		"""
		survey_response = self._generate_survey_response()
		survey_response['responses'].pop()
		return survey_response

	def get_invalid_sr_responses_gt_questions(self) -> Dict:
		"""
		Returns an invalid survey response, with
		num of responses > num of related survey questions.
		"""
		survey_response = self._generate_survey_response()
		redundant_response = {
				"question": self.Qid.txt_pk,
				"response_text": "changed my mind",
			}
		survey_response['responses'].append(redundant_response)
		return survey_response

	def get_invalid_sr_unrelated_questions(self, survey_pk2: int) -> Dict:
		"""
		Returns an invalid survey response, with responses
		to unrelated questions to the survey.
		"""
		self._set_self_qid2_self_rid2(survey_pk2)
		self.sel_response['question'] = self.Qid2.sel_pk
		self.sel_response['response_select'] = self.Rid2.sel_pks[1]
		return self._generate_survey_response()

	def get_invalid_sr_unrelated_resp_options(self, survey_pk2: int) -> Dict:
		"""
		Returns an invalid survey response, with response options
		unrelated to the question.
		"""
		self._set_self_qid2_self_rid2(survey_pk2)
		self.sel_response['response_select'] = self.Rid2.sel_pks[1]
		self.selmult_response['response_select'] = [
			self.Rid2.sel_mult_pks[0],
			self.Rid.sel_mult_pks[2],
		]
		return self._generate_survey_response()


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
