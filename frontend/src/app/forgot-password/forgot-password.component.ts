

import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';

@Component({
  selector: 'app-forgot-password',
  templateUrl: './forgot-password.component.html',
  styleUrls: ['./forgot-password.component.css']
})
export class ForgotPasswordComponent {

  email = '';
  otp = '';
  password = '';
  confirmPassword = '';

  step = 1;

  apiForgot = 'http://127.0.0.1:8000/api/forgot-password/';
  apiReset = 'http://127.0.0.1:8000/api/reset-password/';

  constructor(private http: HttpClient, private router: Router) {}

  sendOtp() {

    this.http.post(this.apiForgot, { email: this.email })
      .subscribe({
        next: () => {
          alert("OTP sent to email");
          this.step = 2;
        },
        error: (err) => {
          alert(err.error.error);
        }
      });

  }

  resetPassword() {

    if (this.password !== this.confirmPassword) {
      alert("Passwords do not match");
      return;
    }

    const body = {
      email: this.email,
      otp: this.otp,
      password: this.password
    };

    this.http.post(this.apiReset, body)
      .subscribe({
        next: () => {
          alert("Password reset successful");
          this.router.navigate(['/login']);
        },
        error: (err) => {
          alert(err.error.error);
        }
      });

  }

}
