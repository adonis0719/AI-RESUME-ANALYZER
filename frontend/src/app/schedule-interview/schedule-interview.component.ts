import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { EmailService } from '../services/email.service';

@Component({
  selector: 'app-schedule-interview',
  templateUrl: './schedule-interview.component.html',
  styleUrls: ['./schedule-interview.component.css']
})
export class ScheduleInterviewComponent implements OnInit {
  emails: string[] = [];
  subject: string = 'Interview Invitation - AI Resume Analyzer';
  message: string = 'Dear Candidate,\n\nWe would like to invite you for an interview.\n\nBest regards,\nRecruitment Team';
  sending = false;

  constructor(
    private router: Router,
    private emailService: EmailService
  ) {}

  ngOnInit(): void {
    const nav = this.router.getCurrentNavigation();
    const state = (nav && nav.extras && nav.extras.state) || history.state;
    if (state && Array.isArray(state.emails)) {
      this.emails = state.emails;
    }
  }

  send() {
    if (!this.emails.length) {
      alert('No recipient emails provided.');
      return;
    }
    if (!this.subject.trim() || !this.message.trim()) {
      alert('Subject and message are required.');
      return;
    }

    this.sending = true;
    this.emailService.sendInterviewEmail(this.emails, this.subject, this.message)
      .subscribe({
        next: () => {
          this.sending = false;
          alert('Emails sent successfully.');
          this.router.navigate(['/recruiter']);
        },
        error: () => {
          this.sending = false;
          alert('Failed to send emails. Please try again.');
        }
      });
  }
}

