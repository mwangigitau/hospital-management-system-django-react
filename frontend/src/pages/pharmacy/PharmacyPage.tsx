import { useState, useCallback } from 'react';
import { useQuery } from '@tanstack/react-query';
import { AlertTriangle, Search, Pill } from 'lucide-react';
import toast from 'react-hot-toast';
import api from '../../lib/api';
import DataTable from '../../components/common/DataTable';
import Badge from '../../components/common/Badge';
import Pagination from '../../components/common/Pagination';
import BarcodeScanner from '../../components/common/BarcodeScanner';

interface Drug {
  id: string;
  drug_code: string;
  name: string;
  barcode: string | null;
  generic_name: string;
  quantity_in_stock: number;
  reorder_level: number;
  unit: string;
  expiry_date?: string;
}

interface PaginatedResponse {
  count: number;
  results: Drug[];
}

export default function PharmacyPage() {
  const [page, setPage] = useState(1);
  const [search, setSearch] = useState('');
  const [searchInput, setSearchInput] = useState('');
  const [scanning, setScanning] = useState(false);
  const [lastScanResult, setLastScanResult] = useState<{
    drug_name: string;
    quantity_dispensed: number;
    batch_number: string;
  } | null>(null);

  const { data, isLoading } = useQuery<PaginatedResponse>({
    queryKey: ['pharmacy-drugs', page, search],
    queryFn: () => api.get('/pharmacy/drugs/', { params: { page, search } }).then((r) => r.data),
    retry: false,
  });

  const handleBarcodeScan = useCallback(async (barcode: string) => {
    setScanning(true);
    setLastScanResult(null);
    try {
      const res = await api.post('/pharmacy/barcode-scan/', { barcode });
      setLastScanResult({
        drug_name: res.data.drug?.name ?? barcode,
        quantity_dispensed: res.data.quantity_dispensed,
        batch_number: res.data.batch?.batch_number ?? '',
      });
      toast.success(`Dispensed: ${res.data.drug?.name}`);
    } catch (err: unknown) {
      const axiosErr = err as { response?: { data?: { detail?: string } } };
      toast.error(axiosErr.response?.data?.detail || 'Scan failed');
    } finally {
      setScanning(false);
    }
  }, []);

  const lowStock = data?.results?.filter((d) => d.quantity_in_stock <= d.reorder_level) ?? [];

  const columns = [
    { key: 'drug_code', label: 'Code' },
    { key: 'name', label: 'Drug Name' },
    { key: 'generic_name', label: 'Generic Name' },
    {
      key: 'quantity_in_stock',
      label: 'Stock',
      render: (d: Drug) => (
        <span className={d.quantity_in_stock <= d.reorder_level ? 'text-red-600 font-semibold' : 'text-gray-700 dark:text-gray-300'}>
          {d.quantity_in_stock} {d.unit}
        </span>
      ),
    },
    { key: 'reorder_level', label: 'Reorder Level', render: (d: Drug) => `${d.reorder_level} ${d.unit}` },
    {
      key: 'stock_status',
      label: 'Status',
      render: (d: Drug) => (
        <Badge variant={d.quantity_in_stock <= d.reorder_level ? 'error' : 'success'}>
          {d.quantity_in_stock <= d.reorder_level ? 'Low Stock' : 'In Stock'}
        </Badge>
      ),
    },
    {
      key: 'expiry_date',
      label: 'Expiry',
      render: (d: Drug) => d.expiry_date ?? '-',
    },
  ];

  return (
    <div className="space-y-5">
      <div>
        <h1 className="text-2xl font-bold text-gray-800 dark:text-white">Pharmacy</h1>
        <p className="text-sm text-gray-500 dark:text-gray-400">Drug stock management</p>
      </div>

      {/* Barcode Scanner Section */}
      <div className="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-xl p-5 space-y-3">
        <div className="flex items-center gap-2 mb-1">
          <Pill className="w-5 h-5 text-primary-600 dark:text-primary-400" />
          <h2 className="font-semibold text-gray-800 dark:text-white text-sm">Barcode Scanner — Dispense</h2>
        </div>
        <BarcodeScanner onScan={handleBarcodeScan} loading={scanning} placeholder="Scan drug barcode…" />
        {lastScanResult && (
          <div className="flex items-center gap-2 text-sm bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 text-green-700 dark:text-green-400 rounded-lg px-4 py-2">
            ✅ <strong>{lastScanResult.drug_name}</strong> — dispensed {lastScanResult.quantity_dispensed} (batch {lastScanResult.batch_number})
          </div>
        )}
      </div>

      {/* Low Stock Alerts */}
      {lowStock.length > 0 && (
        <div className="flex items-start gap-3 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 text-red-700 dark:text-red-400 rounded-xl p-4">
          <AlertTriangle className="w-5 h-5 flex-shrink-0 mt-0.5" />
          <div>
            <p className="font-medium text-sm">Low Stock Alert</p>
            <p className="text-sm">{lowStock.length} drug(s) below reorder level: {lowStock.map((d) => d.name).join(', ')}</p>
          </div>
        </div>
      )}

      {/* Search */}
      <div className="flex gap-2">
        <div className="relative max-w-sm flex-1">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
          <input
            value={searchInput}
            onChange={(e) => setSearchInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && setSearch(searchInput)}
            placeholder="Search drugs..."
            className="w-full pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-sm text-gray-800 dark:text-white focus:outline-none focus:ring-2 focus:ring-primary-500"
          />
        </div>
        <button
          onClick={() => setSearch(searchInput)}
          className="px-4 py-2 bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 text-gray-700 dark:text-gray-200 rounded-lg text-sm font-medium transition-colors"
        >
          Search
        </button>
      </div>

      <DataTable
        columns={columns}
        data={data?.results ?? []}
        loading={isLoading}
        rowKey={(d) => d.id}
        emptyMessage="No drugs found"
      />

      <Pagination page={page} totalPages={data ? Math.ceil(data.count / 20) : 1} onPageChange={setPage} />
    </div>
  );
}
