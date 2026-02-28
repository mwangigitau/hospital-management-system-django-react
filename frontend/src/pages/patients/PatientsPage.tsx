import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { Search, UserPlus, Pencil } from 'lucide-react';
import api from '../../lib/api';
import DataTable from '../../components/common/DataTable';
import Pagination from '../../components/common/Pagination';
import PatientFormModal from './PatientFormModal';
import Badge from '../../components/common/Badge';
import { format } from 'date-fns';

interface Patient {
  id: string;
  patient_number: string;
  first_name: string;
  last_name: string;
  date_of_birth: string;
  gender: 'M' | 'F' | 'O';
  phone: string;
  nhif_number: string;
  email?: string;
}

interface PaginatedResponse {
  count: number;
  results: Patient[];
}

export default function PatientsPage() {
  const [page, setPage] = useState(1);
  const [search, setSearch] = useState('');
  const [searchInput, setSearchInput] = useState('');
  const [modalOpen, setModalOpen] = useState(false);
  const [editPatient, setEditPatient] = useState<Patient | undefined>(undefined);

  const { data, isLoading, refetch } = useQuery<PaginatedResponse>({
    queryKey: ['patients', page, search],
    queryFn: () =>
      api
        .get('/patients/patients/', { params: { page, search } })
        .then((r) => r.data),
  });

  const totalPages = data ? Math.ceil(data.count / 20) : 1;

  const handleSearch = () => setSearch(searchInput);

  const columns = [
    { key: 'patient_number', label: 'Patient No' },
    {
      key: 'name',
      label: 'Name',
      render: (p: Patient) => `${p.first_name} ${p.last_name}`,
    },
    {
      key: 'date_of_birth',
      label: 'DOB',
      render: (p: Patient) => {
        try { return format(new Date(p.date_of_birth), 'dd MMM yyyy'); } catch { return p.date_of_birth; }
      },
    },
    {
      key: 'gender',
      label: 'Gender',
      render: (p: Patient) => (
        <Badge variant={p.gender === 'M' ? 'info' : p.gender === 'F' ? 'purple' : 'gray'}>
          {p.gender === 'M' ? 'Male' : p.gender === 'F' ? 'Female' : 'Other'}
        </Badge>
      ),
    },
    { key: 'phone', label: 'Phone' },
    { key: 'nhif_number', label: 'NHIF No' },
    {
      key: 'actions',
      label: 'Actions',
      render: (p: Patient) => (
        <button
          onClick={() => { setEditPatient(p); setModalOpen(true); }}
          className="p-1.5 text-gray-400 hover:text-primary-600 hover:bg-primary-50 dark:hover:bg-primary-900/20 rounded-lg transition-colors"
        >
          <Pencil className="w-4 h-4" />
        </button>
      ),
    },
  ];

  return (
    <div className="space-y-5">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-800 dark:text-white">Patients</h1>
          <p className="text-sm text-gray-500 dark:text-gray-400">
            {data ? `${data.count} total patients` : 'Loading...'}
          </p>
        </div>
        <button
          onClick={() => { setEditPatient(undefined); setModalOpen(true); }}
          className="flex items-center gap-2 bg-primary-600 hover:bg-primary-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors"
        >
          <UserPlus className="w-4 h-4" />
          Register Patient
        </button>
      </div>

      {/* Search */}
      <div className="flex gap-2">
        <div className="relative flex-1 max-w-sm">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
          <input
            value={searchInput}
            onChange={(e) => setSearchInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
            placeholder="Search patients..."
            className="w-full pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-sm text-gray-800 dark:text-white focus:outline-none focus:ring-2 focus:ring-primary-500"
          />
        </div>
        <button
          onClick={handleSearch}
          className="px-4 py-2 bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 text-gray-700 dark:text-gray-200 rounded-lg text-sm font-medium transition-colors"
        >
          Search
        </button>
      </div>

      <DataTable
        columns={columns}
        data={data?.results ?? []}
        loading={isLoading}
        rowKey={(p) => p.id}
        emptyMessage="No patients found"
      />

      <Pagination page={page} totalPages={totalPages} onPageChange={setPage} />

      <PatientFormModal
        isOpen={modalOpen}
        onClose={() => setModalOpen(false)}
        onSuccess={refetch}
        patient={editPatient}
      />
    </div>
  );
}
