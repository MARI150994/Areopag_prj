from django import forms
from django.forms import ModelForm, ModelChoiceField
from catalog.models import Equipment, Init


class SelectCategory(ModelForm):
    class Meta:
        model = Equipment
        fields = ['category']
        widgets = {
            'category': forms.CheckboxSelectMultiple
        }

class SelectModels(forms.Form):
    select = forms.ModelChoiceField(queryset=Equipment.objects.get(pk=1).init_set.all())
