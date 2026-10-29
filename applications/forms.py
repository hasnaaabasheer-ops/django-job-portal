from django import forms

from .models import Application


class ApplicationForm(forms.ModelForm):

    class Meta:

        model = Application

        fields = [
            'resume',
            'cover_letter',
        ]

        widgets = {

            'resume': forms.ClearableFileInput(
                attrs={
                    'class': 'form-control',
                    'accept': '.pdf,.docx'
                }
            ),

            'cover_letter': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 8,
                    'placeholder': 'Write your cover letter...'
                }
            ),
        }

    def clean_resume(self):

        resume = self.cleaned_data.get('resume')

        if not resume:
            raise forms.ValidationError(
                'Please upload your resume.'
            )

        allowed_extensions = [
            '.pdf',
            '.docx',
        ]

        file_name = resume.name.lower()

        if not any(
            file_name.endswith(ext)
            for ext in allowed_extensions
        ):
            raise forms.ValidationError(
                'Only PDF and DOCX files are allowed.'
            )

        return resume