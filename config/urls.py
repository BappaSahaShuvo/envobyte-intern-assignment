from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('contacts.urls')),
    
    # Enables the "Log in" button in the Chrome browser interface
    path('api-auth/', include('rest_framework.urls')),
    
    # JWT Auth Endpoints (For professional API testing like Postman)
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]