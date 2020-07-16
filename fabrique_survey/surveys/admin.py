from django.contrib import admin

from .models import Question, Response, Survey


class QuestionInlineAdmin(admin.StackedInline):
    model = Question
    extra = 0


class ResponseInlineAdmin(admin.StackedInline):
    model = Response
    extra = 0


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = (ResponseInlineAdmin,)
    list_display = (
        'title',
        'survey',
    )


@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = (
        'response_text',
    )


@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    inlines = (QuestionInlineAdmin,)
    list_display = (
        'title',
        'description',
        'start_date',
        'end_date',
    )
