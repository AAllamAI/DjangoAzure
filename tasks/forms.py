from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "description", "is_completed"]
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "عنوان المهمة",
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "وصف المهمة (اختياري)",
                "rows": 3,
            }),
            "is_completed": forms.CheckboxInput(attrs={
                "class": "form-check-input",
            }),
        }
        labels = {
            "title": "العنوان",
            "description": "الوصف",
            "is_completed": "مكتملة",
        }
