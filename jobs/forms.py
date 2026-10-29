from django import forms
from .models import Job


class JobForm(forms.ModelForm):

    class Meta:
        model = Job

        fields = [
            'title',
            'company_name',
            'description',
            'location',
            'job_type',
            'salary',
            'skills',
            'experience',
            'deadline',
            'status',
        ]

        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Job title'
                }
            ),

            'company_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Company name'
                }
            ),

            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 5,
                    'placeholder': 'Describe the job'
                }
            ),

            'location': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'e.g. Kochi'
                }
            ),

            'job_type': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            ),

            'salary': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Annual salary',
                    'step': '0.01'
                }
            ),

            'skills': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3,
                    'placeholder': 'Python, Django, HTML, CSS...'
                }
            ),

            'experience': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': '0',
                    'placeholder': 'Experience in years'
                }
            ),

            'deadline': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date'
                }
            ),

            'status': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            ),
        }

    def clean_salary(self):
        salary = self.cleaned_data['salary']

        if salary <= 0:
            raise forms.ValidationError(
                'Salary must be greater than 0.'
            )

        return salary