from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from django.shortcuts import render
from .models import Document, Tag
from .utils import convert_to_pdf
from .pagination import DocumentPagination, TagPagination
from .forms import DocumentForm
from .serializers import DocumentSerializer, TagSerializer
from custom_auth.utils.permissions import require_group
from django.http import JsonResponse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, action
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
#from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
from rest_framework.response import Response
from django.http import HttpResponse, FileResponse
from django.utils.encoding import smart_str
import os
# import docx2pdf
from django.conf import settings


# Create your views here.


class DocumentViewSet(ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    pagination_class = DocumentPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        tag = self.request.query_params.get('tag')
        if tag:
            return Document.objects.filter(tags__id=tag)
        return Document.objects.all()
    
    @action(detail=False, methods=['post'])
    def add_document(self, request):
        serializer = DocumentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def download_document(self, request, pk):
        document = Document.objects.get(pk=pk)
        file_path = document.original_file.path
        file_name = document.original_file.name
        if not os.path.exists(file_path):
            return Response({'error': 'File not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Extrai apenas o nome do arquivo
        file_name = os.path.basename(file_path)
        
        response = FileResponse(open(file_path, 'rb'), as_attachment=True)
        response['Content-Disposition'] = f'attachment; filename="{smart_str(file_name)}"'
        return response
    
    @action(detail=False, methods=['get'])
    def view_document(self, request, pk):
        document = Document.objects.get(pk=pk)
        file_path = document.pdf_file_version.path
        file_name = document.pdf_file_version.name
        if not os.path.exists(file_path):
            return Response({'error': 'File not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Extrai apenas o nome do arquivo
        file_name = os.path.basename(file_path)
        
        response = FileResponse(open(file_path, 'rb'), as_attachment=True)
        response['Content-Disposition'] = f'attachment; filename="{smart_str(file_name)}"'
        return response

class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = TagPagination
    permission_classes = [IsAuthenticated]
    
    # def get_queryset(self):
    #     return Tag.objects.all()
    

    
    





# def add_document(request):
#     if request.method == 'POST':
#         form = DocumentForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('list_documents')
#     else:
#         form = DocumentForm()
#     return render(request, 'add_document.html', {'form': form})

# @api_view(['GET'])
# @login_required
# def list_documents(request):
#     paginator = DocumentPagination()
#     tag = request.query_params.get('tag')
#     if tag:
#         documents = Document.objects.filter(tags__id=tag)
#     else:
#         documents = Document.objects.all()
#     result_page = paginator.paginate_queryset(documents, request)
#     serializer = DocumentSerializer(result_page, many=True)
#     return paginator.get_paginated_response(serializer.data)

# @api_view(['GET'])
# @login_required
# def list_tags(request):
#     paginator = TagPagination()
#     tags = Tag.objects.all()
#     result_page = paginator.paginate_queryset(tags, request)
#     serializer = TagSerializer(result_page, many=True)
#     return paginator.get_paginated_response(serializer.data)



# @api_view(['GET'])
# @login_required
# @require_group('premium')
# def download_document(request, pk):
#     document = Document.objects.get(pk=pk)
#     file_path = document.original_file.path
#     file_name = document.original_file.name
#     if not os.path.exists(file_path):
#         return JsonResponse({'status': 'error', 'message': 'File not found'})
    
#     # Extrai apenas o nome do arquivo
#     file_name = os.path.basename(file_path)

#     response = FileResponse(open(file_path, 'rb'), as_attachment=True)
#     response['Content-Disposition'] = f'attachment; filename="{smart_str(file_name)}"'
#     return response

# @api_view(['GET'])
# @login_required
# def view_document(request, pk):
#     #pythoncom.CoInitialize()  # Inicializa o COM
#     document = Document.objects.get(pk=pk)
#     file_path = os.path.join(settings.MEDIA_ROOT, document.original_file.path)
#     file_name = document.original_file.name
#     if not os.path.exists(file_path):
#         return JsonResponse({'status': 'error', 'message': 'File not found'})
#     if  (file_name.endswith('.docx') or file_name.endswith('.doc')) and not document.pdf_file_version:
#         # Converte o arquivo para PDF
#         new_pdf_file_path = os.path.join(settings.MEDIA_ROOT, f'documents/{document.uuid}/{document.uuid}.pdf')
#         os.makedirs(os.path.dirname(new_pdf_file_path), exist_ok=True)
#         # docx2pdf.convert(file_path, new_pdf_file_path)
#         pdf_converted_path  = convert_to_pdf(file_path, new_pdf_file_path)
#         if not pdf_converted_path or not os.path.exists(pdf_converted_path):
#             return JsonResponse({'status': 'error', 'message': 'Failed to convert to PDF'})
#         document.pdf_file_version.name = 'documents/{uuid}/{uuid}.pdf'.format(uuid=document.uuid)
#         document.save()
    
#     pdf_file_path = (
#         file_path if file_name.endswith('.pdf') else os.path.join(settings.MEDIA_ROOT, document.pdf_file_version.path)
#     )
    
   
       
#     return FileResponse(open(pdf_file_path, 'rb'), as_attachment=True, filename=file_name)