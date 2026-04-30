import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { clsx } from 'clsx';
import api from '../../lib/api';
import Badge from '../../components/common/Badge';

type Tab = 'wards' | 'admissions' | 'beds';

interface Ward { id: string; name: string; ward_type: string; total_beds: number; occupied_beds: number; }
interface Admission { id: string; patient_name: string; ward: string; bed: string; admitted_at: string; status: string; }
interface Bed { id: string; bed_number: string; room: string; ward: string; status: 'available' | 'occupied' | 'reserved' | 'maintenance'; patient_name?: string; }

const bedStatusConfig = {
  available: { label: 'Available', color: 'bg-green-100 border-green-300 text-green-700' },
  occupied: { label: 'Occupied', color: 'bg-red-100 border-red-300 text-red-700' },
  reserved: { label: 'Reserved', color: 'bg-yellow-100 border-yellow-300 text-yellow-700' },
  maintenance: { label: 'Maintenance', color: 'bg-gray-100 border-gray-300 text-gray-600' },
};

// Placeholder data for demonstration
const mockBeds: Bed[] = Array.from({ length: 24 }, (_, i) => ({
  id: String(i + 1),
  bed_number: `B${String(i + 1).padStart(2, '0')}`,
  room: `Room ${Math.floor(i / 4) + 1}`,
  ward: 'General Ward',
  status: (['available', 'occupied', 'occupied', 'available', 'reserved'][i % 5]) as Bed['status'],
  patient_name: i % 2 === 1 ? `Patient ${i}` : undefined,
}));

