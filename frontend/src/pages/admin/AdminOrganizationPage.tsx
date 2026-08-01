import React, { useEffect, useState } from 'react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { Input } from '../../components/ui/Input';
import { Building2, Plus, CheckCircle2 } from 'lucide-react';
import { OrganizationService } from '../../api/services';
import { State, District, Taluka, Village, Designation } from '../../types';

export const AdminOrganizationPage: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'STATES' | 'DISTRICTS' | 'TALUKAS' | 'VILLAGES' | 'DESIGNATIONS'>('STATES');
  const [states, setStates] = useState<State[]>([]);
  const [districts, setDistricts] = useState<District[]>([]);
  const [talukas, setTalukas] = useState<Taluka[]>([]);
  const [villages, setVillages] = useState<Village[]>([]);
  const [designations, setDesignations] = useState<Designation[]>([]);

  const [showAddModal, setShowAddModal] = useState(false);
  const [formState, setFormState] = useState<any>({ name: '', code: '', state_id: '', district_id: '', taluka_id: '', title: '', level_scope: 'STATE' });
  const [successMsg, setSuccessMsg] = useState('');
  const [error, setError] = useState('');

  const extractList = (res: any) => {
    if (!res) return [];
    if (Array.isArray(res)) return res;
    if (Array.isArray(res.results)) return res.results;
    if (Array.isArray(res.data)) return res.data;
    return [];
  };

  const loadData = () => {
    OrganizationService.getStates().then((res) => setStates(extractList(res))).catch(() => {});
    OrganizationService.getDistricts().then((res) => setDistricts(extractList(res))).catch(() => {});
    OrganizationService.getTalukas().then((res) => setTalukas(extractList(res))).catch(() => {});
    OrganizationService.getVillages().then((res) => setVillages(extractList(res))).catch(() => {});
    OrganizationService.getDesignations().then((res) => setDesignations(extractList(res))).catch(() => {});
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    try {
      if (activeTab === 'STATES') {
        await OrganizationService.createState({ name: formState.name, code: formState.code });
      } else if (activeTab === 'DISTRICTS') {
        await OrganizationService.createDistrict({ name: formState.name, code: formState.code, state: Number(formState.state_id) });
      } else if (activeTab === 'TALUKAS') {
        await OrganizationService.createTaluka({ name: formState.name, district: Number(formState.district_id) });
      } else if (activeTab === 'VILLAGES') {
        await OrganizationService.createVillage({ name: formState.name, taluka: Number(formState.taluka_id) });
      } else if (activeTab === 'DESIGNATIONS') {
        await OrganizationService.createDesignation({ title: formState.title, level_scope: formState.level_scope });
      }

      setSuccessMsg(`Created new ${activeTab.slice(0, -1)} entry successfully!`);
      setShowAddModal(false);
      setFormState({ name: '', code: '', state_id: '', district_id: '', taluka_id: '', title: '', level_scope: 'STATE' });
      loadData();
      setTimeout(() => setSuccessMsg(''), 3000);
    } catch (err: any) {
      setError(err?.message || 'Creation failed.');
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-100 flex items-center gap-2">
            <Building2 className="text-amber-400" size={24} /> Organization Hierarchy Management
          </h1>
          <p className="text-xs text-slate-400 mt-1">Manage master administrative records (States, Districts, Talukas, Villages, Designations)</p>
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

      {/* Hierarchy Level Tabs */}
      <div className="flex flex-wrap items-center gap-2 bg-slate-900 p-1.5 rounded-xl border border-slate-800">
        {(['STATES', 'DISTRICTS', 'TALUKAS', 'VILLAGES', 'DESIGNATIONS'] as const).map((tab) => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className={`px-4 py-2 rounded-lg text-xs font-bold transition ${
              activeTab === tab ? 'bg-amber-500 text-slate-950 shadow-md' : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            {tab}
          </button>
        ))}
      </div>

      <Card className="p-4">
        <div className="overflow-x-auto">
          {activeTab === 'STATES' && (
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-950 text-slate-400 border-b border-slate-800">
                <tr>
                  <th className="p-3">State Name</th>
                  <th className="p-3">ISO Code</th>
                  <th className="p-3">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60 text-slate-200">
                {states.map((s) => (
                  <tr key={s.id} className="hover:bg-slate-800/30">
                    <td className="p-3 font-bold">{s.name}</td>
                    <td className="p-3 font-mono text-amber-400">{s.code}</td>
                    <td className="p-3"><Badge variant="success">Active</Badge></td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}

          {activeTab === 'DISTRICTS' && (
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-950 text-slate-400 border-b border-slate-800">
                <tr>
                  <th className="p-3">District Name</th>
                  <th className="p-3">Code</th>
                  <th className="p-3">Parent State</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60 text-slate-200">
                {districts.map((d) => (
                  <tr key={d.id} className="hover:bg-slate-800/30">
                    <td className="p-3 font-bold">{d.name}</td>
                    <td className="p-3 font-mono text-amber-400">{d.code || 'N/A'}</td>
                    <td className="p-3">{d.state_name || 'N/A'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}

          {activeTab === 'TALUKAS' && (
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-950 text-slate-400 border-b border-slate-800">
                <tr>
                  <th className="p-3">Taluka Name</th>
                  <th className="p-3">Parent District</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60 text-slate-200">
                {talukas.map((t) => (
                  <tr key={t.id} className="hover:bg-slate-800/30">
                    <td className="p-3 font-bold">{t.name}</td>
                    <td className="p-3">{t.district_name || 'N/A'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}

          {activeTab === 'VILLAGES' && (
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-950 text-slate-400 border-b border-slate-800">
                <tr>
                  <th className="p-3">Village / Ward Name</th>
                  <th className="p-3">Pincode</th>
                  <th className="p-3">Parent Taluka</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60 text-slate-200">
                {villages.map((v) => (
                  <tr key={v.id} className="hover:bg-slate-800/30">
                    <td className="p-3 font-bold">{v.name}</td>
                    <td className="p-3 font-mono text-amber-400">{v.pin_code || 'N/A'}</td>
                    <td className="p-3">{v.taluka_name || 'N/A'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}

          {activeTab === 'DESIGNATIONS' && (
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-950 text-slate-400 border-b border-slate-800">
                <tr>
                  <th className="p-3">Designation Title</th>
                  <th className="p-3">Scope Tier</th>
                  <th className="p-3">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60 text-slate-200">
                {designations.map((des) => (
                  <tr key={des.id} className="hover:bg-slate-800/30">
                    <td className="p-3 font-bold">{des.title}</td>
                    <td className="p-3 font-mono text-amber-400">{des.level_scope}</td>
                    <td className="p-3"><Badge variant="success">Active</Badge></td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </Card>

      {/* Add Modal */}
      {showAddModal && (
        <div className="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-sm flex items-center justify-center p-4">
          <Card className="max-w-md w-full p-6 space-y-4">
            <div className="flex items-center justify-between">
              <h3 className="text-lg font-bold text-slate-100">Add New {activeTab.slice(0, -1)}</h3>
              <Button size="sm" variant="ghost" onClick={() => setShowAddModal(false)}>Close</Button>
            </div>

            {error && <div className="p-3 rounded-lg bg-rose-500/10 border border-rose-500/30 text-rose-400 text-xs">{error}</div>}

            <form onSubmit={handleCreate} className="space-y-4">
              {activeTab === 'STATES' && (
                <>
                  <Input label="State Name *" value={formState.name} onChange={(e) => setFormState({ ...formState, name: e.target.value })} required />
                  <Input label="State Code (e.g. MH) *" value={formState.code} onChange={(e) => setFormState({ ...formState, code: e.target.value })} required />
                </>
              )}

              {activeTab === 'DISTRICTS' && (
                <>
                  <div>
                    <label className="block text-xs font-semibold text-slate-300 mb-1.5">Parent State *</label>
                    <select
                      className="w-full bg-slate-950/80 border border-slate-800 text-slate-100 text-sm rounded-lg p-2.5 outline-none"
                      value={formState.state_id}
                      onChange={(e) => setFormState({ ...formState, state_id: e.target.value })}
                      required
                    >
                      <option value="">Select State</option>
                      {states.map((s) => <option key={s.id} value={s.id}>{s.name}</option>)}
                    </select>
                  </div>
                  <Input label="District Name *" value={formState.name} onChange={(e) => setFormState({ ...formState, name: e.target.value })} required />
                  <Input label="District Code (Optional)" value={formState.code} onChange={(e) => setFormState({ ...formState, code: e.target.value })} />
                </>
              )}

              {activeTab === 'TALUKAS' && (
                <>
                  <div>
                    <label className="block text-xs font-semibold text-slate-300 mb-1.5">Parent District *</label>
                    <select
                      className="w-full bg-slate-950/80 border border-slate-800 text-slate-100 text-sm rounded-lg p-2.5 outline-none"
                      value={formState.district_id}
                      onChange={(e) => setFormState({ ...formState, district_id: e.target.value })}
                      required
                    >
                      <option value="">Select District</option>
                      {districts.map((d) => <option key={d.id} value={d.id}>{d.name}</option>)}
                    </select>
                  </div>
                  <Input label="Taluka Name *" value={formState.name} onChange={(e) => setFormState({ ...formState, name: e.target.value })} required />
                </>
              )}

              {activeTab === 'VILLAGES' && (
                <>
                  <div>
                    <label className="block text-xs font-semibold text-slate-300 mb-1.5">Parent Taluka *</label>
                    <select
                      className="w-full bg-slate-950/80 border border-slate-800 text-slate-100 text-sm rounded-lg p-2.5 outline-none"
                      value={formState.taluka_id}
                      onChange={(e) => setFormState({ ...formState, taluka_id: e.target.value })}
                      required
                    >
                      <option value="">Select Taluka</option>
                      {talukas.map((t) => <option key={t.id} value={t.id}>{t.name}</option>)}
                    </select>
                  </div>
                  <Input label="Village Name *" value={formState.name} onChange={(e) => setFormState({ ...formState, name: e.target.value })} required />
                </>
              )}

              {activeTab === 'DESIGNATIONS' && (
                <>
                  <Input label="Designation Title *" value={formState.title} onChange={(e) => setFormState({ ...formState, title: e.target.value })} required />
                  <div>
                    <label className="block text-xs font-semibold text-slate-300 mb-1.5">Administrative Level Scope *</label>
                    <select
                      className="w-full bg-slate-950/80 border border-slate-800 text-slate-100 text-sm rounded-lg p-2.5 outline-none"
                      value={formState.level_scope}
                      onChange={(e) => setFormState({ ...formState, level_scope: e.target.value })}
                    >
                      <option value="STATE">STATE</option>
                      <option value="DISTRICT">DISTRICT</option>
                      <option value="TALUKA">TALUKA</option>
                      <option value="VILLAGE">VILLAGE</option>
                    </select>
                  </div>
                </>
              )}

              <Button type="submit" className="w-full">Create Record</Button>
            </form>
          </Card>
        </div>
      )}
    </div>
  );
};
