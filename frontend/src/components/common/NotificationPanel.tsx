import { useRef, useEffect } from 'react';
import { clsx } from 'clsx';
import { X, CheckCheck, Trash2, Bell } from 'lucide-react';
import { formatDistanceToNow } from 'date-fns';

import {
  useNotificationStore,
  AppNotification,
  NotificationLevel,
} from '../../store/notificationStore';

interface NotificationPanelProps {
  onClose: () => void;
}

const levelStyles: Record<NotificationLevel, string> = {
  success: 'bg-green-50 dark:bg-green-900/20 border-l-4 border-green-500',
  info: 'bg-blue-50 dark:bg-blue-900/20 border-l-4 border-blue-400',
  warning: 'bg-yellow-50 dark:bg-yellow-900/20 border-l-4 border-yellow-500',
  error: 'bg-red-50 dark:bg-red-900/20 border-l-4 border-red-500',
};

const levelDot: Record<NotificationLevel, string> = {
  success: 'bg-green-500',
  info: 'bg-blue-400',
  warning: 'bg-yellow-500',
  error: 'bg-red-500',
};

function NotificationItem({ n }: { n: AppNotification }) {
  const markRead = useNotificationStore((s) => s.markRead);

  const timeAgo = (() => {
    try {
      return formatDistanceToNow(new Date(n.timestamp), { addSuffix: true });
    } catch {
      return '';
    }
  })();

  return (
    <div
      className={clsx(
        'px-4 py-3 cursor-pointer hover:opacity-90 transition-opacity',
        levelStyles[n.level],
        !n.read && 'font-medium',
      )}
      onClick={() => markRead(n.id)}
    >
      <div className="flex items-start gap-2">
        <span
          className={clsx(
            'mt-1.5 flex-shrink-0 w-2 h-2 rounded-full',
            n.read ? 'bg-gray-300 dark:bg-gray-600' : levelDot[n.level],
          )}
        />
        <div className="flex-1 min-w-0">
          <p className="text-sm text-gray-800 dark:text-gray-100 truncate">
            {n.title}
          </p>
          <p className="text-xs text-gray-500 dark:text-gray-400 mt-0.5 line-clamp-2">
            {n.message}
          </p>
          <p className="text-xs text-gray-400 dark:text-gray-500 mt-1">{timeAgo}</p>
        </div>
      </div>
    </div>
  );
}

export default function NotificationPanel({ onClose }: NotificationPanelProps) {
  const { notifications, unreadCount, markAllRead, clear } =
    useNotificationStore();
  const panelRef = useRef<HTMLDivElement>(null);

  // Close on outside click
  useEffect(() => {
    function handleClick(e: MouseEvent) {
      if (panelRef.current && !panelRef.current.contains(e.target as Node)) {
        onClose();
      }
    }
    document.addEventListener('mousedown', handleClick);
    return () => document.removeEventListener('mousedown', handleClick);
  }, [onClose]);

  return (
    <div
      ref={panelRef}
      className="absolute right-0 top-12 w-80 sm:w-96 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-xl shadow-2xl z-50 flex flex-col max-h-[32rem] overflow-hidden"
    >
      {/* Header */}
      <div className="flex items-center justify-between px-4 py-3 border-b border-gray-100 dark:border-gray-700 flex-shrink-0">
        <div className="flex items-center gap-2">
          <Bell className="w-4 h-4 text-primary-600 dark:text-primary-400" />
          <span className="font-semibold text-gray-800 dark:text-white text-sm">
            Notifications
          </span>
          {unreadCount > 0 && (
            <span className="bg-primary-600 text-white text-xs font-bold px-1.5 py-0.5 rounded-full">
              {unreadCount}
            </span>
          )}
        </div>
        <div className="flex items-center gap-1">
          {unreadCount > 0 && (
            <button
              onClick={markAllRead}
              title="Mark all as read"
              className="p-1.5 text-gray-400 hover:text-primary-600 dark:hover:text-primary-400 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
            >
              <CheckCheck className="w-4 h-4" />
            </button>
          )}
          {notifications.length > 0 && (
            <button
              onClick={clear}
              title="Clear all"
              className="p-1.5 text-gray-400 hover:text-red-500 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
            >
              <Trash2 className="w-4 h-4" />
            </button>
          )}
          <button
            onClick={onClose}
            className="p-1.5 text-gray-400 hover:text-gray-700 dark:hover:text-gray-200 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
          >
            <X className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* List */}
      <div className="overflow-y-auto flex-1 divide-y divide-gray-100 dark:divide-gray-700/50">
        {notifications.length === 0 ? (
          <div className="flex flex-col items-center justify-center py-12 text-gray-400 dark:text-gray-500">
            <Bell className="w-10 h-10 mb-3 opacity-30" />
            <p className="text-sm">No notifications yet</p>
          </div>
        ) : (
          notifications.map((n) => <NotificationItem key={n.id} n={n} />)
        )}
      </div>
    </div>
  );
}
