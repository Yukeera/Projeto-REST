import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MatTableModule } from '@angular/material/table';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { MatChipsModule } from '@angular/material/chips';
import { MatCardModule } from '@angular/material/card';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { GatewayService } from '../../services/gateway.service';

@Component({
  selector: 'app-drivers',
  imports: [
    CommonModule,
    ReactiveFormsModule,
    MatTableModule,
    MatButtonModule,
    MatIconModule,
    MatFormFieldModule,
    MatInputModule,
    MatSelectModule,
    MatChipsModule,
    MatCardModule,
    MatSnackBarModule,
  ],
  templateUrl: './drivers.html',
  styleUrl: './drivers.css'
})
export class Drivers implements OnInit {
  drivers: any[] = [];
  showForm = false;
  editingDriver: any = null;
  form: FormGroup;

  displayedColumns = ['name', 'license_number', 'phone', 'status', 'actions'];

  statusLabels: Record<string, string> = {
    available: 'Disponível',
    on_route: 'Em rota',
    unavailable: 'Indisponível',
  };

  statusColors: Record<string, string> = {
    available: 'primary',
    on_route: 'accent',
    unavailable: 'warn',
  };

  constructor(
    private gateway: GatewayService,
    private fb: FormBuilder,
    private snackBar: MatSnackBar,
  ) {
    this.form = this.fb.group({
      name: ['', Validators.required],
      license_number: ['', Validators.required],
      phone: ['', Validators.required],
      status: ['available', Validators.required],
    });
  }

  ngOnInit() {
    this.loadDrivers();
  }

  loadDrivers() {
    this.gateway.getDrivers().subscribe({
      next: (data) => this.drivers = [...data],
      error: () => this.snackBar.open('Erro ao carregar motoristas.', 'Fechar', { duration: 3000 })
    });
  }

  openCreateForm() {
    this.editingDriver = null;
    this.form.reset({ status: 'available' });
    this.showForm = true;
  }

  openEditForm(driver: any) {
    this.editingDriver = driver;
    this.form.patchValue({
      name: driver.name,
      license_number: driver.license_number,
      phone: driver.phone,
      status: driver.status,
    });
    this.showForm = true;
  }

  saveDriver() {
    if (this.form.invalid) return;

    if (this.editingDriver) {
      this.gateway.updateDriver(this.editingDriver.id, this.form.value).subscribe({
        next: () => {
          this.snackBar.open('Motorista atualizado!', 'Fechar', { duration: 3000 });
          this.showForm = false;
          this.loadDrivers();
        },
        error: () => this.snackBar.open('Erro ao atualizar motorista.', 'Fechar', { duration: 3000 })
      });
    } else {
      this.gateway.createDriver(this.form.value).subscribe({
        next: () => {
          this.snackBar.open('Motorista criado!', 'Fechar', { duration: 3000 });
          this.showForm = false;
          this.form.reset({ status: 'available' });
          this.loadDrivers();
        },
        error: () => this.snackBar.open('Erro ao criar motorista.', 'Fechar', { duration: 3000 })
      });
    }
  }

  deleteDriver(id: number) {
    if (!confirm('Deseja remover este motorista?')) return;
    this.gateway.deleteDriver(id).subscribe({
      next: () => {
        this.snackBar.open('Motorista removido.', 'Fechar', { duration: 3000 });
        this.loadDrivers();
      }
    });
  }
}
