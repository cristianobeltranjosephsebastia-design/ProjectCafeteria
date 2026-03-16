from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import PedidoSerializer
from .authentication import FirebaseAuthentication
from Cafeteria.firebase_config import initialize_firebase
from firebase_admin import firestore

db = initialize_firebase()

class PedidoApiView(APIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pedido_id=None):
        limit = int(request.query_params.get('limit', 10))
        last_doc_id = request.query_params.get('last_doc_id')
        
        uid_usuario = request.user.uid
        rol_usuario = request.user.rol # Administrador, Cajero, Cliente

        try:
            query = db.collection('pedidos')


            if rol_usuario in ['Administrador', 'Cajero']:
                query = query.order_by('fecha_creacion', direction=firestore.Query.DESCENDING)
            else:
                query = (query.where('usuario_id', '==', uid_usuario)
                        .order_by('fecha_creacion', direction=firestore.Query.DESCENDING))

            # Paginación (ajustada a la colección 'pedidos')
            if last_doc_id:
                last_doc = db.collection('pedidos').document(last_doc_id).get()
                if last_doc.exists:
                    query = query.start_after(last_doc)

            docs = query.limit(limit).stream()

            pedidos = []
            for doc in docs:
                data = doc.to_dict()
                data['id'] = doc.id
                pedidos.append(data)

            return Response(
                {"Mensaje": f"Listando como {rol_usuario}", "datos": pedidos},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response({"Error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        serializer = PedidoSerializer(data=request.data)
        if serializer.is_valid():
            datos_validados = serializer.validated_data
            datos_validados['usuario_id'] = request.user.uid
            datos_validados['rol_creador'] = request.user.rol
            datos_validados['fecha_creacion'] = firestore.SERVER_TIMESTAMP
            datos_validados['estado'] = 'pendiente' 

            try:

                nuevo_doc = db.collection('pedidos').add(datos_validados)
                return Response(
                    {"mensaje": "Pedido creado correctamente ✅", "id": nuevo_doc[1].id},
                    status=status.HTTP_201_CREATED
                )
            except Exception as e:
                return Response({"Error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id=None):
        if not id:
            return Response({"Error": "ID requerido"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = PedidoSerializer(data=request.data)
        if serializer.is_valid():
            try:
                doc_ref = db.collection('pedidos').document(id)
                doc = doc_ref.get()

                if not doc.exists:
                    return Response({"Error": "Pedido no encontrado"}, status=status.HTTP_404_NOT_FOUND)

                pedido_data = doc.to_dict()


                if request.user.rol != 'Administrador' and pedido_data.get('usuario_id') != request.user.uid:
                    return Response(
                        {"error": "No tienes permiso para editar este pedido"},
                        status=status.HTTP_403_FORBIDDEN
                    )

                doc_ref.update(serializer.validated_data)
                return Response({"mensaje": "Pedido actualizado correctamente ✅"}, status=status.HTTP_200_OK)

            except Exception as e:
                return Response({"Error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id=None):
        if not id:
            return Response({"Error": "ID requerido"}, status=status.HTTP_400_BAD_REQUEST)

        try:

            doc_ref = db.collection('pedidos').document(id)
            doc = doc_ref.get()

            if not doc.exists:
                return Response({"Error": "Pedido no encontrado"}, status=status.HTTP_404_NOT_FOUND)

            pedido_data = doc.to_dict()

            if request.user.rol != 'Administrador' and pedido_data.get('usuario_id') != request.user.uid:
                return Response(
                    {"error": "No tienes permiso para eliminar este pedido"},
                    status=status.HTTP_403_FORBIDDEN
                )

            doc_ref.delete()
            return Response({"mensaje": "Pedido eliminado correctamente ✅"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"Error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)