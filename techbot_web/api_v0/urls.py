from rest_framework.routers import DefaultRouter
from django.conf.urls import url, include
from .views import *


router = DefaultRouter()
#router.register(r'users', UserViewSet)

urlpatterns = [
    url(r'^users/(?P<telegram_id>\w+)/polls', PollList.as_view()),
    url(r'^polls/(?P<code>\w+)/$', QuestionList.as_view()),
    url(r'^questions/(?P<pk>\w+)/addAnswer/$', AnswerAdd.as_view())
]

urlpatterns += router.urls