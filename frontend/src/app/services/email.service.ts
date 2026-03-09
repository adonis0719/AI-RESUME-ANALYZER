import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class EmailService {
  private apiUrl = 'http://127.0.0.1:8000/api';

  constructor(private http: HttpClient) {}

  sendInterviewEmail(emails: string[], subject: string, message: string): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/send-interview-email/`, {
      emails,
      subject,
      message
    });
  }
}

