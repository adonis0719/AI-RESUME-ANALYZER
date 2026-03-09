import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface CategoryDetail {
  matched: string[];
  missing: string[];
  percentage: number;
  weight: number;
}

export interface Recommendation {
  skill: string;
  category: string;
  priority: number;
}

export interface CompareResult {
  overall_match_percentage: number;
  rule_score?: number;
  ai_similarity?: number;
  domain?: string;
  category_match: { [key: string]: CategoryDetail };
  recommendations: Recommendation[];
  interview_questions: string[];
}

@Injectable({
  providedIn: 'root'
})
export class CompareService {

  private apiUrl = 'http://127.0.0.1:8000/api';

  constructor(private http: HttpClient) {}

  compare(resumeId: number, jobId: number): Observable<CompareResult> {
    return this.http.post<CompareResult>(`${this.apiUrl}/compare/`, {
      resume_id: resumeId,
      job_id: jobId
    });
  }
}