from rest_framework.permissions  import BasePermission

class IsStudent(BasePermission):
    message = "Amalyotni amalga oshirish uchun sizda ruxsat mavjud emas!"
    def has_permission(self, request, view):
        return bool(request.user and request.user.role == 'student')