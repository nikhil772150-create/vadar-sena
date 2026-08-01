import React, { useEffect, useState } from 'react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { AnalyticsService, CMSService, EventsService } from '../../api/services';
import { Newspaper, Calendar, DollarSign, Layers } from 'lucide-react';

export const AdminDashboard: React.FC = () => {
  const [newsCount, setNewsCount] = useState<number>(0);
  const [eventsCount, setEventsCount] = useState<number>(0);
  const [donationTotal, setDonationTotal] = useState<number>(0);
  const [regionalNodes, setRegionalNodes] = useState<any[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  const extractList = (res: any) => {
    if (!res) return [];
    if (Array.isArray(res)) return res;
    if (Array.isArray(res.results)) return res.results;
    if (Array.isArray(res.data)) return res.data;
    return [];
  };

  useEffect(() => {
    Promise.all([
      CMSService.getNews({}),
      EventsService.getEvents({}),
      AnalyticsService.getDonationReport(),
      AnalyticsService.getRegionalStats(),
    ])
      .then(([newsRes, eventsRes, donationRes, regionalRes]) => {
        setNewsCount(extractList(newsRes).length);
        setEventsCount(extractList(eventsRes).length);
        setDonationTotal(donationRes?.data?.summary?.total_amount || 0);
        setRegionalNodes(extractList(regionalRes));
      })
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return <div className="text-center py-12 text-slate-400 text-xs font-semibold">Loading Admin Control Dashboard...</div>;
  }

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-2xl font-bold text-slate-100 font-heading">NGO Executive Dashboard</h1>
        <p className="text-xs text-slate-400 mt-1 font-medium">Real-time content management, events monitoring, and financial collection overview</p>
      </div>

      {/* Counter Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
        <Card className="p-5 border-orange-500/30">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">Press Releases & News</span>
            <div className="w-8 h-8 rounded-xl bg-orange-500/10 border border-orange-500/30 flex items-center justify-center text-orange-400">
              <Newspaper size={18} />
            </div>
          </div>
          <p className="text-3xl font-black text-slate-100 mt-3 font-heading">{newsCount}</p>
          <span className="text-[11px] text-orange-400 font-bold uppercase tracking-wider block mt-1">Published Articles</span>
        </Card>

        <Card className="p-5 border-emerald-500/30">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">Scheduled Events</span>
            <div className="w-8 h-8 rounded-xl bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-center text-emerald-400">
              <Calendar size={18} />
            </div>
          </div>
          <p className="text-3xl font-black text-emerald-400 mt-3 font-heading">{eventsCount}</p>
          <span className="text-[11px] text-slate-400 font-semibold block mt-1">Public Rallies & Meets</span>
        </Card>

        <Card className="p-5 border-sky-500/30">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">Verified Fund Collection</span>
            <div className="w-8 h-8 rounded-xl bg-sky-500/10 border border-sky-500/30 flex items-center justify-center text-sky-400">
              <DollarSign size={18} />
            </div>
          </div>
          <p className="text-2xl font-black text-sky-400 mt-3 font-heading">₹{donationTotal.toLocaleString()}</p>
          <span className="text-[11px] text-slate-400 font-semibold block mt-1">Verified Public Donations</span>
        </Card>

        <Card className="p-5 border-purple-500/30">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">Regional Hierarchy Nodes</span>
            <div className="w-8 h-8 rounded-xl bg-purple-500/10 border border-purple-500/30 flex items-center justify-center text-purple-400">
              <Layers size={18} />
            </div>
          </div>
          <p className="text-3xl font-black text-purple-400 mt-3 font-heading">{regionalNodes.length}</p>
          <span className="text-[11px] text-slate-400 font-semibold block mt-1">State / District Units</span>
        </Card>
      </div>

      {/* Regional Units Grid */}
      <Card title="Active Organizational Nodes Overview" subtitle="Regional hierarchy management and state unit directory">
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
          {regionalNodes.length > 0 ? (
            regionalNodes.map((n: any, idx: number) => (
              <div key={idx} className="p-4 rounded-xl bg-[#090d16] border border-slate-800 flex items-center justify-between">
                <div>
                  <h4 className="text-sm font-bold text-slate-100 font-heading">{n.name || n.state_name || `Unit #${idx + 1}`}</h4>
                  <span className="text-[10px] text-orange-400 font-mono">Code: {n.code || 'MH'}</span>
                </div>
                <Badge variant="success">Active Node</Badge>
              </div>
            ))
          ) : (
            <p className="text-xs text-slate-500 py-6 col-span-3 text-center font-medium">Master organization units loaded.</p>
          )}
        </div>
      </Card>
    </div>
  );
};
