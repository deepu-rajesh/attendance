import { Component, OnInit } from '@angular/core';
import { CommonModule, DatePipe } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../../core/services/api';
import { AuthService } from '../../core/services/auth';
import { Router } from '@angular/router';
import { ChangeDetectorRef } from '@angular/core';

@Component({
  selector: 'app-manager-dashboard',
  standalone: true,
  imports: [CommonModule, DatePipe, FormsModule],
  templateUrl: './manager-dashboard.html',
  styleUrls: ['./manager-dashboard.css']
})
export class ManagerDashboard implements OnInit {
  attendanceRecords: any[] = [];
  leaveRequests: any[] = [];
  users: any[] = [];
  activeTab: 'attendance' | 'leave' | 'users' = 'attendance';
  remarks: { [key: number]: string } = {};
  filterDate: string = '';

  constructor(
    private api: ApiService,
    private auth: AuthService,
    private router: Router,
    private cdr: ChangeDetectorRef
  ) {}

  get filteredAttendance() {
    if (!this.filterDate) {
      return this.attendanceRecords;
    }
    return this.attendanceRecords.filter(record => record.date === this.filterDate);
  }

  ngOnInit() {
    this.loadData();
  }

  loadData() {
    if (this.activeTab === 'attendance') {
      this.api.getAttendance().subscribe(data => {
        this.attendanceRecords = data;
        this.cdr.detectChanges();
      });
    } else if (this.activeTab === 'users') {
      this.api.getUsers().subscribe(data => {
        this.users = data;
        this.cdr.detectChanges();
      });
    } else if (this.activeTab === 'leave') {
      this.api.getLeaveRequests().subscribe(data => {
        this.leaveRequests = data;
        this.leaveRequests.forEach((req: any) => {
           if (this.remarks[req.id] === undefined) {
              this.remarks[req.id] = req.remarks || '';
           }
        });
        this.cdr.detectChanges();
      });
    }
  }

  setActiveTab(tab: 'attendance' | 'leave' | 'users') {
    this.activeTab = tab;
    this.loadData();
  }

  updateLeaveStatus(id: number, status: string) {
    this.api.updateLeaveStatus(id, status, this.remarks[id]).subscribe(() => this.loadData());
  }

  toggleUserStatus(id: number) {
    this.api.toggleUserStatus(id).subscribe(() => this.loadData());
  }

  logout() {
    this.auth.logout();
    this.router.navigate(['/login']);
  }
}
