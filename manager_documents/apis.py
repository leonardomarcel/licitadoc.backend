from django.shortcuts import render
from .models import Document
from .forms import DocumentForm
from django.http import JsonResponse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
from rest_framework.response import Response
from django.http import HttpResponse, FileResponse
from django.utils.encoding import smart_str
import os
import docx2pdf
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
@permission_classes([IsAuthenticated])
def list_documents(request):
    documents = Document.objects.all()
    serializer = DocumentSerializer(documents, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def download_document(request, pk):
    document = Document.objects.get(pk=pk)
    file_path = document.document.path
    file_name = document.document.name
    print(file_path)
    if not os.path.exists(file_path):
        return JsonResponse({'status': 'error', 'message': 'File not found'})
    
    # Extrai apenas o nome do arquivo
    file_name = os.path.basename(file_path)

    response = FileResponse(open(file_path, 'rb'), as_attachment=True)
    response['Content-Disposition'] = f'attachment; filename="{smart_str(file_name)}"'
    return response

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_document(request, pk):
    pythoncom.CoInitialize()  # Inicializa o COM
    document = Document.objects.get(pk=pk)
    file_path = document.document.path
    file_name = document.document.name
    if not os.path.exists(file_path):
        return JsonResponse({'status': 'error', 'message': 'File not found'})
    if file_name.endswith('.doc'):
        # Converte o arquivo para PDF
        pdf_file_path = file_path.replace('.doc', '.pdf')
        docx2pdf.convert(file_path, pdf_file_path)
    elif file_name.endswith('.docx'):
        pdf_file_path = file_path.replace('.docx', '.pdf')
        docx2pdf.convert(file_path, pdf_file_path)
    else:
        pdf_file_path = file_path
    print(pdf_file_path)
       
    #response = FileResponse(open(pdf_file_path, "rb"), content_type="application/pdf")    
    return FileResponse(open(pdf_file_path, 'rb'), as_attachment=True, filename=file_name)