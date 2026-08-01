import React, { useEffect, useState } from 'react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Building2, MapPin, Layers } from 'lucide-react';
import { OrganizationService } from '../../api/services';
import { State, District } from '../../types';

export const OrganizationPublicPage: React.FC = () => {
  const [states, setStates] = useState<State[]>([]);
  const [districts, setDistricts] = useState<District[]>([]);
  const [selectedState, setSelectedState] = useState<number | null>(null);

  const extractList = (res: any) => {
    if (!res) return [];
    if (Array.isArray(res)) return res;
    if (Array.isArray(res.results)) return res.results;
    if (Array.isArray(res.data)) return res.data;
    return [];
  };

  useEffect(() => {
    OrganizationService.getStates().then((res) => {
      const list = extractList(res);
      setStates(list);
      if (list.length > 0) {
        setSelectedState(list[0].id);
      }
    }).catch(() => {});
  }, []);

  useEffect(() => {
    if (selectedState) {
      OrganizationService.getDistricts(selectedState).then((res) => {
        setDistricts(extractList(res));
      }).catch(() => {});
    }
  }, [selectedState]);

  return (
    <div className="space-y-8 py-10 px-4 max-w-7xl mx-auto bvs-bg-pattern">
      <div>
        <h1 className="text-3xl font-black text-slate-100 flex items-center gap-3 font-heading">
          <Building2 className="text-orange-400" size={32} /> Organizational Hierarchy Directory
        </h1>
        <p className="text-xs text-slate-400 mt-2 font-medium">Explore active administrative units across States, Districts, Talukas, and Villages</p>
      </div>

      {/* State Selector Pills */}
      <div className="flex flex-wrap items-center gap-3">
        {states.map((s) => (
          <button
            key={s.id}
            onClick={() => setSelectedState(s.id)}
            className={`px-5 py-2.5 rounded-xl text-xs font-bold transition flex items-center gap-2 ${
              selectedState === s.id
                ? 'bg-gradient-to-r from-orange-600 to-amber-600 text-slate-950 shadow-lg shadow-orange-600/25 border border-amber-400/40'
                : 'bg-[#0d121c] text-slate-300 border border-slate-800 hover:border-slate-700'
            }`}
          >
            <MapPin size={14} /> {s.name} ({s.code})
          </button>
        ))}
      </div>

      {/* Districts Grid */}
      <Card className="p-6">
        <h3 className="text-lg font-bold text-slate-100 mb-4 flex items-center gap-2 font-heading">
          <Layers size={18} className="text-orange-400" /> Registered Districts
        </h3>

        {districts.length > 0 ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
            {districts.map((d) => (
              <div key={d.id} className="p-4 rounded-xl bg-[#090d16] border border-slate-800 flex items-center justify-between">
                <div>
                  <h4 className="text-sm font-bold text-slate-100 font-heading">{d.name}</h4>
                  <span className="text-[10px] text-slate-400 font-mono">Code: {d.code || 'N/A'}</span>
                </div>
                <Badge variant={d.is_active ? 'success' : 'danger'}>
                  {d.is_active ? 'Active Node' : 'Inactive'}
                </Badge>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-xs text-slate-500 py-6 text-center font-medium">No district units registered under this state yet.</p>
        )}
      </Card>
    </div>
  );
};
