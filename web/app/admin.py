from django.contrib import admin
from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import Location, Message, JournalArticle

class JournalArticleAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = JournalArticle
        fields = '__all__'

class JournalArticleAdmin(admin.ModelAdmin):
    form = JournalArticleAdminForm

admin.site.register(Location)
admin.site.register(Message)
admin.site.register(JournalArticle, JournalArticleAdmin)
