from django.urls import path

from . import apis


urlpatterns = [
    path('documents/', apis.list_documents, name='list_documents'),
    path('download/<int:pk>', apis.download_document, name='download_document'),
    path('view/<int:pk>', apis.view_document, name='view_document'),
    path('documents/add', apis.add_document, name='add_document'),

]

