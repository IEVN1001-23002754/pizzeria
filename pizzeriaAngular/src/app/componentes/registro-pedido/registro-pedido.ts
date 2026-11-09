import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { PedidoService } from '../../pedido.service';
import { PizzaTemporal } from '../pizzeria-interfaz';

@Component({
  imports: [CommonModule, ReactiveFormsModule, RouterLink],
  standalone: true,
  selector: 'app-registro-pedido',
  styleUrl: './registro-pedido.css',
  templateUrl: './registro-pedido.html',
})
export class RegistroPedido implements OnInit {
  pedidoForm!: FormGroup;
  listaTemporal: PizzaTemporal[] = [];
  totalGeneral: number = 0;
  mensajeExito: string = '';
  
  // Control del Modal de Ticket
  mostrarModalTicket: boolean = false;
  datosTicket: any = null;

  public Array = Array;

  constructor(
    private fb: FormBuilder, 
    private pedidoService: PedidoService,
    private cdr: ChangeDetectorRef
  ) {}

  ngOnInit(): void {
    this.pedidoForm = this.fb.group({
      nombre: [this.pedidoService.datosCliente.nombre, [Validators.required]],
      direccion: [this.pedidoService.datosCliente.direccion, [Validators.required]],
      telefono: [this.pedidoService.datosCliente.telefono, [Validators.required, Validators.pattern(/^[0-9\-]{1,20}$/)]],
      fecha_pedido: [this.pedidoService.datosCliente.fecha_pedido, [Validators.required]],
      tamano: ['', [Validators.required]],
      ingredientes: [[]],
      num_pizzas: [1, [Validators.required, Validators.min(1)]]
    });

    this.cargarTemporal();
  }

  onCheckboxChange(e: any) {
    const ingredientesField = this.pedidoForm.get('ingredientes');
    if (!ingredientesField) return;
    
    const currentValues = [...ingredientesField.value];
    if (e.target.checked) {
      currentValues.push(e.target.value);
    } else {
      const index = currentValues.indexOf(e.target.value);
      if (index > -1) {
        currentValues.splice(index, 1);
      }
    }
    ingredientesField.setValue(currentValues);
  }

  cargarTemporal() {
    this.pedidoService.obtenerTemporal().subscribe({
      next: (res: any) => {
        if (Array.isArray(res)) {
          this.listaTemporal = res;
        } else if (res && Array.isArray(res.pizzas)) {
          this.listaTemporal = res.pizzas;
        } else if (res && Array.isArray(res.temporal)) {
          this.listaTemporal = res.temporal;
        } else {
          this.listaTemporal = [];
        }
        this.calcularTotal();
        this.cdr.detectChanges();
      },
      error: (err: any) => console.error('Error al cargar temporal:', err)
    });
  }

  calcularTotal() {
    this.totalGeneral = this.listaTemporal.reduce((acc, item) => acc + (Number(item.subtotal) || 0), 0);
  }

  agregarPizza() {
    if (this.pedidoForm.invalid) return;

    const formValues = this.pedidoForm.value;
    
    this.pedidoService.datosCliente = {
      nombre: formValues.nombre,
      direccion: formValues.direccion,
      telefono: formValues.telefono,
      fecha_pedido: formValues.fecha_pedido
    };

    const payload = {
      tamano: formValues.tamano,
      ingredientes: formValues.ingredientes,
      num_pizzas: formValues.num_pizzas
    };

    this.pedidoService.agregarTemporal(payload).subscribe({
      next: (res: any) => {
        this.mensajeExito = `¡Pizza agregada con éxito! Subtotal: $${res.subtotal}`;
        
        this.pedidoForm.patchValue({
          tamano: '',
          ingredientes: [],
          num_pizzas: 1
        });

        const checkboxes = document.querySelectorAll('input[type="checkbox"]') as NodeListOf<HTMLInputElement>;
        checkboxes.forEach(cb => cb.checked = false);

        this.cargarTemporal();
        this.cdr.detectChanges(); // Forzamos el renderizado inmediato en pantalla
      },
      error: (err: any) => console.error(err)
    });
  }

  quitarPizza(id?: number) {
    if (!id) return;
    this.pedidoService.quitarTemporal(id).subscribe({
      next: () => this.cargarTemporal(),
      error: (err: any) => console.error('Error al quitar:', err)
    });
  }

  terminarPedido() {
    const formValues = this.pedidoForm.value;
    const payload = {
      nombre: formValues.nombre,
      direccion: formValues.direccion,
      telefono: formValues.telefono,
      fecha_pedido: formValues.fecha_pedido,
      total: this.totalGeneral
    };

    this.pedidoService.terminarPedido(payload).subscribe({
      next: (res: any) => {
        this.datosTicket = {
          folio: res.id_pedido || 'OK',
          cliente: {
            nombre: formValues.nombre,
            direccion: formValues.direccion,
            telefono: formValues.telefono
          },
          pizzas: [...this.listaTemporal],
          total: this.totalGeneral,
          fecha: new Date().toLocaleString()
        };

        this.pedidoForm.reset({
          nombre: '',
          direccion: '',
          telefono: '',
          fecha_pedido: new Date().toISOString().split('T')[0],
          tamano: '',
          ingredientes: [],
          num_pizzas: 1
        });

        this.pedidoService.datosCliente = {
          nombre: '',
          direccion: '',
          telefono: '',
          fecha_pedido: new Date().toISOString().split('T')[0]
        };

        this.listaTemporal = [];
        this.totalGeneral = 0;
        this.mensajeExito = '';

        this.mostrarModalTicket = true;
        this.cdr.detectChanges();
      },
      error: (err: any) => console.error('Error al terminar pedido:', err)
    });
  }

  cerrarModalTicket() {
    this.mostrarModalTicket = false;
    this.datosTicket = null;
    this.cdr.detectChanges();
  }

  nuevoPedido() {
    if (confirm('¿Estás seguro de iniciar un nuevo pedido? Se descartarán las pizzas actuales.')) {
      this.pedidoService.vaciarTemporal().subscribe({
        next: () => {
          this.pedidoForm.reset({
            nombre: '',
            direccion: '',
            telefono: '',
            fecha_pedido: new Date().toISOString().split('T')[0],
            tamano: '',
            ingredientes: [],
            num_pizzas: 1
          });
          this.listaTemporal = [];
          this.totalGeneral = 0;
          this.mensajeExito = '';
          this.cdr.detectChanges();
        },
        error: (err: any) => console.error('Error al vaciar temporal:', err)
      });
    }
  }
}