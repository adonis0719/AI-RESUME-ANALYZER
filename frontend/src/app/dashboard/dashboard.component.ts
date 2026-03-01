import { Component, OnInit } from '@angular/core';
import { AuthService } from '../services/auth.service';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit {

  resumes: any[] = [];

  constructor(private authService: AuthService) {}

  ngOnInit(): void {
    this.authService.getResumes().subscribe(
      (data: any) => {
        console.log("Resumes loaded:", data);
        this.resumes = data;
      },
      (error: any) => {
        console.log("Error loading resumes:", error);
      }
    );
  }
}