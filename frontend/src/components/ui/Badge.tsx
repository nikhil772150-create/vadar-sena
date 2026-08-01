import React from 'react';
import { clsx } from 'clsx';

interface BadgeProps {
  children: React.ReactNode;
  variant?: 'success' | 'warning' | 'danger' | 'info' | 'neutral';
  className?: string;
}

export const Badge: React.FC<BadgeProps> = ({ children, variant = 'info', className }) => {
  const variants = {
    success: 'bg-emerald-950/80 text-emerald-400 border-emerald-500/40 shadow-sm shadow-emerald-500/10',
    warning: 'bg-orange-950/80 text-orange-400 border-orange-500/40 shadow-sm shadow-orange-500/10',
    danger: 'bg-rose-950/80 text-rose-400 border-rose-500/40 shadow-sm shadow-rose-500/10',
    info: 'bg-sky-950/80 text-sky-400 border-sky-500/40 shadow-sm shadow-sky-500/10',
    neutral: 'bg-slate-900/90 text-slate-300 border-slate-700/80',
  };

  return (
    <span className={clsx('inline-flex items-center px-3 py-1 rounded-full text-[10px] font-extrabold tracking-wider border uppercase', variants[variant], className)}>
      {children}
    </span>
  );
};
