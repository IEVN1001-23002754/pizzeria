import { Routes } from '@angular/router';
import { Inicio } from './componentes/inicio/inicio';
import { RegistroPedido } from './componentes/registro-pedido/registro-pedido';

export const routes: Routes = [
  { path: '', redirectTo: 'inicio', pathMatch: 'full' },
  { 
    path: 'inicio', 
    loadComponent: () => import('./componentes/inicio/inicio').then((c) => c.Inicio) 
  },
  { 
    path: 'registro-pedido', 
    loadComponent: () => import('./componentes/registro-pedido/registro-pedido').then((c) => c.RegistroPedido) 
  },
  { 
    path: 'ventas', 
    loadComponent: () => import('./componentes/ventas/ventas').then((c) => c.Ventas) 
  },
  { path: '**', redirectTo: '' }
];