import json
from channels.generic.websocket import AsyncWebsocketConsumer
from Cafeteria.firebase_config import initialize_firebase
from firebase_admin import firestore
from asgiref.sync import sync_to_async

db = initialize_firebase()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = "sala_general"
        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )
        await self.accept()
        
        # 1. Intentar cargar el historial
        try:
            historial = await self.obtener_historial_firestore()
            for msg in historial:
                await self.send(text_data=json.dumps(msg))
            print(f"✅ Historial enviado a nuevo usuario")
        except Exception as e:
            print(f"⚠️ Error cargando historial al conectar: {e}")

        print(f"✅ Conexión exitosa en {self.room_name}")

    async def disconnect(self, close_code):
        if hasattr(self, 'room_name'):
            await self.channel_layer.group_discard(self.room_name, self.channel_name)
        print("❌ Conexión cerrada")

    async def receive(self, text_data):
        data = json.loads(text_data)
        usuario = data.get('usuario', 'Anónimo')
        mensaje = data.get('mensaje', '')
        
        await self.guardar_mensaje_firestore(usuario, mensaje)

        await self.channel_layer.group_send(
            self.room_name,
            {
                'type': 'chat_message',
                'usuario': usuario,
                'mensaje': mensaje
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'usuario': event['usuario'],
            'mensaje': event['mensaje']
        }))

    # --- ESTAS FUNCIONES DEBEN ESTAR DENTRO DE LA CLASE (INDENTADAS) ---

    @sync_to_async
    def obtener_historial_firestore(self):
        try:
            # Traemos los últimos 20 mensajes ordenados por fecha
            docs = db.collection('mensajes').order_by('fecha', direction=firestore.Query.ASCENDING).limit(20).stream()
            lista = []
            for d in docs:
                datos = d.to_dict()
                lista.append({
                    'usuario': datos.get('usuario', 'Anónimo'),
                    'mensaje': datos.get('mensaje', '')
                })
            return lista
        except Exception as e:
            print(f"❌ Error en obtener_historial: {e}")
            return []

    @sync_to_async
    def guardar_mensaje_firestore(self, usuario, mensaje):
        try:
            db.collection('mensajes').add({
                'usuario': usuario,
                'mensaje': mensaje,
                'fecha': firestore.SERVER_TIMESTAMP
            })
            print(f"🔥 Mensaje guardado en Firestore")
        except Exception as e:
            print(f"⚠️ Error guardando: {e}")