from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path, reverse_lazy
from django.views.generic.base import RedirectView

from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

from .surveys.views import (
    QuestionSerializerViewSet,
    SurveyResponseViewSet,
    SurveyViewSet,
)

router = DefaultRouter()
router.register('surveys', SurveyViewSet, 'surveys')
router.register('survey-responses', SurveyResponseViewSet, 'survey-responses')
router.register('questions', QuestionSerializerViewSet, 'questions')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('api-token-auth/', views.obtain_auth_token),

    # the 'api-root' from django rest-frameworks default router
    # http://www.django-rest-framework.org/api-guide/routers/#defaultrouter
    re_path('', RedirectView.as_view(url=reverse_lazy('api-root'), permanent=False)),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
