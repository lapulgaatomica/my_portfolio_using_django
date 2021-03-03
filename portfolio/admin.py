from django.contrib import admin
from .models import About, Competency, Reason, Message, PastWork

admin.site.register(About)
admin.site.register(Competency)
admin.site.register(Reason)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('email', 'date',)


@admin.register(PastWork)
class PastWorkAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_added', 'date_modified')
