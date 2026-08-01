import React, { useEffect, useState } from 'react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { BarChart3, Download, Users, DollarSign, PieChart } from 'lucide-react';
import { AnalyticsService } from '../../api/services';

export const AdminReportsPage: React.FC = () => {
  const [memberReport, setMemberReport] = useState<any>(null);
  const [donationReport, setDonationReport] = useState<any>(null);

  useEffect(() => {
    AnalyticsService.getMemberReport().then((res) => setMemberReport(res.data)).catch(() => {});
    AnalyticsService.getDonationReport().then((res) => setDonationReport(res.data)).catch(() => {});
  }, []);

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-100 flex items-center gap-2">
            <BarChart3 className="text-amber-400" size={24} /> System Reports & Analytics
          </h1>
          <p className="text-xs text-slate-400 mt-1">Structured reports for Member Onboarding Growth, Financial Fund Summaries, and Regional Aggregations</p>
        </div>

        <Button size="sm" onClick={() => window.print()} variant="outline">
          <Download size={16} className="mr-1.5" /> Export Report Print
        </Button>
      </div>

      {/* Summary Stat Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4">
        <Card className="p-5 border-amber-500/20">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-400">Total Records</span>
            <Users className="text-amber-400" size={18} />
          </div>
          <p className="text-2xl font-black text-slate-100 mt-2">{memberReport?.total_records || 0}</p>
          <span className="text-[10px] text-amber-400 font-mono">Member Growth Metric</span>
        </Card>

        <Card className="p-5 border-emerald-500/20">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-400">Verified Fund Sum</span>
            <DollarSign className="text-emerald-400" size={18} />
          </div>
          <p className="text-2xl font-black text-slate-100 mt-2">₹{donationReport?.summary?.total_amount || 0}</p>
          <span className="text-[10px] text-emerald-400 font-mono">Financial Collection</span>
        </Card>

        <Card className="p-5 border-blue-500/20">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-400">Approved Members</span>
            <Users className="text-blue-400" size={18} />
          </div>
          <p className="text-2xl font-black text-slate-100 mt-2">{memberReport?.summary?.approved || 0}</p>
          <span className="text-[10px] text-blue-400 font-mono">Verified Card Holders</span>
        </Card>

        <Card className="p-5 border-purple-500/20">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-400">Pending Approvals</span>
            <PieChart className="text-purple-400" size={18} />
          </div>
          <p className="text-2xl font-black text-slate-100 mt-2">{memberReport?.summary?.pending || 0}</p>
          <span className="text-[10px] text-purple-400 font-mono">Action Required</span>
        </Card>
      </div>

      {/* Member Growth Table */}
      <Card className="p-6">
        <h3 className="text-base font-bold text-slate-100 mb-4">Regional Member Onboarding Summary</h3>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-950 text-slate-400 border-b border-slate-800">
              <tr>
                <th className="p-3">Member ID</th>
                <th className="p-3">Full Name</th>
                <th className="p-3">Phone</th>
                <th className="p-3">State / District</th>
                <th className="p-3">Status</th>
                <th className="p-3">Registered Date</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60 text-slate-200">
              {memberReport?.data && memberReport.data.length > 0 ? (
                memberReport.data.map((m: any) => (
                  <tr key={m.id} className="hover:bg-slate-800/30">
                    <td className="p-3 font-mono text-amber-400">{m.membership_number || 'Pending'}</td>
                    <td className="p-3 font-bold">{m.first_name} {m.last_name}</td>
                    <td className="p-3 font-mono">{m.phone_number}</td>
                    <td className="p-3">{m.state__name || 'N/A'} / {m.district__name || 'N/A'}</td>
                    <td className="p-3">
                      <Badge variant={m.status === 'APPROVED' ? 'success' : m.status === 'PENDING' ? 'warning' : 'danger'}>
                        {m.status}
                      </Badge>
                    </td>
                    <td className="p-3 font-mono text-slate-400">{new Date(m.created_at).toLocaleDateString()}</td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan={6} className="p-8 text-center text-slate-500">No member data compiled.</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
};
