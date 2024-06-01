from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from .models import Message, Room, Topic, User
from .forms import MyUserCreationForm

# Register your models here.
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'email','is_staff','bio','avatar')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('name','email','bio','avatar',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username','email','name','bio','avatar', 'password1', 'password2', ),
        }),
    )

    search_fields = ('username', 'email')
    ordering = ('username','email')


class CustomRoom(admin.ModelAdmin):
    model = Room
    list_display = ('host','topic','name','description','created','updated')
    search_fields = ('host', 'topic','name')
    ordering = ('host','name', 'topic')

class CustomMessage(admin.ModelAdmin):
    model = Message
    list_display = ('user','room','body','created','updated')
    search_fields = ('user','room')
    ordering = ('user', 'room')

admin.site.register(User, CustomUserAdmin)
admin.site.register(Room, CustomRoom)
admin.site.register(Topic)
admin.site.register(Message,CustomMessage)
