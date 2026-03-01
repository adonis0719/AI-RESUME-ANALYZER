import { Component, OnInit } from '@angular/core';
import { CompareService } from '../services/compare.service';

interface CategoryDetail {
  matched: string[];
  missing: string[];
  percentage: number;
  weight: number;
}

interface Recommendation {
  skill: string;
  category: string;
  priority: number;
}

interface CompareResult {
  overall_match_percentage: number;
  category_match: { [key: string]: CategoryDetail };
  recommendations: Recommendation[];
}

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html'
})
export class DashboardComponent implements OnInit {

  result?: CompareResult;

  constructor(private compareService: CompareService) {}

  ngOnInit() {
    this.compareService.compare(12, 6).subscribe({
      next: (res: CompareResult) => {
        this.result = res;
      },
      error: (err) => {
        console.log(err);
      }
    });
  }
}