from django.contrib import admin

from .models import Notebook, NotebookTab, Note
from django.shortcuts import HttpResponse
from reversion.admin import VersionAdmin
@admin.register(Notebook)
class NotebookAdmin(admin.ModelAdmin):
    pass

@admin.register(NotebookTab)
class NotebookTabAdmin(admin.ModelAdmin):

    response = HttpResponse('blah')
    response.set_cookie('last_notebook', 'notebook_id')

    pass

@admin.register(Note)
class NoteAdmin(VersionAdmin):

    pass

