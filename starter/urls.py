from . import views
from django.urls import path
from .views import *

urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', FileUploadView.as_view()),
]
