import React from 'react';
import { Link } from 'react-router-dom';
import { Mail, Phone, MapPin, ChevronRight } from 'lucide-react';

export const Footer: React.FC = () => {
  return (
    <footer className="bg-[#070a11] border-t border-slate-800/90 text-slate-400 text-sm mt-auto relative overflow-hidden">
      {/* Background Subtle Radial Gradient */}
      <div className="absolute inset-0 bg-gradient-to-t from-orange-950/20 via-transparent to-transparent pointer-events-none" />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 grid grid-cols-1 md:grid-cols-4 gap-12 relative z-10">
        <div className="space-y-4">
          <Link to="/" className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-orange-500 via-amber-500 to-rose-600 flex items-center justify-center font-black text-slate-950 text-xs shadow-md shadow-orange-500/20">
              BVS
            </div>
            <div>
              <span className="font-extrabold text-slate-100 text-base tracking-tight block font-heading">Bharatiya Vadar Sena</span>
              <span className="text-[10px] text-orange-400 font-bold uppercase tracking-widest block">Official Information Portal</span>
            </div>
          </Link>
          <p className="text-xs text-slate-400 leading-relaxed">
            Empowering the Vadar community across India with structured regional representation, official press bulletins, public rallies, and transparent fund management.
          </p>
        </div>

        <div>
          <h4 className="font-bold text-slate-100 mb-4 text-xs uppercase tracking-widest text-orange-400 font-heading">Quick Navigation</h4>
          <ul className="space-y-2.5 text-xs font-semibold">
            <li><Link to="/about" className="hover:text-orange-400 transition flex items-center gap-1.5"><ChevronRight size={12} className="text-orange-500" /> About Organization</Link></li>
            <li><Link to="/organization" className="hover:text-orange-400 transition flex items-center gap-1.5"><ChevronRight size={12} className="text-orange-500" /> Hierarchy Structure</Link></li>
            <li><Link to="/events" className="hover:text-orange-400 transition flex items-center gap-1.5"><ChevronRight size={12} className="text-orange-500" /> Statewide Rallies & Events</Link></li>
            <li><Link to="/donate" className="hover:text-orange-400 transition flex items-center gap-1.5"><ChevronRight size={12} className="text-orange-500" /> Support & Donations</Link></li>
          </ul>
        </div>

        <div>
          <h4 className="font-bold text-slate-100 mb-4 text-xs uppercase tracking-widest text-orange-400 font-heading">Media & Resources</h4>
          <ul className="space-y-2.5 text-xs font-semibold">
            <li><Link to="/news" className="hover:text-orange-400 transition flex items-center gap-1.5"><ChevronRight size={12} className="text-orange-500" /> Press Releases & Bulletins</Link></li>
            <li><Link to="/gallery" className="hover:text-orange-400 transition flex items-center gap-1.5"><ChevronRight size={12} className="text-orange-500" /> Photo & Video Gallery</Link></li>
            <li><Link to="/contact" className="hover:text-orange-400 transition flex items-center gap-1.5"><ChevronRight size={12} className="text-orange-500" /> Contact & Support Desk</Link></li>
            <li><Link to="/login" className="hover:text-orange-400 transition flex items-center gap-1.5"><ChevronRight size={12} className="text-orange-500" /> Admin Portal Access</Link></li>
          </ul>
        </div>

        <div>
          <h4 className="font-bold text-slate-100 mb-4 text-xs uppercase tracking-widest text-orange-400 font-heading">Central Office</h4>
          <div className="space-y-3 text-xs text-slate-400">
            <div className="flex items-center gap-2.5">
              <div className="w-7 h-7 rounded-lg bg-orange-500/10 border border-orange-500/20 flex items-center justify-center text-orange-400 shrink-0">
                <MapPin size={14} />
              </div>
              <span>Pune, Maharashtra, India</span>
            </div>
            <div className="flex items-center gap-2.5">
              <div className="w-7 h-7 rounded-lg bg-orange-500/10 border border-orange-500/20 flex items-center justify-center text-orange-400 shrink-0">
                <Phone size={14} />
              </div>
              <span className="font-mono">+91 98765 43210</span>
            </div>
            <div className="flex items-center gap-2.5">
              <div className="w-7 h-7 rounded-lg bg-orange-500/10 border border-orange-500/20 flex items-center justify-center text-orange-400 shrink-0">
                <Mail size={14} />
              </div>
              <span className="font-mono">contact@vadarsena.org</span>
            </div>
          </div>
        </div>
      </div>

      <div className="border-t border-slate-900/90 py-6 text-center text-xs text-slate-500 relative z-10 flex flex-col sm:flex-row items-center justify-between max-w-7xl mx-auto px-4">
        <span>&copy; {new Date().getFullYear()} Bharatiya Vadar Sena (BVS). All Rights Reserved.</span>
        <span className="text-[11px] text-slate-600 mt-2 sm:mt-0 font-mono">Official NGO Information System</span>
      </div>
    </footer>
  );
};
