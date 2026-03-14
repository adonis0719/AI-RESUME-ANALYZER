import { Component } from '@angular/core';
import { AuthService } from '../services/auth.service';
import { Router } from '@angular/router'; 

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css'] 
})
export class LoginComponent {

  username = '';
  password = '';
  loading = false;
  showPassword = false;

  constructor(
    private authService: AuthService,
    private router: Router
    ) {}

  login() {
    this.loading = true;
    this.authService.login(this.username, this.password)
      .subscribe(
        (response: any) => {
          this.loading = false;
          this.authService.saveToken(response.access, response.is_admin);
            if (response.is_admin) {
              this.router.navigate(['/admin-dashboard']);
            }
            else{
              this.router.navigate(['/dashboard']);
            }

          this.authService.getResumes().subscribe(
            res => console.log("Resumes:", res),
            err => console.log("Resume error:", err)
          );

        },
        (error) => {
          this.loading = false;
          alert('Login failed');
        }
      );
  }
}