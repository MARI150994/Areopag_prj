from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from .models import Equipment, Init
from django.shortcuts import get_object_or_404
from .forms.forms import SelectCategory, SelectModels, EnterNumber
from django.urls import reverse


def index(request):
    menu = "Составить описание схемы"
    return render(
        request,
        'index.html',
        context={'menu': menu}
    )


def choice_category(request):
    # choice category
    if request.method == "POST":
        form = SelectCategory(request.POST)
        if form.is_valid():
            return HttpResponseRedirect(reverse('enter_number'))
    else:
        form = SelectCategory()
    return render(request, 'choice_category.html', {'form': form})


def enter_number(request):
    # enter number equipment of choisen category
    data = request.POST.getlist('category')
    forms = []
    if request.method == 'POST':
        # add to list of forms new instance of form EnterNumber and set label equal name of selected category before
        # put data of category into hidden input form to pass it into result view
        for el in data:
            forms.append(EnterNumber())
            forms[-1].fields['number'].label = f'{el}'
            forms[-1].fields['category'].initial = f'{el}'
    else:
        form = EnterNumber()
    return render(request, 'enter_number.html', {'form': forms, 'data': data})


def select_models(request):
    # take a list of select category from enter_number func
    # data = enter_number.data
    data = request.POST.getlist('category')
    # take a list of number of category from form
    number_models = request.POST.getlist('number')
    if request.method == 'POST':
        form_list = []
        for el in range(len(number_models)):
            for i in range(int(number_models[el])):
                form_list.append(SelectModels(cat=data[el]))
        return render(
            request, 'result.html',
            {
                'data': number_models,
                'data_cat': data,
                'form': form_list,
            }
        )
    else:
        return render(request, 'result.html', {'data': data, 'data_test': data_test})


def final(request):
    models_id = request.POST.getlist('select')
    forms = []
    for f in models_id:
        forms.append(Init.objects.get(pk=f))
    ports_of_models = {}
    for model in models_id:
        model_obj = Init.objects.get(pk=model)
        model_ports = model_obj.list_of_necessary_ports()
        model_name = model_obj.model_name
        ports_of_models.update({model_name: model_ports})
    return render(request, 'final.html', {'data': models_id, 'ports': ports_of_models, 'forms': forms})
