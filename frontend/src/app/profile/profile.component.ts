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


  constructor(private authService: AuthService) {}

  ngOnInit() {

    this.authService.getProfile().subscribe((res: any) => {

      this.username = res.username;
      this.email = res.email;
      this.profile_name = res.profile_name;

    });

  }

  updateProfile() {

    this.authService.updateProfile(this.username, this.profile_name)
    .subscribe({
      next: () => alert("Profile updated"),
      error: err => alert(err.error.error)
    });

  }

  changePassword(){

    if(this.newPassword !== this.confirmPassword){
      alert("Passwords do not match");
      return;
    }

    this.authService.changePassword(this.currentPassword, this.newPassword)
    .subscribe({
      next: () => alert("Password updated successfully"),
      error: err => alert(err.error.error)
    });

  }

}