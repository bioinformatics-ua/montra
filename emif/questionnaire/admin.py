#!/usr/bin/python
# vim: set fileencoding=utf-8

from django.contrib import admin
from models import *

class ChoiceAdmin(admin.ModelAdmin):
    list_display = ['sortid', 'text', 'value', 'question']

class ChoiceInline(admin.TabularInline):
    ordering = ['sortid']
    model = Choice
    extra = 5

class QuestionSetAdmin(admin.ModelAdmin):
    #ordering = ['questionnaire', 'sortid', ]
    list_filter = ['questionnaire', ]
    list_display = ['questionnaire', 'heading', 'sortid', ]
    list_editable = ['sortid', ]

class QuestionAdmin(admin.ModelAdmin):
    ordering = ['questionset__questionnaire', 'questionset', 'number']
    inlines = [ChoiceInline]

    def changelist_view(self, request, extra_context=None):
        "Hack to have Questionnaire list accessible for custom changelist template"
        if not extra_context:
            extra_context = {}
        extra_context['questionnaires'] = Questionnaire.objects.all().order_by('name')
        return super(QuestionAdmin, self).changelist_view(request, extra_context)

class QuestionnaireAdmin(admin.ModelAdmin):
    pass


admin.site.register(Questionnaire, QuestionnaireAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(QuestionSet, QuestionSetAdmin)
