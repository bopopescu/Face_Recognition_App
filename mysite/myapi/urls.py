# myapi/urls.py

from django.urls import include, path
from rest_framework import routers
from . import views
from rest_framework.urlpatterns import format_suffix_patterns


router = routers.DefaultRouter()
router.register(r'people', views.PersonViewSet)
router.register(r'admins', views.AdminViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='face_recognition')),
    path('', views.api_root),
    path('people/<int:pk>/highlight/', views.PersonHighlight.as_view()),
]


