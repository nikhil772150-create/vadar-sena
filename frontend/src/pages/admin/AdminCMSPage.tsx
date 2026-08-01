import React, { useEffect, useState } from 'react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { Input } from '../../components/ui/Input';
import { Newspaper, Plus, CheckCircle2 } from 'lucide-react';
import { CMSService } from '../../api/services';
import { News, NewsCategory, FAQ, HomepageBanner } from '../../types';

export const AdminCMSPage: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'NEWS' | 'CATEGORIES' | 'FAQS' | 'BANNERS'>('NEWS');
  const [news, setNews] = useState<News[]>([]);
  const [categories, setCategories] = useState<NewsCategory[]>([]);
  const [faqs, setFaqs] = useState<FAQ[]>([]);
  const [banners, setBanners] = useState<HomepageBanner[]>([]);

  const [showAddModal, setShowAddModal] = useState(false);
  const [formData, setFormData] = useState<any>({ title: '', content: '', category_id: '', name: '', question: '', answer: '', caption: '', target_url: '' });
  const [successMsg, setSuccessMsg] = useState('');

  const extractList = (res: any) => {
    if (!res) return [];
    if (Array.isArray(res)) return res;
    if (Array.isArray(res.results)) return res.results;
    if (Array.isArray(res.data)) return res.data;
    return [];
  };

  const loadData = () => {
    CMSService.getNews({}).then((res) => setNews(extractList(res))).catch(() => {});
    CMSService.getCategories().then((res) => setCategories(extractList(res))).catch(() => {});
    CMSService.getFaqs().then((res) => setFaqs(extractList(res))).catch(() => {});
    CMSService.getBanners().then((res) => setBanners(extractList(res))).catch(() => {});
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      if (activeTab === 'NEWS') {
        await CMSService.createNews({
          title: formData.title,
          content: formData.content,
          category: formData.category_id ? Number(formData.category_id) : null,
          status: 'PUBLISHED'
        });
      } else if (activeTab === 'CATEGORIES') {
        await CMSService.createCategory({ name: formData.name });
      } else if (activeTab === 'FAQS') {
        await CMSService.createFaq({ question: formData.question, answer: formData.answer });
      } else if (activeTab === 'BANNERS') {
        await CMSService.createBanner({ title: formData.title, caption: formData.caption, target_url: formData.target_url });
      }

      setSuccessMsg(`Created ${activeTab.toLowerCase()} record!`);
      setShowAddModal(false);
      setFormData({ title: '', content: '', category_id: '', name: '', question: '', answer: '', caption: '', target_url: '' });
      loadData();
      setTimeout(() => setSuccessMsg(''), 3000);
    } catch (err: any) {
      alert(err?.message || "Failed to create entry.");
    }
  };

  const handlePublish = async (id: number) => {
    await CMSService.publishNews(id);
    loadData();
  };

  const handleArchive = async (id: number) => {
    await CMSService.archiveNews(id);
    loadData();
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-100 flex items-center gap-2">
            <Newspaper className="text-amber-400" size={24} /> News & Content Management (CMS)
          </h1>
          <p className="text-xs text-slate-400 mt-1">Publish news articles, categories, FAQs, and homepage banners</p>
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

      {/* Tabs */}
      <div className="flex flex-wrap items-center gap-2 bg-slate-900 p-1.5 rounded-xl border border-slate-800">
        {(['NEWS', 'CATEGORIES', 'FAQS', 'BANNERS'] as const).map((tab) => (
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
        {activeTab === 'NEWS' && (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-950 text-slate-400 border-b border-slate-800">
                <tr>
                  <th className="p-3">Title</th>
                  <th className="p-3">Category</th>
                  <th className="p-3">Status</th>
                  <th className="p-3 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60 text-slate-200">
                {news.map((item) => (
                  <tr key={item.id} className="hover:bg-slate-800/30">
                    <td className="p-3 font-bold">{item.title}</td>
                    <td className="p-3">{item.category_name || 'General'}</td>
                    <td className="p-3">
                      <Badge variant={item.status === 'PUBLISHED' ? 'success' : item.status === 'DRAFT' ? 'warning' : 'neutral'}>
                        {item.status}
                      </Badge>
                    </td>
                    <td className="p-3 text-right space-x-2">
                      {item.status === 'DRAFT' && (
                        <Button size="sm" onClick={() => handlePublish(item.id)}>Publish</Button>
                      )}
                      {item.status === 'PUBLISHED' && (
                        <Button size="sm" variant="outline" onClick={() => handleArchive(item.id)}>Archive</Button>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {activeTab === 'CATEGORIES' && (
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
            {categories.map((c) => (
              <div key={c.id} className="p-4 rounded-xl bg-slate-950 border border-slate-800 flex items-center justify-between">
                <div>
                  <h4 className="text-sm font-bold text-slate-100">{c.name}</h4>
                  <span className="text-[10px] text-slate-400 font-mono">Slug: {c.slug}</span>
                </div>
                <Badge variant="success">Active</Badge>
              </div>
            ))}
          </div>
        )}

        {activeTab === 'FAQS' && (
          <div className="space-y-4">
            {faqs.map((f) => (
              <div key={f.id} className="p-4 rounded-xl bg-slate-950 border border-slate-800 space-y-1">
                <h4 className="text-sm font-bold text-slate-100">{f.question}</h4>
                <p className="text-xs text-slate-400">{f.answer}</p>
              </div>
            ))}
          </div>
        )}

        {activeTab === 'BANNERS' && (
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {banners.map((b) => (
              <div key={b.id} className="p-4 rounded-xl bg-slate-950 border border-slate-800 space-y-2">
                <h4 className="text-sm font-bold text-slate-100">{b.title}</h4>
                <p className="text-xs text-slate-400">{b.caption}</p>
              </div>
            ))}
          </div>
        )}
      </Card>

      {/* Add Modal */}
      {showAddModal && (
        <div className="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-sm flex items-center justify-center p-4">
          <Card className="max-w-md w-full p-6 space-y-4">
            <div className="flex items-center justify-between">
              <h3 className="text-lg font-bold text-slate-100">Add New {activeTab.slice(0, -1)}</h3>
              <Button size="sm" variant="ghost" onClick={() => setShowAddModal(false)}>Close</Button>
            </div>

            <form onSubmit={handleCreate} className="space-y-4">
              {activeTab === 'NEWS' && (
                <>
                  <Input label="News Title *" value={formData.title} onChange={(e) => setFormData({ ...formData, title: e.target.value })} required />
                  <div>
                    <label className="block text-xs font-semibold text-slate-300 mb-1.5">Category</label>
                    <select
                      className="w-full bg-slate-950/80 border border-slate-800 text-slate-100 text-sm rounded-lg p-2.5 outline-none"
                      value={formData.category_id}
                      onChange={(e) => setFormData({ ...formData, category_id: e.target.value })}
                    >
                      <option value="">General Category</option>
                      {categories.map((c) => <option key={c.id} value={c.id}>{c.name}</option>)}
                    </select>
                  </div>
                  <div>
                    <label className="block text-xs font-semibold text-slate-300 mb-1.5">Article Content *</label>
                    <textarea
                      rows={4}
                      className="w-full bg-slate-950/80 border border-slate-800 text-slate-100 text-sm rounded-lg p-3 outline-none"
                      value={formData.content}
                      onChange={(e) => setFormData({ ...formData, content: e.target.value })}
                      required
                    />
                  </div>
                </>
              )}

              {activeTab === 'CATEGORIES' && (
                <Input label="Category Name *" value={formData.name} onChange={(e) => setFormData({ ...formData, name: e.target.value })} required />
              )}

              {activeTab === 'FAQS' && (
                <>
                  <Input label="Question *" value={formData.question} onChange={(e) => setFormData({ ...formData, question: e.target.value })} required />
                  <Input label="Answer *" value={formData.answer} onChange={(e) => setFormData({ ...formData, answer: e.target.value })} required />
                </>
              )}

              {activeTab === 'BANNERS' && (
                <>
                  <Input label="Banner Title *" value={formData.title} onChange={(e) => setFormData({ ...formData, title: e.target.value })} required />
                  <Input label="Caption *" value={formData.caption} onChange={(e) => setFormData({ ...formData, caption: e.target.value })} required />
                </>
              )}

              <Button type="submit" className="w-full">Create CMS Entry</Button>
            </form>
          </Card>
        </div>
      )}
    </div>
  );
};
