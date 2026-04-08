import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class PedidosService {
  private apiUrl = 'http://127.0.0.1:8000/api/pedidos/';

  constructor(private http: HttpClient) { }

  // 1. Obtener las estadisticas
  getEstadisticas(token: string): Observable<any> {
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${token}`
    });
    return this.http.get(`${this.apiUrl}estadisticas/`, { headers });
  }

  // 2. Crear pedidos
  crearPedido(pedido: any, token: string): Observable<any> {
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    });
    
    // Enviamos el objeto pedido por POST
    return this.http.post(this.apiUrl, pedido, { headers });
  }
}