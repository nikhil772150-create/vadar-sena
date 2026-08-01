import React from 'react';
import { clsx } from 'clsx';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'danger' | 'outline' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  isLoading?: boolean;
}

export const Button: React.FC<ButtonProps> = ({
  children,
  variant = 'primary',
  size = 'md',
  isLoading = false,
  className,
  disabled,
  ...props
}) => {
  const base = 'font-bold rounded-xl transition-all duration-300 inline-flex items-center justify-center active:scale-[0.97] focus:outline-none focus:ring-2 focus:ring-orange-500/50 disabled:opacity-50 disabled:pointer-events-none tracking-wide';
  
  const variants = {
    primary: 'bg-gradient-to-r from-orange-600 via-amber-600 to-orange-500 hover:from-orange-500 hover:to-amber-500 text-slate-950 shadow-lg shadow-orange-600/25 hover:shadow-orange-600/40 border border-amber-400/40 font-extrabold',
    secondary: 'bg-slate-800/90 hover:bg-slate-700/90 text-slate-100 border border-slate-700/80 hover:border-slate-600 shadow-md',
    danger: 'bg-gradient-to-r from-rose-700 to-rose-600 hover:from-rose-600 hover:to-rose-500 text-white shadow-lg shadow-rose-700/25 border border-rose-500/40',
    outline: 'border border-orange-500/40 text-orange-400 hover:bg-orange-500/10 hover:border-orange-400/70 backdrop-blur-sm',
    ghost: 'text-slate-300 hover:bg-slate-800/70 hover:text-orange-400',
  };

  const sizes = {
    sm: 'px-3.5 py-1.5 text-xs gap-1.5',
    md: 'px-4.5 py-2.5 text-xs uppercase tracking-wider gap-2',
    lg: 'px-6.5 py-3.5 text-sm uppercase tracking-wider gap-2.5',
  };

  return (
    <button
      className={clsx(base, variants[variant], sizes[size], isLoading && 'opacity-70 cursor-not-allowed', className)}
      disabled={disabled || isLoading}
      {...props}
    >
      {isLoading ? (
        <span className="inline-flex items-center gap-2">
          <svg className="animate-spin h-4 w-4 text-current" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          Loading...
        </span>
      ) : children}
    </button>
  );
};
