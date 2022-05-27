from django.urls import path, include

#? djangorestframework-simplejwt
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

#? drf-spectacular
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView, SpectacularJSONAPIView

#? User
from user import views as UserViews

urlpatterns = [
    #? Auth Routes
    path('auth/token/',
         TokenObtainPairView.as_view(),
         name='obtain_token_pair'),
    path('auth/token/refresh/',
         TokenRefreshView.as_view(),
         name='token_refresh'),

    #? Schema
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/json/', SpectacularJSONAPIView.as_view(), name='json_schema'),
    path('schema/swagger/',
         SpectacularSwaggerView.as_view(url_name='schema'),
         name='swagger'),
    path('schema/redoc/',
         SpectacularRedocView.as_view(url_name='schema'),
         name='redoc'),

    #? User
    path('user/list/', UserViews.UserListAPIView.as_view(), name='user-list'),
    path('user/<int:pk>/',
         UserViews.UserDetailAPIView.as_view(),
         name='user-detail'),
    path('user/create/',
         UserViews.UserCreateAPIView.as_view(),
         name='user-create'),
]
