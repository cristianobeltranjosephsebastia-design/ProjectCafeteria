from rest_framework import permissions

class EsCajeroOAdmin(permissions.BasePermission):
    """
    Permiso para que solo el Cajero o el Administrador vean todos los pedidos.
    """
    def has_permission(self, request, view):
        # Primero verificamos que el usuario esté autenticado
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Luego verificamos el rol según tu documentación (RF-01)
        return request.user.rol in ['Cajero', 'Administrador']

class EsDueñoDelPedido(permissions.BasePermission):
    """
    Permiso para que un Cliente solo vea sus propios pedidos.
    """
    def has_object_permission(self, request, obj, view):
        # Comparamos el UID del usuario con el del pedido
        return obj.get('usuario_id') == request.user.uid