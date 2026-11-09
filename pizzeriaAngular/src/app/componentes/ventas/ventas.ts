import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { PedidoService } from '../../pedido.service';
import { Venta } from '../pizzeria-interfaz';

@Component({
  selector: 'app-ventas',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './ventas.html',
  styleUrl: './ventas.css'
})
export class Ventas {
  tipoBusqueda: 'dia' | 'mes' = 'dia';
  
  // Cambiamos a select de días de la semana
  diaSeleccionado: string = 'lunes';
  diasSemana = [
    { label: 'Lunes', value: 'lunes' },
    { label: 'Martes', value: 'martes' },
    { label: 'Miércoles', value: 'miercoles' },
    { label: 'Jueves', value: 'jueves' },
    { label: 'Viernes', value: 'viernes' },
    { label: 'Sábado', value: 'sabado' },
    { label: 'Domingo', value: 'domingo' }
  ];

  mesSeleccionado: string = '11'; // Noviembre por defecto
  anioSeleccionado: string = '2026';
  
  resultadosVentas: Venta[] = [];
  totalVentasPeriodo: number = 0;

  constructor(private pedidoService: PedidoService) {}

  buscarVentas() {
    if (this.tipoBusqueda === 'dia') {
      if (!this.diaSeleccionado) return;
      // Envía el día en texto tal como lo pide Flask (lunes, martes, etc.)
      this.pedidoService.obtenerVentasPorDia(this.diaSeleccionado).subscribe({
        next: (res: any) => {
          this.resultadosVentas = Array.isArray(res) ? res : (res.ventas || []);
          this.calcularTotalVentas();
        },
        error: (err) => console.error('Error al buscar ventas por día:', err)
      });
    } else {
      this.pedidoService.obtenerVentasPorMes(this.mesSeleccionado, this.anioSeleccionado).subscribe({
        next: (res: any) => {
          this.resultadosVentas = Array.isArray(res) ? res : (res.ventas || []);
          this.calcularTotalVentas();
        },
        error: (err) => console.error('Error al buscar ventas por mes:', err)
      });
    }
  }

  calcularTotalVentas() 
  {
    this.totalVentasPeriodo = this.resultadosVentas.reduce((acc, item: any) => {
      const monto = Number(item.total || item.total_pedido || 0);
      return acc + monto;
    }, 0);
  }
}