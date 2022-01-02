from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from .models import Equipment, Init
from django.shortcuts import get_object_or_404
from .forms.select import SelectCategory


def index(request):
    """
    :param request: 
    :return: home page with all options
    """""
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
            data_1 = []
            for i in range(len(checked)):
                result = get_object_or_404(Equipment, pk=checked[i])
                data_1.append(result)
            data = []
            for j in data_1:
                data.append(j.init_set.all())
            return render(
                request, 'result.html',
                {
                    'data': data,
                }

        return render(
            request,
            'scheme.html',
            context={'list_cat': list_category}
        )
    else:
        form = SelectCategory()
    return render(request, 'category.html', {'form': form})


def result(request):
    return render(
        request, 'result.html',
        {
            'data': data,
        }
    )