export default function ADTPage() {
  const [activeTab, setActiveTab] = useState<Tab>('wards');

  const { data: wards, isLoading: wardsLoading } = useQuery<Ward[]>({
    queryKey: ['wards'],
    queryFn: () => api.get('/adt/wards/').then((r) => r.data.results ?? r.data),
    retry: false,
  });

  const { data: admissions, isLoading: admissionsLoading } = useQuery<Admission[]>({
    queryKey: ['admissions'],
    queryFn: () => api.get('/adt/admissions/').then((r) => r.data.results ?? r.data),
    retry: false,
    enabled: activeTab === 'admissions',
  });

  const tabs: { key: Tab; label: string }[] = [
    { key: 'wards', label: 'Wards' },
    { key: 'admissions', label: 'Admissions' },
    { key: 'beds', label: 'Bed Status' },
  ];

  return (
    <div className="space-y-5">
      <div>
        <h1 className="text-2xl font-bold text-gray-800 dark:text-white">ADT Management</h1>
        <p className="text-sm text-gray-500 dark:text-gray-400">Admissions, Discharges &amp; Transfers</p>
      </div>

      {/* Tabs */}
      <div className="flex gap-1 bg-gray-100 dark:bg-gray-800 p-1 rounded-xl w-fit">
        {tabs.map((t) => (
          <button
            key={t.key}
            onClick={() => setActiveTab(t.key)}
            className={clsx(
              'px-4 py-2 rounded-lg text-sm font-medium transition-colors',
              activeTab === t.key
                ? 'bg-white dark:bg-gray-700 text-gray-800 dark:text-white shadow-sm'
                : 'text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200'
            )}
          >
            {t.label}
          </button>
        ))}
      </div>

      {/* Wards Tab */}
      {activeTab === 'wards' && (
        <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-5">
          {wardsLoading
            ? Array(6).fill(0).map((_, i) => (
                <div key={i} className="h-32 bg-gray-100 dark:bg-gray-800 rounded-xl animate-pulse" />
              ))
            : (wards ?? []).map((ward) => {
                const pct = ward.total_beds ? Math.round((ward.occupied_beds / ward.total_beds) * 100) : 0;
                return (
                  <div key={ward.id} className="bg-white dark:bg-gray-800 rounded-xl border border-gray-100 dark:border-gray-700 shadow-sm p-5">
                    <div className="flex items-start justify-between mb-3">
                      <div>
                        <h3 className="font-semibold text-gray-800 dark:text-white">{ward.name}</h3>
                        <p className="text-xs text-gray-400">{ward.ward_type}</p>
                      </div>
                      <Badge variant={pct > 80 ? 'error' : pct > 60 ? 'warning' : 'success'}>
                        {pct}% full
                      </Badge>
                    </div>
                    <div className="flex justify-between text-sm text-gray-500 dark:text-gray-400 mb-2">
                      <span>Occupied: {ward.occupied_beds}</span>
                      <span>Total: {ward.total_beds}</span>
                    </div>
                    <div className="w-full bg-gray-100 dark:bg-gray-700 rounded-full h-2">
                      <div
                        className={clsx('h-2 rounded-full', pct > 80 ? 'bg-red-500' : pct > 60 ? 'bg-yellow-500' : 'bg-green-500')}
                        style={{ width: `${pct}%` }}
                      />
                    </div>
                  </div>
                );
              })}
          {!wardsLoading && !wards?.length && (
            <p className="text-gray-400 col-span-full text-center py-10">No wards found</p>
          )}
        </div>
      )}

      {/* Admissions Tab */}
      {activeTab === 'admissions' && (
        <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-100 dark:border-gray-700 shadow-sm overflow-hidden">
          <table className="w-full text-sm">
            <thead className="bg-gray-50 dark:bg-gray-900 border-b border-gray-200 dark:border-gray-700">
              <tr>
                {['Patient', 'Ward', 'Bed', 'Admitted', 'Status'].map((h) => (
                  <th key={h} className="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase">{h}</th>
                ))}
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100 dark:divide-gray-700">
              {admissionsLoading ? (
                <tr><td colSpan={5} className="text-center py-10 text-gray-400">Loading...</td></tr>
              ) : admissions?.length ? (
                admissions.map((adm) => (
                  <tr key={adm.id} className="hover:bg-gray-50 dark:hover:bg-gray-900">
                    <td className="px-4 py-3 text-gray-700 dark:text-gray-300">{adm.patient_name}</td>
                    <td className="px-4 py-3 text-gray-500">{adm.ward}</td>
                    <td className="px-4 py-3 text-gray-500">{adm.bed}</td>
                    <td className="px-4 py-3 text-gray-500">{adm.admitted_at}</td>
                    <td className="px-4 py-3">
                      <Badge variant="success">{adm.status}</Badge>
                    </td>
                  </tr>
                ))
              ) : (
                <tr><td colSpan={5} className="text-center py-10 text-gray-400">No admissions found</td></tr>
              )}
            </tbody>
          </table>
        </div>
      )}

      {/* Bed Status Tab */}
      {activeTab === 'beds' && (
        <div className="space-y-4">
          <div className="flex flex-wrap gap-3 p-3 bg-white dark:bg-gray-800 rounded-xl border border-gray-100 dark:border-gray-700 shadow-sm w-fit">
            {Object.entries(bedStatusConfig).map(([key, { label, color }]) => (
              <div key={key} className="flex items-center gap-2 text-sm">
                <div className={clsx('w-4 h-4 rounded border', color)} />
                <span className="text-gray-600 dark:text-gray-400">{label}</span>
              </div>
            ))}
          </div>
          <div className="grid grid-cols-4 sm:grid-cols-6 md:grid-cols-8 gap-3">
            {mockBeds.map((bed) => {
              const cfg = bedStatusConfig[bed.status];
              return (
                <div
                  key={bed.id}
                  title={bed.patient_name ?? bed.status}
                  className={clsx(
                    'p-2 rounded-lg border text-center text-xs cursor-pointer hover:opacity-80 transition-opacity',
                    cfg.color
                  )}
                >
                  <div className="font-bold">{bed.bed_number}</div>
                  <div className="text-xs opacity-70">{bed.room}</div>
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
}
