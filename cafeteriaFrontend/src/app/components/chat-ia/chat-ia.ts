import { Component } from '@angular/core';
import { PedidosService } from '../../services/pedidos.service';

@Component({
  selector: 'app-chat-ia',
  standalone: true,
  templateUrl: './chat-ia.html',
  styleUrls: ['./chat-ia.css']
})
export class ChatIaComponent {
  pregunta: string = '';
  chatHistory: { role: string, text: string }[] = [];

  constructor(private pedidosService: PedidosService) {}

  preguntarIA() {
    if (!this.pregunta) return;
    
    this.chatHistory.push({ role: 'user', text: this.pregunta });
    
    this.pedidosService.consultarIA(this.pregunta).subscribe({
      next: (res) => {
        this.chatHistory.push({ role: 'bot', text: res.respuesta });
        this.pregunta = '';
      }
    });
  }
}