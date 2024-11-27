import axios from 'axios';
import { Document, DocumentListResponse } from '../types/document';

const API_URL = 'http://localhost:8000/api';

export const api = {
  async getDocuments(params: {
    search?: string;
    sort_by?: string;
    sort_order?: string;
    page: number;
    per_page: number;
  }): Promise<DocumentListResponse> {
    const response = await axios.get(`${API_URL}/documents`, { params });
    return response.data;
  },

  async getDocument(id: number): Promise<Document> {
    const response = await axios.get(`${API_URL}/documents/${id}`);
    return response.data;
  },

  async createDocument(data: { name: string; content: string }): Promise<Document> {
    const response = await axios.post(`${API_URL}/documents`, data);
    return response.data;
  },

  async deleteDocument(id: number): Promise<void> {
    await axios.delete(`${API_URL}/documents/${id}`);
  }
};