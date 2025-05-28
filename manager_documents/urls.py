from reest_framework.routers import DefaultRouter

from . import apis


router = DefaultRouter()
router.register(r'documents', apis.DocumentViewSet, basename='document')
router.register(r'tags', apis.TagViewSet, basename='tag')
