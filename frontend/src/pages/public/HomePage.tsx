import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { CMSService, EventsService } from '../../api/services';
import { News, Event } from '../../types';
import { HeartHandshake, ArrowRight, Calendar, Newspaper, Layers, Video, MapPin, Sparkles } from 'lucide-react';

export const HomePage: React.FC = () => {
  const [latestNews, setLatestNews] = useState<News[]>([]);
  const [upcomingEvents, setUpcomingEvents] = useState<Event[]>([]);

  useEffect(() => {
    CMSService.getNews({ limit: 3 }).then((res) => {
      const list = Array.isArray(res) ? res : res.results || res.data || [];
      setLatestNews(list.slice(0, 3));
    }).catch(() => {});

    EventsService.getEvents({ limit: 3 }).then((res) => {
      const list = Array.isArray(res) ? res : res.results || res.data || [];
      setUpcomingEvents(list.slice(0, 3));
    }).catch(() => {});
  }, []);

  return (
    <div className="space-y-20 py-8 bvs-bg-pattern">
      {/* Hero Section */}
      <section className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-12 pb-14 text-center">
        {/* Dual Radial Ambient Backdrops */}
        <div className="absolute top-1/3 left-1/4 -translate-x-1/2 -translate-y-1/2 w-[450px] h-[300px] bg-orange-600/10 blur-[130px] rounded-full pointer-events-none" />
        <div className="absolute top-1/3 right-1/4 translate-x-1/2 -translate-y-1/2 w-[450px] h-[300px] bg-rose-600/10 blur-[130px] rounded-full pointer-events-none" />

        <div className="relative z-10 space-y-6">
          <div className="inline-flex items-center gap-2 px-4.5 py-1.5 rounded-full bg-gradient-to-r from-orange-500/10 via-amber-500/20 to-rose-500/10 border border-orange-500/30 text-orange-400 text-xs font-extrabold tracking-wider uppercase shadow-lg shadow-orange-500/5">
            <Sparkles size={14} className="text-orange-400" /> Official Administrative & Media Portal
          </div>
          
          <h1 className="text-4xl sm:text-6xl lg:text-7xl font-black text-slate-100 tracking-tight leading-[1.1] max-w-5xl mx-auto font-heading">
            Empowering & Representing the <br className="hidden sm:inline" />
            <span className="bvs-gradient-text">Bharatiya Vadar Sena</span>
          </h1>

          <p className="max-w-2xl mx-auto text-base sm:text-lg text-slate-300 font-medium leading-relaxed">
            Uniting the community across India through structured regional governance, verified public welfare initiatives, official news bulletins, and statewide assemblies.
          </p>

          <div className="pt-4 flex flex-wrap items-center justify-center gap-4">
            <Link to="/events">
              <Button size="lg" className="bvs-glow-saffron">
                Explore Rallies & Events <ArrowRight size={18} />
              </Button>
            </Link>
            <Link to="/donate">
              <Button size="lg" variant="outline">
                <HeartHandshake size={18} /> Support & Donate
              </Button>
            </Link>
          </div>
        </div>

        {/* Custom 4-Stat Counter Grid */}
        <div className="mt-16 grid grid-cols-2 md:grid-cols-4 gap-5 max-w-4xl mx-auto">
          <div className="p-5 rounded-2xl bg-[#0d121c]/80 border border-slate-800 backdrop-blur-md hover:border-orange-500/30 transition">
            <p className="text-2xl sm:text-3xl font-black text-orange-400 font-heading">4 Tiers</p>
            <span className="text-[11px] text-slate-400 font-semibold uppercase tracking-wider block mt-1">State to Village Network</span>
          </div>
          <div className="p-5 rounded-2xl bg-[#0d121c]/80 border border-slate-800 backdrop-blur-md hover:border-orange-500/30 transition">
            <p className="text-2xl sm:text-3xl font-black text-amber-400 font-heading">100%</p>
            <span className="text-[11px] text-slate-400 font-semibold uppercase tracking-wider block mt-1">Transparent Welfare</span>
          </div>
          <div className="p-5 rounded-2xl bg-[#0d121c]/80 border border-slate-800 backdrop-blur-md hover:border-orange-500/30 transition">
            <p className="text-2xl sm:text-3xl font-black text-rose-400 font-heading">24/7</p>
            <span className="text-[11px] text-slate-400 font-semibold uppercase tracking-wider block mt-1">Public Information Desk</span>
          </div>
          <div className="p-5 rounded-2xl bg-[#0d121c]/80 border border-slate-800 backdrop-blur-md hover:border-orange-500/30 transition">
            <p className="text-2xl sm:text-3xl font-black text-emerald-400 font-heading">Direct</p>
            <span className="text-[11px] text-slate-400 font-semibold uppercase tracking-wider block mt-1">Leadership Bulletins</span>
          </div>
        </div>
      </section>

      {/* Core Pillars */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <h2 className="text-2xl sm:text-4xl font-black text-slate-100 font-heading">Core Organizational Pillars</h2>
          <p className="text-xs sm:text-sm text-slate-400 mt-2 font-medium">Structured governance and community support systems</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <Card className="text-center p-8 group">
            <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-orange-500/20 to-amber-500/10 text-orange-400 flex items-center justify-center mx-auto mb-6 border border-orange-500/30 group-hover:scale-110 transition duration-300 shadow-xl shadow-orange-500/10">
              <Layers size={30} />
            </div>
            <h3 className="text-xl font-bold text-slate-100 mb-3 font-heading">Regional Hierarchy</h3>
            <p className="text-xs text-slate-400 leading-relaxed font-medium">
              Structured 4-tier administrative network connecting State, District, Taluka, and Village office bearer committees seamlessly.
            </p>
          </Card>

          <Card className="text-center p-8 group">
            <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-rose-500/20 to-orange-500/10 text-rose-400 flex items-center justify-center mx-auto mb-6 border border-rose-500/30 group-hover:scale-110 transition duration-300 shadow-xl shadow-rose-500/10">
              <Video size={30} />
            </div>
            <h3 className="text-xl font-bold text-slate-100 mb-3 font-heading">Media & Press Gallery</h3>
            <p className="text-xs text-slate-400 leading-relaxed font-medium">
              Official press bulletins, state rally photo coverage, and video recordings directly broadcasted from central leadership.
            </p>
          </Card>

          <Card className="text-center p-8 group">
            <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-amber-500/20 to-orange-500/10 text-amber-400 flex items-center justify-center mx-auto mb-6 border border-amber-500/30 group-hover:scale-110 transition duration-300 shadow-xl shadow-amber-500/10">
              <HeartHandshake size={30} />
            </div>
            <h3 className="text-xl font-bold text-slate-100 mb-3 font-heading">Community Welfare</h3>
            <p className="text-xs text-slate-400 leading-relaxed font-medium">
              Transparent financial contributions, verified donation e-receipts, youth educational grants, and emergency assistance.
            </p>
          </Card>
        </div>
      </section>

      {/* Latest Press Releases & News */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex flex-col sm:flex-row items-start sm:items-end justify-between gap-4 mb-10 pb-4 border-b border-slate-800">
          <div>
            <div className="inline-flex items-center gap-1.5 text-xs font-extrabold text-orange-400 uppercase tracking-wider mb-2">
              <Newspaper size={16} /> Press Releases
            </div>
            <h2 className="text-2xl sm:text-3xl font-black text-slate-100 font-heading">Latest News & Bulletins</h2>
          </div>
          <Link to="/news" className="text-xs font-bold text-orange-400 hover:text-orange-300 transition flex items-center gap-1">
            View All Press Bulletins <ArrowRight size={14} />
          </Link>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {latestNews.length > 0 ? (
            latestNews.map((item) => (
              <Card key={item.id} className="flex flex-col justify-between">
                <div>
                  <Badge variant="warning" className="mb-3">{item.category_name || 'Announcement'}</Badge>
                  <h3 className="font-bold text-slate-100 text-base line-clamp-2 mb-2 font-heading">{item.title}</h3>
                  <p className="text-xs text-slate-400 line-clamp-3 leading-relaxed font-medium">{item.content}</p>
                </div>
                <div className="mt-6 pt-3.5 border-t border-slate-800/80 text-[11px] text-slate-500 font-mono flex items-center justify-between">
                  <span>{new Date(item.created_at).toLocaleDateString()}</span>
                  <Link to="/news" className="text-orange-400 hover:underline font-bold">Read details &rarr;</Link>
                </div>
              </Card>
            ))
          ) : (
            <Card className="col-span-3 text-center py-12 text-slate-500 text-xs font-medium">No press releases published yet.</Card>
          )}
        </div>
      </section>

      {/* Upcoming Events */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-12">
        <div className="flex flex-col sm:flex-row items-start sm:items-end justify-between gap-4 mb-10 pb-4 border-b border-slate-800">
          <div>
            <div className="inline-flex items-center gap-1.5 text-xs font-extrabold text-orange-400 uppercase tracking-wider mb-2">
              <Calendar size={16} /> Rallies & Assemblies
            </div>
            <h2 className="text-2xl sm:text-3xl font-black text-slate-100 font-heading">Upcoming Events & Conventions</h2>
          </div>
          <Link to="/events" className="text-xs font-bold text-orange-400 hover:text-orange-300 transition flex items-center gap-1">
            View Full Calendar <ArrowRight size={14} />
          </Link>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {upcomingEvents.length > 0 ? (
            upcomingEvents.map((item) => (
              <Card key={item.id} className="flex flex-col justify-between">
                <div>
                  <div className="flex items-center justify-between mb-3">
                    <Badge variant="success">{item.status}</Badge>
                  </div>
                  <h3 className="font-bold text-slate-100 text-base mb-2 font-heading">{item.title}</h3>
                  <p className="text-xs text-slate-400 line-clamp-2 leading-relaxed mb-4 font-medium">{item.description}</p>
                </div>
                <div className="pt-4 border-t border-slate-800 text-xs text-slate-300 space-y-2 font-medium">
                  <div className="flex items-center gap-2">
                    <MapPin size={14} className="text-orange-400 shrink-0" />
                    <span className="truncate">{item.venue_address}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <Calendar size={14} className="text-orange-400 shrink-0" />
                    <span>{new Date(item.start_time).toLocaleString()}</span>
                  </div>
                </div>
              </Card>
            ))
          ) : (
            <Card className="col-span-3 text-center py-12 text-slate-500 text-xs font-medium">No upcoming events scheduled currently.</Card>
          )}
        </div>
      </section>
    </div>
  );
};
