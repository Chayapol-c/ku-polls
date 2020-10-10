"""Config for Django admin page."""
from django.contrib import admin

from .models import Question, Choice


class ChoiceInline(admin.StackedInline):
    """Choice object config in Django admin page."""

    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    """Question object config in Django admin page."""

    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date information', {'fields': [
         'pub_date', 'end_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date',
                    'end_date', 'was_published_recently')
    list_filter = ['pub_date', 'end_date']
    search_fields = ['question_text']


admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
