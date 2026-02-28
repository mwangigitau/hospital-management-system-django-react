import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { PlusCircle } from 'lucide-react';
import api from '../../lib/api';
import DataTable from '../../components/common/DataTable';
import Badge from '../../components/common/Badge';
import Pagination from '../../components/common/Pagination';
import { format } from 'date-fns';

interface Invoice {
  id: string;
  invoice_number: string;
  patient_name: string;
  total_amount: number;
  status: 'draft' | 'pending' | 'paid' | 'cancelled';
  created_at: string;
}

interface PaginatedResponse {
  count: number;
  results: Invoice[];
}

const statusBadge: Record<string, 'gray' | 'warning' | 'success' | 'error'> = {
  draft: 'gray',
  pending: 'warning',
  paid: 'success',
  cancelled: 'error',
};

export default function BillingPage() {
  const [page, setPage] = useState(1);

  const { data, isLoading } = useQuery<PaginatedResponse>({
    queryKey: ['invoices', page],
    queryFn: () => api.get('/billing/invoices/', { params: { page } }).then((r) => r.data),
    retry: false,
  });

  const columns = [
    { key: 'invoice_number', label: 'Invoice #' },
    { key: 'patient_name', label: 'Patient' },
    {
      key: 'total_amount',
      label: 'Amount (KES)',
      render: (inv: Invoice) =>
        new Intl.NumberFormat('en-KE', { style: 'currency', currency: 'KES' }).format(inv.total_amount),
    },
    {
      key: 'status',
      label: 'Status',
      render: (inv: Invoice) => (
        <Badge variant={statusBadge[inv.status] ?? 'gray'}>
          {inv.status.charAt(0).toUpperCase() + inv.status.slice(1)}
        </Badge>
      ),
    },
    {
      key: 'created_at',
      label: 'Date',
      render: (inv: Invoice) => {
        try { return format(new Date(inv.created_at), 'dd MMM yyyy'); } catch { return inv.created_at; }
      },
    },
  ];

  return (
    <div className="space-y-5">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-800 dark:text-white">Billing</h1>
          <p className="text-sm text-gray-500 dark:text-gray-400">
            {data ? `${data.count} invoices` : 'Manage invoices'}
          </p>
        </div>
        <button className="flex items-center gap-2 bg-primary-600 hover:bg-primary-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors">
          <PlusCircle className="w-4 h-4" />
          Create Invoice
        </button>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {[
          { label: 'Total Invoices', value: data?.count ?? 0, color: 'bg-blue-50 dark:bg-blue-900/20 text-blue-700 dark:text-blue-300' },
          { label: 'Pending', value: '-', color: 'bg-yellow-50 dark:bg-yellow-900/20 text-yellow-700 dark:text-yellow-300' },
          { label: 'Paid', value: '-', color: 'bg-green-50 dark:bg-green-900/20 text-green-700 dark:text-green-300' },
          { label: 'Cancelled', value: '-', color: 'bg-red-50 dark:bg-red-900/20 text-red-700 dark:text-red-300' },
        ].map((c) => (
          <div key={c.label} className={`rounded-xl p-4 ${c.color}`}>
            <p className="text-xs font-medium opacity-70 mb-1">{c.label}</p>
            <p className="text-2xl font-bold">{c.value}</p>
          </div>
        ))}
      </div>

      <DataTable
        columns={columns}
        data={data?.results ?? []}
        loading={isLoading}
        rowKey={(inv) => inv.id}
        emptyMessage="No invoices found"
      />

      <Pagination page={page} totalPages={data ? Math.ceil(data.count / 20) : 1} onPageChange={setPage} />
    </div>
  );
}
