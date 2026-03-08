import { Component, OnInit } from '@angular/core';
import { CompareService, CompareResult } from '../services/compare.service';
import { HttpClient } from '@angular/common/http';
import { ThemeService } from '../services/theme.service';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit {

  loading = false;

  animatedScore: number = 0
  resumes: any[] = [];
  jobs: any[] = [];

  selectedResumeId?: number;
  selectedJobId?: number;

  result?: CompareResult;

  selectedFile?: File;
  resumeTitle = '';

  jobTitle = '';
  jobText = '';

  private apiUrl = 'http://127.0.0.1:8000/api';

  constructor(
    private http: HttpClient,
    private compareService: CompareService,
    public themeService: ThemeService
  ) {}

  get currentTheme() {
    return this.themeService.getTheme();
  }

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

    if (!this.selectedResumeId || !this.selectedJobId) {
      alert("Please select both resume and job.");
      return;
    }

    this.loading = true;

    this.compareService
      .compare(this.selectedResumeId, this.selectedJobId)
      .subscribe({
        next: (res) => {
          this.result = res;
          this.loading = false;

          this.animatedScore = 0;
          const target = res.overall_match_percentage;

          const step = target / 40;   // controls animation smoothness

          const interval = setInterval(() => {

            if (this.animatedScore < target) {
              this.animatedScore = +(this.animatedScore + step).toFixed(2);
            } else {
              this.animatedScore = target;
              clearInterval(interval);
            }

          }, 20);

          setTimeout(() => {
            const el = document.getElementById("resultSection");
            if (el) {
              el.scrollIntoView({ behavior: "smooth", block: "start" });
            }
          }, 100);
        },
        error: (err) => {
          console.log(err);
          this.loading = false;
        }
      });

  }

  viewResume(filePath: string) {
    
    const url = "http://127.0.0.1:8000" + filePath;

    window.open(url, "_blank");

  }


  

  deleteResume(id: number) {


    if (!confirm("Delete this resume?")) return;

    this.http.delete(`${this.apiUrl}/resumes/${id}/`)
      .subscribe(() => {
        this.loadResumes();
      });
  }

  deleteJob(id: number) {

    if (!confirm("Delete this job description?")) return;

    this.http.delete(`${this.apiUrl}/jobs/${id}/`)
      .subscribe(() => {
        this.loadJobs();
      });
  }
  
  getScoreLabel(score: number) {

    if (score >= 90) return "Excellent Match";
    if (score >= 70) return "Good Match";
    if (score >= 50) return "Average Match";

    return "Poor Match";

  }


  getScoreColor(score: number) {

    if (score >= 90) return "bg-success";
    if (score >= 70) return "bg-primary";
    if (score >= 50) return "bg-warning";

    return "bg-danger";

  }

  toggleTheme() {
    this.themeService.toggleTheme();
  }

  scrollToCompare() {
    const el = document.getElementById('compareSection');
    if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
}