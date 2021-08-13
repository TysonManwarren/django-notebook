from django.contrib import admin

from django.contrib import admin

from .models import Notebook, NotebookTab

@admin.register(Notebook)
class NotebookAdmin(admin.ModelAdmin):
    pass

@admin.register(NotebookTab)
class NotebookTabAdmin(admin.ModelAdmin):
    pass
