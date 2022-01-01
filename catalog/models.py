from django.db import models


class Equipment(models.Model):
    """
    This model defining category of equipment e.g:
    Двигатель
    Датчик давления
    Датчик температуры
    ...
    """
    category = models.CharField(max_length=30)

    def __str__(self):
        return self.category


class Init(models.Model):
    """
    Define a specific type of equipment and it's parameters
    """
    category_model = models.ForeignKey(Equipment, on_delete=models.SET_NULL, null=True)
    model_name = models.CharField(max_length=50, help_text="enter correct model name or select from list")
    init_port = models.CharField(max_length=20, help_text="list of necessary ports like: AC1, AC2, DC1")
    additional_port = models.CharField(max_length=30, blank=True, help_text="list of additional ports like: AC1, AC2, DC1")

    def __str__(self):
        return self.model_name
