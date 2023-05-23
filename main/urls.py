from django.urls import path
from .views import *


urlpatterns = [
    path("register", UserCreate.as_view(), name="register"),
    path("", HomePage.as_view(), name="home"),
    path('login', LoginView.as_view(), name='login'),
    path('talk', TalkView.as_view(), name='talk'),
    path('profile/<int:pk>', ProfileView.as_view(), name='profile'),
    path('create_profile', CreateProfile.as_view(), name='create-profile'),
    path('update_profile/<slug:pk>', UpdateProfile.as_view(), name='update-profile'),
    path('otheruser/<slug:pk>', OtherProfile.as_view(), name='person'),
    path('logout', LogoutView.as_view(next_page='login'), name='logout'),
    path('like_talk/<int:pk>', like_or_unlike, name='like_talk'),
    path('search/', SearchView.as_view(), name='search'),
]
