from django.contrib import admin
from .models import Schedule, Announcement, Document, Group, Comment

# Register your models here.

admin.site.register(Schedule),
admin.site.register(Announcement),
admin.site.register(Document),
admin.site.register(Group),
admin.site.register(Comment),

