import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../../core/services/api';
import { AuthService } from '../../core/services/auth';
import { Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { ChangeDetectorRef } from '@angular/core';

@Component({
  selector: 'app-admin-dashboard',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './admin-dashboard.html'
})
export class AdminDashboard implements OnInit {
  users: any[] = [];
  leaveTypes: any[] = [];
  newLeaveTypeName: string = '';
  activeTab: 'users' | 'leave_types' | 'reports' = 'users';
  reportStartDate: string = '';
  reportEndDate: string = '';
  private apiUrl = 'http://127.0.0.1:8000/api/core';

  constructor(
    private api: ApiService,
    private auth: AuthService,
    private http: HttpClient,
    private router: Router,
    private cdr: ChangeDetectorRef
  ) {}

  ngOnInit() {
    this.loadData();
  }

  loadData() {
    this.api.getLeaveTypes().subscribe(data => {
      this.leaveTypes = data;
      this.cdr.detectChanges();
    });
    this.http.get<any[]>(`${this.apiUrl}/users/`).subscribe(data => {
      this.users = data;
      this.cdr.detectChanges();
    });
  }

  toggleUserStatus(userId: number) {
    this.api.toggleUserStatus(userId).subscribe(() => {
      this.loadData();
    });
  }

  verifyUser(userId: number) {
    this.http.patch(`${this.apiUrl}/users/${userId}/verify/`, {}).subscribe(() => {
      this.loadData();
    });
  }

  generateReport() {
    this.api.generateReport(this.reportStartDate, this.reportEndDate).subscribe((blob: Blob) => {
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `attendance_report_${new Date().toISOString().split('T')[0]}.pdf`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      a.remove();
    }, error => {
      console.error('Error generating report:', error);
      alert('Failed to generate report. Please try again.');
    });
  }

  addLeaveType() {
    if (this.newLeaveTypeName.trim()) {
      this.api.addLeaveType(this.newLeaveTypeName.trim()).subscribe(() => {
        this.newLeaveTypeName = '';
        this.loadData();
      });
    }
  }

  deleteLeaveType(id: number) {
    if (confirm('Are you sure you want to delete this leave type?')) {
      this.api.deleteLeaveType(id).subscribe(() => {
        this.loadData();
      });
    }
  }

  logout() {
    this.auth.logout();
    this.router.navigate(['/login']);
  }
}
