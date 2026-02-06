from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError

from .models import User


class SignupForm(forms.ModelForm):
    password1 = forms.CharField(label="Passwort", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Passwort wiederholen", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("email",)

    def clean_email(self):
        email = (self.cleaned_data.get("email") or "").strip().lower()
        if not email:
            raise ValidationError("Bitte eine E-Mail-Adresse angeben.")
        if User.objects.filter(email=email).exists():
            raise ValidationError("Diese E-Mail-Adresse ist bereits registriert.")
        return email

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get("password1")
        p2 = cleaned.get("password2")
        if p1 and p2 and p1 != p2:
            self.add_error("password2", "Die Passwörter stimmen nicht überein.")
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = user.email.lower()
        user.set_password(self.cleaned_data["password1"])
        # WICHTIG: Admin-Freigabe erforderlich
        user.is_active = False
        if commit:
            user.save()
        return user


class IMTBAuthenticationForm(AuthenticationForm):
    """
    Zeigt eine klare Meldung, wenn ein Konto noch nicht durch Admin freigeschaltet ist.
    Django blockt inaktive User ohnehin; wir geben nur bessere UX.
    """

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise ValidationError(
                "Ihr Konto ist noch nicht freigeschaltet. Bitte warten Sie auf die Admin-Freigabe.",
                code="inactive",
            )
        return super().confirm_login_allowed(user)
