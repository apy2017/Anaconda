from rest_framework import serializers
from poll_editor.models import User, Poll, Question, Answer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'name',
            'last_name'
        ]


class PollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = [
            'code',
            'name',
            'owner'
        ]


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = [
            'pk',
            'caption',
        ]


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = [
            'caption',
        ]
