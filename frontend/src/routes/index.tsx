import React, { Suspense, lazy } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

// Layouts
import { PublicLayout } from '../layouts/PublicLayout';
import { AdminLayout } from '../layouts/AdminLayout';

// Public Pages
const HomePage = lazy(() => import('../pages/public/HomePage').then(m => ({ default: m.HomePage })));
const LoginPage = lazy(() => import('../pages/public/LoginPage').then(m => ({ default: m.LoginPage })));
const AboutPage = lazy(() => import('../pages/public/AboutPage').then(m => ({ default: m.AboutPage })));
const OrganizationPublicPage = lazy(() => import('../pages/public/OrganizationPublicPage').then(m => ({ default: m.OrganizationPublicPage })));
const NewsPage = lazy(() => import('../pages/public/NewsPage').then(m => ({ default: m.NewsPage })));
const EventsPage = lazy(() => import('../pages/public/EventsPage').then(m => ({ default: m.EventsPage })));
const GalleryPage = lazy(() => import('../pages/public/GalleryPage').then(m => ({ default: m.GalleryPage })));
const DonationPage = lazy(() => import('../pages/public/DonationPage').then(m => ({ default: m.DonationPage })));
const ContactPage = lazy(() => import('../pages/public/ContactPage').then(m => ({ default: m.ContactPage })));

// Admin Panel Pages
const AdminDashboard = lazy(() => import('../pages/admin/AdminDashboard').then(m => ({ default: m.AdminDashboard })));
const AdminDonationsPage = lazy(() => import('../pages/admin/AdminDonationsPage').then(m => ({ default: m.AdminDonationsPage })));
const AdminOrganizationPage = lazy(() => import('../pages/admin/AdminOrganizationPage').then(m => ({ default: m.AdminOrganizationPage })));
const AdminCMSPage = lazy(() => import('../pages/admin/AdminCMSPage').then(m => ({ default: m.AdminCMSPage })));
const AdminEventsMeetingsPage = lazy(() => import('../pages/admin/AdminEventsMeetingsPage').then(m => ({ default: m.AdminEventsMeetingsPage })));
const AdminReportsPage = lazy(() => import('../pages/admin/AdminReportsPage').then(m => ({ default: m.AdminReportsPage })));

const LoadingSpinner = () => (
  <div className="flex items-center justify-center p-12 text-xs font-semibold text-slate-400">
    <div className="animate-spin h-5 w-5 border-2 border-amber-500 border-t-transparent rounded-full mr-3" />
    Loading BVSMS View...
  </div>
);

const ProtectedRoute: React.FC<{ children: React.ReactNode; allowedTypes?: string[] }> = ({ children, allowedTypes }) => {
  const { isAuthenticated, isLoading, user } = useAuth();

  if (isLoading) return <LoadingSpinner />;
  if (!isAuthenticated) return <Navigate to="/login" replace />;

  if (allowedTypes && user && !allowedTypes.includes(user.user_type)) {
    return <Navigate to="/" replace />;
  }

  return <>{children}</>;
};

export const AppRoutes: React.FC = () => {
  return (
    <Suspense fallback={<LoadingSpinner />}>
      <Routes>
        {/* Public Routes */}
        <Route element={<PublicLayout />}>
          <Route path="/" element={<HomePage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/about" element={<AboutPage />} />
          <Route path="/organization" element={<OrganizationPublicPage />} />
          <Route path="/news" element={<NewsPage />} />
          <Route path="/events" element={<EventsPage />} />
          <Route path="/gallery" element={<GalleryPage />} />
          <Route path="/donate" element={<DonationPage />} />
          <Route path="/contact" element={<ContactPage />} />
        </Route>

        {/* Admin Panel Routes */}
        <Route
          path="/admin"
          element={
            <ProtectedRoute allowedTypes={['ADMIN', 'SUPERADMIN']}>
              <AdminLayout />
            </ProtectedRoute>
          }
        >
          <Route index element={<AdminDashboard />} />
          <Route path="organization" element={<AdminOrganizationPage />} />
          <Route path="cms" element={<AdminCMSPage />} />
          <Route path="events" element={<AdminEventsMeetingsPage />} />
          <Route path="donations" element={<AdminDonationsPage />} />
          <Route path="reports" element={<AdminReportsPage />} />
        </Route>

        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Suspense>
  );
};
