import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { WebsocketService } from '../../services/websocket'; 

@Component({
  selector: 'app-websocket',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './websocket.html',
  styleUrl: './websocket.css'
})
export class WebsocketComponent implements OnInit {
  mensajes: any[] = [];
  mensajeNuevo: string = '';

  constructor(private wsService: WebsocketService) {} 

  get totalMensajes(): number {
    return this.mensajes.length;
  }

  ngOnInit() {
    this.wsService.getMensajes().subscribe((data) => {
      this.mensajes = [...this.mensajes, data];
      this.scrollToBottom();
    });
  }

  enviar() {
    if (this.mensajeNuevo.trim()) {
      this.wsService.enviarMensaje('Usuario3', this.mensajeNuevo);
      this.mensajeNuevo = '';
    }
  }

  private scrollToBottom() {
    setTimeout(() => {
      const container = document.querySelector('.mensajes-container');
      if (container) {
        container.scrollTop = container.scrollHeight;
      }
    }, 100);
  }
}