from collections import namedtuple
from typing import List

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, View
from django.http import HttpResponseBadRequest
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from .models import Project, SelectedModel, Scheme
from .forms import SelectCategoryForm, SelectModelForm, EnterNumberForm, ResultForm, CreateProjectForm
from .utils import validate_get_request_categories, validate_get_request_counts, generate_file


# home page
def index(request):
    return render(request, 'catalog/index.html')


# user profile and option for it
@login_required()
def user_profile(request):
    user = request.user
    return render(request, 'catalog/user_profile.html', {'user': user})


# create new project and connect to user
class CreateProject(LoginRequiredMixin, CreateView):
    template_name = 'catalog/create_project.html'
    form_class = CreateProjectForm

    def form_valid(self, form):
        new_prj = form.save(commit=False)
        new_prj.author = self.request.user
        new_prj.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('select_category', kwargs={'slug': self.object.slug})


# show users projects
class ProjectsListUser(LoginRequiredMixin, ListView):
    model = Project

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(author=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.request.user.get_username
        return context


# show all projects
class ProjectsListAll(LoginRequiredMixin, ListView):
    model = Project

    # redirect_field_name = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'всех пользователей'
        return context


class ProjectDetail(LoginRequiredMixin, DetailView):
    model = Project
    template = 'catalog/project_detail.html'
    context_object_name = 'prj'
    redirect_field_name = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['result'] = Scheme.objects.filter(model__project=self.object)
        return context


# select category of equipment
@login_required(redirect_field_name=None)
def select_category(request, slug):
    project = get_object_or_404(Project, slug=slug)
    form = SelectCategoryForm()
    return render(request, 'catalog/select_category.html', {'form': form, 'prj': project})


# function create forms to enter number of selected categories, such forms as number of selected categories
@login_required(redirect_field_name=None)
def count_category(request, slug):
    project = get_object_or_404(Project, slug=slug)
    categories = request.GET.getlist('category')
    # check get request and return True if valid
    categories_is_valid = validate_get_request_categories(categories)
    forms = []
    if categories_is_valid:
        for i, cat in enumerate(categories):
            forms.append(EnterNumberForm(label=cat, category=cat))
    else:
        return HttpResponseBadRequest('Данные по указанному запросу не существуют')
    return render(request, 'catalog/count_category.html', {'forms': forms, 'prj': project})


# select concrete name 3d model of equipment (from selected categories and numbers of this categories)
class SelectModel(LoginRequiredMixin, View):
    model = SelectedModel

    # validate request params
    def dispatch(self, request, *args, **kwargs):
        self.slug = kwargs.get('slug')
        self.project = get_object_or_404(Project, slug=self.slug)
        # check categories from request
        self.categories = validate_get_request_categories(request.GET.getlist('category'))
        # check integer number from request
        self.counts = validate_get_request_counts(request.GET.getlist('count'))
        if self.categories and self.counts and len(self.categories) == len(self.counts):
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponseBadRequest('Данные по указанному запросу не существуют')

    # create several form for selection 3d model of equipment
    def get(self, request, *args, **kwargs):
        # prepare list of unbounded forms
        forms = []
        for i, category in enumerate(self.categories):
            for k in range(self.counts[i]):
                # prepare list of empty forms and generate labels for it
                form = SelectModelForm(
                    label=f'{category} № {k + 1}',
                    cat=category,
                    prefix=f'{category} {k}'
                )
                forms.append(form)
        context = {'forms': forms, 'prj': self.project}
        return render(request, 'catalog/select_models.html', context=context)

    def post(self, request, *args, **kwargs):
        # prepare list of bounded forms
        bound_forms = []
        for i, category in enumerate(self.categories):
            for k in range(self.counts[i]):
                bound_forms.append(
                    SelectModelForm(
                        f'{category} № {k + 1}',
                        category,
                        request.POST,
                        prefix=f'{category} {k}'
                    )
                )

        all_form_is_valid = True
        errors = []
        symbols = []
        models = []
        # validate each form and add errors in error (symbols between several forms can't repeat)
        for form in bound_forms:
            if form.is_valid():
                if form.cleaned_data['symbol'] not in symbols:
                    symbols.append(form.cleaned_data['symbol'])
                else:
                    errors.append(form.cleaned_data['symbol'])
                    all_form_is_valid = False
                models.append(form.cleaned_data['model'])
            else:
                all_form_is_valid = False
        if all_form_is_valid:
            # delete old selected models if exist
            if self.project.models.count():
                self.project.models.all().delete()
            # create instances of SelectedModel
            for i in range(len(bound_forms)):
                SelectedModel.objects.create(
                    symbol=symbols[i],
                    model=models[i],
                    project=self.project
                )
            return redirect('create_scheme', slug=self.slug)
        context = {'forms': bound_forms, 'custom_errors': errors, 'prj': self.project}
        return render(request, 'catalog/select_models.html', context=context)


# several forms where user must connect each selected 3d model to some point and selecte cable for it
class CreateScheme(LoginRequiredMixin, View):

    def dispatch(self, request, *args, **kwargs):
        self.slug = kwargs.get('slug')
        self.project = get_object_or_404(Project, slug=self.slug)
        # nmaedtuple more readble
        self.Data = namedtuple('Data', ['form', 'model', 'port'])
        self.data_list: List[Data] = []
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        # prepare list of unbounded forms
        # give all selected models for this project
        for selected_model in self.project.models.all():
            # for each port in selected model create unbounded form
            for port in selected_model.model.ports.all():
                self.data_list.append(
                    self.Data(
                        form=ResultForm(prefix=selected_model.symbol + port.name),
                        model=selected_model,
                        port=port
                    )
                )
        context = {'data_list': self.data_list, 'prj': self.project}
        return render(request, 'catalog/create_scheme.html', context=context)

    def post(self, request, *args, **kwargs):
        # prepare list of bounded forms
        for selected_model in self.project.models.all():
            # if schemes instances already exist delete it all
            if selected_model.schemes.count() > 0:
                selected_model.schemes.all().delete()
            # for each port in selected model create bonded form
            for port in selected_model.model.ports.all():
                self.data_list.append(
                    self.Data(
                        form=ResultForm(request.POST, prefix=selected_model.symbol + port.name),
                        model=selected_model,
                        port=port
                    )
                )

        all_form_is_valid = True
        cables = []
        cables_des = []
        connects = []
        errors = []
        # save data to database only if all forms is valid
        for i, data in enumerate(self.data_list):
            if data.form.is_valid():
                cables.append(data.form.cleaned_data['cable'])
                if data.form.cleaned_data['cable_symbol'] not in cables_des:
                    cables_des.append(data.form.cleaned_data['cable_symbol'])
                else:
                    errors.append(data.form.cleaned_data['cable_symbol'])
                    all_form_is_valid = False
                if data.form.cleaned_data['connect'] not in connects:
                    connects.append(data.form.cleaned_data['connect'])
                else:
                    errors.append(data.form.cleaned_data['connect'])
                    all_form_is_valid = False
            else:
                all_form_is_valid = False

        # only if all form is valid create new instances in database
        if all_form_is_valid:
            for i, data in enumerate(self.data_list):
                Scheme.objects.create(
                    model=data.model,
                    port=data.port,
                    cable=cables[i],
                    cable_symbol=cables_des[i],
                    connect=connects[i]
                )
            # generate file contained all this data and bound file with current Project
            generate_file(self.project)
            return redirect('project_detail', slug=self.slug)
        context = {'data_list': self.data_list, 'custom_errors': errors, 'prj': self.project}
        return render(request, 'catalog/create_scheme.html', context=context)
