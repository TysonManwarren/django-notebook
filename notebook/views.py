from django.shortcuts import reverse, redirect, get_object_or_404, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, DetailView, CreateView
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages

from django_tables2 import RequestConfig

from .models import Tags, Note, Notebook
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


        return qs_notes, qs_notebooks

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['create_form'] = NoteForm()
        #context['pinned_qs'] = self.object_list.filter(pinned=True)

        #context['qs'] = self.object_list.filter(pinned=False)[:30]
        #context['notebooks'] = self.object_list.filter(pinned=False)[:30]

        context['qs'] = self.object_list[0][:30]
        context['notebooks'] = self.object_list[1][:30]

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
        context['form_title'] = f'Επεξεργασια {self.object.title}'
        return context

    def form_valid(self, form):
        form.save()
        messages.success(self.request, f'Η σημειωση ανανεώθηκε!')
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
    messages.warning(request, 'Διαγραφηκε')
    return redirect(reverse('notes:home'))




