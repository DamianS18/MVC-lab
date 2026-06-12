from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import TicketEvent


class EmailSignUpForm(UserCreationForm):
    password_help_text = "Od 8 do 32 znakow. Wymagana cyfra oraz mala i wielka litera."

    first_name = forms.CharField(
        label="Imie",
        max_length=150,
        widget=forms.TextInput(attrs={"autocomplete": "given-name"}),
    )
    last_name = forms.CharField(
        label="Nazwisko",
        max_length=150,
        widget=forms.TextInput(attrs={"autocomplete": "family-name"}),
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"autocomplete": "email"}),
    )
    password1 = forms.CharField(
        label="Haslo",
        help_text=password_help_text,
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    )
    password2 = forms.CharField(
        label="Potwierdzenie hasla",
        help_text="Wpisz to samo haslo ponownie.",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    )

    class Meta:
        model = get_user_model()
        fields = ["first_name", "last_name", "email"]

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        user_model = get_user_model()
        if user_model.objects.filter(username=email).exists() or user_model.objects.filter(email=email).exists():
            raise forms.ValidationError("Konto z takim adresem email juz istnieje.")
        return email

    def clean_password1(self):
        password = self.cleaned_data["password1"]
        errors = []
        if len(password) < 8 or len(password) > 32:
            errors.append("Haslo musi miec od 8 do 32 znakow.")
        if not any(char.isdigit() for char in password):
            errors.append("Haslo musi zawierac przynajmniej jedna cyfre.")
        if not any(char.islower() for char in password):
            errors.append("Haslo musi zawierac przynajmniej jedna mala litere.")
        if not any(char.isupper() for char in password):
            errors.append("Haslo musi zawierac przynajmniej jedna wielka litere.")
        if errors:
            raise forms.ValidationError(errors)
        return password

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.username = self.cleaned_data["email"]
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class EmailLoginForm(AuthenticationForm):
    username = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"autocomplete": "email"}),
    )
    password = forms.CharField(
        label="Haslo",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
    )


class TicketEventForm(forms.ModelForm):
    class Meta:
        model = TicketEvent
        fields = [
            "event_name",
            "event_date",
            "location",
            "category",
            "subcategory",
            "description",
            "artists",
            "seats",
        ]
        widgets = {
            "event_date": forms.DateInput(attrs={"type": "date"}),
            "seats": forms.NumberInput(attrs={"min": "0"}),
        }
