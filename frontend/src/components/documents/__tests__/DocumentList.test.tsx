import { render, screen, fireEvent, waitFor, RenderResult } from '@testing-library/react';
import { vi, describe, it, expect, beforeEach } from 'vitest';
import axios from 'axios';
import DocumentList from '../DocumentList';
import type { FC, ReactElement } from 'react';

// Mock axios
vi.mock('axios');
const mockedAxios = vi.mocked(axios, true);

// Mock data
const mockDocuments = [
  {
    id: 1,
    name: 'Meeting Notes.txt',
    content: 'Discussion points from team meeting',
    created_at: '2024-11-26T10:00:00Z',
    size: 1024
  },
  {
    id: 2,
    name: 'Project Plan.txt',
    content: 'Q4 Project Timeline',
    created_at: '2024-11-26T11:00:00Z',
    size: 2048
  }
];

// Test wrapper component
const TestWrapper: FC<{ children: ReactElement }> = ({ children }) => {
  return children;
};

// Custom render function
const customRender = (ui: ReactElement): RenderResult => {
  return render(ui, {
    wrapper: TestWrapper
  });
};

describe('DocumentList', () => {
  beforeEach(() => {
    // Reset mocks before each test
    vi.clearAllMocks();
    
    // Setup default mock response
    mockedAxios.get.mockResolvedValue({
      data: {
        documents: mockDocuments,
        total: mockDocuments.length
      }
    });
  });

  it('renders loading state initially', () => {
    customRender(<DocumentList />);
    expect(screen.getByRole('status')).toBeInTheDocument();
  });

  it('renders documents after loading', async () => {
    customRender(<DocumentList />);
    
    await waitFor(() => {
      expect(screen.getByText('Meeting Notes.txt')).toBeInTheDocument();
      expect(screen.getByText('Project Plan.txt')).toBeInTheDocument();
    });
  });

  it('handles search functionality', async () => {
    customRender(<DocumentList />);
    
    const searchInput = screen.getByPlaceholderText(/search/i);
    fireEvent.change(searchInput, { target: { value: 'Meeting' } });
    
    await waitFor(() => {
      expect(mockedAxios.get).toHaveBeenCalledWith(
        expect.stringContaining('search=Meeting')
      );
    });
  });

  it('handles document deletion', async () => {
    mockedAxios.delete.mockResolvedValueOnce({ data: { message: 'success' } });
    
    customRender(<DocumentList />);
    
    await waitFor(() => {
      const deleteButton = screen.getAllByRole('button')[1];
      fireEvent.click(deleteButton);
    });
    
    const confirmSpy = vi.spyOn(window, 'confirm');
    confirmSpy.mockImplementation(() => true);
    
    await waitFor(() => {
      expect(mockedAxios.delete).toHaveBeenCalled();
    });
  });

  it('handles error states', async () => {
    mockedAxios.get.mockRejectedValueOnce(new Error('Failed to fetch'));
    
    customRender(<DocumentList />);
    
    await waitFor(() => {
      expect(screen.getByText(/failed to load documents/i)).toBeInTheDocument();
    });
  });

  it('handles sorting by name', async () => {
    customRender(<DocumentList />);
    
    const nameHeader = screen.getByText(/name/i);
    fireEvent.click(nameHeader);
    
    await waitFor(() => {
      expect(mockedAxios.get).toHaveBeenCalledWith(
        expect.stringContaining('sort_by=name')
      );
    });
  });

  it('creates new document', async () => {
    mockedAxios.post.mockResolvedValueOnce({
      data: {
        id: 3,
        name: 'new.txt',
        content: 'New content',
        created_at: '2024-11-26T12:00:00Z',
        size: 512
      }
    });
    
    customRender(<DocumentList />);
    
    const newButton = screen.getByText(/new document/i);
    fireEvent.click(newButton);
    
    const nameInput = screen.getByPlaceholderText(/document name/i);
    const contentInput = screen.getByPlaceholderText(/document content/i);
    
    fireEvent.change(nameInput, { target: { value: 'new.txt' } });
    fireEvent.change(contentInput, { target: { value: 'New content' } });
    
    const submitButton = screen.getByText(/create/i);
    fireEvent.click(submitButton);
    
    await waitFor(() => {
      expect(mockedAxios.post).toHaveBeenCalledWith(
        expect.any(String),
        {
          name: 'new.txt',
          content: 'New content'
        }
      );
    });
  });

  it('shows pagination controls', async () => {
    mockedAxios.get.mockResolvedValueOnce({
      data: {
        documents: mockDocuments,
        total: 15
      }
    });

    customRender(<DocumentList />);

    await waitFor(() => {
      expect(screen.getByText(/next/i)).toBeInTheDocument();
      expect(screen.getByText(/previous/i)).toBeInTheDocument();
    });
  });

  it('handles pagination navigation', async () => {
    customRender(<DocumentList />);

    await waitFor(() => {
      const nextButton = screen.getByText(/next/i);
      fireEvent.click(nextButton);
    });

    await waitFor(() => {
      expect(mockedAxios.get).toHaveBeenCalledWith(
        expect.stringContaining('page=2')
      );
    });
  });
});