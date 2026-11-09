import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Cliente, PizzaTemporal, Venta } from './componentes/pizzeria-interfaz';

@Injectable({
  providedIn: 'root'
})
export class PedidoService {
  private API_URL = 'http://127.0.0.1:5000/api';

  public datosCliente: Cliente = {
    nombre: '',
    direccion: '',
    telefono: '',
    fecha_pedido: new Date().toISOString().split('T')[0]
  };

  constructor(private http: HttpClient) { }

  agregarTemporal(pizza: any): Observable<any> {
    return this.http.post(`${this.API_URL}/temporal`, pizza);
  }

  obtenerTemporal(): Observable<PizzaTemporal[]> {
    return this.http.get<PizzaTemporal[]>(`${this.API_URL}/temporal`);
  }

  quitarTemporal(id_temporal: number): Observable<any> {
    return this.http.delete(`${this.API_URL}/temporal/${id_temporal}`);
  }

  vaciarTemporal(): Observable<any> {
    return this.http.delete(`${this.API_URL}/temporal`);
  }

  terminarPedido(pedidoData: any): Observable<any> {
    return this.http.post(`${this.API_URL}/pedidos`, pedidoData);
  }

  obtenerVentasPorDia(dia: string): Observable<Venta[]> {
    return this.http.get<Venta[]>(`${this.API_URL}/ventas/dia?dia=${dia}`);
  }

  obtenerVentasPorMes(mes: string, anio: string): Observable<Venta[]> {
    return this.http.get<Venta[]>(`${this.API_URL}/ventas/mes?mes=${mes}&anio=${anio}`);
  }
}