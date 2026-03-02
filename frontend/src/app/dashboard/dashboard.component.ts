import { Component, OnInit } from '@angular/core';
import { CompareService, CompareResult } from '../services/compare.service';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit {

  resumes: any[] = [];
  jobs: any[] = [];

  selectedResumeId?: number;
  selectedJobId?: number;

  result?: CompareResult;

  selectedFile?: File;
  resumeTitle = '';

  jobTitle = '';
  jobText = '';

  currentTheme: string = 'light';

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

  

  onFileSelected(event: any) {
    this.selectedFile = event.target.files[0];
  }
  
  uploadResume() {
    if (!this.selectedFile || !this.resumeTitle) return;
  
    const formData = new FormData();
    formData.append('file', this.selectedFile);
    formData.append('title', this.resumeTitle);
  
    this.http.post(`${this.apiUrl}/resumes/`, formData)
      .subscribe(() => {
        this.loadResumes(); // refresh list
        this.resumeTitle = '';
      });
  }
  
  uploadJob() {
    const data = {
      title: this.jobTitle,
      description: this.jobText
    };
  
    this.http.post(`${this.apiUrl}/jobs/`, data)
      .subscribe(() => {
        this.loadJobs(); // refresh list
        this.jobTitle = '';
        this.jobText = '';
      });
  }

  compare() {
    if (!this.selectedResumeId || !this.selectedJobId) return;

    this.compareService.compare(this.selectedResumeId, this.selectedJobId)
      .subscribe(res => {
        this.result = res;
      });
  }

  toggleTheme() {
    this.currentTheme =
      this.currentTheme === 'light' ? 'dark' : 'light';
  }
}