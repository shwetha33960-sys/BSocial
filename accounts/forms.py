from .models import Profile
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q

User = get_user_model()


class SignUpForm(UserCreationForm):
    full_name = forms.CharField(max_length=120, required=True, label="Full Name")
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("full_name", "username", "email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email and User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["full_name"]
        if commit:
            user.save()
        return user


class SignInForm(forms.Form):
    identifier = forms.CharField(label="Username or Email", max_length=254)
    password = forms.CharField(widget=forms.PasswordInput, label="Password")

    def clean(self):
        cleaned_data = super().clean()
        identifier = cleaned_data.get("identifier")
        password = cleaned_data.get("password")

        if identifier and password:
            user = User.objects.filter(Q(username=identifier) | Q(email__iexact=identifier)).first()
            if user is None:
                raise forms.ValidationError("We could not find an account with that username or email.")
            if not user.check_password(password):
                raise forms.ValidationError("The password you entered is incorrect.")
            cleaned_data["user"] = user
        return cleaned_data


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(label="Email Address")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email and not User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("No account exists with this email.")
        return email
    
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            "profile_picture",
            "bio",
            "location",
            "date_of_birth",
            "gender",
        ]

        widgets = {
            "date_of_birth": forms.DateInput(attrs={"type": "date"}),
        }
