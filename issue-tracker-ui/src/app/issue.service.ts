import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Issue } from './issue';

@Injectable({
  providedIn: 'root'
})
export class IssueService {
  private apiUrl = 'http://localhost:8000'; // Your Python backend URL

  constructor(private http: HttpClient) { }

  getIssues(
    search: string = '',
    status: string = '',
    priority: string = '',
    assignee: string = '',
    sortBy: string = 'updatedAt',
    order: string = 'desc',
    page: number = 1,
    pageSize: number = 10
  ): Observable<Issue[]> {
    let params = new HttpParams()
      .set('search', search)
      .set('status', status)
      .set('priority', priority)
      .set('assignee', assignee)
      .set('sortBy', sortBy)
      .set('order', order)
      .set('page', page.toString())
      .set('pageSize', pageSize.toString());

    return this.http.get<Issue[]>(`${this.apiUrl}/issues`, { params });
  }

  getIssue(id: string): Observable<Issue> {
    return this.http.get<Issue>(`${this.apiUrl}/issues/${id}`);
  }

  createIssue(issue: Partial<Issue>): Observable<Issue> {
    return this.http.post<Issue>(`${this.apiUrl}/issues`, issue);
  }

  updateIssue(id: string, issue: Partial<Issue>): Observable<Issue> {
    return this.http.put<Issue>(`${this.apiUrl}/issues/${id}`, issue);
  }
}