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

#? Attendance
from attendance import views as AttenViews

#? Classes
from classes import views as ClassViews

#? College
from college import views as CollegeViews

#? Course
from course import views as CourseViews

#? Department
from department import views as DeptViews

#? Student
from student import views as StudViews

#? image upload
from .views import ImageUploadAPIView

#? University
from university import views as UniViews

#? Contact
from contact import views as ContactViews

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

    #? Attendance
    path('attendance/',
         AttenViews.AttendanceListCreateAPIView.as_view(),
         name='attendance-list-create'),
    path('attendance/bulk/',
         AttenViews.AttendanceBulkCreateAPIView.as_view(),
         name='attendance-bulk-create'),
    path('attendance/<int:pk>/',
         AttenViews.AttendanceRetrieveUpdateDestroyAPIView.as_view(),
         name='attendance-retrieve-update-destroy'),

    #? Classes
    path('class/',
         ClassViews.ClassListCreateAPIView.as_view(),
         name='Class-list-create'),
    path('class/<int:pk>/',
         ClassViews.ClassRetrieveUpdateDestroyAPIView.as_view(),
         name='class-retrieve-update-destroy'),

    #? College
    path('college/',
         CollegeViews.CollegeListCreateAPIView.as_view(),
         name='college-list-create'),
    path('college/<int:pk>/',
         CollegeViews.CollegeRetrieveUpdateDestroyAPIView.as_view(),
         name='college-retrieve-update-destroy'),

    #? Course
    path('course/',
         CourseViews.CourseListCreateAPIView.as_view(),
         name='course-list-create'),
    path('course/<int:pk>/',
         CourseViews.CourseRetrieveUpdateDestroyAPIView.as_view(),
         name='course-retrieve-update-destroy'),

    #? Department
    path('department/',
         DeptViews.DepartmentListCreateAPIView.as_view(),
         name='department-list-create'),
    path('department/<int:pk>/',
         DeptViews.DepartmentRetrieveUpdateDestroyAPIView.as_view(),
         name='department-retrieve-update-destroy'),
    path('department-type/',
         DeptViews.DepartmentTypeListCreateAPIView.as_view(),
         name='department-type-list-create'),
    path('department-type/<int:pk>/',
         DeptViews.DepartmentTypeRetrieveUpdateDestroyAPIView.as_view(),
         name='department-type-list-create'),

    #? Student
    path('student/',
         StudViews.StudentListCreateAPIView.as_view(),
         name='student-list-create'),
    path('student/bulk',
         StudViews.StudentBulkCreateAPIView.as_view(),
         name='student-bulk-create'),
    path('student/<int:pk>/',
         StudViews.StudentRetrieveUpdateDestroyAPIView.as_view(),
         name='student-retrieve-update-destroy'),

    #? Image Upload
    path('image-upload/', ImageUploadAPIView.as_view(), name='image-upload'),

    #? University
    path('university/',
         UniViews.UniversityListCreateAPIView.as_view(),
         name='university-list-create'),
    path('university/<int:pk>/',
         UniViews.UniversityRetrieveUpdateDestroyAPIView.as_view(),
         name='university-retrieve-update-destroy'),

    #? Contact
    path('contact/',
         ContactViews.ContactListAPIView.as_view(),
         name='contact-list'),
    path('contact/add/',
         ContactViews.ContactCreateAPIView.as_view(),
         name='contact-add'),
    path('contact/<int:pk>/',
         ContactViews.ContactRetrieveUpdateDestroyAPIView.as_view(),
         name='contact-retrieve-update-destroy'),
]
