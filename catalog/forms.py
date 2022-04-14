from django import forms
from django.forms import ModelForm
from catalog.models import Category, Project, Cable, CATEGORY_CHOICES, Scheme
from django.core.exceptions import ValidationError


class CreateProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['slug', 'description']


class EnterNumberForm(forms.Form):
    count = forms.IntegerField(required=True, label='Введите количество:',
                               widget=forms.NumberInput(attrs={"class": "form-control", "min": 1}))
    category = forms.CharField(widget=forms.HiddenInput())

    def __init__(self, label, category, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['count'].label = label
        self.fields['category'].initial = category


class SelectCategoryForm(forms.Form):
    category = forms.MultipleChoiceField(
        choices=CATEGORY_CHOICES,
        widget=forms.CheckboxSelectMultiple(attrs={"class": "form-check-input"}),
        required=True,
    )


class SelectModelForm(forms.Form):
    model = forms.ModelChoiceField(queryset=None, widget=forms.Select(attrs={"class": "form-select"}))
    symbol = forms.SlugField(label='Обозначение на схеме', widget=forms.TextInput(attrs={"class": "form-control"}))

    def __init__(self, label, cat, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['model'].queryset = Category.objects.get(name=cat).modelname_set.all()
        self.fields['model'].label = label


class ResultForm(ModelForm):
    cable = forms.ModelChoiceField(queryset=Cable.objects.all(), widget=forms.Select(attrs={"class": "form-select"}),
                                   required=True)
    cable_symbol = forms.SlugField(max_length=12, required=True,
                                   widget=forms.TextInput(attrs={"class": "form-control"}))
    connect = forms.SlugField(max_length=12, required=True, widget=forms.TextInput(attrs={"class": "form-control"}))

    class Meta:
        model = Scheme
        fields = ['cable', 'cable_symbol', 'connect']

    def clean(self):
        if self.cleaned_data['cable_symbol'] == self.cleaned_data['connect']:
            raise ValidationError(
                f'Обозначение {self.cleaned_data["cable_symbol"]} кабеля и места подключения совпадают'
            )
        return super().clean()
