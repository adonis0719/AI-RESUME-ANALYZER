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

resume:any;

ngOnInit(){

const data = localStorage.getItem("resumeDetails");

if(data){
this.resume = JSON.parse(data);
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

}
