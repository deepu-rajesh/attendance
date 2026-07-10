import { Component, OnInit } from '@angular/core';
import { CommonModule, DatePipe } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { ApiService } from '../../core/services/api';
import { AuthService } from '../../core/services/auth';
import { Router } from '@angular/router';
import { ChangeDetectorRef } from '@angular/core';

@Component({
  selector: 'app-employee-dashboard',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, DatePipe],
  templateUrl: './employee-dashboard.html',
  styleUrls: ['./employee-dashboard.css']
})
export class EmployeeDashboard implements OnInit {
  attendanceRecords: any[] = [];
  leaveRequests: any[] = [];
  leaveTypes: any[] = [];
  leaveForm: FormGroup;
  isCheckedIn: boolean = false;

  constructor(
    private api: ApiService,
    private auth: AuthService,
    private fb: FormBuilder,
    private router: Router,
    private cdr: ChangeDetectorRef
  ) {
    this.leaveForm = this.fb.group({
      leave_type: ['', Validators.required],
      start_date: ['', Validators.required],
      end_date: ['', Validators.required],
      reason: ['', Validators.required]
    });
  }

  ngOnInit() {
    this.loadData();
  }

  loadData() {
    this.api.getAttendance().subscribe(data => {
      this.attendanceRecords = data;
      const today = new Date().toISOString().split('T')[0];
      const todayRecord = data.find((r: any) => r.date === today);
      this.isCheckedIn = todayRecord && !todayRecord.check_out;
      this.cdr.detectChanges();
    });

    this.api.getLeaveRequests().subscribe(data => {
      this.leaveRequests = data;
      this.cdr.detectChanges();
    });
    this.api.getLeaveTypes().subscribe(data => {
      this.leaveTypes = data;
      this.cdr.detectChanges();
    });
  }

  checkIn() {
    this.api.checkIn().subscribe(() => this.loadData());
  }

  checkOut() {
    this.api.checkOut().subscribe(() => this.loadData());
  }

  submitLeave() {
    if (this.leaveForm.valid) {
      this.api.applyLeave(this.leaveForm.value).subscribe(() => {
        this.leaveForm.reset();
        this.loadData();
      });
    }
  }

  logout() {
    this.auth.logout();
    this.router.navigate(['/login']);
  }
}
