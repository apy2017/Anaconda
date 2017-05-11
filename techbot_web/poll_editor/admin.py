from django.contrib import admin
from .models import User, Poll, Question, Answer


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['name', 'telegram_id']


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner']


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['caption', 'from_poll']


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['caption', 'on_question']
