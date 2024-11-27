export interface Document {
    id: number;
    name: string;
    content: string;
    created_at: string;
    size: number;
  }
  
  export interface DocumentListResponse {
    documents: Document[];
    total: number;
  }
  
  export interface SortConfig {
    field: 'name' | 'created_at';
    order: 'asc' | 'desc';
  }