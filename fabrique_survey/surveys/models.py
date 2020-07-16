from datetime import datetime

from django.db import models
from django.utils import timezone


class SurveyQuerySet(models.QuerySet):
	def get_active_surveys(self):
		"""Only get surveys that are not overdue."""
		now = datetime.now(tz=timezone.utc)
		return self.filter(end_date__gt=now)


class Survey(models.Model):
	"""
	Survey questionnare list with nested questions and response options.
	"""
	objects = SurveyQuerySet.as_manager()
	title = models.CharField(max_length=300, db_index=True, blank=False)
	start_date = models.DateTimeField(blank=False)
	end_date = models.DateTimeField(blank=False)
	description = models.TextField(db_index=True, blank=True)

	class Meta:
		verbose_name = 'Survey'
		verbose_name_plural = 'Surveys'
		ordering = ['start_date', 'title']

	def __str__(self):
		return self.title


class Question(models.Model):
	"""Question with nested response options."""
	TEXT = 'text'
	SELECT = 'select'
	SELECT_MULTIPLE = 'select multiple'

	QUESTION_TYPES = (
		(TEXT, 'text'),
		(SELECT, 'select'),
		(SELECT_MULTIPLE, 'select multiple'),
	)
	title = models.TextField()
	survey = models.ForeignKey(
		Survey,
		on_delete=models.SET_NULL,
		related_name='questions',
		null=True,
	)
	question_type = models.CharField(
		max_length=200,
		choices=QUESTION_TYPES,
		default=TEXT,
	)

	class Meta:
		verbose_name = 'Question'
		verbose_name_plural = 'Questions'

	def __str__(self):
		return self.title


class ResponseOption(models.Model):
	"""
	Select options for select [multiple] question types.
	"""
	title = models.CharField(max_length=100)
	question = models.ForeignKey(
		Question,
		on_delete=models.SET_NULL,
		related_name='response_options',
		null=True,
	)

	class Meta:
		verbose_name = 'Response option'
		verbose_name_plural = 'Response options'

	def __str__(self):
		return self.title


class Response(models.Model):
	"""A response to a single question."""
	question = models.ForeignKey(
		Question,
		on_delete=models.SET_NULL,
		null=True,
		related_name='responses',
	)
	response_text = models.CharField(max_length=200, blank=True)
	response_select = models.ManyToManyField(
		ResponseOption,
		related_name='responses',
		blank=True,
	)

	class Meta:
		verbose_name = 'Response'
		verbose_name_plural = 'Responses'

	def __str__(self):
		return self.response_text or str(self.response_select)


class SurveyResponseQuerySet(models.QuerySet):
	def by_user(self, user_id):
		return self.filter(user_id=user_id)


class SurveyResponse(models.Model):
	"""Survey responses list with nested responses."""
	objects = SurveyResponseQuerySet.as_manager()
	user_id = models.CharField(max_length=100, blank=False)
	survey = models.ForeignKey(
		Survey,
		on_delete=models.SET_NULL,
		related_name='survey_responses',
		null=True,
	)
	responses = models.ManyToManyField(
		Response,
		related_name='survey_responses',
		blank=False,
	)

	class Meta:
		verbose_name = 'Survey response'
		verbose_name_plural = 'Survey responses'

	def __str__(self):
		return f'{self.survey}-{self.user_id}'
