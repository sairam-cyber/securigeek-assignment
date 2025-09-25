import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { IssueService } from '../issue.service';
import { Issue } from '../issue';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-issue-detail',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './issue-detail.component.html',
  styleUrl: './issue-detail.component.css'
})
export class IssueDetailComponent implements OnInit {
  issue: Issue | undefined;

  constructor(
    private route: ActivatedRoute,
    private issueService: IssueService
  ) { }

  ngOnInit(): void {
    const id = this.route.snapshot.paramMap.get('id');
    if (id) {
      this.issueService.getIssue(id).subscribe(data => {
        this.issue = data;
      });
    }
  }
}