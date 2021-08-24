import os

from rest_framework.decorators import api_view
from rest_framework.response import Response
from reversion.models import Version
from django.db.models import F

from django.shortcuts import reverse, redirect, get_object_or_404, HttpResponseRedirect, render
from django.urls import reverse_lazy
from django.conf import settings
from django.http import JsonResponse
from django.utils import timezone
from django.views.generic import ListView, UpdateView, DetailView, CreateView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages

from django_tables2 import RequestConfig

from .models import Tags, Note, Notebook, NotebookTab
from .forms import NoteForm
from history.signals import object_viewed_signal
#from .tables import TagsTable


#@method_decorator(staff_member_required, name='dispatch')
class NoteHomepageView(ListView):

    template_name = 'notes/homepage.html'
    model = Note

    def get_queryset(self):

        qs_notes = Note.objects.all()

        note_id = ''

        if 'id' in self.kwargs:
            id = self.kwargs['id']
            qs_notes = [Note.objects.all().filter(id=id)]
            if self.request.user.is_authenticated and self.get_object() is not None:
                object_viewed_signal.send(self.get_object().__class__, instance=self.get_object(), request=self.request)

        elif 'notebook_id' in self.kwargs:
            notebook_id = self.kwargs['notebook_id']
            qs_notes = [Note.objects.all().filter(id=notebook_id)]

        elif 'notebooktab_id' in self.kwargs:

            # We are on a tab, find out which one here
            notebooktab_id = self.kwargs['notebooktab_id']

            # Get all the notes for the tab
            qs_notes = Note.objects.all().filter(notebooktab_id=notebooktab_id)

            # Are we viewing a specific note?
            if 'note_id' in self.kwargs:
                note_id = self.kwargs['note_id']

                the_note_object =  Note.objects.all().filter(id=note_id)[0]

                if self.request.user.is_authenticated and the_note_object is not None:
                    object_viewed_signal.send(the_note_object.__class__, instance=the_note_object, request=self.request)

            else:

                # Get the note id of the first note
                if len(qs_notes) > 0:
                    note_id = qs_notes[0].id

        else:
            qs_notes = Note.filters_data(self.request, qs_notes)
            qs_notes = []

        qs_notebooks = Notebook.objects.all()

        qs_notebooks_and_tabs = Notebook.objects.all().select_related()

        return qs_notes, qs_notebooks, qs_notebooks_and_tabs, note_id

    def get_context_data(self,**kwargs):

        context = super().get_context_data(**kwargs)

        notebooktab_id = ''
        if 'notebooktab_id' in self.kwargs:
            notebooktab_id = self.kwargs['notebooktab_id']
            context['notebooktab_id'] = notebooktab_id

        context['create_form'] = NoteForm(initial ={'notebooktab': notebooktab_id})

        context['qs'] = self.object_list[0][:30]
        context['notebooks'] = self.object_list[1][:30]
        context['notebooks_and_tabs'] = self.object_list[2][:30]

        context['note_id'] = self.object_list[3]

        context['action_url'] = '/search/'
        context['q'] = self.request.GET.get('q', None)

        if self.request.path == '/search/':
            qs1 = Note.objects.all().filter(title__icontains=context['q'])
            qs2 = Note.objects.all().filter(description__icontains=context['q'])
            context['qs'] = qs1 | qs2

        return context



#@staff_member_required
def validate_new_note_view(request):
    form = NoteForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'New note added')
    return redirect(reverse('notes:note', args=[form.instance.notebooktab_id, form.instance.id]))


#@method_decorator(staff_member_required, name='dispatch')
class NoteUpdateView(UpdateView):

    form_class = NoteForm

    template_name = 'notes/form.html'
    model = Note

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse_lazy('notes:note', args=[self.object.notebooktab_id, self.object.id])
        context['form_title'] = f'[ MODIFYING ] {self.object.title}'
        return context

    def form_valid(self, form):
        self.success_url = reverse_lazy('notes:note', args=[self.object.notebooktab_id, self.object.id])
        form.save()
        messages.success(self.request, f'The note has been updated')
        return super().form_valid(form)


#@staff_member_required
def tabbed_view(request, pk):
    # instance = get_object_or_404(Note, id=pk)
    # instance.pinned = False if instance.pinned else True
    # instance.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'), reverse('notes:home'))

#@staff_member_required
def tab(request, pk):
    # instance = get_object_or_404(Note, id=pk)
    # instance.pinned = False if instance.pinned else True
    # instance.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'), reverse('notes:home'))

#@staff_member_required
def delete_note_view(request, pk):
    instance = get_object_or_404(Note, id=pk)
    instance.delete()
    messages.warning(request, 'Deleted')
    return redirect(reverse('notes:home'))


@csrf_exempt
def upload_image(request):
    if request.method == "POST":
        file_obj = request.FILES['file']
        file_name_suffix = file_obj.name.split(".")[-1]
        if file_name_suffix not in ["jpg", "png", "gif", "jpeg", ]:
            return JsonResponse({"message": "Wrong file format"})

        upload_time = timezone.now()
        path = os.path.join(
            settings.MEDIA_ROOT,
            'tinymce',
            str(upload_time.year),
            str(upload_time.month),
            str(upload_time.day)
        )
        # If there is no such path, create
        if not os.path.exists(path):
            os.makedirs(path)

        file_path = os.path.join(path, file_obj.name)

        file_url = f'{settings.MEDIA_URL}tinymce/{upload_time.year}/{upload_time.month}/{upload_time.day}/{file_obj.name}'

        if os.path.exists(file_path):
            return JsonResponse({
                "message": "file already exist",
                'location': file_url
            })

        with open(file_path, 'wb+') as f:
            for chunk in file_obj.chunks():
                f.write(chunk)

        return JsonResponse({
            'message': 'Image uploaded successfully',
            'location': file_url
        })
    return JsonResponse({'detail': "Wrong request"})


@api_view()
def note_history(request, note_id):
    note = Note.objects.get(id=note_id)
    versions = Version.objects.get_for_object(note)

    data = versions.values('pk',
                           date_created=F('revision__date_created'),
                           user=F('revision__user__username'),
                           comment=F('revision__comment'))

    return Response({"data": data})

@api_view()
def note_version(request, version_id):
    v = Version.objects.get(id=version_id)
    return Response({"data": v.field_dict})