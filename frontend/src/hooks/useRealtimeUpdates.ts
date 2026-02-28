import { useEffect } from 'react';
import { useQueryClient } from '@tanstack/react-query';
import toast from 'react-hot-toast';

import { wsManager, WSMessage } from '../lib/websocket';
import { useNotificationStore, NotificationLevel } from '../store/notificationStore';
import { useAuthStore } from '../store/authStore';

/**
 * Maps a backend app label to the React Query cache keys that should be
 * invalidated when that app broadcasts a change.
 */
const APP_QUERY_KEYS: Record<string, string[][]> = {
  patients: [['patients']],
  adt: [['wards'], ['admissions'], ['beds']],
  appointments: [['appointments'], ['queue']],
  clinical: [['consultations'], ['prescriptions']],
  nursing: [['vitals'], ['nursing-notes']],
  pharmacy: [['drugs'], ['drug-batches'], ['stock-movements'], ['prescriptions']],
  inventory: [['items'], ['store-items'], ['stock-transfers']],
  laboratory: [['lab-requests'], ['test-results']],
  billing: [['invoices'], ['payments']],
};

function showToast(level: NotificationLevel, text: string): void {
  const opts = { duration: 4000 };
  switch (level) {
    case 'success':
      toast.success(text, opts);
      break;
    case 'warning':
      toast(text, { ...opts, icon: '⚠️' });
      break;
    case 'error':
      toast.error(text, opts);
      break;
    default:
      toast(text, { ...opts, icon: '🔔' });
  }
}

/**
 * Mount this hook once at the app root (inside <QueryClientProvider>).
 *
 * • Opens the WebSocket when the user is authenticated.
 * • On every `data.update` event:
 *     1. Instantly invalidates the relevant React Query cache keys so the
 *        UI refetches and shows fresh data without a manual page refresh.
 *     2. Adds an entry to the in-app notification store.
 *     3. Pops a toast.
 * • On `notification` events (personal alerts):
 *     1. Adds to the notification store.
 *     2. Pops a toast.
 * • Tears down the connection when the user logs out.
 */
export function useRealtimeUpdates(): void {
  const queryClient = useQueryClient();
  const addNotification = useNotificationStore((s) => s.add);
  const { isAuthenticated } = useAuthStore();

  useEffect(() => {
    if (!isAuthenticated) {
      wsManager.disconnect();
      return;
    }

    const token = localStorage.getItem('access_token');
    if (!token) return;

    wsManager.connect(token);

    const unsubscribe = wsManager.addHandler((msg: WSMessage) => {
      if (msg.type === 'data.update') {
        const app = msg.app as string;
        const notification = msg.notification as
          | { title: string; message: string; level: NotificationLevel }
          | null
          | undefined;

        // 1. Invalidate React Query caches – triggers background refetch
        const keys = APP_QUERY_KEYS[app] ?? [];
        keys.forEach((key) => queryClient.invalidateQueries({ queryKey: key }));

        // 2. Add to notification panel + show toast
        if (notification) {
          const level: NotificationLevel = notification.level ?? 'info';
          addNotification({
            title: notification.title,
            message: notification.message,
            level,
            timestamp: (msg.timestamp as string) ?? new Date().toISOString(),
            app,
            model: msg.model as string | undefined,
            action: msg.action as string | undefined,
          });
          showToast(level, `${notification.title}: ${notification.message}`);
        }
      } else if (msg.type === 'notification') {
        // Personal notification from the server
        const level: NotificationLevel = (msg.level as NotificationLevel) ?? 'info';
        addNotification({
          title: msg.title as string,
          message: msg.message as string,
          level,
          timestamp: (msg.timestamp as string) ?? new Date().toISOString(),
        });
        showToast(level, msg.message as string);
      }
    });

    return unsubscribe;
  }, [isAuthenticated, queryClient, addNotification]);
}
