from django.urls import path
from .import views


urlpatterns = [

    path('',views.note, name='note'),
    path('upload_notes/', views.upload_notes, name="upload_notes"),
    path('my_notes/', views.my_notes, name="my_notes"),
    path('contact/', views.contact, name="contact"),
    path('delete_mynotes/<int:pid>',views.delete_mynotes,name="delete_mynotes"),
    path('allsubjects/', views.AllSubjectPage, name="subjects"),
   path('notes/<int:note_id>/download/', views.download_note, name='download_note'),
]