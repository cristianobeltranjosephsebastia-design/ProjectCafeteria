from rest_framework import serializers

class PedidoSerializer(serializers.Serializer):
    """
    Validar los datos de los pedidos de la cafetería antes de enviarlos a Firestore
    """
    producto = serializers.CharField(max_length=150)
    notas = serializers.CharField(required=False, allow_blank=True)
    cantidad = serializers.IntegerField(default=1)
    estado = serializers.CharField(default='pendiente', max_length=20, required=False)

    def validate_producto(self, value):
        """
        Validación personalizada: Asegurar que el nombre del producto sea descriptivo
        """
        if len(value) < 3:
            raise serializers.ValidationError("El nombre del producto debe tener al menos 3 caracteres")
        return value

    def validate_cantidad(self, value):
        """
        Validación para evitar pedidos con cantidades negativas o en cero.
        """
        if value <= 0:
            raise serializers.ValidationError("La cantidad debe ser mayor a cero")
        return value