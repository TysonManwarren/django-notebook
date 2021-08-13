from django.contrib import admin

from .models import Notebook, NotebookTab
from django.shortcuts import HttpResponse
@admin.register(Notebook)
class NotebookAdmin(admin.ModelAdmin):
    pass

@admin.register(NotebookTab)
class NotebookTabAdmin(admin.ModelAdmin):

    response = HttpResponse('blah')
    response.set_cookie('last_notebook', 'notebook_id')

    pass

