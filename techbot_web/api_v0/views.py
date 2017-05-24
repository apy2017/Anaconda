from django.shortcuts import render
from django.conf import settings
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_xml.renderers import XMLRenderer
from django.http import Http404
from django.contrib.auth.models import User
from .serializers import *
from poll_editor.models import Poll, Question, Answer, AnswerContainer


class PollList(generics.ListAPIView):
    def get_serializer_class(self):
        return PollSerializer

    def get_queryset(self):
        try:
            return Poll.objects.filter(owner=self.request.user)

        except (User.DoesNotExist, self.request.user, ValueError) as e:
            raise Http404


class AnswerList(generics.ListAPIView):
    def get_serializer_class(self):
        return AnswerSerializer

    def get_queryset(self):
        try:
            pk = self.kwargs['pk']
            answer_container = AnswerContainer.objects.get(pk=pk)
            return Answer.objects.filter(from_container=answer_container)

        except ValueError as e:
            raise Http404


class AnswerContainerList(generics.ListAPIView):
    def get_serializer_class(self):
        return AnswerContainerSerializer

    def get_queryset(self):
        try:
            polls = Poll.objects.filter(owner=self.request.user)
            answer_containers = AnswerContainer.objects.filter(on_poll__in=polls)
            return answer_containers

        except (User.DoesNotExist, self.request.user, ValueError) as e:
            raise Http404


class AnswerContainerListPoll(generics.ListAPIView):
    def get_serializer_class(self):
        return AnswerContainerSerializer

    def get_queryset(self):
        try:
            poll_code = self.kwargs['code']
            polls = Poll.objects.get(code=poll_code)
            answer_containers = AnswerContainer.objects.filter(on_poll=polls)
            return answer_containers

        except ValueError as e:
            raise Http404


class AnswerContainerListXML(generics.ListAPIView):
    renderer_classes = (XMLRenderer,)
    def get_serializer_class(self):
        return AnswerContainerSerializerXML

    def get_queryset(self):
        try:
            poll_code = self.kwargs['code']
            poll = Poll.objects.get(code=poll_code)
            answer_containers = poll.answercontainer_set.all()
            return answer_containers

        except ValueError as e:
            raise Http404


class AnswerContainerEdit(generics.CreateAPIView):
    def get_serializer_class(self):
        return AnswerContainerSerializer

    def post(self, request, pk):
        try:
            answer_container = AnswerContainer.objects.get(pk=pk)
            polls = Poll.objects.filter(owner=self.request.user)
            answer_containers = AnswerContainer.objects.filter(on_poll__in=polls)
            if answer_container in answer_containers:
                if request.data['action'] == 'edit':
                    pass
                elif request.data['action'] == 'delete':
                    answer_container.delete()
                return Response({'ok': True})
            else:
                raise Http404
        except KeyError as e:
            raise Http404


class PollAdd(generics.CreateAPIView):
    def get_serializer_class(self):
        return PollSerializer

    def post(self, request):
        try:
            poll = Poll(owner=request.user, name=request.data['name'])
            poll.save()
            return Response(PollSerializer(poll).data)
        except KeyError as e:
            raise Http404


class PollEdit(generics.CreateAPIView):
    def get_serializer_class(self):
        return PollSerializer

    def post(self, request, pk):
        try:
            legal_polls = Poll.objects.filter(owner=request.user)
            poll = Poll.objects.get(pk=pk)
            if poll in legal_polls:
                if request.data['action'] == 'edit':
                    poll.name = request.data['name']
                    poll.save()
                elif request.data['action'] == 'delete':
                    poll.delete()
                return Response({'ok': True})
            else:
                raise Http404
        except (Question.DoesNotExist, KeyError) as e:
            raise Http404


@authentication_classes([])
@permission_classes([])
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


@authentication_classes([])
@permission_classes([])
class AnswerAdd(generics.CreateAPIView):
    def get_serializer_class(self):
        return AnswerSerializer

    def post(self, request, pk):
        try:
            question = Question.objects.get(pk=pk)
            answer_container = AnswerContainer.objects.get(pk=int(request.data['answer_container_pk']))
            answer = Answer(from_container=answer_container, on_question=question, caption=request.data['caption'])
            answer.save()
            return Response()
        except (Question.DoesNotExist, KeyError) as e:
            raise Http404


@authentication_classes([])
@permission_classes([])
class AnswerContainerAdd(generics.CreateAPIView):
    def get_serializer_class(self):
        return AnswerContainerSerializer

    def post(self, request):
        telegram_username = request.data[
            'telegram_username'] if 'telegram_username' in request.data else 'AnonymousUser'
        try:
            poll = Poll.objects.get(code=request.data['poll_code'])
            answer_container = AnswerContainer(telegram_username=telegram_username,
                                               on_poll=poll)
            answer_container.save()
            poll.passes += 1
            poll.save()
            return Response(AnswerContainerSerializer(answer_container).data)
        except (Question.DoesNotExist, KeyError) as e:
            raise Http404


class QuestionEdit(generics.CreateAPIView):
    def get_serializer_class(self):
        return QuestionSerializer

    def post(self, request, pk):
        try:
            legal_polls = Poll.objects.filter(owner=request.user)
            question = Question.objects.get(pk=pk)
            if question.from_poll in legal_polls:
                if request.data['action'] == 'edit':
                    print(question.caption)
                    print(request.data['caption'])
                    question.caption = request.data['caption']
                    question.save()
                    print(question.caption)
                elif request.data['action'] == 'delete':
                    question.delete()
                return Response({'ok': True})
            else:
                raise Http404
        except (Question.DoesNotExist, KeyError) as e:
            raise Http404


class QuestionAdd(generics.CreateAPIView):
    def get_serializer_class(self):
        return QuestionSerializer

    def post(self, request, code):
        try:
            legal_polls = Poll.objects.filter(owner=request.user)
            poll = Poll.objects.get(code=code)
            if poll in legal_polls:
                question = Question(from_poll=poll, caption='New question')
                question.save()
                return Response(QuestionSerializer(question).data)
            else:
                raise Http404
        except (Question.DoesNotExist, self.request.user.DoesNotExist, KeyError) as e:
            raise Http404
