import React from 'react';
import { clsx } from 'clsx';

interface CardProps {
  children: React.ReactNode;
  className?: string;
  title?: string;
  subtitle?: string;
}

export const Card: React.FC<CardProps> = ({ children, className, title, subtitle }) => {
  return (
    <div className={clsx('bvs-card bvs-card-hover rounded-2xl p-6 relative overflow-hidden group', className)}>
      {/* Top subtle accent glow bar */}
      <div className="absolute top-0 left-0 right-0 h-[2px] bg-gradient-to-r from-transparent via-orange-500/30 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
      
      {(title || subtitle) && (
        <div className="mb-5 pb-3.5 border-b border-slate-800/80">
          {title && <h3 className="text-lg font-bold text-slate-100 tracking-tight font-heading">{title}</h3>}
          {subtitle && <p className="text-xs text-slate-400 mt-1 leading-relaxed">{subtitle}</p>}
        </div>
      )}
      {children}
    </div>
  );
};
