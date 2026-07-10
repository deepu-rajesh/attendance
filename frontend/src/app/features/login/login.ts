import { Component, NgZone } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';
import { AuthService } from '../../core/services/auth';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, RouterModule],
  templateUrl: './login.html',
  styleUrls: ['./login.css']
})
export class Login {
  loginForm: FormGroup;
  error: string = '';

  constructor(
    private fb: FormBuilder,
    private authService: AuthService,
    private router: Router,
    private ngZone: NgZone
  ) {
    this.loginForm = this.fb.group({
      username: ['', Validators.required],
      password: ['', Validators.required]
    });
  }

  onSubmit() {
    if (this.loginForm.valid) {
      this.authService.login(this.loginForm.value).subscribe({
        next: () => {
          this.authService.currentUser$.subscribe(user => {
            if (user) {
              this.ngZone.run(() => {
                if (user.role === 'employee') this.router.navigate(['/employee']);
                else if (user.role === 'manager') this.router.navigate(['/manager']);
                else if (user.role === 'admin') this.router.navigate(['/admin']);
              });
            }
          });
        },
        error: () => {
          this.error = 'Invalid credentials';
        }
      });
    }
  }
}
