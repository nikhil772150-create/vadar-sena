import React, { useEffect, useState } from 'react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { DonationService } from '../../api/services';
import { Donation } from '../../types';

export const AdminDonationsPage: React.FC = () => {
  const [donations, setDonations] = useState<Donation[]>([]);

  const fetchDonations = () => {
    DonationService.getDonations().then((res) => setDonations(res.results || [])).catch(() => {});
  };

  useEffect(() => {
    fetchDonations();
  }, []);

  const handleVerify = async (id: number) => {
    await DonationService.verifyDonation(id, "Verified by Admin");
    fetchDonations();
  };

  const handleReject = async (id: number) => {
    await DonationService.rejectDonation(id, "Payment receipt invalid");
    fetchDonations();
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-100">Donation Verification Engine</h1>
        <p className="text-xs text-slate-400 mt-1">Review financial contributions and payment receipts</p>
      </div>

      <Card className="p-4">
        <table className="w-full text-left text-xs">
          <thead className="bg-slate-950 text-slate-400 border-b border-slate-800">
            <tr>
              <th className="p-3">Donor Name</th>
              <th className="p-3">Phone</th>
              <th className="p-3">Amount (INR)</th>
              <th className="p-3">Transaction ID</th>
              <th className="p-3">Status</th>
              <th className="p-3 text-right">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60 text-slate-200">
            {donations.map((d) => (
              <tr key={d.id}>
                <td className="p-3 font-semibold">{d.donor_name}</td>
                <td className="p-3 font-mono">{d.phone_number}</td>
                <td className="p-3 font-bold text-emerald-400">₹{d.amount}</td>
                <td className="p-3 font-mono">{d.transaction_id}</td>
                <td className="p-3">
                  <Badge variant={d.status === 'VERIFIED' ? 'success' : d.status === 'PENDING' ? 'warning' : 'danger'}>
                    {d.status}
                  </Badge>
                </td>
                <td className="p-3 text-right space-x-2">
                  {d.status === 'PENDING' && (
                    <>
                      <Button size="sm" variant="primary" onClick={() => handleVerify(d.id)}>Verify</Button>
                      <Button size="sm" variant="danger" onClick={() => handleReject(d.id)}>Reject</Button>
                    </>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </Card>
    </div>
  );
};
