import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

const GATEWAY_URL = 'http://127.0.0.1:8000/gateway';

@Injectable({
  providedIn: 'root'
})
export class GatewayService {

  constructor(private http: HttpClient) {}

  // ─── DRIVERS ──────────────────────────────────────────────────────────────
  getDrivers(): Observable<any[]> {
    return this.http.get<any[]>(`${GATEWAY_URL}/drivers/`);
  }

  getDriver(id: number): Observable<any> {
    return this.http.get<any>(`${GATEWAY_URL}/drivers/${id}/`);
  }

  createDriver(data: any): Observable<any> {
    return this.http.post<any>(`${GATEWAY_URL}/drivers/`, data);
  }

  updateDriver(id: number, data: any): Observable<any> {
    return this.http.put<any>(`${GATEWAY_URL}/drivers/${id}/`, data);
  }

  deleteDriver(id: number): Observable<any> {
    return this.http.delete<any>(`${GATEWAY_URL}/drivers/${id}/`);
  }

  // ─── VEHICLES ─────────────────────────────────────────────────────────────
  getVehicles(): Observable<any[]> {
    return this.http.get<any[]>(`${GATEWAY_URL}/vehicles/`);
  }

  getVehicle(id: number): Observable<any> {
    return this.http.get<any>(`${GATEWAY_URL}/vehicles/${id}/`);
  }

  createVehicle(data: any): Observable<any> {
    return this.http.post<any>(`${GATEWAY_URL}/vehicles/`, data);
  }

  updateVehicle(id: number, data: any): Observable<any> {
    return this.http.put<any>(`${GATEWAY_URL}/vehicles/${id}/`, data);
  }

  deleteVehicle(id: number): Observable<any> {
    return this.http.delete<any>(`${GATEWAY_URL}/vehicles/${id}/`);
  }

  // ─── DELIVERIES ───────────────────────────────────────────────────────────
  getDeliveries(): Observable<any[]> {
    return this.http.get<any[]>(`${GATEWAY_URL}/deliveries/`);
  }

  getDelivery(id: number): Observable<any> {
    return this.http.get<any>(`${GATEWAY_URL}/deliveries/${id}/`);
  }

  createDelivery(data: any): Observable<any> {
    return this.http.post<any>(`${GATEWAY_URL}/deliveries/`, data);
  }

  updateDelivery(id: number, data: any): Observable<any> {
    return this.http.put<any>(`${GATEWAY_URL}/deliveries/${id}/`, data);
  }

  deleteDelivery(id: number): Observable<any> {
    return this.http.delete<any>(`${GATEWAY_URL}/deliveries/${id}/`);
  }

  // ─── HATEOAS ACTIONS ──────────────────────────────────────────────────────
  // Executa uma ação usando o link HATEOAS retornado pela API
  executeAction(url: string): Observable<any> {
    return this.http.post<any>(url, {});
  }
}
