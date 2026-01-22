from django.urls import path

from . import views

urlpatterns = [
    path('<str:username>/', views.user_detail, name='user-detail'),
    path('user/edit/', views.edit_profile, name='edit_profile'),
    path('user/leave/', views.leave, name='leave'),
]
