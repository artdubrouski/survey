from typing import List

from drf_writable_nested.serializers import WritableNestedModelSerializer

from fabrique_survey.surveys.models import (
	Question,
	Response,
	ResponseOption,
	Survey,
	SurveyResponse,
)

from rest_framework import serializers
from rest_framework.serializers import ValidationError


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
		question = data.get('question')
		qtype_is_select = question.question_type == 'select'
		qtype_is_selectmult = question.question_type == 'select multiple'
		qtype_is_text = question.question_type == 'text'
		q_pk, q_title = question.pk, question.title

		if qtype_is_selectmult and len(data.get('response_select', [])) < 2:
			raise ValidationError(
				f'Multiple items should be selected for question {q_pk} "{q_title}"'
			)
		elif qtype_is_select and len(data.get('response_select', [])) > 1:
			raise ValidationError(
				f'Only one item should be selected for question {q_pk} "{q_title}"'
			)
		elif qtype_is_text and not data.get('response_text'):
			raise ValidationError(
				f'response_text field is empty for question {q_pk} "{q_title}"'
			)
		if (qtype_is_select or qtype_is_selectmult) and not data.get('response_select'):
			raise ValidationError(
				f'response_select field is empty for question {q_pk} "{q_title}"'
			)
		if qtype_is_select or qtype_is_selectmult:
			data.pop('response_text', None)
		elif qtype_is_text:
			data.pop('response_select', None)
		return data

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
	question_type = serializers.ChoiceField(choices=Question.QUESTION_TYPES, required=False)
	survey_title = serializers.SerializerMethodField()

	def get_survey_title(self, obj) -> str:
		"""Human-readable survey title."""
		if obj.survey:
			return obj.survey.title
		else:
			return 'deleted'

	def update(self, instance, validated_data):
		if instance.question_type in ('select', 'select multiple') and validated_data.get('question_type') == 'text':
			instance.response_options.clear()
		return super().update(instance, validated_data)

	def validate(self, data):
		if data.get('question_type') == 'text' and data.get('response_options'):
			raise ValidationError('Text response does not require response options')
		elif data.get('question_type') in ('select', 'select multiple') \
			and (not data.get('response_options') or len(data.get('response_options'))) == 1:
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
		self._validate_start_date_on_update(instance, validated_data)
		self._validate_end_date_on_update(instance, validated_data)
		return super().update(instance, validated_data)

	def _validate_start_date_on_update(self, instance, validated_data):
		"""Restricts survey start date changing."""
		updated_start_date = validated_data.get('start_date')
		if not updated_start_date or updated_start_date == instance.start_date:
			return
		if instance.start_date != updated_start_date:
			raise ValidationError('start_date can\'t be changed')

	def _validate_end_date_on_update(self, instance, validated_data):
		"""Check end date > start date."""
		updated_end_date = validated_data.get('end_date')
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
			raise serializers.ValidationError('end date should be greater than start date')
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
		self._validate_responses_question_equality(data)
		self._validate_response_questions(data)
		self._validate_response_options(data)
		return data

	def _validate_responses_question_equality(self, data):
		"""Check if responses count equal to questions count."""
		responses = data.get('responses')
		try:
			questions = data.get('survey').questions
		except AttributeError:
			raise ValidationError('survey ID not provided')
		if len(responses) < questions.count():
			raise ValidationError('You have not answered all the survey questions')
		elif len(responses) > questions.count():
			raise ValidationError('You have answered some questions more than once')

	def _validate_response_questions(self, data):
		"""Check if all the questions are related to the survey."""
		responses_questions_ids = {resp.get('question').pk for resp in data.get('responses', [])}
		try:
			questions = data.get('survey').questions.all()
		except AttributeError:
			raise ValidationError('Provide questions to which you respond.')
		survey_questions_ids = {q.pk for q in questions}

		if responses_questions_ids < survey_questions_ids:
			invalid_ids = survey_questions_ids - responses_questions_ids
			raise ValidationError(f'You haven\'t asnswered questions {invalid_ids}')
		if responses_questions_ids != survey_questions_ids:
			invalid_ids = responses_questions_ids - survey_questions_ids
			raise ValidationError(
				f'These questions are not related to the survey: {invalid_ids}'
			)

	def _validate_response_options(self, data):
		"""
		Check if all selected response options are related to the question.
		"""
		for resp in data.get('responses', []):
			selections = resp.get('response_select')
			if selections is not None:
				valid_question = resp.get('question')  # validated earlier in caller func
				for selection in selections:
					if selection.question.pk != valid_question.pk:
						valid_options = ', '.join(
							[f'{r.pk} "{r.title}"' for r in valid_question.response_options.all()]
						)
						raise ValidationError(
							f'Response option {selection.pk} "{selection.title}" is unrelated to the question '
							f'{valid_question.pk} "{valid_question.title}". '
							f'Valid options are: {valid_options}'
						)

	class Meta:
		model = SurveyResponse
		fields = ('pk', 'user_id', 'survey', 'responses')
