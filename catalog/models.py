from django.db import models

CATEGORY_CHOICES = (
    ('Двигатели асинхронные', 'Двигатели асинхронные'),
    ('Датчики давления', 'Датчики давления'),
    ('Гусары', 'Гусары'),
    ('Расходомеры', 'Расходомеры'),
    ('Кабельные ввода', 'Кабельные ввода'),
    ('Датчики температуры', 'Датчики температуры'),
    ('Задвижки с электроманитным управлением', 'Задвижки с электроманитным управлением'),
)

class Equipment(models.Model):
    """
    This model defining category of equipment e.g:
    Двигатель
    Датчик давления
    Датчик температуры
    ...
    """
    category = models.CharField(max_length=40, choices=CATEGORY_CHOICES, verbose_name='Категории оборудования', default='Двигатели асинхронные')

    def __str__(self):
        return self.category


class Init(models.Model):
    """
    Define a model  of equipment and it's parameters
    """
    category_model = models.ForeignKey(Equipment, on_delete=models.SET_NULL, null=True)
    model_name = models.CharField(max_length=50, help_text="enter correct model name or select from list")
    init_port = models.CharField(max_length=20, help_text="necessary port like: AC1, AC2, DC1")
    additional_port = models.CharField(max_length=30, blank=True, help_text="list of additional ports like: AC1, AC2, DC1")

    def list_of_necessary_ports(self):
        """Return list of necessary port"""
        necessary_port = self.init_port.split(' ')
        return necessary_port

    def list_of_optional_ports(self):
        if self.additional_port:
            return self.additional_port.split(' ')
        else:
            return None

    def __str__(self):
        return self.model_name


class Cable(models.Model):
    natural_name = models.CharField(max_length=50, help_text='real name like "ВВГнг-14х1,5"')
    init_name = models.CharField(max_length=50, help_text='system name for scheme initialization like "VVG_NG_1x1,5"')

    def __str__(self):
        return self.natural_name

