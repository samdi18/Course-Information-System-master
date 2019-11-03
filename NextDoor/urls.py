from django.urls import path
from . import views
from .views import (
    group_list,
    user_group_list,
    group_create,
)



urlpatterns = [
    path('', views.home, name="home"),
    path('about/', views.about, name="about"),
    path('contact/', views.contact, name="contact"),
    path('add_schedule/<int:pk>', views.add_schedule, name="add_schedule"),
    path('edit_schedule/<int:pk>/<int:id>', views.update_schedule, name='edit_schedule'),
    path('delete_schedule/<int:pk>/<int:id>', views.delete_schedule, name='delete_schedule'),
    path('add_announcement/<int:pk>', views.add_announcement, name='add_announcement'),
    path('lectures/', views.lecture_list, name='lecture_list'),
    path('upload_lecture/<int:pk>', views.upload_lecture, name='upload_lecture'),
    path('group_list/',group_list.as_view(), name='group_list'),
    path('user_group_list/',user_group_list.as_view(), name='user_group_list'),
    path('group/<int:pk>/', views.group, name='group'),
    path('update_group/<int:pk>', views.update_group, name='update_group'),
    path('delete_group/<int:pk>', views.delete_group, name='delete_group'),
    path('add_comment/<int:pk>', views.add_comment, name='add_comment'),
    path('comment_remove/<int:pk>/<int:id>', views.comment_remove, name='comment_remove'),
    path('comment_approve/<int:pk>/<int:id>', views.comment_approve, name='comment_approve'),
    path('group_create/', views.group_create, name='group_create'),
    path('group_entered/<int:pk>/', views.enter_pass, name='enter_pass'),
]


