import { Component, OnInit } from '@angular/core';
import { AuthService } from '../services/auth.service';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.css'] 
})
export class ProfileComponent implements OnInit {

  username = '';
  email = '';
  profile_name = '';
  currentPassword = '';
  newPassword = '';
  confirmPassword = '';
  loading = false;
  savingProfile = false;
  savingPassword = false;

  constructor(private authService: AuthService) {}

  ngOnInit() {
    this.loading = true;
    this.authService.getProfile().subscribe({
      next: (res: any) => {
        this.username = res.username;
        this.email = res.email;
        this.profile_name = res.profile_name;
        this.loading = false;
      },
      error: () => { this.loading = false; }
    });
  }

  updateProfile() {
    this.savingProfile = true;
    this.authService.updateProfile(this.username, this.profile_name).subscribe({
      next: () => {
        this.savingProfile = false;
        alert("Profile updated");
      },
      error: err => {
        this.savingProfile = false;
        alert(err.error?.error || "Update failed");
      }
    });
  }

  changePassword() {
    if (this.newPassword !== this.confirmPassword) {
      alert("Passwords do not match");
      return;
    }
    this.savingPassword = true;
    this.authService.changePassword(this.currentPassword, this.newPassword).subscribe({
      next: () => {
        this.savingPassword = false;
        alert("Password updated successfully");
      },
      error: err => {
        this.savingPassword = false;
        alert(err.error?.error || "Password update failed");
      }
    });
  }

}