import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import Modal from '../../components/common/Modal';
import LoadingSpinner from '../../components/common/LoadingSpinner';
import api from '../../lib/api';

const schema = z.object({
  first_name: z.string().min(1, 'First name is required'),
  last_name: z.string().min(1, 'Last name is required'),
  date_of_birth: z.string().min(1, 'Date of birth is required'),
  gender: z.enum(['M', 'F', 'O'], { error: 'Gender is required' }),
  blood_group: z.string().optional(),
  phone: z.string().min(10, 'Phone number must be at least 10 digits'),
  email: z.string().email('Invalid email').or(z.literal('')).optional(),
  address: z.string().optional(),
  nhif_number: z.string().optional(),
});

type FormData = z.infer<typeof schema>;

interface PatientFormModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSuccess: () => void;
  patient?: Partial<FormData> & { id?: string };
}

const bloodGroups = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'];

export default function PatientFormModal({ isOpen, onClose, onSuccess, patient }: PatientFormModalProps) {
  const isEdit = !!patient?.id;

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
    reset,
  } = useForm<FormData>({
    resolver: zodResolver(schema),
    defaultValues: patient,
  });

  const onSubmit = async (data: FormData) => {
    try {
      if (isEdit) {
        await api.patch(`/patients/patients/${patient?.id}/`, data);
      } else {
        await api.post('/patients/patients/', data);
      }
      reset();
      onSuccess();
      onClose();
    } catch (err) {
      console.error(err);
    }
  };

  const inputClass =
    'w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-800 dark:text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent text-sm';

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title={isEdit ? 'Edit Patient' : 'Register Patient'}
      size="xl"
    >
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">First Name *</label>
            <input {...register('first_name')} className={inputClass} placeholder="First name" />
            {errors.first_name && <p className="mt-1 text-xs text-red-500">{errors.first_name.message}</p>}
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Last Name *</label>
            <input {...register('last_name')} className={inputClass} placeholder="Last name" />
            {errors.last_name && <p className="mt-1 text-xs text-red-500">{errors.last_name.message}</p>}
          </div>
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Date of Birth *</label>
            <input {...register('date_of_birth')} type="date" className={inputClass} />
            {errors.date_of_birth && <p className="mt-1 text-xs text-red-500">{errors.date_of_birth.message}</p>}
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Gender *</label>
            <select {...register('gender')} className={inputClass}>
              <option value="">Select gender</option>
              <option value="M">Male</option>
              <option value="F">Female</option>
              <option value="O">Other</option>
            </select>
            {errors.gender && <p className="mt-1 text-xs text-red-500">{errors.gender.message}</p>}
          </div>
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Blood Group</label>
            <select {...register('blood_group')} className={inputClass}>
              <option value="">Select blood group</option>
              {bloodGroups.map((bg) => <option key={bg} value={bg}>{bg}</option>)}
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Phone *</label>
            <input {...register('phone')} className={inputClass} placeholder="+254700000000" />
            {errors.phone && <p className="mt-1 text-xs text-red-500">{errors.phone.message}</p>}
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Email</label>
          <input {...register('email')} type="email" className={inputClass} placeholder="patient@example.com" />
          {errors.email && <p className="mt-1 text-xs text-red-500">{errors.email.message}</p>}
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Address</label>
          <input {...register('address')} className={inputClass} placeholder="Physical address" />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">NHIF Number</label>
          <input {...register('nhif_number')} className={inputClass} placeholder="NHIF membership number" />
        </div>

        <div className="flex justify-end gap-3 pt-2">
          <button
            type="button"
            onClick={onClose}
            className="px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-200 bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 rounded-lg transition-colors"
          >
            Cancel
          </button>
          <button
            type="submit"
            disabled={isSubmitting}
            className="flex items-center gap-2 px-4 py-2 text-sm font-medium bg-primary-600 hover:bg-primary-700 disabled:bg-primary-400 text-white rounded-lg transition-colors"
          >
            {isSubmitting && <LoadingSpinner size="sm" />}
            {isEdit ? 'Save Changes' : 'Register Patient'}
          </button>
        </div>
      </form>
    </Modal>
  );
}
