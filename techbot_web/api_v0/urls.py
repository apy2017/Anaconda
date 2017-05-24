from rest_framework.routers import DefaultRouter
from django.conf.urls import url, include
from .views import *

router = DefaultRouter()
# router.register(r'users', UserViewSet)

urlpatterns = [
    url(r'^polls/add/$', PollAdd.as_view()),
    url(r'^polls/(?P<pk>\w+)/edit/$', PollEdit.as_view()),
    url(r'^polls/(?P<code>\w+)/answerContainers/xml',  AnswerContainerListXML.as_view()),
    url(r'^polls/(?P<code>\w+)/answerContainers/$',  AnswerContainerListPoll.as_view()),
    url(r'^polls/(?P<code>\w+)/addQuestion/$', QuestionAdd.as_view()),
    url(r'^polls/(?P<code>\w+)/', QuestionList.as_view()),
    url(r'^polls/', PollList.as_view()),
    url(r'^questions/addAnswerContainer/$', AnswerContainerAdd.as_view()),
    url(r'^questions/(?P<pk>\w+)/edit/$', QuestionEdit.as_view()),
    url(r'^questions/(?P<pk>\w+)/addAnswer/$', AnswerAdd.as_view()),
    url(r'^answerContainers/(?P<pk>\w+)/edit/$', AnswerContainerEdit.as_view()),
    url(r'^answerContainers/(?P<pk>\w+)/$', AnswerList.as_view()),
    url(r'^answerContainers/', AnswerContainerList.as_view()),

]

urlpatterns += router.urls
