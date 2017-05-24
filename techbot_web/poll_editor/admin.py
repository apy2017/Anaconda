from django.contrib import admin
from .models import Poll, Question, Answer, AnswerContainer


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner']


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['caption', 'from_poll']


@admin.register(AnswerContainer)
class AnswerContainerAdmin(admin.ModelAdmin):
    list_display = ['on_poll', 'telegram_username']


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['caption', 'from_container', 'on_question']
