from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EventViewSet, CustomLoginView, CustomLogoutView, RegisterUserView, UserProfileView

# Creiamo un router per gestire gli endpoint REST
router = DefaultRouter()
router.register(r'events', EventViewSet)  # /admin/events/

app_name = "backend_api"

urlpatterns = [
    path("api/", include(router.urls)),  # Registriamo le API con DRF
    path('api/auth/login/', CustomLoginView.as_view(), name="api_login"),
    path('api/auth/logout/', CustomLogoutView.as_view(), name='api_logout'),
    path("api/auth/register/", RegisterUserView.as_view(), name="register"),
    path("api/auth/profile/", UserProfileView.as_view(), name="user-profile"),
]