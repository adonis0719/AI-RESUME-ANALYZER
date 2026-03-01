import { Component } from '@angular/core';
import { AuthService } from '../services/auth.service';
import { Router } from '@angular/router'; 

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html'
})
export class LoginComponent {

  username = '';
  password = '';

  constructor(
    private authService: AuthService,
    private router: Router
    ) {}

  login() {

    this.authService.login(this.username, this.password)
      .subscribe(
        (response: any) => {

          console.log("Response:", response);
          this.authService.saveToken(response.access);
          this.router.navigate(['/dashboard']);

          this.authService.getResumes().subscribe(
            res => console.log("Resumes:", res),
            err => console.log("Resume error:", err)
          );

        },
        (error) => {
          console.log("Error:", error);
          alert('Login failed');
        }
      );
  }
}