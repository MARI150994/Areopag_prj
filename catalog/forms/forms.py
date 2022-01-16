from django import forms
from django.forms import ModelForm, ModelChoiceField, IntegerField, CharField
from django.forms.widgets import HiddenInput
from catalog.models import Equipment, Init
from django.forms import formset_factory


class EnterNumber(forms.Form):
    number = IntegerField(min_value=1, max_value=30)
    category = CharField(widget=HiddenInput())

class SelectCategory(ModelForm):
    class Meta:
        model = Equipment
        fields = ['category']
        widgets = {
            'category': forms.CheckboxSelectMultiple
        }

class SelectModels(forms.Form):
    #select = forms.ModelChoiceField(queryset=Equipment.objects.get(category='Двигатели асинхронные').init_set.all())
    select = forms.ModelChoiceField(queryset=None, label='')

    def __init__(self, cat, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['select'].queryset = Equipment.objects.get(category=cat).init_set.all()

#class SelectModels(ModelForm):
 #   class Meta:
  #      model = Init
   #     fields = ['model_name']
