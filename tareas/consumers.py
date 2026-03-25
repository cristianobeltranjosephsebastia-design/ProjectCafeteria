import json
from channels.generic.websocket import AsyncWebsocketConsumer
from Cafeteria.firebase_config import initialize_firebase
from firebase_admin import firestore
from asgiref.sync import sync_to_async

db = initialize_firebase()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.channel_layer.group_add(self.room_name, self.channel_name)
        self.accept()

    async def disconnect(self, class_code):
        await self.channel_layer.group_discard(self.room_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        mensaje = data['mensaje']
        usuario = data['usuario']

        # 1. Guardar el mensaje en Firestore
        await self.guardar_mensaje(usuario, mensaje)

        # 2. Enviar el mensaje a todos los clientes conectados
        await self.channel_layer.group_send(
            self.room_name,
            {
                'type': 'chat_mensaje',
                'mensaje': mensaje,
                'usuario': usuario
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'mensaje': event['mensaje'],
            'usuario': event['usuario']
        }))
    @sync_to_async
    def guardar_mensaje_firestore(self, usuario, mensaje):
        """
        Funcion para interactuar con Firestore de forma que no se interrumpa el websocket
        """
        try:
            db.collection('api_chat_mensajes').add({
                'usuario': usuario,
                'mensaje': mensaje,
                'timestamp': firestore.SERVER_TIMESTAMP
            })
        except Exception as e:
            print(f"Error al guardar mensaje en Firestore: {e}")