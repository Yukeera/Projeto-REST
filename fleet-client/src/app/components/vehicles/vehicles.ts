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
  selector: 'app-vehicles',
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
  templateUrl: './vehicles.html',
  styleUrl: './vehicles.css'
})
export class Vehicles implements OnInit {
  vehicles: any[] = [];
  drivers: any[] = [];
  showForm = false;
  editingVehicle: any = null;
  form: FormGroup;

  displayedColumns = ['license_plate', 'model', 'year', 'capacity', 'status', 'driver', 'actions'];

  statusLabels: Record<string, string> = {
    available: 'Disponível',
    in_use: 'Em uso',
    maintenance: 'Em manutenção',
  };

  statusColors: Record<string, string> = {
    available: 'primary',
    in_use: 'accent',
    maintenance: 'warn',
  };

  constructor(
    private gateway: GatewayService,
    private fb: FormBuilder,
    private snackBar: MatSnackBar,
  ) {
    this.form = this.fb.group({
      license_plate: ['', Validators.required],
      model: ['', Validators.required],
      year: ['', Validators.required],
      cargo_capacity_kg: ['', Validators.required],
      status: ['available', Validators.required],
      driver: [null],
    });
  }

  ngOnInit() {
    this.loadVehicles();
    this.loadDrivers();
  }

  loadVehicles() {
    this.gateway.getVehicles().subscribe({
      next: (data) => this.vehicles = [...data],
      error: () => this.snackBar.open('Erro ao carregar veículos.', 'Fechar', { duration: 3000 })
    });
  }

  loadDrivers() {
    this.gateway.getDrivers().subscribe({
      next: (data) => this.drivers = [...data],
      error: () => {}
    });
  }

  openCreateForm() {
    this.editingVehicle = null;
    this.form.reset({ status: 'available' });
    this.showForm = true;
  }

  openEditForm(vehicle: any) {
    this.editingVehicle = vehicle;
    this.form.patchValue({
      license_plate: vehicle.license_plate,
      model: vehicle.model,
      year: vehicle.year,
      cargo_capacity_kg: vehicle.cargo_capacity_kg,
      status: vehicle.status,
      driver: vehicle.driver,
    });
    this.showForm = true;
  }

  saveVehicle() {
    if (this.form.invalid) return;

    if (this.editingVehicle) {
      this.gateway.updateVehicle(this.editingVehicle.id, this.form.value).subscribe({
        next: () => {
          this.snackBar.open('Veículo atualizado!', 'Fechar', { duration: 3000 });
          this.showForm = false;
          this.loadVehicles();
        },
        error: () => this.snackBar.open('Erro ao atualizar veículo.', 'Fechar', { duration: 3000 })
      });
    } else {
      this.gateway.createVehicle(this.form.value).subscribe({
        next: () => {
          this.snackBar.open('Veículo criado!', 'Fechar', { duration: 3000 });
          this.showForm = false;
          this.form.reset({ status: 'available' });
          this.loadVehicles();
        },
        error: () => this.snackBar.open('Erro ao criar veículo.', 'Fechar', { duration: 3000 })
      });
    }
  }

  deleteVehicle(id: number) {
    if (!confirm('Deseja remover este veículo?')) return;
    this.gateway.deleteVehicle(id).subscribe({
      next: () => {
        this.snackBar.open('Veículo removido.', 'Fechar', { duration: 3000 });
        this.loadVehicles();
      }
    });
  }

  getDriverName(driverId: number): string {
    const driver = this.drivers.find(d => d.id === driverId);
    return driver ? driver.name : 'Sem motorista';
  }
}
