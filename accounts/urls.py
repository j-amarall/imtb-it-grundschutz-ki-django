from django.urls import path

from .views import IMTBLoginView, logout_view, signup

urlpatterns = [
    path("signup/", signup, name="signup"),
    path("login/", IMTBLoginView.as_view(), name="login"),
    path("logout/", logout_view, name="logout"),
]
