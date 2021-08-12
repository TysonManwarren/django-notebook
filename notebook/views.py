import os

from django.shortcuts import reverse, redirect, get_object_or_404, HttpResponseRedirect
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
from .forms import NoteForm, TagForm
from .tables import TagsTable


@method_decorator(staff_member_required, name='dispatch')
class NoteHomepageView(ListView):
    template_name = 'notes/homepage.html'
    #model = Note

    def get_queryset(self):

        qs_notes = Note.objects.all()
        qs_notes = Note.filters_data(self.request, qs_notes)

        qs_notebooks = Notebook.objects.all()

        qs_notebooks_and_tabs = Notebook.objects.all().select_related()

        return qs_notes, qs_notebooks, qs_notebooks_and_tabs

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['create_form'] = NoteForm()
        #context['pinned_qs'] = self.object_list.filter(pinned=True)

        #context['qs'] = self.object_list.filter(pinned=False)[:30]
        #context['notebooks'] = self.object_list.filter(pinned=False)[:30]

        context['qs'] = self.object_list[0][:30]
        context['notebooks'] = self.object_list[1][:30]
        context['notebooks_and_tabs'] = self.object_list[2][:30]

        return context



@staff_member_required
def validate_new_note_view(request):
    form = NoteForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'New message added')
    return redirect(reverse('notes:home'))


@method_decorator(staff_member_required, name='dispatch')
class NoteUpdateView(UpdateView):
    form_class = NoteForm
    success_url = reverse_lazy('notes:home')
    template_name = 'notes/form.html'
    model = Note

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = self.success_url
        context['form_title'] = f'EDIT {self.object.title}'
        return context

    def form_valid(self, form):
        form.save()
        messages.success(self.request, f'The note has been updated')
        return super().form_valid(form)


@staff_member_required
def pinned_view(request, pk):
    instance = get_object_or_404(Note, id=pk)
    instance.pinned = False if instance.pinned else True
    instance.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'), reverse('notes:home'))


@staff_member_required
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

