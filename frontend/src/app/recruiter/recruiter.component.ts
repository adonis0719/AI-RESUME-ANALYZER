
import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';

@Component({
selector: 'app-recruiter',
templateUrl: './recruiter.component.html',
styleUrls: ['./recruiter.component.css']
})

export class RecruiterComponent implements OnInit {

ngOnInit(){

const data = localStorage.getItem("recruiterResults");

if(data){
this.results = JSON.parse(data);
}

}    

files: File[] = [];
jobDescription = '';
results: any[] = [];

api = 'http://127.0.0.1:8000/api/recruiter/analyze/';

constructor(private http: HttpClient, private router: Router) {}

onFileSelect(event: any) {

this.files = Array.from(event.target.files);

}

analyze() {

const formData = new FormData();

for (let file of this.files) {
formData.append('resumes', file);
}

formData.append('job_description', this.jobDescription);

this.http.post<any>(this.api, formData)
.subscribe(res => {

this.results = res.ranked_resumes;

localStorage.setItem("recruiterResults", JSON.stringify(this.results));

});



}

selectedDetails:any = null;

showDetails(resume:any){
    this.selectedDetails=resume.details;
}

downloadReport(){

let csv = "Rank,Resume,Score\n";

this.results.forEach((r:any,i:number)=>{

csv += `${i+1},${r.name},${r.score}%\n`;

});

const blob = new Blob([csv], {type:'text/csv'});

const url = window.URL.createObjectURL(blob);

const a = document.createElement("a");

a.href = url;

a.download = "resume_ranking_report.csv";

a.click();

}

getMatched(value: any) {
  return value?.matched || [];
}

getMissing(value: any) {
  return value?.missing || [];
}

openDetails(resume:any){

localStorage.setItem("resumeDetails", JSON.stringify(resume));

this.router.navigate(['/recruiter-details']);

}

clearResults(){

this.results = [];

localStorage.removeItem("recruiterResults");

}
}
