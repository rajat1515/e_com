from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied

class IsRole(permissions.BasePermission):
    role = None

    def has_permission(self, request, view):
        try:
            request.user.vendoruser
        except:
            return False
        if str(request.user) == "AnonymousUser" or \
                not ( request.user.vendoruser.role == self.role):
            raise PermissionDenied
        return True


class IsSalesperson(IsRole):
    role = 'salesperson'


class IsSupervisor(IsRole):
    role = 'supervisor'


class IsAdmin(IsRole):
    role = 'admin'


class IsCustomer(IsRole):
    role = 'customer'
