from rest_framework import serializers
from poll_editor.models import Poll, Question, Answer, AnswerContainer


class PollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = [
            'pk',
            'code',
            'name',
            'owner',
            'passes'
        ]


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = [
            'pk',
            'caption',
        ]


class AnswerContainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerContainer
        fields = [
            'on_poll',
            'pk',
            'telegram_username'
        ]
        depth = 1


class AnswerContainerSerializerXML(serializers.ModelSerializer):
    class Meta:
        model = AnswerContainer
        fields = [
            'on_poll',
            'pk',
            'telegram_username',
            'answer_set'
        ]
        depth = 1


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = [
            'pk',
            'on_question',
            'caption',
        ]
        depth = 1
