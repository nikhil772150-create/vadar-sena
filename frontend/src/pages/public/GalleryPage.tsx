import React, { useEffect, useState } from 'react';
import { Card } from '../../components/ui/Card';
import { Image as ImageIcon, Video, Folder, ExternalLink } from 'lucide-react';
import { GalleryService } from '../../api/services';
import { GalleryAlbum, GalleryVideo } from '../../types';

export const GalleryPage: React.FC = () => {
  const [albums, setAlbums] = useState<GalleryAlbum[]>([]);
  const [videos, setVideos] = useState<GalleryVideo[]>([]);
  const [activeTab, setActiveTab] = useState<'ALBUMS' | 'VIDEOS'>('ALBUMS');

  const extractList = (res: any) => {
    if (!res) return [];
    if (Array.isArray(res)) return res;
    if (Array.isArray(res.results)) return res.results;
    if (Array.isArray(res.data)) return res.data;
    return [];
  };

  useEffect(() => {
    GalleryService.getAlbums().then((res) => setAlbums(extractList(res))).catch(() => {});
    GalleryService.getVideos().then((res) => setVideos(extractList(res))).catch(() => {});
  }, []);

  return (
    <div className="space-y-8 py-10 px-4 max-w-7xl mx-auto bvs-bg-pattern">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-black text-slate-100 flex items-center gap-3 font-heading">
            <ImageIcon className="text-orange-400" size={32} /> Organization Media Gallery
          </h1>
          <p className="text-xs text-slate-400 mt-2 font-medium">Photo albums, event coverages, and video highlights</p>
        </div>

        <div className="flex items-center gap-2 bg-[#0d121c] p-1.5 rounded-xl border border-slate-800">
          <button
            onClick={() => setActiveTab('ALBUMS')}
            className={`px-4 py-2 rounded-lg text-xs font-bold transition flex items-center gap-2 ${activeTab === 'ALBUMS' ? 'bg-gradient-to-r from-orange-600 to-amber-600 text-slate-950 shadow-md' : 'text-slate-400 hover:text-slate-200'}`}
          >
            <Folder size={14} /> Photo Albums ({albums.length})
          </button>
          <button
            onClick={() => setActiveTab('VIDEOS')}
            className={`px-4 py-2 rounded-lg text-xs font-bold transition flex items-center gap-2 ${activeTab === 'VIDEOS' ? 'bg-gradient-to-r from-orange-600 to-amber-600 text-slate-950 shadow-md' : 'text-slate-400 hover:text-slate-200'}`}
          >
            <Video size={14} /> Video Gallery ({videos.length})
          </button>
        </div>
      </div>

      {activeTab === 'ALBUMS' ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
          {albums.length > 0 ? (
            albums.map((alb) => (
              <Card key={alb.id} className="p-6 flex flex-col justify-between">
                <div>
                  <div className="w-12 h-12 rounded-xl bg-orange-500/10 border border-orange-500/30 flex items-center justify-center text-orange-400 mb-4 shadow-lg shadow-orange-500/10">
                    <Folder size={24} />
                  </div>
                  <h3 className="text-base font-bold text-slate-100 mb-2 font-heading">{alb.title}</h3>
                  <p className="text-xs text-slate-400 line-clamp-2 font-medium">{alb.description || 'No description provided.'}</p>
                </div>
                <div className="mt-4 pt-3 border-t border-slate-800 text-[11px] text-slate-500 font-mono">
                  Created {new Date(alb.created_at).toLocaleDateString()}
                </div>
              </Card>
            ))
          ) : (
            <div className="col-span-full py-12 text-center text-xs text-slate-500 font-medium">
              No photo albums published yet.
            </div>
          )}
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
          {videos.length > 0 ? (
            videos.map((vid) => (
              <Card key={vid.id} className="p-6 flex flex-col justify-between">
                <div>
                  <div className="w-12 h-12 rounded-xl bg-rose-500/10 border border-rose-500/30 flex items-center justify-center text-rose-400 mb-4 shadow-lg shadow-rose-500/10">
                    <Video size={24} />
                  </div>
                  <h3 className="text-base font-bold text-slate-100 mb-2 font-heading">{vid.title}</h3>
                  <p className="text-xs text-slate-400 line-clamp-2 font-medium">{vid.description || 'Video recording'}</p>
                </div>
                <div className="mt-4 pt-3 border-t border-slate-800 flex items-center justify-between">
                  <a
                    href={vid.video_url}
                    target="_blank"
                    rel="noreferrer"
                    className="text-xs font-bold text-orange-400 hover:underline inline-flex items-center gap-1"
                  >
                    Watch Video <ExternalLink size={12} />
                  </a>
                </div>
              </Card>
            ))
          ) : (
            <div className="col-span-full py-12 text-center text-xs text-slate-500 font-medium">
              No video links published yet.
            </div>
          )}
        </div>
      )}
    </div>
  );
};
