from rest_framework.routers import DefaultRouter

from . import apis


router = DefaultRouter()
router.register(r'document', apis.DocumentViewSet, basename='document')
router.register(r'tag', apis.TagViewSet, basename='tag')
