import { useRef, useEffect, useState, useCallback } from 'react';
import { ScanLine, Loader2 } from 'lucide-react';

interface BarcodeScannerProps {
  /** Called when a barcode is submitted (Enter key or button click). */
  onScan: (barcode: string) => void;
  /** Disables the input while a scan is being processed. */
  loading?: boolean;
  /** Placeholder text inside the input. */
  placeholder?: string;
}

/**
 * Reusable barcode input component.
 *
 * Works with both hardware barcode scanners (which type characters rapidly
 * and append Enter) and manual keyboard entry.  The input is auto-focused
 * and cleared after every successful scan so the next scan can happen
 * immediately.
 */
export default function BarcodeScanner({
  onScan,
  loading = false,
  placeholder = 'Scan or type barcode…',
}: BarcodeScannerProps) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [value, setValue] = useState('');

  // Keep the input focused so hardware scanners always feed into it.
  useEffect(() => {
    inputRef.current?.focus();
  }, [loading]);

  const submit = useCallback(() => {
    const trimmed = value.trim();
    if (!trimmed || loading) return;
    onScan(trimmed);
    setValue('');
  }, [value, loading, onScan]);

  return (
    <div className="flex items-center gap-2">
      <div className="relative flex-1">
        <ScanLine className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-primary-500" />
        <input
          ref={inputRef}
          value={value}
          onChange={(e) => setValue(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === 'Enter') {
              e.preventDefault();
              submit();
            }
          }}
          placeholder={placeholder}
          disabled={loading}
          autoComplete="off"
          className="w-full pl-11 pr-4 py-2.5 border-2 border-primary-300 dark:border-primary-600 rounded-lg bg-white dark:bg-gray-700 text-sm text-gray-800 dark:text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition disabled:opacity-60"
        />
      </div>
      <button
        onClick={submit}
        disabled={loading || !value.trim()}
        className="inline-flex items-center gap-2 px-5 py-2.5 bg-primary-600 hover:bg-primary-700 disabled:bg-primary-400 text-white font-medium rounded-lg text-sm transition-colors"
      >
        {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <ScanLine className="w-4 h-4" />}
        {loading ? 'Processing…' : 'Scan'}
      </button>
    </div>
  );
}
