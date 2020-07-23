from typing import List, Union

from drf_writable_nested.serializers import WritableNestedModelSerializer

from rest_framework import serializers
from rest_framework.serializers import ValidationError

from survey.surveys.models import (
	Question,
	Response,
	ResponseOption,
	Survey,
	SurveyResponse,
)


class ResponseOptionSerializer(serializers.ModelSerializer):
	class Meta:
		model = ResponseOption
		fields = '__all__'


class ResponseSerializer(serializers.ModelSerializer):
	question_title = serializers.SerializerMethodField()
	response_select_titles = serializers.SerializerMethodField()

	def get_response_select_titles(self, obj) -> List[str]:
		"""Human-readable responses titles."""
		return [resp.title for resp in obj.response_select.all()]

	def get_question_title(self, obj) -> str:
		"""Human-readable question title."""
		if obj.question:
			return obj.question.title
		else:
			return 'deleted'

	def to_internal_value(self, data):
		"""
		Converts response_select type int to list for ManyToMany validation.
		"""
		if isinstance(data.get('response_select'), int):
			data['response_select'] = [data['response_select']]
		return super().to_internal_value(data)

	def validate(self, data):
		if (question := data.get('question')) is None:
			raise ValidationError('Question ID not provided')

		qtype = {
			'is_sel': (question.question_type == 'select'),
			'is_selmult': (question.question_type == 'select multiple'),
			'is_txt': (question.question_type == 'text'),
		}
		q_pk, q_title = question.pk, question.title

		if qtype['is_selmult'] and len(data.get('response_select', [])) < 2:
			raise ValidationError(
				f'Multiple items should be selected for question {q_pk} "{q_title}"'
			)
		elif qtype['is_sel'] and len(data.get('response_select', [])) > 1:
			raise ValidationError(
				f'Only one item should be selected for question {q_pk} "{q_title}"'
			)
		elif qtype['is_txt'] and not data.get('response_text'):
			raise ValidationError(
				f'response_text field is empty for question {q_pk} "{q_title}"'
			)
		if ((qtype['is_sel'] or qtype['is_selmult']) and
				not data.get('response_select')):
			raise ValidationError(
				f'response_select field is empty for question {q_pk} "{q_title}"'
			)
		self._pop_redundant_fields(data, qtype)
		return data

	def _pop_redundant_fields(self, data, qtype: dict) -> None:
		if qtype['is_sel'] or qtype['is_selmult']:
			data.pop('response_text', None)
		elif qtype['is_txt']:
			data.pop('response_select', None)

	class Meta:
		model = Response
		fields = (
			'question',
			'question_title',
			'response_text',
			'response_select',
			'response_select_titles',
		)


class QuestionSerializer(WritableNestedModelSerializer):
	response_options = ResponseOptionSerializer(required=False, many=True)
	question_type = serializers.ChoiceField(
		choices=Question.QUESTION_TYPES,
		required=False,
	)
	survey_title = serializers.SerializerMethodField()

	def get_survey_title(self, obj) -> str:
		"""Human-readable survey title."""
		if obj.survey:
			return obj.survey.title
		else:
			return 'deleted'

	def update(self, instance, validated_data):
		if (instance.question_type in ('select', 'select multiple') and
				validated_data.get('question_type') == 'text'):
			instance.response_options.clear()
		return super().update(instance, validated_data)

	def validate(self, data):
		if data.get('question_type') == 'text' and data.get('response_options'):
			raise ValidationError(
				'Text response does not require response options'
			)
		elif (data.get('question_type') in ('select', 'select multiple') and
				(not data.get('response_options') or
				len(data.get('response_options'))) == 1):
			raise ValidationError('Provide at least two response options.')
		return data

	class Meta:
		model = Question
		fields = (
			'pk',
			'survey',
			'survey_title',
			'title',
			'question_type',
			'response_options',
		)


