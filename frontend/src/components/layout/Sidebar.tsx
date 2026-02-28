import { NavLink } from 'react-router-dom';
import {
  LayoutDashboard, Users, Bed, Calendar, Stethoscope,
  Heart, Pill, Package, FlaskConical, Receipt, Shield, Settings,
  LogOut, ChevronLeft, ChevronRight,
} from 'lucide-react';
import { useAuthStore } from '../../store/authStore';
import { clsx } from 'clsx';

const navItems = [
  {
    section: 'CLINICAL', items: [
      { label: 'Dashboard', icon: LayoutDashboard, path: '/' },
      { label: 'Patients', icon: Users, path: '/patients' },
      { label: 'ADT', icon: Bed, path: '/adt' },
      { label: 'Appointments', icon: Calendar, path: '/appointments' },
      { label: 'Consultations', icon: Stethoscope, path: '/clinical' },
      { label: 'Nursing', icon: Heart, path: '/nursing' },
    ],
  },
  {
    section: 'PHARMACY', items: [
      { label: 'Pharmacy', icon: Pill, path: '/pharmacy' },
      { label: 'Inventory', icon: Package, path: '/inventory' },
    ],
  },
  {
    section: 'DIAGNOSTICS', items: [
      { label: 'Laboratory', icon: FlaskConical, path: '/laboratory' },
    ],
  },
  {
    section: 'FINANCE', items: [
      { label: 'Billing', icon: Receipt, path: '/billing' },
    ],
  },
  {
    section: 'ADMIN', items: [
      { label: 'Users', icon: Shield, path: '/admin/users' },
      { label: 'Settings', icon: Settings, path: '/admin/settings' },
    ],
  },
];

interface SidebarProps {
  collapsed: boolean;
  onToggle: () => void;
}

export default function Sidebar({ collapsed, onToggle }: SidebarProps) {
  const { logout, user } = useAuthStore();

  return (
    <aside
      className={clsx(
        'flex flex-col bg-sidebar-bg text-sidebar-text transition-all duration-300 h-screen sticky top-0',
        collapsed ? 'w-16' : 'w-64'
      )}
    >
      {/* Logo */}
      <div className="flex items-center justify-between px-4 py-5 border-b border-slate-700">
        {!collapsed && (
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 bg-primary-500 rounded-lg flex items-center justify-center">
              <Heart className="w-5 h-5 text-white" />
            </div>
            <span className="text-white font-bold text-lg">HMS Pro</span>
          </div>
        )}
        {collapsed && (
          <div className="mx-auto w-8 h-8 bg-primary-500 rounded-lg flex items-center justify-center">
            <Heart className="w-5 h-5 text-white" />
          </div>
        )}
        {!collapsed && (
          <button
            onClick={onToggle}
            className="text-sidebar-text hover:text-white transition-colors"
          >
            <ChevronLeft className="w-5 h-5" />
          </button>
        )}
      </div>

      {/* Collapsed toggle */}
      {collapsed && (
        <button
          onClick={onToggle}
          className="flex justify-center py-3 text-sidebar-text hover:text-white transition-colors"
        >
          <ChevronRight className="w-5 h-5" />
        </button>
      )}

      {/* Navigation */}
      <nav className="flex-1 overflow-y-auto py-4 scrollbar-thin">
        {navItems.map(({ section, items }) => (
          <div key={section} className="mb-4">
            {!collapsed && (
              <p className="px-4 text-xs font-semibold text-slate-500 uppercase tracking-wider mb-1">
                {section}
              </p>
            )}
            {collapsed && <div className="border-t border-slate-700 mx-3 mb-2" />}
            {items.map(({ label, icon: Icon, path }) => (
              <NavLink
                key={path}
                to={path}
                end={path === '/'}
                className={({ isActive }) =>
                  clsx(
                    'flex items-center gap-3 px-4 py-2.5 mx-2 rounded-lg transition-colors text-sm font-medium',
                    isActive
                      ? 'bg-sidebar-active text-sidebar-activeText'
                      : 'text-sidebar-text hover:bg-sidebar-hover hover:text-white'
                  )
                }
                title={collapsed ? label : undefined}
              >
                <Icon className="w-5 h-5 flex-shrink-0" />
                {!collapsed && <span>{label}</span>}
              </NavLink>
            ))}
          </div>
        ))}
      </nav>

      {/* User & Logout */}
      <div className="border-t border-slate-700 p-3">
        {!collapsed && user && (
          <div className="flex items-center gap-3 px-2 py-2 mb-2">
            <div className="w-8 h-8 bg-primary-600 rounded-full flex items-center justify-center text-white text-xs font-bold flex-shrink-0">
              {user.first_name?.[0]}{user.last_name?.[0]}
            </div>
            <div className="overflow-hidden">
              <p className="text-white text-sm font-medium truncate">
                {user.first_name} {user.last_name}
              </p>
              <p className="text-slate-400 text-xs truncate">{user.role?.name || 'User'}</p>
            </div>
          </div>
        )}
        <button
          onClick={logout}
          className={clsx(
            'flex items-center gap-3 w-full px-4 py-2.5 rounded-lg text-sm font-medium text-sidebar-text hover:bg-sidebar-hover hover:text-white transition-colors',
            collapsed && 'justify-center'
          )}
          title={collapsed ? 'Logout' : undefined}
        >
          <LogOut className="w-5 h-5 flex-shrink-0" />
          {!collapsed && <span>Logout</span>}
        </button>
      </div>
    </aside>
  );
}
