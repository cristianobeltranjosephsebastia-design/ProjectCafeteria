import { Component, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet } from '@angular/router';


import { DashboardComponent } from './components/dashboard/dashboard';
import { PedidoFormComponent } from './components/pedido-form/pedido-form';
import { WebsocketComponent } from './components/websocket/websocket';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, DashboardComponent, PedidoFormComponent, WebsocketComponent, CommonModule],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  protected readonly title = signal('cafeteriaFrontend');
}
