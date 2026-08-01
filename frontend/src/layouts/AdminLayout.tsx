import React from 'react';
import { Outlet, Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { LayoutDashboard, Building2, Newspaper, Calendar, DollarSign, BarChart3, LogOut, ArrowLeft } from 'lucide-react';

export const AdminLayout: React.FC = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const navItems = [
    { label: 'Executive Dashboard', path: '/admin', icon: LayoutDashboard },
    { label: 'Organization Hierarchy', path: '/admin/organization', icon: Building2 },
    { label: 'News & Static CMS', path: '/admin/cms', icon: Newspaper },
    { label: 'Events & Meetings', path: '/admin/events', icon: Calendar },
    { label: 'Donations Verification', path: '/admin/donations', icon: DollarSign },
    { label: 'Reports & Analytics', path: '/admin/reports', icon: BarChart3 },
  ];

  return (
    <div className="min-h-screen bg-[#090d16] text-slate-100 flex">
      <aside className="w-64 bg-[#0d121c] border-r border-slate-800/90 flex flex-col p-4">
        <div className="flex items-center gap-3 mb-8 px-2">
          <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-orange-500 to-amber-600 flex items-center justify-center font-extrabold text-slate-950 text-xs shadow-md shadow-orange-500/20">
            ADM
          </div>
          <div>
            <h2 className="font-extrabold text-sm text-slate-100 font-heading">BVS Admin Control</h2>
            <span className="text-[10px] text-orange-400 font-mono uppercase tracking-widest">{user?.user_type}</span>
          </div>
        </div>

        <nav className="space-y-1.5 flex-1">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = location.pathname === item.path;
            return (
              <Link
                key={item.path}
                to={item.path}
                className={`flex items-center gap-3 px-3.5 py-2.5 rounded-xl text-xs font-bold transition-all duration-200 ${
                  isActive
                    ? 'bg-gradient-to-r from-orange-600/30 to-amber-600/20 text-orange-400 border border-orange-500/40 shadow-sm'
                    : 'text-slate-400 hover:bg-slate-800/60 hover:text-slate-200'
                }`}
              >
                <Icon size={16} className={isActive ? 'text-orange-400' : 'text-slate-500'} />
                {item.label}
              </Link>
            );
          })}
        </nav>

        <div className="border-t border-slate-800/90 pt-4 space-y-2">
          <button
            onClick={() => navigate('/')}
            className="w-full flex items-center gap-2 px-3.5 py-2 rounded-xl text-xs font-semibold text-slate-400 hover:bg-slate-800 hover:text-slate-200 transition"
          >
            <ArrowLeft size={16} /> Public Website
          </button>
          <button
            onClick={logout}
            className="w-full flex items-center gap-2 px-3.5 py-2 rounded-xl text-xs font-semibold text-rose-400 hover:bg-rose-500/10 transition"
          >
            <LogOut size={16} /> Logout
          </button>
        </div>
      </aside>

      <main className="flex-1 p-8 overflow-y-auto bvs-bg-pattern">
        <Outlet />
      </main>
    </div>
  );
};
