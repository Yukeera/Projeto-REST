import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MatTableModule } from '@angular/material/table';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatDialogModule } from '@angular/material/dialog';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { MatChipsModule } from '@angular/material/chips';
import { MatCardModule } from '@angular/material/card';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { GatewayService } from '../../services/gateway.service';

@Component({
  selector: 'app-deliveries',
  imports: [
    CommonModule,
    ReactiveFormsModule,
    MatTableModule,
    MatButtonModule,
    MatIconModule,
    MatDialogModule,
    MatFormFieldModule,
    MatInputModule,
    MatSelectModule,
    MatChipsModule,
    MatCardModule,
    MatSnackBarModule,
  ],
  templateUrl: './deliveries.html',
  styleUrl: './deliveries.css'
})
export class Deliveries implements OnInit {
  deliveries: any[] = [];
  vehicles: any[] = [];
  showForm = false;
  editingDelivery: any = null; // guarda a entrega sendo editada
  form: FormGroup;

  displayedColumns = ['tracking_code', 'recipient_name', 'origin', 'destination', 'status', 'actions'];

  statusLabels: Record<string, string> = {
    created: 'Criada',
    in_transit: 'Em trânsito',
    delivered: 'Entregue',
    cancelled: 'Cancelada',
  };

  statusColors: Record<string, string> = {
    created: 'primary',
    in_transit: 'accent',
    delivered: 'warn',
    cancelled: '',
  };

  constructor(
    private gateway: GatewayService,
    private fb: FormBuilder,
    private snackBar: MatSnackBar,
  ) {
    this.form = this.fb.group({
      origin_address: ['', Validators.required],
      destination_address: ['', Validators.required],
      recipient_name: ['', Validators.required],
      recipient_phone: ['', Validators.required],
      cargo_weight_kg: ['', Validators.required],
      vehicle: [null],
    });
  }

  ngOnInit() {
    this.loadDeliveries();
    this.loadVehicles();
  }

  loadDeliveries() {
    this.gateway.getDeliveries().subscribe({
      next: (data) => this.deliveries = [...data],
      error: () => this.snackBar.open('Erro ao carregar entregas.', 'Fechar', { duration: 3000 })
    });
  }

  loadVehicles() {
    this.gateway.getVehicles().subscribe({
      next: (data) => this.vehicles = [...data],
      error: () => {}
    });
  }

  openCreateForm() {
    this.editingDelivery = null;
    this.form.reset();
    this.showForm = true;
  }

  openEditForm(delivery: any) {
    this.editingDelivery = delivery;
    // preenche o formulário com os dados da entrega atual
    this.form.patchValue({
      origin_address: delivery.origin_address,
      destination_address: delivery.destination_address,
      recipient_name: delivery.recipient_name,
      recipient_phone: delivery.recipient_phone,
      cargo_weight_kg: delivery.cargo_weight_kg,
      vehicle: delivery.vehicle,
    });
    this.showForm = true;
  }

  saveDelivery() {
    if (this.form.invalid) return;

    if (this.editingDelivery) {
      // modo edição → PUT
      this.gateway.updateDelivery(this.editingDelivery.id, this.form.value).subscribe({
        next: () => {
          this.snackBar.open('Entrega atualizada com sucesso!', 'Fechar', { duration: 3000 });
          this.showForm = false;
          this.editingDelivery = null;
          this.loadDeliveries();
        },
        error: () => this.snackBar.open('Erro ao atualizar entrega.', 'Fechar', { duration: 3000 })
      });
    } else {
      // modo criação → POST
      this.gateway.createDelivery(this.form.value).subscribe({
        next: () => {
          this.snackBar.open('Entrega criada com sucesso!', 'Fechar', { duration: 3000 });
          this.showForm = false;
          this.form.reset();
          this.loadDeliveries();
        },
        error: () => this.snackBar.open('Erro ao criar entrega.', 'Fechar', { duration: 3000 })
      });
    }
  }

  executeAction(delivery: any, actionKey: string) {
    const url = delivery.links[actionKey];
    if (!url) return;

    this.gateway.executeAction(url).subscribe({
      next: () => {
        this.snackBar.open('Ação executada com sucesso!', 'Fechar', { duration: 3000 });
        this.loadDeliveries();
      },
      error: (err) => {
        const msg = err.error?.error || 'Erro ao executar ação.';
        this.snackBar.open(msg, 'Fechar', { duration: 4000 });
      }
    });
  }

  deleteDelivery(id: number) {
    if (!confirm('Deseja remover esta entrega?')) return;
    this.gateway.deleteDelivery(id).subscribe({
      next: () => {
        this.snackBar.open('Entrega removida.', 'Fechar', { duration: 3000 });
        this.loadDeliveries();
      }
    });
  }

  getActionLabel(action: string): string {
    const labels: Record<string, string> = {
      start: 'Iniciar',
      complete: 'Concluir',
      cancel: 'Cancelar',
    };
    return labels[action] || action;
  }

  getActionIcon(action: string): string {
    const icons: Record<string, string> = {
      start: 'play_arrow',
      complete: 'check_circle',
      cancel: 'cancel',
    };
    return icons[action] || 'bolt';
  }

  getHateoasActions(delivery: any): string[] {
    if (!delivery.links) return [];
    return Object.keys(delivery.links).filter(k => k !== 'self' && k !== 'vehicle');
  }
}
