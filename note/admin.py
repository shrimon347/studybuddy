from django.contrib import admin
from .models import Notes, AllSubject,Contact

# Register your models here.

class NoteAdmin(admin.ModelAdmin):
    list_display = ('user','branch', 'subject', 'filetype','downloads','notesfile','approval_status', 'status')
    ordering = ('branch',)
    search_fields = ('subject', 'branch')
    list_editable = ('status',)

    def approval_status(self, obj):
        approved = 'Approved' if obj.status else 'Not Approved'
        return approved

    approval_status.short_description = 'Approval Status'

class AllsubjectAdmin(admin.ModelAdmin):
    list_display = ('name',)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('user','name','notesfile','description','phone')

admin.site.register(Notes, NoteAdmin)
admin.site.register(Contact,ContactAdmin)
admin.site.register(AllSubject,AllsubjectAdmin)