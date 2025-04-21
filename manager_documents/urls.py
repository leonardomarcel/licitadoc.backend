from django.urls import path

from . import apis


urlpatterns = [
    path('api/documents/', apis.list_documents, name='list_documents'),
    path('api/tags/', apis.list_tags, name='list_tags'),
    path('api/download/<int:pk>', apis.download_document, name='download_document'),
    path('api/view/<int:pk>', apis.view_document, name='view_document'),
    path('api/documents/add', apis.add_document, name='add_document'),

]

