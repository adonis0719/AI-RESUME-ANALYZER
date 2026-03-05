
import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
selector: 'app-recruiter',
templateUrl: './recruiter.component.html',
styleUrls: ['./recruiter.component.css']
})

export class RecruiterComponent {

files: File[] = [];
jobDescription = '';
results: any[] = [];

api = 'http://127.0.0.1:8000/api/recruiter/analyze/';

constructor(private http: HttpClient) {}

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

});

}

}
