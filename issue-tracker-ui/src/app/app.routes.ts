import { Routes } from '@angular/router';
import { IssueListComponent } from './issue-list/issue-list.component';
import { IssueDetailComponent } from './issue-detail/issue-detail.component';

export const routes: Routes = [
    { path: '', component: IssueListComponent },
    { path: 'issues/:id', component: IssueDetailComponent },
];