"""
URL configuration for letsCode project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from assignments.urls import enrollment_router
from questions.urls import question_router

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("user_profile.urls")),
    path("", include(question_router.urls)),
    path("", include(enrollment_router.urls)),
    path("api/", include("assignments.urls")),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

# curl -X POST -d "username=hira.ijaz&password=123" http://127.0.0.1:8000/api/auth/token/
