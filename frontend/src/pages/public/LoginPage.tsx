import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { Card } from '../../components/ui/Card';
import { Input } from '../../components/ui/Input';
import { Button } from '../../components/ui/Button';
import { AuthService } from '../../api/services';
import { Lock, ArrowLeft } from 'lucide-react';

export const LoginPage: React.FC = () => {
  const [phoneNumber, setPhoneNumber] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    try {
      const res = await AuthService.login(phoneNumber, password);
      const access = res.data?.tokens?.access || res.data?.access;
      const refresh = res.data?.tokens?.refresh || res.data?.refresh;

      if (res.success && access) {
        await login(access, refresh);
        navigate('/admin');
      } else {
        setError(res.message || 'Login failed.');
      }
    } catch (err: any) {
      setError(err?.message || err?.errors?.non_field_errors?.[0] || 'Invalid phone number or password.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="max-w-md mx-auto px-4 py-20 relative bvs-bg-pattern">
      {/* Background ambient glow */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[380px] h-[260px] bg-orange-600/10 blur-[110px] rounded-full pointer-events-none" />

      <Card className="relative z-10 p-8 shadow-2xl border-orange-500/30">
        <div className="text-center mb-6">
          <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-orange-500/20 to-rose-500/10 text-orange-400 flex items-center justify-center mx-auto mb-4 border border-orange-500/30 shadow-xl shadow-orange-500/10">
            <Lock size={30} />
          </div>
          <h2 className="text-2xl font-black text-slate-100 tracking-tight font-heading">Admin Authentication</h2>
          <p className="text-xs text-slate-400 mt-1 font-medium">Sign in with authorized administrator credentials</p>
        </div>

        {error && (
          <div className="mb-5 p-3.5 rounded-xl bg-rose-950/80 border border-rose-500/30 text-rose-400 text-xs font-semibold flex items-center gap-2">
            <span>⚠️ {error}</span>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <Input
            label="Phone Number"
            placeholder="e.g. 9876543210"
            value={phoneNumber}
            onChange={(e) => setPhoneNumber(e.target.value)}
            required
          />
          <Input
            label="Password"
            type="password"
            placeholder="••••••••"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />

          <Button type="submit" size="lg" className="w-full mt-2 bvs-glow-saffron" isLoading={isLoading}>
            Sign In to Admin Panel
          </Button>
        </form>

        <div className="mt-8 pt-4 border-t border-slate-800/80 text-center">
          <Link to="/" className="text-xs font-bold text-slate-400 hover:text-orange-400 transition inline-flex items-center gap-1.5">
            <ArrowLeft size={14} /> Back to Public Information Portal
          </Link>
        </div>
      </Card>
    </div>
  );
};
