import { clsx } from 'clsx';
import { LucideIcon } from 'lucide-react';

type CardColor = 'blue' | 'green' | 'purple' | 'orange';

interface StatsCardProps {
  label: string;
  value: string | number;
  change?: string;
  icon: LucideIcon;
  color: CardColor;
}

const colorMap: Record<CardColor, { bg: string; icon: string; text: string }> = {
  blue: {
    bg: 'bg-blue-50 dark:bg-blue-900/20',
    icon: 'bg-blue-100 text-blue-600 dark:bg-blue-800 dark:text-blue-300',
    text: 'text-blue-600 dark:text-blue-400',
  },
  green: {
    bg: 'bg-green-50 dark:bg-green-900/20',
    icon: 'bg-green-100 text-green-600 dark:bg-green-800 dark:text-green-300',
    text: 'text-green-600 dark:text-green-400',
  },
  purple: {
    bg: 'bg-purple-50 dark:bg-purple-900/20',
    icon: 'bg-purple-100 text-purple-600 dark:bg-purple-800 dark:text-purple-300',
    text: 'text-purple-600 dark:text-purple-400',
  },
  orange: {
    bg: 'bg-orange-50 dark:bg-orange-900/20',
    icon: 'bg-orange-100 text-orange-600 dark:bg-orange-800 dark:text-orange-300',
    text: 'text-orange-600 dark:text-orange-400',
  },
};

export default function StatsCard({ label, value, change, icon: Icon, color }: StatsCardProps) {
  const c = colorMap[color];
  return (
    <div className={clsx('rounded-xl p-5 shadow-sm border border-gray-100 dark:border-gray-700 bg-white dark:bg-gray-800')}>
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm text-gray-500 dark:text-gray-400 font-medium">{label}</p>
          <p className="text-2xl font-bold text-gray-800 dark:text-white mt-1">{value}</p>
          {change && (
            <p className={clsx('text-xs font-medium mt-1', c.text)}>
              {change} from last month
            </p>
          )}
        </div>
        <div className={clsx('w-12 h-12 rounded-xl flex items-center justify-center', c.icon)}>
          <Icon className="w-6 h-6" />
        </div>
      </div>
    </div>
  );
}
