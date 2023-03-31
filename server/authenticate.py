from rest_framework.permissions import BasePermission


class Authenticate(BasePermission):
  def has_permission(self, req, view):
    return req.user and req.user.is_authenticated