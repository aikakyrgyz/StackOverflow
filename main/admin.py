from django.contrib import admin
from .models import CodeImage, Problem, Comment, Reply
# Register your models here.

class ProblemImageInline(admin.TabularInline):
    model = CodeImage
    max_num = 5
    min_num = 1

@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    inlines = [ProblemImageInline, ]

class CommentInline(admin.TabularInline):
    model = Comment

@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    inlines = [CommentInline, ]