import api from './client';
import { ApiResponse, DashboardSummary, State, District, Taluka, Village } from '../types';

export const AuthService = {
  login: (phone_number: string, password?: string) =>
    api.post<any, ApiResponse>('/auth/login/', { phone_number, password }),
  requestOtp: (phone_number: string) =>
    api.post<any, ApiResponse>('/auth/send-otp/', { phone_number }),
  verifyOtp: (phone_number: string, otp_code: string) =>
    api.post<any, ApiResponse>('/auth/verify-otp/', { phone_number, otp_code }),
  getProfile: () =>
    api.get<any, ApiResponse>('/auth/me/'),
};

export const OrganizationService = {
  getStates: () => api.get<any, any>('/organization/states/'),
  getDistricts: (stateId?: number) => api.get<any, any>('/organization/districts/', { params: { state: stateId } }),
  getTalukas: (districtId?: number) => api.get<any, any>('/organization/talukas/', { params: { district: districtId } }),
  getVillages: (talukaId?: number) => api.get<any, any>('/organization/villages/', { params: { taluka: talukaId } }),
  getDesignations: () => api.get<any, any>('/organization/designations/'),
  createState: (data: Partial<State>) => api.post<any, ApiResponse>('/organization/states/', data),
  createDistrict: (data: Partial<District>) => api.post<any, ApiResponse>('/organization/districts/', data),
  createTaluka: (data: Partial<Taluka>) => api.post<any, ApiResponse>('/organization/talukas/', data),
  createVillage: (data: Partial<Village>) => api.post<any, ApiResponse>('/organization/villages/', data),
  createDesignation: (data: any) => api.post<any, ApiResponse>('/organization/designations/', data),
};

export const MemberService = {
  register: (payload: any) => api.post<any, ApiResponse>('/members/register/', payload),
  getMembers: (params?: any) => api.get<any, any>('/members/', { params }),
  getMemberDetail: (id: number) => api.get<any, ApiResponse>(`/members/${id}/`),
  approveMember: (id: number, remarks?: string) => api.post<any, ApiResponse>(`/members/${id}/approve/`, { remarks }),
  rejectMember: (id: number, remarks?: string) => api.post<any, ApiResponse>(`/members/${id}/reject/`, { remarks }),
  suspendMember: (id: number, remarks?: string) => api.post<any, ApiResponse>(`/members/${id}/suspend/`, { remarks }),
  restoreMember: (id: number, remarks?: string) => api.post<any, ApiResponse>(`/members/${id}/restore/`, { remarks }),
  verifyCard: (qrToken: string) => api.get<any, ApiResponse>(`/members/verify-card/${qrToken}/`),
  getCard: (id: number) => api.get<any, ApiResponse>(`/members/${id}/card/`),
  getDocuments: (id: number) => api.get<any, ApiResponse>(`/members/${id}/documents/`),
  uploadDocument: (id: number, data: any) => api.post<any, ApiResponse>(`/members/${id}/documents/`, data),
  requestTransfer: (id: number, data: any) => api.post<any, ApiResponse>(`/members/${id}/transfer/`, data),
};

export const CMSService = {
  getNews: (params?: any) => api.get<any, any>('/news-cms/news/', { params }),
  getNewsDetail: (id: number) => api.get<any, ApiResponse>(`/news-cms/news/${id}/`),
  getCategories: () => api.get<any, any>('/news-cms/categories/'),
  getStaticPage: (slug: string) => api.get<any, any>(`/news-cms/pages/${slug}/`),
  getFaqs: () => api.get<any, any>('/news-cms/faqs/'),
  getBanners: () => api.get<any, any>('/news-cms/banners/'),
  createNews: (data: any) => api.post<any, ApiResponse>('/news-cms/news/', data),
  publishNews: (id: number) => api.post<any, ApiResponse>(`/news-cms/news/${id}/publish/`),
  archiveNews: (id: number) => api.post<any, ApiResponse>(`/news-cms/news/${id}/archive/`),
  createCategory: (data: any) => api.post<any, ApiResponse>('/news-cms/categories/', data),
  createFaq: (data: any) => api.post<any, ApiResponse>('/news-cms/faqs/', data),
  createBanner: (data: any) => api.post<any, ApiResponse>('/news-cms/banners/', data),
};

export const EventsService = {
  getEvents: (params?: any) => api.get<any, any>('/events-meetings/events/', { params }),
  createEvent: (data: any) => api.post<any, ApiResponse>('/events-meetings/events/', data),
  rsvpEvent: (id: number, status: string) => api.post<any, ApiResponse>(`/events-meetings/events/${id}/rsvp/`, { status }),
  getMeetings: () => api.get<any, any>('/events-meetings/meetings/'),
  createMeeting: (data: any) => api.post<any, ApiResponse>('/events-meetings/meetings/', data),
  addMeetingMinutes: (id: number, data: any) => api.post<any, ApiResponse>(`/events-meetings/meetings/${id}/add_minutes/`, data),
};

export const GalleryService = {
  getAlbums: () => api.get<any, any>('/gallery/albums/'),
  createAlbum: (data: any) => api.post<any, ApiResponse>('/gallery/albums/', data),
  getVideos: () => api.get<any, any>('/gallery/videos/'),
  createVideo: (data: any) => api.post<any, ApiResponse>('/gallery/videos/', data),
};

export const CommunicationsService = {
  submitContact: (data: any) => api.post<any, ApiResponse>('/communications/contact/', data),
  getContactInquiries: () => api.get<any, any>('/communications/contact/'),
  getNotifications: () => api.get<any, ApiResponse>('/communications/notifications/'),
};

export const DonationService = {
  submitDonation: (data: any) => api.post<any, ApiResponse>('/donations/', data),
  getDonations: (params?: any) => api.get<any, any>('/donations/', { params }),
  verifyDonation: (id: number, remarks?: string) => api.post<any, ApiResponse>(`/donations/${id}/verify/`, { remarks }),
  rejectDonation: (id: number, remarks?: string) => api.post<any, ApiResponse>(`/donations/${id}/reject/`, { remarks }),
  getMyDonations: () => api.get<any, ApiResponse>('/donations/my_donations/'),
};

export const AnalyticsService = {
  getDashboardSummary: () => api.get<any, ApiResponse<DashboardSummary>>('/analytics/dashboard/'),
  getMemberReport: (params?: any) => api.get<any, ApiResponse>('/analytics/reports/members/', { params }),
  getDonationReport: (params?: any) => api.get<any, ApiResponse>('/analytics/reports/donations/', { params }),
  getRegionalStats: () => api.get<any, any>('/analytics/regional-stats/'),
};
