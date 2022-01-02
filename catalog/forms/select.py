from django import forms
from catalog.models import Equipment, CATEGORY_CHOICES


class SelectCategory(forms.Form):
    category = forms.MultipleChoiceField(choices=CATEGORY_CHOICES,
                                         widget=forms.CheckboxSelectMultiple,
                                         label="Выберите категории используемого оборудования")
