from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import (NoteHomepageView, validate_new_note_view, NoteUpdateView, tabbed_view,
                    delete_note_view, upload_image, note_history, note_version)

app_name = 'notes'

urlpatterns = [

    path('', NoteHomepageView.as_view(), name='home'),
    path('tabbed/<int:pk>/', tabbed_view, name='tabbed'),
    path('validate-note-creation/', validate_new_note_view, name='validate_note_creation'),
    path('note/update/<int:notebooktab_id>/<uuid:pk>/', NoteUpdateView.as_view(), name='note_update'),
    path('note/delete/<uuid:pk>/', delete_note_view, name="delete_note"),
    path('view/<uuid:id>/', NoteHomepageView.as_view(), name="id"),
    path('notebook/<int:notebook_id>/', NoteHomepageView.as_view(), name="notebook_id"),
    path('notebook/tab/<int:notebooktab_id>/', NoteHomepageView.as_view(), name="tab"),
    path('notebook/tab/<int:notebooktab_id>/note/<uuid:note_id>', NoteHomepageView.as_view(), name='note'),

    # Revisions / Versioning
    path('api/note/<uuid:note_id>/history/', note_history, name='note_history'),
    path('api/note/version/<int:version_id>/', note_version, name='note_version'),

    # Upload pictures
    path('upload_image/', upload_image),

    # Tinymce editor
    path('tinymce/', include('tinymce.urls')),

    # Search
    path('search/', NoteHomepageView.as_view(), name='search')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
