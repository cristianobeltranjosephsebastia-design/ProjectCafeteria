import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { PedidosService } from '../../services/pedidos.service';

@Component({
  selector: 'app-pedido-form',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './pedido-form.html',
  styleUrl: './pedido-form.css'
})
export class PedidoFormComponent {
  pedidoForm: FormGroup;

  constructor(
    private fb: FormBuilder,
    private pedidosService: PedidosService
  ) {
    this.pedidoForm = this.fb.group({
      cliente: ['', Validators.required],
      producto: ['', Validators.required],
      cantidad: [1, [Validators.required, Validators.min(1)]],
      notas: ['']
    });
  }

  enviarPedido() {
    if (this.pedidoForm.valid) {
      const nuevoPedido = this.pedidoForm.value;
      const token = 'eyJhbGciOiJSUzI1NiIsImtpZCI6IjVlODJhZmI0ZWY2OWI3NjM4MzA2OWFjNmI1N2U3ZTY1MjAzYmZlOTYiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vY2FmZXRlcmlhcHJvamVjdC0zNTJiZSIsImF1ZCI6ImNhZmV0ZXJpYXByb2plY3QtMzUyYmUiLCJhdXRoX3RpbWUiOjE3NzU2NjM3MTYsInVzZXJfaWQiOiI5MVhBdEhKNGF4T2t3V1o1bVhkSjVGUm16MHMyIiwic3ViIjoiOTFYQXRISjRheE9rd1daNW1YZEo1RlJtejBzMiIsImlhdCI6MTc3NTY2MzcxNiwiZXhwIjoxNzc1NjY3MzE2LCJlbWFpbCI6ImVzdG9lc3VuYXBydWViYTZAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOmZhbHNlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7ImVtYWlsIjpbImVzdG9lc3VuYXBydWViYTZAZ21haWwuY29tIl19LCJzaWduX2luX3Byb3ZpZGVyIjoicGFzc3dvcmQifX0.e4SKLuQmnEtezlhY5mjJZJYC6xyK37wcYydzl3pbfhrKCb-lJ0l8uLghC30CLUcjSoCuobLUBJLLxhCmX6lU3DOR00MkIj90kPt2Jr6D1qVtV6RRYpWze1H4fVdYUHdZXRUOj7IPg3Wh7Ux_CMixxuEPfajKNoXEZH6FBkTejP5qmwH9W4t50P0osBmK9DsclQWJBJwqaf6RFK791xUixGZze1HT3eCJn8cmdd30oyJxIsqOg-qSHsvmEW5DviWplYHxFWPkbgm3DSf8SWIGAmKKSyDFojePn1-hMHalv7ViOFXwnDJ6TjzgSlFkjc0aSqQuL2OabL6HGdjxGPRu7Q';

      this.pedidosService.crearPedido(nuevoPedido, token).subscribe({
        next: (res) => {
          alert('¡Pedido creado con éxito!');
          this.pedidoForm.reset({ cantidad: 1 });
        },
        error: (err) => console.error('Error al crear:', err)
      });
    }
  }
}