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
      const token = 'eyJhbGciOiJSUzI1NiIsImtpZCI6IjVlODJhZmI0ZWY2OWI3NjM4MzA2OWFjNmI1N2U3ZTY1MjAzYmZlOTYiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vY2FmZXRlcmlhcHJvamVjdC0zNTJiZSIsImF1ZCI6ImNhZmV0ZXJpYXByb2plY3QtMzUyYmUiLCJhdXRoX3RpbWUiOjE3NzU2MDcwNDYsInVzZXJfaWQiOiJkVGs5Y0paVTFPUVd1Z3pTTlJWQm9aUGJOVDgyIiwic3ViIjoiZFRrOWNKWlUxT1FXdWd6U05SVkJvWlBiTlQ4MiIsImlhdCI6MTc3NTYwNzA0NiwiZXhwIjoxNzc1NjEwNjQ2LCJlbWFpbCI6ImVzdG9lc3VuYXBydWViYTJAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOmZhbHNlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7ImVtYWlsIjpbImVzdG9lc3VuYXBydWViYTJAZ21haWwuY29tIl19LCJzaWduX2luX3Byb3ZpZGVyIjoicGFzc3dvcmQifX0.cJdKNOisG0mcnF0a6fjjCHvTcmoiH-RrJAH-6LoGo0peQSeK5SQFoB8UMk2JtVSwitJ8X0iXqiS6ReE8d8fUTqe9J8KGHisgb7KSnVgOLu0oBGiJrc3f2YY0xsj0QxaM3QFqIKFNFkeuYIFiLenEJdU6e_Bjaixg3a6CHbIrgRWO-64ZMGT3oE_0WIpxrPUVM3tSSqSnBo856vgrMIwtYHwM2aQbQNrdpDkiuQrIeLI5qDB1Xhnzf8GgRZsyhTwpdwhVJcvr6yeGX5VEwENZn_pgpq7cpP3cd5VEmiF30xHZ0dgTW9_7uvCy-QtwYtFOiymfclMULdEheZztm9pCYg'; 

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