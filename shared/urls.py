from django.urls import path

from shared import views as shared_views

urlpatterns = [
    path('', shared_views.index, name='home'),
]
