from rest_framework import permissions


class UserIsAdmin(permissions.BasePermission):
    '''
        permission check if the user is Admin
    '''

    def has_permission(self, request, view):
        if request.user.is_admin:
            return True
        return False


class UserIsPrincipal(permissions.BasePermission):
    '''
        permission check if the user is Principal
    '''

    def has_permission(self, request, view):
        if request.user.is_principal:
            return True
        return False


class UserIsHOD(permissions.BasePermission):
    '''
        permission check if the user is HOD
    '''

    def has_permission(self, request, view):
        if request.user.is_hod:
            return True
        return False


class UserIsTeacher(permissions.BasePermission):
    '''
        permission check if the user is Teacher
    '''

    def has_permission(self, request, view):
        if request.user.is_teacher:
            return True
        return False


class UserIsTeacherRO(permissions.BasePermission):
    '''
        permission check if the user is Teacher
    '''

    def has_permission(self, request, view):
        if request.user.is_teacher:
            if request.method in permissions.SAFE_METHODS:
                return True
            else:
                return False
        return False
