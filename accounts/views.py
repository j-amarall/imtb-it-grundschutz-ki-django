from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from .forms import IMTBAuthenticationForm, SignupForm


class IMTBLoginView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = IMTBAuthenticationForm


def signup(request):
    if request.user.is_authenticated:
        return redirect("/")

    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Vielen Dank für Ihre Registrierung. Ihr Konto wurde angelegt und muss noch durch einen Admin freigeschaltet werden.",
            )
            return redirect("/accounts/login/")
    else:
        form = SignupForm()

    return render(request, "accounts/signup.html", {"form": form})


@require_POST
def logout_view(request):
    logout(request)
    return redirect("/")
