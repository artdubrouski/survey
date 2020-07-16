from rest_framework import filters, viewsets
from rest_framework.permissions import AllowAny, IsAdminUser

from .models import Question, Survey, SurveyResponse
from .serializers import (
	QuestionSerializer,
	SurveyResponseSerializer,
	SurveySerializer,
)
from .services import set_user_id_cookie, user_id_get_or_create


class QuestionSerializerViewSet(viewsets.ModelViewSet):
	serializer_class = QuestionSerializer
	permission_classes = [IsAdminUser]
	queryset = Question.objects.all()
	filter_backends = [filters.OrderingFilter]
	ordering_fields = ['survey']


class SurveyResponseViewSet(viewsets.ModelViewSet):
	serializer_class = SurveyResponseSerializer
	permission_classes = [AllowAny]
	http_method_names = ['get', 'post']

	def get_queryset(self):
		if self.request.auth:
			return SurveyResponse.objects.all()
		else:
			user_id = self.request.COOKIES.get('user_id')
			return SurveyResponse.objects.by_user(user_id)

	def create(self, request, *args, **kwargs):
		request, cookie_is_set = user_id_get_or_create(request)
		response = super().create(request, *args, **kwargs)
		response = set_user_id_cookie(request, response, cookie_is_set)
		return response


class SurveyViewSet(viewsets.ModelViewSet):
	serializer_class = SurveySerializer

	def get_permissions(self):
		if self.request.method == 'GET':
			permission_classes = [AllowAny]
		else:
			permission_classes = [IsAdminUser]
		return [permission() for permission in permission_classes]

	def get_queryset(self):
		if self.request.user.is_staff:
			return Survey.objects.all()
		return Survey.objects.get_active_surveys()
