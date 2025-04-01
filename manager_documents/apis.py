from django.shortcuts import render
from .models import Document
from .forms import DocumentForm
from django.http import JsonResponse
from django.shortcuts import redirect
from rest_framework.decorators import api_view
from rest_framework import serializers
from rest_framework.response import Response
from django.http import HttpResponse, FileResponse
import mimetypes
import os
import docx2pdf
from django.conf import settings
import shutil
import pythoncom

# Create your views here.

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'


def add_document(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('list_documents')
    else:
        form = DocumentForm()
    return render(request, 'add_document.html', {'form': form})

@api_view(['GET'])
def list_documents(request):
    documents = Document.objects.all()
    serializer = DocumentSerializer(documents, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def download_document(request, pk):
    document = Document.objects.get(pk=pk)
    file_path = document.original_file.path
    file_name = document.document.name
    if not os.path.exists(file_path):
        return JsonResponse({'status': 'error', 'message': 'File not found'})
    return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=file_name)

@api_view(['GET'])
def view_document(request, pk):
    pythoncom.CoInitialize()  # Inicializa o COM
    document = Document.objects.get(pk=pk)
    file_path = os.path.join(settings.MEDIA_ROOT, document.original_file.path)
    file_name = document.original_file.name
    if not os.path.exists(file_path):
        return JsonResponse({'status': 'error', 'message': 'File not found'})
    if  (file_name.endswith('.docx') or file_name.endswith('.doc')) and not document.pdf_file_version:
        # Converte o arquivo para PDF
        new_pdf_file_path = os.path.join(settings.MEDIA_ROOT, f'documents/{document.uuid}/{document.uuid}.pdf')
        os.makedirs(os.path.dirname(new_pdf_file_path), exist_ok=True)
        docx2pdf.convert(file_path, new_pdf_file_path)
        document.pdf_file_version.name = 'documents/{uuid}/{uuid}.pdf'.format(uuid=document.uuid)
        document.save()
    
    if file_name.endswith('.pdf'):
        pdf_file_path = file_path
        file_name = document.original_file.name
    else:
        pdf_file_path = os.path.join(settings.MEDIA_ROOT, document.pdf_file_version.path)
        file_name = document.pdf_file_version.name
    print(pdf_file_path)
    print(file_name)
       
    return FileResponse(open(pdf_file_path, 'rb'), as_attachment=True, filename=file_name)