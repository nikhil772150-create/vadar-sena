import React, { useState, useEffect } from 'react';
import { Card } from '../../components/ui/Card';
import { Input } from '../../components/ui/Input';
import { Button } from '../../components/ui/Button';
import { Heart, CheckCircle2 } from 'lucide-react';
import { DonationService, OrganizationService } from '../../api/services';
import { State, District } from '../../types';

export const DonationPage: React.FC = () => {
  const [states, setStates] = useState<State[]>([]);
  const [districts, setDistricts] = useState<District[]>([]);

  const [formData, setFormData] = useState({
    donor_name: '',
    phone_number: '',
    email: '',
    amount: '',
    purpose: 'General Organization Fund',
    transaction_id: '',
    payment_method: 'UPI',
    upi_ref: '',
    state: '',
    district: '',
  });

  const [error, setError] = useState('');
  const [successMsg, setSuccessMsg] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const extractList = (res: any) => {
    if (!res) return [];
    if (Array.isArray(res)) return res;
    if (Array.isArray(res.results)) return res.results;
    if (Array.isArray(res.data)) return res.data;
    return [];
  };

  useEffect(() => {
    OrganizationService.getStates().then((res) => setStates(extractList(res))).catch(() => {});
  }, []);

  const handleStateChange = (stateId: string) => {
    setFormData({ ...formData, state: stateId, district: '' });
    setDistricts([]);
    if (stateId) {
      OrganizationService.getDistricts(Number(stateId)).then((res) => setDistricts(extractList(res))).catch(() => {});
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setSuccessMsg('');
    setIsLoading(true);

    try {
      const payload = {
        ...formData,
        amount: parseFloat(formData.amount),
        state: formData.state ? Number(formData.state) : null,
        district: formData.district ? Number(formData.district) : null,
      };

      const res = await DonationService.submitDonation(payload);
      if (res.success) {
        setSuccessMsg("Donation details submitted successfully! Your receipt status is PENDING VERIFICATION by admin.");
        setFormData({
          donor_name: '',
          phone_number: '',
          email: '',
          amount: '',
          purpose: 'General Organization Fund',
          transaction_id: '',
          payment_method: 'UPI',
          upi_ref: '',
          state: '',
          district: '',
        });
      } else {
        setError(res.message || 'Donation submission failed.');
      }
    } catch (err: any) {
      const msg = err?.message || err?.errors?.transaction_id?.[0] || 'Submission failed. Please check inputs.';
      setError(msg);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto px-4 py-12 space-y-8 bvs-bg-pattern">
      <div>
        <h1 className="text-3xl font-black text-slate-100 flex items-center gap-3 font-heading">
          <Heart className="text-rose-500 fill-rose-500/20" size={32} /> Organization Support & Donations
        </h1>
        <p className="text-xs text-slate-400 mt-2 font-medium">Support community welfare, educational scholarships, and regional outreach programs</p>
      </div>

      <Card title="Donation Submission Form" subtitle="Submit your transaction reference for official verification and e-receipt">
        {error && <div className="mb-4 p-3.5 rounded-xl bg-rose-950/80 border border-rose-500/30 text-rose-400 text-xs font-semibold">{error}</div>}
        {successMsg && (
          <div className="mb-4 p-4 rounded-xl bg-emerald-950/80 border border-emerald-500/30 text-emerald-400 text-xs flex items-start gap-3">
            <CheckCircle2 size={18} className="shrink-0 mt-0.5" />
            <div>
              <span className="font-bold block mb-1">Thank you for your generous contribution!</span>
              {successMsg}
            </div>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Input label="Full Donor Name *" value={formData.donor_name} onChange={(e) => setFormData({ ...formData, donor_name: e.target.value })} required />
            <Input label="10-Digit Phone Number *" placeholder="e.g. 9876543210" value={formData.phone_number} onChange={(e) => setFormData({ ...formData, phone_number: e.target.value })} required />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Input label="Email Address (Optional)" type="email" value={formData.email} onChange={(e) => setFormData({ ...formData, email: e.target.value })} />
            <Input label="Donation Amount (INR) *" type="number" min="1" step="0.01" placeholder="e.g. 1000" value={formData.amount} onChange={(e) => setFormData({ ...formData, amount: e.target.value })} required />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-xs font-bold text-slate-300 mb-1.5 uppercase tracking-wider">Payment Method *</label>
              <select
                className="w-full bg-[#0d121c] border border-slate-800 text-slate-100 text-sm rounded-xl p-2.5 outline-none focus:border-orange-500 font-semibold"
                value={formData.payment_method}
                onChange={(e) => setFormData({ ...formData, payment_method: e.target.value })}
              >
                <option value="UPI">UPI / GPay / PhonePe</option>
                <option value="BANK_TRANSFER">Bank Transfer (NEFT/RTGS)</option>
                <option value="CASH">Cash</option>
                <option value="CHEQUE">Cheque</option>
              </select>
            </div>

            <Input label="Transaction / Ref ID *" placeholder="e.g. TXN987654321" value={formData.transaction_id} onChange={(e) => setFormData({ ...formData, transaction_id: e.target.value })} required />
            <Input label="UPI Ref Number (Optional)" placeholder="e.g. 123456789012" value={formData.upi_ref} onChange={(e) => setFormData({ ...formData, upi_ref: e.target.value })} />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-bold text-slate-300 mb-1.5 uppercase tracking-wider">State (Optional)</label>
              <select
                className="w-full bg-[#0d121c] border border-slate-800 text-slate-100 text-sm rounded-xl p-2.5 outline-none focus:border-orange-500 font-semibold"
                value={formData.state}
                onChange={(e) => handleStateChange(e.target.value)}
              >
                <option value="">Select State</option>
                {states.map((s) => <option key={s.id} value={s.id}>{s.name}</option>)}
              </select>
            </div>

            <div>
              <label className="block text-xs font-bold text-slate-300 mb-1.5 uppercase tracking-wider">District (Optional)</label>
              <select
                className="w-full bg-[#0d121c] border border-slate-800 text-slate-100 text-sm rounded-xl p-2.5 outline-none focus:border-orange-500 font-semibold"
                value={formData.district}
                onChange={(e) => setFormData({ ...formData, district: e.target.value })}
                disabled={!formData.state}
              >
                <option value="">Select District</option>
                {districts.map((d) => <option key={d.id} value={d.id}>{d.name}</option>)}
              </select>
            </div>
          </div>

          <Input label="Purpose / Cause" value={formData.purpose} onChange={(e) => setFormData({ ...formData, purpose: e.target.value })} required />

          <Button type="submit" size="lg" className="w-full bvs-glow-saffron" isLoading={isLoading}>
            <Heart size={16} className="mr-2 fill-current" /> Submit Donation Verification
          </Button>
        </form>
      </Card>
    </div>
  );
};
