import { Component, OnInit } from '@angular/core';
import { IssueService } from '../issue.service';
import { Issue } from '../issue';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router'; // Import Router

@Component({
  selector: 'app-issue-list',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './issue-list.component.html',
  styleUrls: ['./issue-list.component.css']
})
export class IssueListComponent implements OnInit {
  // --- State for the list ---
  issues: Issue[] = [];
  searchTerm: string = '';
  statusFilter: string = '';
  priorityFilter: string = '';
  assigneeFilter: string = '';
  sortBy: string = 'updatedAt';
  order: string = 'desc';
  page: number = 1;
  pageSize: number = 10;

  // --- State for the form modal ---
  isFormVisible = false;
  isEditing = false;
  currentIssue: Partial<Issue> = {};

  constructor(private issueService: IssueService, private router: Router) { } // Inject Router

  ngOnInit(): void {
    this.loadIssues();
  }

  loadIssues(): void {
    this.issueService.getIssues(
      this.searchTerm, this.statusFilter, this.priorityFilter,
      this.assigneeFilter, this.sortBy, this.order, this.page, this.pageSize
    ).subscribe(data => {
      this.issues = data;
    });
  }

  // --- List Actions ---
  sort(column: string): void {
    if (this.sortBy === column) {
      this.order = this.order === 'asc' ? 'desc' : 'asc';
    } else {
      this.sortBy = column;
      this.order = 'asc';
    }
    this.loadIssues();
  }

  previousPage(): void {
    if (this.page > 1) {
      this.page--;
      this.loadIssues();
    }
  }

  nextPage(): void {
    this.page++;
    this.loadIssues();
  }

  viewIssue(issue: Issue): void {
    this.router.navigate(['/issues', issue.id]); // Navigate to detail page
  }

  // --- Form Actions ---
  openCreateForm(): void {
    this.isEditing = false;
    this.currentIssue = { title: '', status: 'open', priority: 'medium', assignee: '' };
    this.isFormVisible = true;
  }

  openEditForm(issue: Issue): void {
    this.isEditing = true;
    this.currentIssue = { ...issue }; // Create a copy to edit
    this.isFormVisible = true;
  }

  closeForm(): void {
    this.isFormVisible = false;
  }

  saveIssue(): void {
    if (this.isEditing && this.currentIssue.id) {
      this.issueService.updateIssue(this.currentIssue.id, this.currentIssue).subscribe(() => {
        this.loadIssues();
        this.closeForm();
      });
    } else {
      this.issueService.createIssue(this.currentIssue).subscribe(() => {
        this.loadIssues();
        this.closeForm();
      });
    }
  }
}