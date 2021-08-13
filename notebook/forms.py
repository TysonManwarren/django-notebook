from django import forms
from .fields import GroupedModelChoiceField
from .models import Note, Notebook, NotebookTab


class BaseForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class NoteForm(BaseForm, forms.ModelForm):

    notebooktab = GroupedModelChoiceField(
        queryset=NotebookTab.objects.exclude(notebook=None),
        choices_groupby='notebook'
    )

    class Meta:
        model = Note
        fields = ['notebooktab', 'title', 'description']


# class TagForm(BaseForm, forms.ModelForm):

#     class Meta:
#         model = Tags
#         fields = '__all__'