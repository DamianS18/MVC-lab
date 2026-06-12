from django.contrib.auth import views as auth_views
from django.urls import path

from . import views
from .forms import EmailLoginForm

app_name = "tasks"

urlpatterns = [
    path("", views.HomeView.as_view(), name="index"),
    path(
        "accounts/login/",
        auth_views.LoginView.as_view(
            authentication_form=EmailLoginForm,
            template_name="tasks/login.html",
        ),
        name="login",
    ),
    path("accounts/logout/", auth_views.LogoutView.as_view(next_page="tasks:index"), name="logout"),
    path("accounts/signup/", views.SignUpView.as_view(), name="signup"),
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("categories/<slug:category_slug>/", views.CategoryView.as_view(), name="category"),
    path("events/", views.EventListView.as_view(), name="list"),
    path("events/add/", views.EventCreateView.as_view(), name="add"),
    path("events/<int:pk>/", views.EventDetailView.as_view(), name="detail"),
    path("events/<int:pk>/reserve/", views.reserve_event, name="reserve"),
    path("events/<int:pk>/edit/", views.EventUpdateView.as_view(), name="edit"),
]
