import { Injectable } from '@angular/core';
import { Subject, Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class WebsocketService {
  private socket!: WebSocket;
  // El Subject es como una antena que retransmite lo que llega de Django
  private mensajesSubject = new Subject<any>();

  constructor() {
    this.conectar();
  }

  private conectar() {
    this.socket = new WebSocket('ws://127.0.0.1:8085/ws/chat/');

    this.socket.onopen = () => console.log('✅ Socket conectado desde Angular');

    this.socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      this.mensajesSubject.next(data); 
    };

    this.socket.onclose = () => {
      console.warn('🔌 Conexión perdida, reintentando...');
      setTimeout(() => this.conectar(), 3000);
    };
  }

  enviarMensaje(usuario: string, mensaje: string) {
    if (this.socket.readyState === WebSocket.OPEN) {
      this.socket.send(JSON.stringify({ usuario, mensaje }));
    }
  }

  getMensajes(): Observable<any> {
    return this.mensajesSubject.asObservable();
  }
}

