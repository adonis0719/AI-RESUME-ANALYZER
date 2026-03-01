import { Component, OnInit } from '@angular/core';
import { CompareService, CompareResult } from '../services/compare.service';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html'
})
export class DashboardComponent implements OnInit {

  resumes: any[] = [];
  jobs: any[] = [];

  selectedResumeId?: number;
  selectedJobId?: number;

  result?: CompareResult;

  private apiUrl = 'http://127.0.0.1:8000/api';

  constructor(
    private http: HttpClient,
    private compareService: CompareService
  ) {}

  ngOnInit() {
    this.loadResumes();
    this.loadJobs();
  }

  loadResumes() {
    this.http.get<any[]>(`${this.apiUrl}/resumes/`)
      .subscribe(res => {
        this.resumes = res;
      });
  }

  loadJobs() {
    this.http.get<any[]>(`${this.apiUrl}/jobs/`)
      .subscribe(res => {
        this.jobs = res;
      });
  }

  compare() {
    if (!this.selectedResumeId || !this.selectedJobId) return;

    this.compareService.compare(this.selectedResumeId, this.selectedJobId)
      .subscribe(res => {
        this.result = res;
      });
  }
}