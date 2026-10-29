from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class RegisterForm(UserCreationForm):

    email = forms.EmailField(
        required=True
    )

    role = forms.ChoiceField(
        choices=[
            ('seeker', 'Job Seeker'),
            ('employer', 'Employer'),
        ],
        widget=forms.RadioSelect
    )

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'role',
            'password1',
            'password2',
        ]

    def save(self, commit=True):
        user = super().save(commit=False)

        role = self.cleaned_data['role']

        if role == 'employer':
            user.is_employer = True
            user.is_seeker = False

        else:
            user.is_employer = False
            user.is_seeker = True

        if commit:
            user.save()

        return user