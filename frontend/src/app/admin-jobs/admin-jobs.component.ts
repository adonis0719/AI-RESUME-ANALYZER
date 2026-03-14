import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-admin-jobs',
  templateUrl: './admin-jobs.component.html',
  styleUrls: ['./admin-jobs.component.css']
})
export class AdminJobsComponent implements OnInit {

  apiUrl = 'http://127.0.0.1:8000/api/admin';
  jobs: any[] = [];
  error = '';

  constructor(private http: HttpClient) {}

  ngOnInit() {
    this.loadJobs();
  }

  loadJobs() {
    this.http.get<any[]>(`${this.apiUrl}/jobs/`).subscribe({
      next: (res) => { this.jobs = res; },
      error: (err) => { this.error = err?.error?.error || 'Failed to load jobs'; }
    });
  }

  deleteJob(id: number) {
    if (!confirm('Delete this job?')) return;
    this.http.delete(`${this.apiUrl}/jobs/${id}/`).subscribe({
      next: () => this.loadJobs(),
      error: (err) => alert(err?.error?.error || 'Failed to delete job')
    });
  }
}
