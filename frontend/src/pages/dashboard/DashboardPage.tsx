import { Users, Bed, Calendar, FlaskConical, Activity, Clock } from 'lucide-react';
import StatsCard from '../../components/common/StatsCard';

const stats = [
  { label: 'Total Patients', value: '1,247', change: '+12%', icon: Users, color: 'blue' as const },
  { label: 'Active Admissions', value: '43', change: '+3', icon: Bed, color: 'green' as const },
  { label: "Today's Appointments", value: '28', change: '-2', icon: Calendar, color: 'purple' as const },
  { label: 'Pending Lab Tests', value: '15', change: '+5', icon: FlaskConical, color: 'orange' as const },
];

const recentActivity = [
  { id: 1, type: 'New Patient', name: 'John Kamau', time: '2 mins ago', status: 'Registered' },
  { id: 2, type: 'Lab Result', name: 'Jane Wanjiku', time: '15 mins ago', status: 'Ready' },
  { id: 3, type: 'Appointment', name: 'Peter Odhiambo', time: '30 mins ago', status: 'Confirmed' },
  { id: 4, type: 'Discharge', name: 'Mary Njeri', time: '1 hr ago', status: 'Discharged' },
  { id: 5, type: 'New Admission', name: 'David Otieno', time: '2 hrs ago', status: 'Admitted' },
];

export default function DashboardPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-800 dark:text-white">Dashboard</h1>
        <p className="text-gray-500 dark:text-gray-400 text-sm mt-1">
          Welcome back — here's what's happening today.
        </p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-5">
        {stats.map((s) => (
          <StatsCard key={s.label} {...s} />
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Recent Activity */}
        <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-100 dark:border-gray-700 shadow-sm p-5">
          <div className="flex items-center gap-2 mb-4">
            <Activity className="w-5 h-5 text-primary-500" />
            <h2 className="text-base font-semibold text-gray-800 dark:text-white">Recent Activity</h2>
          </div>
          <div className="space-y-3">
            {recentActivity.map((item) => (
              <div key={item.id} className="flex items-center justify-between py-2 border-b border-gray-50 dark:border-gray-700 last:border-0">
                <div>
                  <p className="text-sm font-medium text-gray-700 dark:text-gray-200">{item.name}</p>
                  <p className="text-xs text-gray-400">{item.type}</p>
                </div>
                <div className="text-right">
                  <span className="inline-block text-xs bg-primary-50 dark:bg-primary-900/30 text-primary-700 dark:text-primary-300 px-2 py-0.5 rounded-full">
                    {item.status}
                  </span>
                  <p className="text-xs text-gray-400 mt-0.5">{item.time}</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Upcoming Appointments */}
        <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-100 dark:border-gray-700 shadow-sm p-5">
          <div className="flex items-center gap-2 mb-4">
            <Clock className="w-5 h-5 text-primary-500" />
            <h2 className="text-base font-semibold text-gray-800 dark:text-white">Today's Schedule</h2>
          </div>
          <div className="space-y-3">
            {[
              { time: '08:00', patient: 'Alice Mwangi', doctor: 'Dr. Kariuki', dept: 'General' },
              { time: '09:30', patient: 'Bob Auma', doctor: 'Dr. Omondi', dept: 'Cardiology' },
              { time: '10:00', patient: 'Carol Njagi', doctor: 'Dr. Waweru', dept: 'Pediatrics' },
              { time: '11:30', patient: 'Dan Kimani', doctor: 'Dr. Mutua', dept: 'Surgery' },
              { time: '14:00', patient: 'Eve Chebet', doctor: 'Dr. Kariuki', dept: 'General' },
            ].map((appt) => (
              <div key={appt.time} className="flex items-start gap-3 py-2 border-b border-gray-50 dark:border-gray-700 last:border-0">
                <div className="w-16 text-xs font-semibold text-primary-600 dark:text-primary-400 pt-0.5">
                  {appt.time}
                </div>
                <div>
                  <p className="text-sm font-medium text-gray-700 dark:text-gray-200">{appt.patient}</p>
                  <p className="text-xs text-gray-400">{appt.doctor} · {appt.dept}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
