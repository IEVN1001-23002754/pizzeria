export interface Cliente 
{
  nombre: string;
  direccion: string;
  telefono: string;
  fecha_pedido: string;
}

export interface PizzaTemporal 
{
  id?: number;
  id_temporal?: number;
  tamano: 'Chica' | 'Mediana' | 'Grande' | string;
  ingredientes: string[];
  num_pizzas: number;
  subtotal: number;
}

export interface Venta 
{
  id_pedido: number;
  nombre: string;
  direccion?: string;
  telefono?: string;
  fecha_pedido: string;
  total: number;
  total_pedido?: number;
}