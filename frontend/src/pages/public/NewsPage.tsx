import React, { useEffect, useState } from 'react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Input } from '../../components/ui/Input';
import { Button } from '../../components/ui/Button';
import { Newspaper, Calendar, Pin, Search } from 'lucide-react';
import { CMSService } from '../../api/services';
import { News, NewsCategory } from '../../types';

export const NewsPage: React.FC = () => {
  const [newsList, setNewsList] = useState<News[]>([]);
  const [categories, setCategories] = useState<NewsCategory[]>([]);
  const [search, setSearch] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<string>('');
  const [activeArticle, setActiveArticle] = useState<News | null>(null);

  const extractList = (res: any) => {
    if (!res) return [];
    if (Array.isArray(res)) return res;
    if (Array.isArray(res.results)) return res.results;
    if (Array.isArray(res.data)) return res.data;
    return [];
  };

  const fetchNews = () => {
    CMSService.getNews({ search, category: selectedCategory })
      .then((res) => setNewsList(extractList(res)))
      .catch(() => {});
  };

  useEffect(() => {
    CMSService.getCategories().then((res) => setCategories(extractList(res))).catch(() => {});
  }, []);

  useEffect(() => {
    fetchNews();
  }, [selectedCategory]);

  return (
    <div className="space-y-8 py-10 px-4 max-w-7xl mx-auto bvs-bg-pattern">
      <div>
        <h1 className="text-3xl font-black text-slate-100 flex items-center gap-3 font-heading">
          <Newspaper className="text-orange-400" size={32} /> Organization News & Announcements
        </h1>
        <p className="text-xs text-slate-400 mt-2 font-medium">Latest press releases, organizational updates, and community bulletins</p>
      </div>

      {/* Search & Filter Header */}
      <Card className="p-5">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div className="w-full sm:w-80">
            <Input
              placeholder="Search news by title or keyword..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && fetchNews()}
            />
          </div>

          <div className="flex items-center gap-3">
            <select
              className="bg-[#0d121c] border border-slate-800 text-slate-100 text-xs rounded-xl p-2.5 outline-none focus:border-orange-500 font-semibold"
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
            >
              <option value="">All Categories</option>
              {categories.map((c) => (
                <option key={c.id} value={c.id}>{c.name}</option>
              ))}
            </select>
            <Button size="sm" onClick={fetchNews}><Search size={14} className="mr-1.5" /> Search</Button>
          </div>
        </div>
      </Card>

      {/* News Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {newsList.length > 0 ? (
          newsList.map((item) => (
            <Card key={item.id} className="p-6 flex flex-col justify-between">
              <div>
                <div className="flex items-center justify-between gap-2 mb-3">
                  <Badge variant="warning">{item.category_name || 'General'}</Badge>
                  {item.is_pinned && (
                    <span className="flex items-center gap-1 text-[10px] font-bold text-orange-400 bg-orange-500/10 px-2 py-0.5 rounded-full border border-orange-500/30">
                      <Pin size={10} /> Pinned
                    </span>
                  )}
                </div>

                <h3 className="text-base font-bold text-slate-100 line-clamp-2 mb-2 font-heading">{item.title}</h3>
                <p className="text-slate-400 text-xs line-clamp-3 mb-4 font-medium">{item.content}</p>
              </div>

              <div className="pt-4 border-t border-slate-800/80 flex items-center justify-between">
                <span className="text-[11px] text-slate-500 flex items-center gap-1 font-mono">
                  <Calendar size={12} /> {new Date(item.published_at || item.created_at).toLocaleDateString()}
                </span>
                <Button size="sm" variant="outline" onClick={() => setActiveArticle(item)}>Read Article</Button>
              </div>
            </Card>
          ))
        ) : (
          <div className="col-span-full py-12 text-center text-xs text-slate-500 font-medium">
            No news articles found matching current filters.
          </div>
        )}
      </div>

      {/* Detail Modal */}
      {activeArticle && (
        <div className="fixed inset-0 z-50 bg-[#090d16]/80 backdrop-blur-md flex items-center justify-center p-4">
          <Card className="max-w-2xl w-full p-6 space-y-4 max-h-[85vh] overflow-y-auto border-orange-500/30">
            <div className="flex items-start justify-between">
              <div>
                <Badge variant="warning">{activeArticle.category_name || 'General'}</Badge>
                <h2 className="text-xl font-bold text-slate-100 mt-2 font-heading">{activeArticle.title}</h2>
                <span className="text-xs text-slate-400 font-mono block mt-1">
                  Published on {new Date(activeArticle.published_at || activeArticle.created_at).toLocaleString()}
                </span>
              </div>
              <Button size="sm" variant="ghost" onClick={() => setActiveArticle(null)}>Close</Button>
            </div>

            <div className="pt-4 border-t border-slate-800 text-slate-200 text-sm leading-relaxed whitespace-pre-line font-medium">
              {activeArticle.content}
            </div>
          </Card>
        </div>
      )}
    </div>
  );
};
