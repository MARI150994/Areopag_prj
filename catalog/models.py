from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.auth.models import User

CATEGORY_CHOICES = (
    ('Двигатели', 'Двигатели асинхронные'),
    ('Давление', 'Датчики давления'),
    ('Гусары', 'Гусары'),
    ('Расходомеры', 'Расходомеры'),
    ('Температура', 'Датчики температуры'),
    ('Задвижки', 'Задвижки с электроманитным управлением')
)


class Category(models.Model):
    name = models.CharField(max_length=40, choices=CATEGORY_CHOICES, verbose_name='Выберите категории оборудования',
                            default='Двигатели', unique=True)

    def __str__(self):
        return self.name


class ModelName(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=50, help_text="enter correct model name or select from list", unique=True)
    ports = models.ManyToManyField('Port')

    def __str__(self):
        return self.name


class Port(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return f'{self.name}'


class Cable(models.Model):
    COLOR_CHOICES = (
        ('MAGENTA', 'Розовый'),
        ('GREEN', 'Зеленый'),
        ('BLACK', 'Черный'),
        ('RED', 'Красный'),
        ('YELLOW', 'Желтый'),
        ('BLUE', 'Синий')
    )
    name = models.CharField("название", max_length=50, help_text='real name like "ВВГнг-14х1,5"', unique=True)
    code = models.CharField("код для сборки", max_length=50,
                            help_text='system name for scheme initialization like "VVG_NG_1x1,5"', unique=True)
    min_bend_radius = models.PositiveSmallIntegerField("радиус изгиба", default=0)
    thickness = models.FloatField("толщина кабеля в миллиметрах", default=0)
    color = models.CharField("цвет изображения", choices=COLOR_CHOICES, max_length=40, default="RED")

    def __str__(self):
        return self.name


class Project(models.Model):
    slug = models.SlugField(max_length=12, help_text='введите номер проекта, например: "423-18v1"', unique=True,
                            verbose_name="номер проекта")
    description = models.CharField(max_length=50, help_text='опишите проект, например: "Газпром, Салават нефтехим"',
                                   unique=True, verbose_name="описание проекта")
    data = models.DateTimeField(auto_now=True, verbose_name="дата")
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True, verbose_name="автор")
    file = models.FileField(upload_to='files/', null=True, blank=True)

    class Meta:
        ordering = ['-data']

    def get_absolute_url(self):
        return reverse('project_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return f"Project: {self.slug}"


class SelectedModel(models.Model):
    model = models.ForeignKey(ModelName, on_delete=models.CASCADE)
    symbol = models.CharField('Обозначение на схеме', max_length=30, null=True)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, related_name='models')

    def __str__(self):
        return f'Проект {self.project}, модель {self.model}, обозначение {self.symbol}'


class Scheme(models.Model):
    model = models.ForeignKey(SelectedModel, on_delete=models.CASCADE, null=True, related_name='schemes')
    port = models.ForeignKey(Port, on_delete=models.CASCADE, null=True)
    cable = models.ForeignKey(Cable, on_delete=models.SET_NULL, null=True)
    cable_symbol = models.SlugField(max_length=12, null=True)
    connect = models.SlugField(max_length=12, null=True)

    class Meta:
        unique_together = ['cable_symbol', 'connect']

    def get_absolute_url(self):
        return reverse('scheme_item_edit', kwargs={'slug': self.model.project.slug, 'pk': self.pk})
