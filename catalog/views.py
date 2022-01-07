from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from .models import Equipment, Init
from django.shortcuts import get_object_or_404
from .forms.select import SelectCategory, SelectModels
from django.urls import reverse


def index(request):
    menu = "Составить описание схемы"
    return render(
        request,
        'index.html',
        context={'menu': menu}
    )

def scheme(request):
    if request.method == "POST":
        form = SelectCategory(request.POST)
        if form.is_valid():
            selection = request.POST.getlist('category')
            #data_1 = []
            #for i in range(len(selection)):
            #    result = get_object_or_404(Equipment, pk=checked[i])
            #    data_1.append(result)
            data = selection
            #for j in data_1:
             #   data.append(j.init_set.all())
            return HttpResponseRedirect(reverse('result'))
    else:
        form = SelectCategory()
        return render(request, 'category.html', {'form': form})


def result(request):
        data = request.POST.getlist('category')
        #data = []
        #for i in selection:
        #    data.append(Equipment(pk=i))
        #j = Equipment(pk=1)
        #a = Equipment.objects.get(pk=1)
        #aa = a.init_set.all()
        form_list = []
        for el in data:
            form_list.append(SelectModels(cat=el))
        #form = SelectModels(cat=data[0])
        return render(
            request, 'result.html',
            {
                'data': data,
                'form': form_list
            }
        )
