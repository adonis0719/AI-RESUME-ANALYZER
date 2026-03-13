import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { timeout, catchError } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class AiChatService {
  private apiUrl = 'http://127.0.0.1:8000/api';

  constructor(private http: HttpClient) {}

  sendMessage(message: string): Observable<{ reply: string }> {
    return this.http.post<{ reply: string }>(`${this.apiUrl}/ai-assistant/`, {
      message
    }).pipe(
      timeout(60000),
      catchError((err) => {
        const msg = err?.status === 401
          ? 'Session expired. Please log in again.'
          : 'AI assistant is temporarily unavailable. Please check your connection and try again.';
        return of({ reply: msg });
      })
    );
  }
}
