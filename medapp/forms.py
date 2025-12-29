from django import forms

from .models import Patient, PatientFile


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ["name", "age", "gender", "medical_history", "assigned_to"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "input-field", "placeholder": "Full name"}),
            "age": forms.NumberInput(attrs={"class": "input-field", "min": 0}),
            "gender": forms.Select(attrs={"class": "input-field"}),
            "medical_history": forms.Textarea(
                attrs={
                    "class": "input-field",
                    "rows": 4,
                    "placeholder": "Add relevant medical notes",
                }
            ),
            "assigned_to": forms.SelectMultiple(attrs={"class": "input-field"}),
        }
        help_texts = {
            "assigned_to": "Select one or more team members responsible for this patient.",
        }


class PatientFileForm(forms.ModelForm):
    class Meta:
        model = PatientFile
        fields = ["file"]
        widgets = {
            "file": forms.FileInput(attrs={"class": "input-field"}),
        }



