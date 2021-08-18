from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import (NoteHomepageView, validate_new_note_view, NoteUpdateView, tabbed_view, delete_note_view, upload_image)

app_name = 'notes'

urlpatterns = [
    path('', NoteHomepageView.as_view(), name='home'),
    path('tabbed/<int:pk>/', tabbed_view, name='tabbed'),
    path('validate-note-creation/', validate_new_note_view, name='validate_note_creation'),
    path('note/update/<int:pk>/', NoteUpdateView.as_view(), name='note_update'),
    path('note/delete/<int:pk>/', delete_note_view, name="delete_note"),

    path('view/<int:id>/', NoteHomepageView.as_view(), name="id"),
    path('notebook/<int:notebook_id>/', NoteHomepageView.as_view(), name="notebook_id"),
    path('notebook/tab/<int:notebooktab_id>/', NoteHomepageView.as_view(), name="tab"),
    path('notebook/tab/<int:notebooktab_id>/note/<int:note_id>', NoteHomepageView.as_view(), name="note"),

    # Upload pictures
    path('upload_image/', upload_image),
    # Tinymce editor
    path('tinymce/', include('tinymce.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
