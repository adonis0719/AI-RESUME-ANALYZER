import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-admin-resumes',
  templateUrl: './admin-resumes.component.html',
  styleUrls: ['./admin-resumes.component.css']
})
export class AdminResumesComponent implements OnInit {

  apiUrl = 'http://127.0.0.1:8000/api/admin';
  resumes: any[] = [];
  error = '';

  constructor(private http: HttpClient) {}

  ngOnInit() {
    this.loadResumes();
  }

  loadResumes() {
    this.http.get<any[]>(`${this.apiUrl}/resumes/`).subscribe({
      next: (res) => { this.resumes = res; },
      error: (err) => { this.error = err?.error?.error || 'Failed to load resumes'; }
    });
  }

  deleteResume(id: number) {
    if (!confirm('Delete this resume?')) return;
    this.http.delete(`${this.apiUrl}/resumes/${id}/`).subscribe({
      next: () => this.loadResumes(),
      error: (err) => alert(err?.error?.error || 'Failed to delete resume')
    });
  }
}
