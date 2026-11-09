import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { RouterLink } from '@angular/router';

@Component({
  imports: [CommonModule, RouterModule, RouterLink],
  standalone: true,
  selector: 'app-inicio',
  styleUrl: './inicio.css',
  templateUrl: './inicio.html',
})

export class Inicio 
{
  
}
