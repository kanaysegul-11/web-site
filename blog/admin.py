from django.contrib import admin
from .models import Post, Comment, ReadabilityInfo, Vote, Category, Tag, CommentReply
@admin.register(Post)

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'category', 'is_featured')
    list_filter = ('category', 'tags', 'is_featured')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}

class CommentReplyInline(admin.TabularInline):
    model = CommentReply
    extra = 1

class CommentAdmin(admin.ModelAdmin):
    inlines = [CommentReplyInline]

admin.site.register(Comment,CommentAdmin)
admin.site.register(CommentReply)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(ReadabilityInfo)
admin.site.register(Vote)
