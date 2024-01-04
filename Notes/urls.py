from . import views
from django.urls import path

urlpatterns = [
    path('notes/create-note', views.create_note, name='create-note')
]