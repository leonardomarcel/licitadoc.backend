from django.contrib import admin

# Register your models here.
from manager_documents.models import Document, Tag

class DocumentAdmin(admin.ModelAdmin):
    fields = ['original_file',  'title', 'description', 'tags']

admin.site.register(Document, DocumentAdmin)
admin.site.register(Tag)