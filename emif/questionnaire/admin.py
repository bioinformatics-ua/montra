#!/usr/bin/python
# vim: set fileencoding=utf-8

from django.contrib import admin
from models import *
from django.utils.safestring import mark_safe

class ChoiceAdmin(admin.ModelAdmin):
    list_display = ['sortid', 'text', 'value', 'question']

class ChoiceInline(admin.TabularInline):
    ordering = ['sortid']
    model = Choice
    extra = 5

def markall_ignoremlt(modeladmin, request, queryset):
    for qset in queryset:
        for question in qset.questions():
            print question
            question.mlt_ignore = True
            question.save()

markall_ignoremlt.short_description = "Mark all questions has ignored from MLT"

def markall_noignoremlt(modeladmin, request, queryset):
    for qset in queryset:
        for question in qset.questions():
            question.mlt_ignore = False
            question.save()

markall_noignoremlt.short_description = "Mark all questions has not ignored from MLT"

class QuestionSetAdmin(admin.ModelAdmin):
    #ordering = ['questionnaire', 'sortid', ]
    list_filter = ['questionnaire', ]
    list_display = ['questionnaire', 'heading', 'sortid', ]
    list_editable = ['sortid', ]
    actions = [markall_ignoremlt, markall_noignoremlt]

class QuestionAdmin(admin.ModelAdmin):
    ordering = ['questionset__questionnaire', 'questionset', 'number']
    inlines = [ChoiceInline]

    def changelist_view(self, request, extra_context=None):
        "Hack to have Questionnaire list accessible for custom changelist template"
        if not extra_context:
            extra_context = {}
        extra_context['questionnaires'] = Questionnaire.objects.all().order_by('name')
        return super(QuestionAdmin, self).changelist_view(request, extra_context)

def clone_questionnaires(modeladmin, request, queryset):
    for query in queryset:
        query.copy()
clone_questionnaires.short_description = "Clone selected questionnaires"

class QuestionnaireAdmin(admin.ModelAdmin):
    actions = [clone_questionnaires]

admin.site.register(Questionnaire, QuestionnaireAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(QuestionSet, QuestionSetAdmin)
