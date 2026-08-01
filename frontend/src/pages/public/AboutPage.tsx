import React, { useEffect, useState } from 'react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Shield, Target, Users, Award, Landmark, CheckCircle2 } from 'lucide-react';
import { OrganizationService } from '../../api/services';
import { Designation } from '../../types';

export const AboutPage: React.FC = () => {
  const [designations, setDesignations] = useState<Designation[]>([]);

  useEffect(() => {
    OrganizationService.getDesignations()
      .then((res) => {
        const list = Array.isArray(res) ? res : res.results || res.data || [];
        setDesignations(list);
      })
      .catch(() => {});
  }, []);

  return (
    <div className="space-y-12 py-10 px-4 max-w-7xl mx-auto bvs-bg-pattern">
      {/* Hero Section */}
      <div className="relative rounded-3xl overflow-hidden bg-gradient-to-r from-orange-950/40 via-slate-900 to-[#0d121c] border border-orange-500/30 p-8 md:p-14 text-center shadow-2xl">
        <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-orange-500/10 border border-orange-500/30 text-orange-400 text-xs font-extrabold tracking-wider uppercase mb-4 shadow-md">
          <Shield size={14} /> Official Administrative Charter
        </div>
        <h1 className="text-3xl md:text-5xl font-black text-slate-100 tracking-tight font-heading">
          About <span className="bvs-gradient-text">Bharatiya Vadar Sena</span>
        </h1>
        <p className="mt-4 max-w-3xl mx-auto text-slate-300 text-sm md:text-base leading-relaxed font-medium">
          Dedicated to the empowerment, unity, social upliftment, and administrative representation of the Vadar community across India through structured governance, digital information broadcast, and welfare programs.
        </p>
      </div>

      {/* Vision & Mission */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <Card className="p-8 relative overflow-hidden border-orange-500/30">
          <div className="w-14 h-14 rounded-2xl bg-orange-500/10 border border-orange-500/30 flex items-center justify-center text-orange-400 mb-6 shadow-lg shadow-orange-500/10">
            <Target size={28} />
          </div>
          <h2 className="text-xl font-bold text-slate-100 mb-3 font-heading">Our Vision</h2>
          <p className="text-slate-300 text-sm leading-relaxed font-medium">
            To build a connected, self-reliant, and socially empowered Vadar community where every regional unit has verified representation, equal opportunities, and support across all administrative levels.
          </p>
        </Card>

        <Card className="p-8 relative overflow-hidden border-rose-500/30">
          <div className="w-14 h-14 rounded-2xl bg-rose-500/10 border border-rose-500/30 flex items-center justify-center text-rose-400 mb-6 shadow-lg shadow-rose-500/10">
            <Landmark size={28} />
          </div>
          <h2 className="text-xl font-bold text-slate-100 mb-3 font-heading">Our Mission</h2>
          <p className="text-slate-300 text-sm leading-relaxed font-medium">
            Establish a transparent, 4-tier organizational hierarchy (State, District, Taluka, Village) to streamline community assistance, welfare management, emergency relief, and youth empowerment.
          </p>
        </Card>
      </div>

      {/* Core Objectives */}
      <Card className="p-8">
        <h2 className="text-xl font-bold text-slate-100 mb-6 flex items-center gap-2 font-heading">
          <Award className="text-orange-400" size={24} /> Key Organizational Pillars
        </h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {[
            "Structured Regional Office Bearer Hierarchy",
            "Statewide Assemblies & Cultural Events",
            "Educational Grants & Youth Mentorship",
            "Financial Welfare & Emergency Relief Funds",
            "Transparent Donation Tracking & E-Receipts",
            "Official Press Releases & Leadership Bulletins"
          ].map((item, idx) => (
            <div key={idx} className="flex items-start gap-3 p-4 rounded-xl bg-[#090d16]/80 border border-slate-800">
              <CheckCircle2 size={18} className="text-orange-400 shrink-0 mt-0.5" />
              <span className="text-xs font-bold text-slate-200">{item}</span>
            </div>
          ))}
        </div>
      </Card>

      {/* Office Bearer Designations Master */}
      <Card className="p-8">
        <h2 className="text-xl font-bold text-slate-100 mb-2 flex items-center gap-2 font-heading">
          <Users className="text-orange-400" size={24} /> Hierarchy Designations & Scope
        </h2>
        <p className="text-xs text-slate-400 mb-6 font-medium">Official administrative roles defined across organization tiers</p>

        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
          {designations.length > 0 ? (
            designations.map((d) => (
              <div key={d.id} className="p-4 rounded-xl bg-[#090d16] border border-slate-800 flex items-center justify-between">
                <div>
                  <h4 className="text-sm font-bold text-slate-100 font-heading">{d.title}</h4>
                  <span className="text-[10px] text-orange-400 font-mono tracking-wider uppercase">{d.level_scope} LEVEL</span>
                </div>
                <Badge variant="success">Active</Badge>
              </div>
            ))
          ) : (
            <p className="text-xs text-slate-500 col-span-3 font-medium">Loading designations catalog...</p>
          )}
        </div>
      </Card>
    </div>
  );
};