class SurveySerializer(WritableNestedModelSerializer):
	questions = QuestionSerializer(many=True, required=True)
	start_date = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%S')
	end_date = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%S')

	def update(self, instance, validated_data):
		self._validate_start_date_on_update(instance, validated_data.get('start_date'))
		self._validate_end_date_on_update(instance, validated_data.get('end_date'))
		return super().update(instance, validated_data)

	def _validate_start_date_on_update(self, instance,
									   updated_start_date: Union[str, None]) -> None:
		"""Restricts survey start date changing."""
		if not updated_start_date or updated_start_date == instance.start_date:
			return
		if instance.start_date != updated_start_date:
			raise ValidationError('start_date can\'t be changed')

	def _validate_end_date_on_update(self, instance,
								     updated_end_date: Union[str, None]) -> None:
		"""Check end date > start date."""
		if not updated_end_date or updated_end_date == instance.end_date:
			return
		if updated_end_date <= instance.start_date:
			raise ValidationError('end date should be greater than start date')

	def validate(self, data):
		if self.context['request'].method == 'PATCH':
			return data
		if not data.get('questions'):
			raise serializers.ValidationError('Provide at least one question.')
		if data.get('end_date') is None:
			return data
		elif data.get('end_date') <= data.get('start_date'):
			raise serializers.ValidationError(
				'end date should be greater than start date'
			)
		return data

	class Meta:
		model = Survey
		fields = (
			'pk',
			'title',
			'start_date',
			'end_date',
			'description',
			'questions',
		)


class SurveyResponseSerializer(WritableNestedModelSerializer):
	responses = ResponseSerializer(many=True)

	def validate(self, data):
		survey = data.get('survey')
		responses = data.get('responses', [])
		self._validate_user_not_already_taken_survey(survey)
		self._validate_responses_question_equality(responses, survey)
		self._validate_response_questions(responses, survey)
		self._validate_response_options(responses)
		return data

	def _validate_user_not_already_taken_survey(self, survey):
		"""Check if user takes the survey for the first time."""
		user_id = self.context['request'].COOKIES.get('user_id')
		if user_id is None:
			return
		if SurveyResponse.objects.has_user_already_taken_survey(survey.pk, user_id):
			raise ValidationError(f'You\'ve already taken survey "{survey}" before')

	def _validate_responses_question_equality(self, responses, survey) -> None:
		"""Check if responses count equal to questions count."""
		try:
			questions = survey.questions
		except AttributeError:
			raise ValidationError('survey ID not provided')
		if len(responses) < questions.count():
			raise ValidationError(
				'You have not answered all the survey questions'
			)
		elif len(responses) > questions.count():
			raise ValidationError(
				'You have answered some questions more than once'
			)

	def _validate_response_questions(self, responses, survey) -> None:
		"""Check if all the questions are related to the survey."""
		responses_questions_ids = {resp.get('question').pk for resp in responses}
		try:
			questions = survey.questions.all()
		except AttributeError:
			raise ValidationError('Provide questions to which you respond.')
		survey_questions_ids = {q.pk for q in questions}

		if responses_questions_ids < survey_questions_ids:
			invalid_ids = survey_questions_ids - responses_questions_ids
			raise ValidationError(
				f'You haven\'t asnswered questions {invalid_ids}'
			)
		if responses_questions_ids != survey_questions_ids:
			invalid_ids = responses_questions_ids - survey_questions_ids
			raise ValidationError(
				f'These questions are not related to the survey: {invalid_ids}'
			)

	def _validate_response_options(self, responses: list) -> None:
		"""
		Check if all selected response options are related to the question.
		"""
		for resp in responses:
			selections = resp.get('response_select')
			if selections is not None:
				valid_question = resp.get('question')
				for selection in selections:
					if selection.question.pk != valid_question.pk:
						valid_resp_options = valid_question.response_options.all()
						valid_options = ', '.join(
							[f'{r.pk} "{r.title}"' for r in valid_resp_options]
						)
						raise ValidationError(
							f'Response option {selection.pk} "{selection.title}" '
							'is unrelated to the question '
							f'{valid_question.pk} "{valid_question.title}". '
							f'Valid options are: {valid_options}'
						)

	class Meta:
		model = SurveyResponse
		fields = ('pk', 'user_id', 'survey', 'responses')
