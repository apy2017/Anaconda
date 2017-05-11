from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework.response import Response
from django.http import Http404
from .serializers import *
from poll_editor.models import User, Poll, Question, Answer


# Create your views here.

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        return UserSerializer


class PollList(generics.ListAPIView):
    def get_serializer_class(self):
        return PollSerializer

    def get_queryset(self):
        try:
            telegram_id = int(self.kwargs['telegram_id'])
            user = User.objects.get(telegram_id=telegram_id)
            return Poll.objects.filter(owner=user)

        except (User.DoesNotExist, ValueError) as e:
            raise Http404


class QuestionList(generics.ListAPIView):
    def get_serializer_class(self):
        return QuestionSerializer

    def get_queryset(self):
        code = self.kwargs['code']
        try:
            poll = Poll.objects.get(code=code)
            return Question.objects.filter(from_poll=poll)
        except Poll.DoesNotExist:
            raise Http404


class AnswerAdd(generics.CreateAPIView):

    def get_serializer_class(self):
        return AnswerSerializer

    def post(self, request, pk):
        try:
            question = Question.objects.get(pk=pk)
            answer = Answer(on_question = question, caption=request.data['caption'])
            answer.save()
            return Response()
        except (Question.DoesNotExist, KeyError) as e:
            raise Http404
