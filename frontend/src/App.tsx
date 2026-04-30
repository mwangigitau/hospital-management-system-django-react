import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Toaster } from 'react-hot-toast';
import { useAuthStore } from './store/authStore';
import { useRealtimeUpdates } from './hooks/useRealtimeUpdates';
import Layout from './components/layout/Layout';
import LoginPage from './pages/auth/LoginPage';
import DashboardPage from './pages/dashboard/DashboardPage';
import PatientsPage from './pages/patients/PatientsPage';
import ADTPage from './pages/adt/ADTPage';
import BillingPage from './pages/billing/BillingPage';
import LaboratoryPage from './pages/laboratory/LaboratoryPage';
import PharmacyPage from './pages/pharmacy/PharmacyPage';
import AppointmentsPage from './pages/appointments/AppointmentsPage';
import ClinicalPage from './pages/clinical/ClinicalPage';
import NursingPage from './pages/nursing/NursingPage';
import InventoryPage from './pages/inventory/InventoryPage';
import UsersPage from './pages/admin/UsersPage';
import SettingsPage from './pages/admin/SettingsPage';

const queryClient = new QueryClient({
  defaultOptions: { queries: { staleTime: 30_000 } },
});

function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { isAuthenticated } = useAuthStore();
  if (!isAuthenticated) return <Navigate to="/login" replace />;
  return <>{children}</>;
}

/** Inner component that can safely call hooks that depend on QueryClient. */
function AppRoutes() {
  // Opens the WebSocket connection when authenticated and tears it down on
  // logout.  Invalidates React Query caches on every data.update event so
  // every page refreshes automatically.
  useRealtimeUpdates();

  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route
        path="/"
        element={
          <ProtectedRoute>
            <Layout />
          </ProtectedRoute>
        }
      >
        <Route index element={<DashboardPage />} />
        <Route path="patients" element={<PatientsPage />} />
        <Route path="adt" element={<ADTPage />} />
        <Route path="appointments" element={<AppointmentsPage />} />
        <Route path="clinical" element={<ClinicalPage />} />
        <Route path="nursing" element={<NursingPage />} />
        <Route path="pharmacy" element={<PharmacyPage />} />
        <Route path="inventory" element={<InventoryPage />} />
        <Route path="laboratory" element={<LaboratoryPage />} />
        <Route path="billing" element={<BillingPage />} />
        <Route path="admin/users" element={<UsersPage />} />
        <Route path="admin/settings" element={<SettingsPage />} />
      </Route>
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <AppRoutes />
        <Toaster position="top-right" />
      </BrowserRouter>
    </QueryClientProvider>
  );
}
