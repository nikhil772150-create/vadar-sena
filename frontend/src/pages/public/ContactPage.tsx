import React, { useState } from 'react';
import { Card } from '../../components/ui/Card';
import { Input } from '../../components/ui/Input';
import { Button } from '../../components/ui/Button';
import { Mail, Phone, MapPin, Send, CheckCircle2 } from 'lucide-react';
import { CommunicationsService } from '../../api/services';

export const ContactPage: React.FC = () => {
  const [formData, setFormData] = useState({
    name: '',
    phone_number: '',
    subject: '',
    message: '',
  });

  const [error, setError] = useState('');
  const [successMsg, setSuccessMsg] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setSuccessMsg('');
    setIsLoading(true);

    try {
      const res = await CommunicationsService.submitContact(formData);
      if (res.success) {
        setSuccessMsg("Your inquiry message has been submitted. Our team will contact you shortly!");
        setFormData({ name: '', phone_number: '', subject: '', message: '' });
      } else {
        setError(res.message || 'Submission failed.');
      }
    } catch (err: any) {
      setError(err?.message || 'Failed to submit contact inquiry.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="max-w-6xl mx-auto px-4 py-12 space-y-8 bvs-bg-pattern">
      <div>
        <h1 className="text-3xl font-black text-slate-100 flex items-center gap-3 font-heading">
          <Mail className="text-orange-400" size={32} /> Contact & Support Desk
        </h1>
        <p className="text-xs text-slate-400 mt-2 font-medium">Get in touch with Bharatiya Vadar Sena administrative office and regional leaders</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Contact Info Cards */}
        <div className="space-y-4 lg:col-span-1">
          <Card className="p-6">
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 rounded-2xl bg-orange-500/10 border border-orange-500/30 flex items-center justify-center text-orange-400 shrink-0 shadow-lg shadow-orange-500/10">
                <MapPin size={22} />
              </div>
              <div>
                <h4 className="text-sm font-bold text-slate-100 font-heading">Central Head Office</h4>
                <p className="text-xs text-slate-400 font-medium">Pune, Maharashtra, India</p>
              </div>
            </div>
          </Card>

          <Card className="p-6">
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 rounded-2xl bg-orange-500/10 border border-orange-500/30 flex items-center justify-center text-orange-400 shrink-0 shadow-lg shadow-orange-500/10">
                <Phone size={22} />
              </div>
              <div>
                <h4 className="text-sm font-bold text-slate-100 font-heading">Official Helpline</h4>
                <p className="text-xs text-slate-400 font-mono">+91 98765 43210</p>
              </div>
            </div>
          </Card>

          <Card className="p-6">
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 rounded-2xl bg-orange-500/10 border border-orange-500/30 flex items-center justify-center text-orange-400 shrink-0 shadow-lg shadow-orange-500/10">
                <Mail size={22} />
              </div>
              <div>
                <h4 className="text-sm font-bold text-slate-100 font-heading">Email Support</h4>
                <p className="text-xs text-slate-400 font-mono">contact@vadarsena.org</p>
              </div>
            </div>
          </Card>
        </div>

        {/* Contact Form */}
        <div className="lg:col-span-2">
          <Card title="Send an Inquiry" subtitle="Fill out the form below to reach out to central organization secretaries">
            {error && <div className="mb-4 p-3.5 rounded-xl bg-rose-950/80 border border-rose-500/30 text-rose-400 text-xs font-semibold">{error}</div>}
            {successMsg && (
              <div className="mb-4 p-3.5 rounded-xl bg-emerald-950/80 border border-emerald-500/30 text-emerald-400 text-xs font-bold flex items-center gap-2">
                <CheckCircle2 size={16} /> {successMsg}
              </div>
            )}

            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <Input label="Your Name *" value={formData.name} onChange={(e) => setFormData({ ...formData, name: e.target.value })} required />
                <Input label="Phone Number *" placeholder="e.g. 9876543210" value={formData.phone_number} onChange={(e) => setFormData({ ...formData, phone_number: e.target.value })} required />
              </div>

              <Input label="Subject *" placeholder="e.g. Rally Registration / Support Inquiry" value={formData.subject} onChange={(e) => setFormData({ ...formData, subject: e.target.value })} required />

              <div>
                <label className="block text-xs font-bold text-slate-300 mb-1.5 uppercase tracking-wider">Message Details *</label>
                <textarea
                  rows={4}
                  className="w-full bg-[#0d121c] border border-slate-800 text-slate-100 text-sm rounded-xl p-3 outline-none focus:border-orange-500 font-medium"
                  placeholder="Type your message details..."
                  value={formData.message}
                  onChange={(e) => setFormData({ ...formData, message: e.target.value })}
                  required
                />
              </div>

              <Button type="submit" size="lg" className="w-full bvs-glow-saffron" isLoading={isLoading}>
                <Send size={16} className="mr-2" /> Send Inquiry
              </Button>
            </form>
          </Card>
        </div>
      </div>
    </div>
  );
};
