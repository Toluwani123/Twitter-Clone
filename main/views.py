from typing import Any, Dict
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.views.generic import *
from .forms import *
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Q

# Create your views here.


class UserCreate(CreateView):
    form_class = UserCreate
    template_name = "talks/registration.html"
    context_object_name = "register"

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password1"]
        first_name = form.cleaned_data["first_name"]
        last_name = form.cleaned_data["last_name"]
        email = form.cleaned_data["email"]

        user = authenticate(username=username, password=password)
        login(self.request, user)

        return redirect("create-profile")

        return super().form_valid(form)


class HomePage(LoginRequiredMixin, ListView):
    model = Talks
    template_name = "talks/home_page.html"
    context_object_name = "register"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
    







class LoginView(LoginView):
    template_name = 'talks/login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    context_object_name = "login"

    def get_success_url(self):
        return reverse_lazy('home')
    
class TalkView(LoginRequiredMixin, CreateView):
    form_class = TalkForm
    template_name = 'talks/talk.html'
    context_object_name = 'create_talk'
    
    def form_valid(self, form):
        talk = form.save(commit=False)
        talk.user = self.request.user
        talk.save()
        return redirect('home')

class ProfileView(LoginRequiredMixin, ListView):

    context_object_name = "profile"
    template_name = 'talks/profile.html'
    def get_queryset(self):
        pk = self.kwargs.get('pk')  # Retrieve the 'pk' parameter from the URL
        return Person.objects.get(user_id=pk)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        person = Person.objects.get(user=user)
        talks = Talks.objects.filter(user=user)
        context['person'] = person
        context['talks'] = talks
        return context
    
        


    
    
class CreateProfile(LoginRequiredMixin, CreateView):
    model = Person
    fields = ['bio', 'profile_picture']
    success_url = reverse_lazy('home')
    template_name = 'talks/createprofile.html'
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CreateProfile, self).form_valid(form)
    
class UpdateProfile(LoginRequiredMixin, UpdateView):
    model = Person
    fields = ['bio', 'profile_picture']
    template_name = 'talks/updateprofile.html'
   
    success_url = reverse_lazy('home')

class OtherProfile(DetailView):
    model = Person
    template_name  = 'talks/otheruser.html'
    context_object_name = 'prof'
    pk_url_kwarg = 'pk'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        talks = Talks.objects.filter(user=pk)
        context['talks'] = talks
        user = self.request.user
        person = Person.objects.get(user=user)
        context['person'] = person
        return context
    
    def post(self, request, pk):
        pk = self.kwargs.get('pk')
        user = self.request.user
        profile = Person.objects.get(user=pk)
        mine = Person.objects.get(user=user)
        action = request.POST['follow']
        if action == 'unfollow':
            mine.followers.remove(profile)
        elif action == 'follow':
            mine.followers.add(profile)
        mine.save()
        return redirect('home')

        
def like_or_unlike(request, pk):
	if request.user.is_authenticated:
		talk = get_object_or_404(Talks, id=pk)
		if talk.likes.filter(id=request.user.id):
			talk.likes.remove(request.user)
		else:
			talk.likes.add(request.user)
		
		return redirect('home')




	else:
		return redirect('register')

class SearchView(ListView):
    model = Talks
    template_name = 'talks/search.html'
    context_object_name = 'search_results'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Talks.objects.filter(Q(body__icontains=query))
        return Talks.objects.none()
    
