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

#? Auth
from authlogic import views as AuthViews

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
    path('user/',
         UserViews.UserListCreateAPIView.as_view(),
         name='user-list-create'),
    path('user/<int:pk>/',
         UserViews.UserRetrieveUpdateDestroyAPIView.as_view(),
         name='user-retrieve-update-destroy'),
    path('user/update_password/<int:pk>/',
         UserViews.UserPasswordUpdateAPIView.as_view(),
         name='user-password-update'),
    path('user/admin/',
         UserViews.UsersAdminListAPIView.as_view(),
         name='user-admin-list'),
    path('user/principal/',
         UserViews.UsersPrincipalListAPIView.as_view(),
         name='user-principal-list'),
    path('user/teacher/',
         UserViews.UsersTeacherListAPIView.as_view(),
         name='user-teacher-list'),
    path('user/hod/',
         UserViews.UsersHodListAPIView.as_view(),
         name='user-hod-list'),

    #? Auth
    path('auth/me/', AuthViews.AuthMeApiView.as_view(), name='auth-me'),
]
