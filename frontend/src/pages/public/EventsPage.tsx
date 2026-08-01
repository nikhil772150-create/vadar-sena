import React, { useEffect, useState } from 'react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { Calendar as CalendarIcon, MapPin, Users, CheckCircle2 } from 'lucide-react';
import { EventsService } from '../../api/services';
import { useAuth } from '../../context/AuthContext';
import { Event } from '../../types';

export const EventsPage: React.FC = () => {
  const [events, setEvents] = useState<Event[]>([]);
  const [activeTab, setActiveTab] = useState<'UPCOMING' | 'ALL'>('UPCOMING');
  const [rsvpSuccess, setRsvpSuccess] = useState<string>('');
  const { isAuthenticated } = useAuth();

  const extractList = (res: any) => {
    if (!res) return [];
    if (Array.isArray(res)) return res;
    if (Array.isArray(res.results)) return res.results;
    if (Array.isArray(res.data)) return res.data;
    return [];
  };

  useEffect(() => {
    EventsService.getEvents().then((res) => {
      setEvents(extractList(res));
    }).catch(() => {});
  }, []);

  const handleRSVP = async (eventId: number) => {
    try {
      const res = await EventsService.rsvpEvent(eventId, 'ATTENDING');
      if (res.success) {
        setRsvpSuccess(`RSVP recorded for Event #${eventId}!`);
        setTimeout(() => setRsvpSuccess(''), 3000);
      }
    } catch (err: any) {
      alert(err?.message || "RSVP failed.");
    }
  };

  const filteredEvents = events.filter((e) => {
    if (activeTab === 'UPCOMING') return e.status === 'UPCOMING';
    return true;
  });

  return (
    <div className="space-y-8 py-10 px-4 max-w-7xl mx-auto bvs-bg-pattern">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-black text-slate-100 flex items-center gap-3 font-heading">
            <CalendarIcon className="text-orange-400" size={32} /> Organization Events & Meetings
          </h1>
          <p className="text-xs text-slate-400 mt-2 font-medium">State rallies, district conventions, youth assemblies, and community meets</p>
        </div>

        <div className="flex items-center gap-2 bg-[#0d121c] p-1.5 rounded-xl border border-slate-800">
          <button
            onClick={() => setActiveTab('UPCOMING')}
            className={`px-4 py-2 rounded-lg text-xs font-bold transition ${activeTab === 'UPCOMING' ? 'bg-gradient-to-r from-orange-600 to-amber-600 text-slate-950 shadow-md' : 'text-slate-400 hover:text-slate-200'}`}
          >
            Upcoming Events
          </button>
          <button
            onClick={() => setActiveTab('ALL')}
            className={`px-4 py-2 rounded-lg text-xs font-bold transition ${activeTab === 'ALL' ? 'bg-gradient-to-r from-orange-600 to-amber-600 text-slate-950 shadow-md' : 'text-slate-400 hover:text-slate-200'}`}
          >
            All Events
          </button>
        </div>
      </div>

      {rsvpSuccess && (
        <div className="p-3 rounded-xl bg-emerald-950/80 border border-emerald-500/30 text-emerald-400 text-xs font-bold flex items-center gap-2">
          <CheckCircle2 size={16} /> {rsvpSuccess}
        </div>
      )}

      {/* Events Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredEvents.length > 0 ? (
          filteredEvents.map((evt) => (
            <Card key={evt.id} className="p-6 flex flex-col justify-between">
              <div>
                <div className="flex items-center justify-between mb-3">
                  <Badge variant={evt.status === 'UPCOMING' ? 'success' : 'neutral'}>{evt.status}</Badge>
                </div>

                <h3 className="text-lg font-bold text-slate-100 mb-2 font-heading">{evt.title}</h3>
                <p className="text-slate-400 text-xs line-clamp-3 mb-4 font-medium">{evt.description}</p>

                <div className="space-y-2 text-xs text-slate-300 font-medium">
                  <div className="flex items-center gap-2">
                    <CalendarIcon size={14} className="text-orange-400" />
                    <span>{new Date(evt.start_time).toLocaleString()}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <MapPin size={14} className="text-orange-400" />
                    <span>{evt.venue_address}</span>
                  </div>
                </div>
              </div>

              <div className="pt-4 border-t border-slate-800 mt-6 flex items-center justify-between">
                {isAuthenticated ? (
                  <Button size="sm" onClick={() => handleRSVP(evt.id)} className="w-full">
                    <Users size={14} className="mr-1.5" /> RSVP Attending
                  </Button>
                ) : (
                  <span className="text-[11px] text-slate-500 font-medium italic">Login to RSVP</span>
                )}
              </div>
            </Card>
          ))
        ) : (
          <div className="col-span-full py-12 text-center text-xs text-slate-500 font-medium">
            No events found in this category.
          </div>
        )}
      </div>
    </div>
  );
};
