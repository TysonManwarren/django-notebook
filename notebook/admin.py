from django.contrib import admin

from django.contrib import admin

from .models import Tags, Notebook, NotebookTab


@admin.register(Tags)
class TagAdmin(admin.ModelAdmin):
    pass

@admin.register(Notebook)
class NotebookAdmin(admin.ModelAdmin):
    pass

@admin.register(NotebookTab)
class NotebookTabAdmin(admin.ModelAdmin):
    pass
