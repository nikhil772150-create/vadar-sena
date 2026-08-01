import React from 'react';
import { clsx } from 'clsx';

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
}

export const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ label, error, className, ...props }, ref) => {
    return (
      <div className="w-full space-y-1.5">
        {label && (
          <label className="block text-xs font-bold text-slate-300 uppercase tracking-wider">
            {label}
          </label>
        )}
        <input
          ref={ref}
          className={clsx(
            'w-full bg-[#0d121c] border border-slate-800 text-slate-100 text-sm rounded-xl px-4 py-2.5 outline-none transition-all duration-200 placeholder:text-slate-600',
            'focus:border-orange-500/80 focus:ring-2 focus:ring-orange-500/20 focus:bg-[#090d16]',
            error && 'border-rose-500 focus:border-rose-500 focus:ring-rose-500/20',
            className
          )}
          {...props}
        />
        {error && <p className="text-[11px] font-semibold text-rose-400 mt-1">{error}</p>}
      </div>
    );
  }
);

Input.displayName = 'Input';
