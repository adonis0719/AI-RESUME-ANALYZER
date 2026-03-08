// import { Component } from '@angular/core';

// @Component({
//   selector: 'app-recruiter-details',
//   templateUrl: './recruiter-details.component.html',
//   styleUrls: ['./recruiter-details.component.css']
// })
// export class RecruiterDetailsComponent {

// }

import { Component, OnInit } from '@angular/core';

@Component({
selector: 'app-recruiter-details',
templateUrl: './recruiter-details.component.html',
styleUrls: ['./recruiter-details.component.css']
})

export class RecruiterDetailsComponent implements OnInit {

resume: any;
interviewQuestions: string[] = [];

ngOnInit(){

const data = localStorage.getItem("resumeDetails");

if (data) {
  this.resume = JSON.parse(data);
  this.interviewQuestions = this.resume?.details?.interview_questions || [];
}

// Ensure details page always starts from top
window.scrollTo({ top: 0, left: 0, behavior: 'auto' });

}

getMatched(value: any) {
  return value?.matched || [];
}

getMissing(value: any) {
  return value?.missing || [];
}

getScoreLabel(score: number) {
  if (score >= 90) return 'Excellent Match';
  if (score >= 70) return 'Good Match';
  if (score >= 50) return 'Average Match';
  return 'Poor Match';
}

copyToClipboard(text: string) {
  navigator.clipboard?.writeText(text).then(() => {
    alert('Copied to clipboard');
  });
}

getResumeUrl() {
  return this.resume?.file_url ? 'http://127.0.0.1:8000' + this.resume.file_url : '#';
}

getDisplayName(name: string) {
  if (!name) return 'Resume';
  return name.replace(/\.(pdf|docx?)$/i, '') || 'Resume';
}

getCategoryPct(value: any) {
  return value?.percentage ?? 0;
}

}
