import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private apiUrl = 'http://127.0.0.1:8000/api/leaves';

  constructor(private http: HttpClient) { }

  // Attendance
  getAttendance(): Observable<any> {
    return this.http.get(`${this.apiUrl}/attendance/`);
  }

  checkIn(): Observable<any> {
    return this.http.post(`${this.apiUrl}/attendance/check_in/`, {});
  }

  checkOut(): Observable<any> {
    return this.http.post(`${this.apiUrl}/attendance/check_out/`, {});
  }

  // Leaves
  getLeaveRequests(): Observable<any> {
    return this.http.get(`${this.apiUrl}/leave-requests/`);
  }

  applyLeave(data: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/leave-requests/`, data);
  }
  
  getLeaveTypes(): Observable<any> {
    return this.http.get(`${this.apiUrl}/leave-types/`);
  }

  addLeaveType(name: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/leave-types/`, { name });
  }

  deleteLeaveType(id: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/leave-types/${id}/`);
  }

  updateLeaveStatus(id: number, status: string, remarks?: string): Observable<any> {
    return this.http.patch(`${this.apiUrl}/leave-requests/${id}/status/`, { status, remarks });
  }

  // Users
  getUsers(): Observable<any> {
    return this.http.get(`http://127.0.0.1:8000/api/core/users/`);
  }

  toggleUserStatus(id: number): Observable<any> {
    return this.http.patch(`http://127.0.0.1:8000/api/core/users/${id}/toggle_active/`, {});
  }

  // Reports
  generateReport(startDate: string, endDate: string): Observable<Blob> {
    const params: any = {};
    if (startDate) params.start_date = startDate;
    if (endDate) params.end_date = endDate;
    return this.http.get(`http://127.0.0.1:8000/api/core/report/`, { params, responseType: 'blob' });
  }
}
