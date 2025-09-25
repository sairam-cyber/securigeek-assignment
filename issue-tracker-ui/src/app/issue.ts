export interface Issue {
    id: string;
    title: string;
    status: string;
    priority: string;
    assignee?: string;
    createdAt: Date;
    updatedAt: Date;
  }