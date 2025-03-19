from django import forms
from manager_documents.models import Document, Tag

class DocumentForm(forms.ModelForm):
    document = forms.FileField(label="Document")
    title = forms.CharField(label="Title")
    description = forms.CharField(label="Description", widget=forms.Textarea)
    tags = forms.MultipleChoiceField(label="Tags", widget=forms.CheckboxSelectMultiple, required=False)

    def __init__(self, *args, **kwargs):
        super(DocumentForm, self).__init__(*args, **kwargs)
        self.fields['tags'].choices = [(tag.id, tag.name) for tag in Tag.objects.all()]



    class Meta:
        model = Document
        fields = ('document', 'title', 'description', 'tags')