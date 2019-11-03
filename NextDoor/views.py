from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Schedule, Announcement, Document, Group, Comment
from .forms import ScheduleForm, AnnouncementForm, DocumentForm, CommentForm, GroupForm, Form
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django import forms
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.utils.crypto import get_random_string
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)


# Create your views here.


def home(request):
    return render(request, 'NextDoor/index.html')


def about(request):
    return render(request, 'NextDoor/about.html', {'title' : 'About'})


class group_list(ListView):

    model = Group
    template_name = 'NextDoor/group_list.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'group'

class user_group_list(ListView):

    model = Group
    template_name = 'NextDoor/user_group_list.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'group'


def group_create(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.owner = request.user
            group.password = get_random_string(length=6)
            group.save()
            title = form.cleaned_data.get('course_name')
            messages.success(request, f'New Course added for {title} having password {group.password} ')
            return redirect('group_list')
    else:
        form = GroupForm()
    template = 'NextDoor/group_create.html'
    context = {'form': form}
    return render(request, template, context)


def group(request, pk, template='NextDoor/group.html' ):
    group= get_object_or_404(Group, pk=pk)
    schedule = Schedule.objects.filter(group_id=pk)
    announcement = Announcement.objects.filter(group_id=pk).order_by('-created')
    comment = Comment.objects.filter(group_id=pk)
    lecture = Document.objects.filter(group_id=pk)
    context = {
             'title' : group.course_name ,
             'schedule': schedule, 'announcement': announcement,
             'lecture': lecture, 'group': group, 'comment':comment
              }
    return render(request, template, context)

def update_group(request, pk, template='NextDoor/group_create.html'):
    group= get_object_or_404(Group, pk = pk)
    form = GroupForm(request.POST or None, instance=group)
    if form.is_valid():
        group = form.save(commit=False)
        group.save()
        messages.success(request,f' Your group has been updated for {group.course_name}')
    
        return redirect('group', pk= group.id )

    else:
        form = GroupForm(instance=group)

        context = {'form':form,'group':group}   
        return render(request, template, context)

def delete_group(request, pk, template='NextDoor/delete_group.html'):
    group= get_object_or_404(Group, pk = pk)  
    if request.method=='POST':
        group.delete()
        messages.success(request, f'Successfully deleted {group.course_name}')
        return redirect('group_list')
    else: return render(request, template, {'object':group, 'group':group})
    

def contact(request):
    return render(request, 'NextDoor/contact.html', {'title': 'contact'})


def add_schedule(request, pk):
    group = get_object_or_404(Group, pk=pk)
    if request.method == 'POST':
        form = ScheduleForm(request.POST)
        if form.is_valid():
            schedule = form.save(commit=False)
            schedule.group = group
            schedule.save()
            exam = form.cleaned_data.get('exam')
            messages.success(request, f'New Schedule added for {exam}')
            return redirect('group', pk= group.id )
    else:
        form = ScheduleForm()
    template = 'NextDoor/add_schedule.html'
    context = {'form': form,'group':group}
    return render(request, template, context)


def update_schedule(request, pk, id, template='NextDoor/add_schedule.html'):
    schedule= get_object_or_404(Schedule, pk=id)
    group= get_object_or_404(Group, pk = pk)
    form = ScheduleForm(request.POST or None, instance=schedule)
    if form.is_valid():
        schedule = form.save(commit=False)
        schedule.group = group
        schedule.save()
        messages.success(request,f' Your schedule has been updated for {schedule.exam}')
    
        return redirect('group', pk= group.id )

    else:
        form = ScheduleForm(instance=schedule)

        context = {'form':form,'schedule':schedule}   
        return render(request, template, context)


def delete_schedule(request, pk, id, template='NextDoor/delete_schedule.html'):
    schedule= get_object_or_404(Schedule, pk=id)  
    group= get_object_or_404(Group, pk = pk)  
    if request.method=='POST':
        schedule.delete()
        messages.success(request, f'Successfully deleted {schedule.exam}')
        return redirect('group', pk= group.id)
    else: return render(request, template, {'object':schedule, 'group':group})


def add_announcement(request, pk):
    group= get_object_or_404(Group, pk = pk)  
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.group = group
            announcement.save()
            return redirect('group', pk= group.id)
    else:
        form = AnnouncementForm()
    template = 'NextDoor/add_announcement.html'
    context = {'form': form, 'group': group}
    return render(request, template, context)


def lecture_list(request):
    return render(request, 'lecture_list.html')


def upload_lecture(request, pk):
    group= get_object_or_404(Group, pk = pk)  
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            lecture = form.save(commit=False)
            lecture.group = group
            lecture.save()
        
            return redirect('group', pk= group.id)
    else:
        form = DocumentForm()
    return render(request, 'NextDoor/upload_lecture.html', {'form': form})


def add_comment(request, pk):
    group = get_object_or_404(Group, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.group = group
            comment.save()
            messages.success(request, f'New Comment Successfully added!')
            return redirect('group', pk= group.id )
    else:
        form = CommentForm()
    template = 'NextDoor/add_comment.html'
    context = {'form': form,'group':group}
    return render(request, template, context)


@login_required
def comment_approve(request, pk, id):
    comment = get_object_or_404(Comment, pk=id)
    group= get_object_or_404(Group, pk = pk) 
    comment.approve()
    return redirect('group', pk=group.id)


@login_required
def comment_remove(request, pk, id):
    comment = get_object_or_404(Comment, pk=id)
    group= get_object_or_404(Group, pk = pk) 
    comment.delete()
    return redirect('group', pk=group.id)


def enter_pass(request, pk):
    group = get_object_or_404(Group, pk=pk)
    if request.method == 'POST':
        form = Form(request.POST)
        if form.is_valid():
            password = form.cleaned_data.get('password')
            if password == group.password:
                return redirect('group', pk= group.id )
            else: return redirect('enter_pass', pk=group.id)
    else:
        form = Form()
    template = 'NextDoor/enterpass.html'
    context = {'form': form,'group':group}
    return render(request, template, context)
