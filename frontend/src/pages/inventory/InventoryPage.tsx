import { useState, useCallback } from 'react';
import { useQuery } from '@tanstack/react-query';
import { Search, Package } from 'lucide-react';
import toast from 'react-hot-toast';
import api from '../../lib/api';
import DataTable from '../../components/common/DataTable';
import Badge from '../../components/common/Badge';
import Pagination from '../../components/common/Pagination';
import BarcodeScanner from '../../components/common/BarcodeScanner';

interface StoreItem {
  id: string;
  store: string;
  store_name: string;
  item: string;
  item_name: string;
  quantity: number;
  unit_cost: number;
}

interface Store {
  id: string;
  name: string;
  store_type: string;
}

interface PaginatedResponse<T> {
  count: number;
  results: T[];
}

export default function InventoryPage() {
  const [page, setPage] = useState(1);
  const [search, setSearch] = useState('');
  const [searchInput, setSearchInput] = useState('');
  const [scanning, setScanning] = useState(false);
  const [selectedStore, setSelectedStore] = useState('');
  const [lastScanResult, setLastScanResult] = useState<{
    item_name: string;
    quantity_removed: number;
    remaining: number;
  } | null>(null);

  const { data: storesData } = useQuery<PaginatedResponse<Store>>({
    queryKey: ['stores'],
    queryFn: () => api.get('/inventory/stores/', { params: { page_size: 100 } }).then((r) => r.data),
    retry: false,
  });

  const { data: storeItemsData, isLoading } = useQuery<PaginatedResponse<StoreItem>>({
    queryKey: ['store-items', page, search],
    queryFn: () =>
      api.get('/inventory/store-items/', { params: { page, search } }).then((r) => r.data),
    retry: false,
  });

  const stores = storesData?.results ?? [];

  const handleBarcodeScan = useCallback(
    async (barcode: string) => {
      if (!selectedStore) {
        toast.error('Please select a store first.');
        return;
      }
      setScanning(true);
      setLastScanResult(null);
      try {
        const res = await api.post('/inventory/barcode-scan/', {
          barcode,
          store: selectedStore,
        });
        setLastScanResult({
          item_name: res.data.item?.name ?? barcode,
          quantity_removed: res.data.quantity_removed,
          remaining: Number(res.data.store_item?.quantity ?? 0),
        });
        toast.success(`Checked out: ${res.data.item?.name}`);
      } catch (err: unknown) {
        const axiosErr = err as { response?: { data?: { detail?: string } } };
        toast.error(axiosErr.response?.data?.detail || 'Scan failed');
      } finally {
        setScanning(false);
      }
    },
    [selectedStore],
  );

  const columns = [
    { key: 'item_name', label: 'Item' },
    { key: 'store_name', label: 'Store' },
    {
      key: 'quantity',
      label: 'Quantity',
      render: (row: StoreItem) => (
        <span className={Number(row.quantity) <= 5 ? 'text-red-600 font-semibold' : 'text-gray-700 dark:text-gray-300'}>
          {row.quantity}
        </span>
      ),
    },
    { key: 'unit_cost', label: 'Unit Cost', render: (row: StoreItem) => `$${row.unit_cost}` },
    {
      key: 'status',
      label: 'Status',
      render: (row: StoreItem) => (
        <Badge variant={Number(row.quantity) <= 5 ? 'error' : 'success'}>
          {Number(row.quantity) <= 5 ? 'Low Stock' : 'In Stock'}
        </Badge>
      ),
    },
  ];

  return (
    <div className="space-y-5">
      <div>
        <h1 className="text-2xl font-bold text-gray-800 dark:text-white">Inventory</h1>
        <p className="text-sm text-gray-500 dark:text-gray-400">Manage store items &amp; barcode scanning</p>
      </div>

      {/* Barcode Scanner Section */}
      <div className="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-xl p-5 space-y-3">
        <div className="flex items-center gap-2 mb-1">
          <Package className="w-5 h-5 text-primary-600 dark:text-primary-400" />
          <h2 className="font-semibold text-gray-800 dark:text-white text-sm">Barcode Scanner — Checkout</h2>
        </div>

        <div className="flex flex-col sm:flex-row gap-3">
          <select
            value={selectedStore}
            onChange={(e) => setSelectedStore(e.target.value)}
            className="w-full sm:w-56 px-3 py-2.5 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-sm text-gray-800 dark:text-white focus:outline-none focus:ring-2 focus:ring-primary-500"
          >
            <option value="">Select Store…</option>
            {stores.map((s) => (
              <option key={s.id} value={s.id}>
                {s.name}
              </option>
            ))}
          </select>
          <div className="flex-1">
            <BarcodeScanner onScan={handleBarcodeScan} loading={scanning} placeholder="Scan item barcode…" />
          </div>
        </div>

        {lastScanResult && (
          <div className="flex items-center gap-2 text-sm bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 text-green-700 dark:text-green-400 rounded-lg px-4 py-2">
            ✅ <strong>{lastScanResult.item_name}</strong> — removed {lastScanResult.quantity_removed}, remaining: {lastScanResult.remaining}
          </div>
        )}
      </div>

      {/* Search */}
      <div className="flex gap-2">
        <div className="relative max-w-sm flex-1">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
          <input
            value={searchInput}
            onChange={(e) => setSearchInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && setSearch(searchInput)}
            placeholder="Search store items..."
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
        data={storeItemsData?.results ?? []}
        loading={isLoading}
        rowKey={(row) => row.id}
        emptyMessage="No store items found"
      />

      <Pagination
        page={page}
        totalPages={storeItemsData ? Math.ceil(storeItemsData.count / 20) : 1}
        onPageChange={setPage}
      />
    </div>
  );
}
