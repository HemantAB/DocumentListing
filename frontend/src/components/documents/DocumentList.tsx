import React, { useState, useEffect } from 'react';
import { format } from 'date-fns';
import { Search, ChevronUp, ChevronDown, Trash2, Plus, Loader2 } from 'lucide-react';
import { Document, SortConfig } from '../../types/document';
import { api } from '../../services/api';
import { Button } from '../ui/button';
import { Input } from '../ui/input';
import { Modal } from '../ui/modal';
import { Alert } from '../ui/alert';
import { 
  Table, 
  TableBody, 
  TableCell, 
  TableHead, 
  TableHeader, 
  TableRow 
} from '../ui/table';

const DocumentList = () => {
  // State
  const [documents, setDocuments] = useState<Document[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [sortConfig, setSortConfig] = useState<SortConfig>({ field: 'name', order: 'asc' });
  const [page, setPage] = useState(1);
  const [totalDocuments, setTotalDocuments] = useState(0);
  const [selectedDocument, setSelectedDocument] = useState<Document | null>(null);
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);
  const [newDocument, setNewDocument] = useState({ name: '', content: '' });
  const perPage = 10;

  // Fetch documents
  const fetchDocuments = async () => {
    try {
      setLoading(true);
      const response = await api.getDocuments({
        search: searchTerm,
        sort_by: sortConfig.field,
        sort_order: sortConfig.order,
        page,
        per_page: perPage
      });
      setDocuments(response.documents);
      setTotalDocuments(response.total);
      setError(null);
    } catch (err) {
      setError('Failed to load documents');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDocuments();
  }, [searchTerm, sortConfig, page]);

  // Sort handling
  const handleSort = (field: 'name' | 'created_at') => {
    setSortConfig(prev => ({
      field,
      order: prev.field === field && prev.order === 'asc' ? 'desc' : 'asc'
    }));
  };

  // Create document
  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await api.createDocument(newDocument);
      setNewDocument({ name: '', content: '' });
      setIsCreateModalOpen(false);
      fetchDocuments();
    } catch (err) {
      setError('Failed to create document');
      console.error(err);
    }
  };

  // Delete document
  const handleDelete = async (id: number) => {
    if (!window.confirm('Are you sure you want to delete this document?')) {
      return;
    }
    try {
      await api.deleteDocument(id);
      fetchDocuments();
    } catch (err) {
      setError('Failed to delete document');
      console.error(err);
    }
  };

  // Format date
  const formatDate = (dateString: string) => {
    return format(new Date(dateString), 'MMM d, yyyy');
  };

  // Format size
  const formatSize = (bytes: number) => {
    const kb = bytes / 1024;
    return `${kb.toFixed(1)} KB`;
  };

  return (
    <div className="container mx-auto px-4 py-8">
      {error && (
        <Alert variant="destructive" className="mb-4">
          {error}
        </Alert>
      )}

      <div className="mb-6 flex justify-between items-center">
        <div className="relative w-72">
          <Search className="absolute left-3 top-2.5 h-4 w-4 text-gray-400" />
          <Input
            placeholder="Search documents..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="pl-10"
          />
        </div>
        <Button onClick={() => setIsCreateModalOpen(true)}>
          <Plus className="mr-2 h-4 w-4" />
          New Document
        </Button>
      </div>

      <div className="bg-white rounded-lg shadow">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead 
                className="cursor-pointer"
                onClick={() => handleSort('name')}
              >
                Name
                {sortConfig.field === 'name' && (
                  sortConfig.order === 'asc' ? 
                    <ChevronUp className="inline ml-2 h-4 w-4" /> : 
                    <ChevronDown className="inline ml-2 h-4 w-4" />
                )}
              </TableHead>
              <TableHead 
                className="cursor-pointer"
                onClick={() => handleSort('created_at')}
              >
                Created
                {sortConfig.field === 'created_at' && (
                  sortConfig.order === 'asc' ? 
                    <ChevronUp className="inline ml-2 h-4 w-4" /> : 
                    <ChevronDown className="inline ml-2 h-4 w-4" />
                )}
              </TableHead>
              <TableHead>Size</TableHead>
              <TableHead>Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {loading ? (
              <TableRow>
                <TableCell colSpan={4} className="text-center py-8">
                  <Loader2 className="h-6 w-6 animate-spin mx-auto" />
                </TableCell>
              </TableRow>
            ) : documents.length === 0 ? (
              <TableRow>
                <TableCell colSpan={4} className="text-center py-8">
                  No documents found
                </TableCell>
              </TableRow>
            ) : (
              documents.map((doc) => (
                <TableRow key={doc.id}>
                  <TableCell 
                    className="cursor-pointer hover:text-blue-600"
                    onClick={() => setSelectedDocument(doc)}
                  >
                    {doc.name}
                  </TableCell>
                  <TableCell>{formatDate(doc.created_at)}</TableCell>
                  <TableCell>{formatSize(doc.size)}</TableCell>
                  <TableCell>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => handleDelete(doc.id)}
                    >
                      <Trash2 className="h-4 w-4 text-red-500" />
                    </Button>
                  </TableCell>
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      </div>

      {/* Pagination */}
      <div className="mt-4 flex items-center justify-between">
        <p className="text-sm text-gray-500">
          Showing {Math.min((page - 1) * perPage + 1, totalDocuments)} to{' '}
          {Math.min(page * perPage, totalDocuments)} of {totalDocuments} documents
        </p>
        <div className="flex gap-2">
          <Button
            variant="outline"
            size="sm"
            onClick={() => setPage(p => Math.max(1, p - 1))}
            disabled={page === 1}
          >
            Previous
          </Button>
          <Button
            variant="outline"
            size="sm"
            onClick={() => setPage(p => p + 1)}
            disabled={page * perPage >= totalDocuments}
          >
            Next
          </Button>
        </div>
      </div>

      {/* Create Document Modal */}
      <Modal
        isOpen={isCreateModalOpen}
        onClose={() => setIsCreateModalOpen(false)}
        title="Create New Document"
      >
        <form onSubmit={handleCreate} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Document Name
            </label>
            <Input
              required
              value={newDocument.name}
              onChange={(e) => setNewDocument(prev => ({
                ...prev,
                name: e.target.value
              }))}
              placeholder="Enter document name"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Content
            </label>
            <textarea
              required
              className="w-full min-h-[200px] p-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
              value={newDocument.content}
              onChange={(e) => setNewDocument(prev => ({
                ...prev,
                content: e.target.value
              }))}
              placeholder="Enter document content"
            />
          </div>
          <div className="flex justify-end gap-2">
            <Button
              type="button"
              variant="outline"
              onClick={() => setIsCreateModalOpen(false)}
            >
              Cancel
            </Button>
            <Button type="submit">
              Create Document
            </Button>
          </div>
        </form>
      </Modal>

      {/* View Document Modal */}
      <Modal
        isOpen={!!selectedDocument}
        onClose={() => setSelectedDocument(null)}
        title={selectedDocument?.name}
      >
        <div>
          <div className="text-sm text-gray-500 mb-2">
            Created: {selectedDocument && formatDate(selectedDocument.created_at)}
          </div>
          <div className="bg-gray-50 p-4 rounded-md min-h-[200px] whitespace-pre-wrap">
            {selectedDocument?.content}
          </div>
        </div>
      </Modal>
    </div>
  );
};

export default DocumentList;