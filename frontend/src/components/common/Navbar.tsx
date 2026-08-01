import React from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { Button } from '../ui/Button';

export const Navbar: React.FC = () => {
  const { user, isAuthenticated, logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const navLinks = [
    { label: 'Home', path: '/' },
    { label: 'About Us', path: '/about' },
    { label: 'Organization', path: '/organization' },
    { label: 'News', path: '/news' },
    { label: 'Events', path: '/events' },
    { label: 'Gallery', path: '/gallery' },
    { label: 'Donate', path: '/donate' },
    { label: 'Contact', path: '/contact' },
  ];

  return (
    <header className="sticky top-0 z-50 bg-[#090d16]/90 backdrop-blur-xl border-b border-slate-800/80 shadow-2xl">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-18 flex items-center justify-between">
        <Link to="/" className="flex items-center gap-3.5 group">
          <div className="w-11 h-11 rounded-2xl bg-gradient-to-br from-orange-500 via-amber-500 to-rose-600 flex items-center justify-center font-black text-slate-950 text-sm shadow-lg shadow-orange-500/25 group-hover:scale-105 transition duration-300 border border-amber-300/30">
            BVS
          </div>
          <div>
            <span className="font-extrabold text-base text-slate-100 tracking-tight block font-heading">Bharatiya Vadar Sena</span>
            <span className="text-[10px] text-orange-400 font-bold uppercase tracking-widest block">Official Information Portal</span>
          </div>
        </Link>

        <nav className="hidden lg:flex items-center gap-1.5 text-xs font-bold text-slate-300 bg-slate-900/60 p-1.5 rounded-2xl border border-slate-800/80">
          {navLinks.map((link) => {
            const isActive = location.pathname === link.path;
            return (
              <Link
                key={link.path}
                to={link.path}
                className={`px-3.5 py-2 rounded-xl transition-all duration-200 ${
                  isActive
                    ? 'bg-gradient-to-r from-orange-600 to-amber-600 text-slate-950 shadow-md font-extrabold'
                    : 'hover:text-orange-400 hover:bg-slate-800/60'
                }`}
              >
                {link.label}
              </Link>
            );
          })}
        </nav>

        <div className="flex items-center gap-3">
          {isAuthenticated ? (
            <div className="flex items-center gap-3">
              {(user?.user_type === 'ADMIN' || user?.user_type === 'SUPERADMIN') && (
                <Button size="sm" onClick={() => navigate('/admin')}>Admin Panel</Button>
              )}
              <Button size="sm" variant="ghost" onClick={logout}>Logout</Button>
            </div>
          ) : (
            <div className="flex items-center gap-2">
              <Link to="/login"><Button size="sm" variant="outline">Admin Login</Button></Link>
            </div>
          )}
        </div>
      </div>
    </header>
  );
};
