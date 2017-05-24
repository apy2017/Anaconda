from django.views.generic import TemplateView, CreateView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect


class IndexView(TemplateView):
    template_name = 'index.html'


class LoginView(TemplateView):
    template_name = 'index.html'


class UserCreate(CreateView):
    template_name = 'registration/register.html'
    success_url = "/main/"
    model = User
    form_class = UserCreationForm

    def form_valid(self, form):
        # save the new user first
        form.save()
        # get the username and password
        username = self.request.POST['username']
        password = self.request.POST['password1']
        # authenticate user then login
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return super(UserCreate, self).form_valid(form)

def logout_view(request):
    logout(request)
    return redirect('/main/')




