import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { PlusCircle } from 'lucide-react';
import api from '../../lib/api';
import DataTable from '../../components/common/DataTable';
import Badge from '../../components/common/Badge';
import Pagination from '../../components/common/Pagination';
import { format } from 'date-fns';

interface LabRequest {
  id: string;
  request_number: string;
  patient_name: string;
  tests: string;
  priority: 'routine' | 'urgent' | 'stat';
  status: 'pending' | 'in_progress' | 'completed' | 'cancelled';
  requested_at: string;
}

interface PaginatedResponse {
  count: number;
  results: LabRequest[];
}

const priorityBadge: Record<string, 'gray' | 'warning' | 'error'> = {
  routine: 'gray',
  urgent: 'warning',
  stat: 'error',
};

const statusBadge: Record<string, 'gray' | 'warning' | 'success' | 'error' | 'info'> = {
  pending: 'warning',
  in_progress: 'info',
  completed: 'success',
  cancelled: 'error',
};

export default function LaboratoryPage() {
  const [page, setPage] = useState(1);

  const { data, isLoading } = useQuery<PaginatedResponse>({
    queryKey: ['lab-requests', page],
    queryFn: () => api.get('/laboratory/requests/', { params: { page } }).then((r) => r.data),
    retry: false,
  });

  const columns = [
    { key: 'request_number', label: 'Request #' },
    { key: 'patient_name', label: 'Patient' },
    { key: 'tests', label: 'Tests' },
    {
      key: 'priority',
      label: 'Priority',
      render: (r: LabRequest) => (
        <Badge variant={priorityBadge[r.priority] ?? 'gray'}>
          {r.priority.toUpperCase()}
        </Badge>
      ),
    },
    {
      key: 'status',
      label: 'Status',
      render: (r: LabRequest) => (
        <Badge variant={statusBadge[r.status] ?? 'gray'}>
          {r.status.replace('_', ' ').replace(/\b\w/g, (c) => c.toUpperCase())}
        </Badge>
      ),
    },
    {
      key: 'requested_at',
      label: 'Requested',
      render: (r: LabRequest) => {
        try { return format(new Date(r.requested_at), 'dd MMM yyyy, HH:mm'); } catch { return r.requested_at; }
      },
    },
  ];

  return (
    <div className="space-y-5">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-800 dark:text-white">Laboratory</h1>
          <p className="text-sm text-gray-500 dark:text-gray-400">Lab test requests and results</p>
        </div>
        <button className="flex items-center gap-2 bg-primary-600 hover:bg-primary-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors">
          <PlusCircle className="w-4 h-4" />
          New Request
        </button>
      </div>

      <DataTable
        columns={columns}
        data={data?.results ?? []}
        loading={isLoading}
        rowKey={(r) => r.id}
        emptyMessage="No lab requests found"
      />

      <Pagination page={page} totalPages={data ? Math.ceil(data.count / 20) : 1} onPageChange={setPage} />
    </div>
  );
}
