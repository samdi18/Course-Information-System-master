
from django import forms
from django.contrib.auth.models import User
from .models import Schedule, Announcement, Document, Group, Comment


class GroupForm(forms.ModelForm):
    
    class Meta:
        model = Group
        
        fields = ['course_name','course_description']



class ScheduleForm(forms.ModelForm):
    exam = forms.CharField()
    date = forms.DateField(
    widget=forms.TextInput(     
        attrs={'type': 'date'} 
    )
)       
    time = forms.TimeField(
    widget=forms.TextInput(     
        attrs={'type': 'time'} 
    )
)           


    class Meta:
        model = Schedule
        fields = ['exam','date','time']



class AnnouncementForm(forms.ModelForm):
    
    class Meta:
        model = Announcement
        
        fields = ['subject','content']


class DocumentForm(forms.ModelForm):

    class Meta:
        model = Document
        fields = ['title', 'document']


class CommentForm(forms.ModelForm):
    
    class Meta:
        model = Comment
        
        fields = ['body','email']


class Form(forms.ModelForm):
    
    class Meta:
        model = Group

        fields = ['password']