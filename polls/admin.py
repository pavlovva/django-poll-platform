from django.contrib import admin
from .models import Poll, Question, AnswerOption, QuestionCondition, UserResponse


class AnswerOptionInline(admin.TabularInline):
    model = AnswerOption
    extra = 0


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 0


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created_at']
    list_filter = ['created_at', 'author']
    search_fields = ['title']
    inlines = [QuestionInline]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['text', 'poll', 'order']
    list_filter = ['poll']
    search_fields = ['text']
    inlines = [AnswerOptionInline]


@admin.register(AnswerOption)
class AnswerOptionAdmin(admin.ModelAdmin):
    list_display = ['text', 'question', 'order']
    list_filter = ['question__poll']


@admin.register(QuestionCondition)
class QuestionConditionAdmin(admin.ModelAdmin):
    list_display = ['question', 'depends_on_question', 'required_answer']


@admin.register(UserResponse)
class UserResponseAdmin(admin.ModelAdmin):
    list_display = ['user', 'poll', 'question', 'answer', 'created_at']
    list_filter = ['poll', 'created_at']
    search_fields = ['user__username']
