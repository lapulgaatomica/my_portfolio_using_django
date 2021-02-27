from django.contrib import admin
from .models import About, Competency, Reason, Message

admin.site.register(About)
admin.site.register(Competency)
admin.site.register(Reason)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('email', 'date',)
