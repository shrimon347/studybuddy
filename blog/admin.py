from django.contrib import admin
from .models import Post, Category, Comment, Like

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('writer', 'title', 'category','content','image','approval_status', 'status','created','modified')
    ordering = ('category',)
    search_fields = ('title', 'category')
    list_editable = ('status',)
    def approval_status(self, obj):
        approved = 'Approved' if obj.status else 'Not Approved'
        return approved

    approval_status.short_description = 'Approval Status'
admin.site.register(Post, PostAdmin)

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title','slug')

class LikeAdmin(admin.ModelAdmin):
    list_display = ('user','post','value')
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user','post','comment','updated','created')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment,CommentAdmin)
admin.site.register(Like,LikeAdmin)