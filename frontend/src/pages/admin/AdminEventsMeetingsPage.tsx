import React, { useEffect, useState } from 'react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { Input } from '../../components/ui/Input';
import { Calendar as CalendarIcon, Plus, CheckCircle2 } from 'lucide-react';
import { EventsService } from '../../api/services';
import { Event, Meeting } from '../../types';

export const AdminEventsMeetingsPage: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'EVENTS' | 'MEETINGS'>('EVENTS');
  const [events, setEvents] = useState<Event[]>([]);
  const [meetings, setMeetings] = useState<Meeting[]>([]);

  const [showAddModal, setShowAddModal] = useState(false);
  const [formData, setFormData] = useState<any>({ title: '', description: '', venue_address: '', start_time: '', subject: '', agenda: '', meeting_date: '', venue_or_link: '' });
  const [successMsg, setSuccessMsg] = useState('');

  const extractList = (res: any) => {
    if (!res) return [];
    if (Array.isArray(res)) return res;
    if (Array.isArray(res.results)) return res.results;
    if (Array.isArray(res.data)) return res.data;
    return [];
  };

  const loadData = () => {
    EventsService.getEvents().then((res) => setEvents(extractList(res))).catch(() => {});
    EventsService.getMeetings().then((res) => setMeetings(extractList(res))).catch(() => {});
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      if (activeTab === 'EVENTS') {
        await EventsService.createEvent({
          title: formData.title,
          description: formData.description,
          venue_address: formData.venue_address,
          start_time: formData.start_time,
          status: 'UPCOMING',
          is_public: true
        });
      } else {
        await EventsService.createMeeting({
          subject: formData.subject,
          agenda: formData.agenda,
          meeting_date: formData.meeting_date,
          venue_or_link: formData.venue_or_link,
          status: 'SCHEDULED'
        });
      }

      setSuccessMsg(`Created ${activeTab.toLowerCase().slice(0, -1)} entry!`);
      setShowAddModal(false);
      setFormData({ title: '', description: '', venue_address: '', start_time: '', subject: '', agenda: '', meeting_date: '', venue_or_link: '' });
      loadData();
      setTimeout(() => setSuccessMsg(''), 3000);
    } catch (err: any) {
      alert(err?.message || "Failed to create entry.");
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-100 flex items-center gap-2">
            <CalendarIcon className="text-amber-400" size={24} /> Events & Committee Meetings
          </h1>
          <p className="text-xs text-slate-400 mt-1">Schedule statewide rallies, executive meetings, and publish official minutes</p>
        </div>

        <Button size="sm" onClick={() => setShowAddModal(true)}>
          <Plus size={16} className="mr-1.5" /> Add {activeTab.slice(0, -1)}
        </Button>
      </div>

      {successMsg && (
        <div className="p-3 rounded-lg bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs flex items-center gap-2">
          <CheckCircle2 size={16} /> {successMsg}
        </div>
      )}

      <div className="flex items-center gap-2 bg-slate-900 p-1.5 rounded-xl border border-slate-800 w-fit">
        <button
          onClick={() => setActiveTab('EVENTS')}
          className={`px-4 py-2 rounded-lg text-xs font-bold transition ${activeTab === 'EVENTS' ? 'bg-amber-500 text-slate-950 shadow-md' : 'text-slate-400'}`}
        >
          Public Events ({events.length})
        </button>
        <button
          onClick={() => setActiveTab('MEETINGS')}
          className={`px-4 py-2 rounded-lg text-xs font-bold transition ${activeTab === 'MEETINGS' ? 'bg-amber-500 text-slate-950 shadow-md' : 'text-slate-400'}`}
        >
          Internal Meetings ({meetings.length})
        </button>
      </div>

      <Card className="p-4">
        {activeTab === 'EVENTS' ? (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-950 text-slate-400 border-b border-slate-800">
                <tr>
                  <th className="p-3">Event Title</th>
                  <th className="p-3">Venue</th>
                  <th className="p-3">Start Time</th>
                  <th className="p-3">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60 text-slate-200">
                {events.map((e) => (
                  <tr key={e.id} className="hover:bg-slate-800/30">
                    <td className="p-3 font-bold">{e.title}</td>
                    <td className="p-3">{e.venue_address}</td>
                    <td className="p-3 font-mono text-amber-400">{new Date(e.start_time).toLocaleString()}</td>
                    <td className="p-3"><Badge variant="success">{e.status}</Badge></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-950 text-slate-400 border-b border-slate-800">
                <tr>
                  <th className="p-3">Subject</th>
                  <th className="p-3">Venue / Link</th>
                  <th className="p-3">Meeting Date</th>
                  <th className="p-3">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60 text-slate-200">
                {meetings.map((m) => (
                  <tr key={m.id} className="hover:bg-slate-800/30">
                    <td className="p-3 font-bold">{m.subject}</td>
                    <td className="p-3">{m.venue_or_link}</td>
                    <td className="p-3 font-mono text-amber-400">{new Date(m.meeting_date).toLocaleString()}</td>
                    <td className="p-3"><Badge variant="warning">{m.status}</Badge></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </Card>

      {/* Add Modal */}
      {showAddModal && (
        <div className="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-sm flex items-center justify-center p-4">
          <Card className="max-w-md w-full p-6 space-y-4">
            <div className="flex items-center justify-between">
              <h3 className="text-lg font-bold text-slate-100">Schedule New {activeTab.slice(0, -1)}</h3>
              <Button size="sm" variant="ghost" onClick={() => setShowAddModal(false)}>Close</Button>
            </div>

            <form onSubmit={handleCreate} className="space-y-4">
              {activeTab === 'EVENTS' ? (
                <>
                  <Input label="Event Title *" value={formData.title} onChange={(e) => setFormData({ ...formData, title: e.target.value })} required />
                  <Input label="Venue Address *" value={formData.venue_address} onChange={(e) => setFormData({ ...formData, venue_address: e.target.value })} required />
                  <Input label="Start Date & Time *" type="datetime-local" value={formData.start_time} onChange={(e) => setFormData({ ...formData, start_time: e.target.value })} required />
                  <div>
                    <label className="block text-xs font-semibold text-slate-300 mb-1.5">Description *</label>
                    <textarea
                      rows={3}
                      className="w-full bg-slate-950/80 border border-slate-800 text-slate-100 text-sm rounded-lg p-2.5 outline-none"
                      value={formData.description}
                      onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                      required
                    />
                  </div>
                </>
              ) : (
                <>
                  <Input label="Meeting Subject *" value={formData.subject} onChange={(e) => setFormData({ ...formData, subject: e.target.value })} required />
                  <Input label="Venue / Video Link *" value={formData.venue_or_link} onChange={(e) => setFormData({ ...formData, venue_or_link: e.target.value })} required />
                  <Input label="Meeting Date & Time *" type="datetime-local" value={formData.meeting_date} onChange={(e) => setFormData({ ...formData, meeting_date: e.target.value })} required />
                  <div>
                    <label className="block text-xs font-semibold text-slate-300 mb-1.5">Agenda *</label>
                    <textarea
                      rows={3}
                      className="w-full bg-slate-950/80 border border-slate-800 text-slate-100 text-sm rounded-lg p-2.5 outline-none"
                      value={formData.agenda}
                      onChange={(e) => setFormData({ ...formData, agenda: e.target.value })}
                      required
                    />
                  </div>
                </>
              )}

              <Button type="submit" className="w-full">Save Entry</Button>
            </form>
          </Card>
        </div>
      )}
    </div>
  );
};
