from django.contrib import admin
from .models import Category, ModelName, Cable, Project, SelectedModel, Port, Scheme


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'slug', 'description', 'data', 'author')
    search_fields = ('slug', 'author', 'description')
    list_display_links = ('id', 'slug',)


class SchemeAdmin(admin.ModelAdmin):
    list_display = ('id', 'model', 'port', 'cable', 'cable_symbol', 'connect',)
    list_display_links = ('id', 'model',)


admin.site.register(Category)
admin.site.register(ModelName)
admin.site.register(Cable)
admin.site.register(Project, ProjectAdmin)
admin.site.register(SelectedModel)
admin.site.register(Port)
admin.site.register(Scheme, SchemeAdmin)
