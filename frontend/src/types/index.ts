export type UserType = 'SUPERADMIN' | 'ADMIN' | 'OFFICE_BEARER' | 'MEMBER' | 'PUBLIC_USER';
export type MemberStatus = 'PENDING' | 'APPROVED' | 'REJECTED' | 'SUSPENDED' | 'INACTIVE' | 'TRANSFERRED';
export type HierarchyLevel = 'NATIONAL' | 'STATE' | 'DISTRICT' | 'TALUKA' | 'VILLAGE';
export type VerificationStatus = 'PENDING' | 'VERIFIED' | 'REJECTED';

export interface ApiResponse<T = any> {
  success: boolean;
  message: string;
  data: T;
  errors?: Record<string, string[]>;
}

export interface User {
  id: number;
  uuid: string;
  phone_number: string;
  email?: string;
  user_type: UserType;
  is_staff: boolean;
  date_joined: string;
}

export interface State {
  id: number;
  uuid: string;
  name: string;
  code: string;
  is_active: boolean;
  districts_count?: number;
}

export interface District {
  id: number;
  uuid: string;
  state: number;
  state_name?: string;
  state_code?: string;
  name: string;
  code?: string;
  is_active: boolean;
  talukas_count?: number;
}

export interface Taluka {
  id: number;
  uuid: string;
  district: number;
  district_name?: string;
  state_name?: string;
  name: string;
  is_active: boolean;
  villages_count?: number;
}

export interface Village {
  id: number;
  uuid: string;
  taluka: number;
  taluka_name?: string;
  district_name?: string;
  name: string;
  pin_code?: string;
  is_active: boolean;
}

export interface Designation {
  id: number;
  uuid: string;
  title: string;
  level_scope: HierarchyLevel;
  display_order: number;
  is_active: boolean;
}

export interface MemberProfile {
  father_husband_name?: string;
  blood_group?: string;
  education?: string;
  occupation?: string;
  address_line?: string;
  pincode?: string;
  emergency_contact_name?: string;
  emergency_contact_phone?: string;
  photo_url?: string;
}

export interface MembershipCard {
  card_number: string;
  qr_token: string;
  issued_at?: string;
  expires_at?: string;
  is_active: boolean;
}

export interface Member {
  id: number;
  uuid: string;
  membership_number?: string;
  first_name: string;
  last_name: string;
  gender: 'MALE' | 'FEMALE' | 'OTHER';
  date_of_birth?: string;
  phone_number: string;
  email?: string;
  status: MemberStatus;
  state: number;
  state_name?: string;
  district: number;
  district_name?: string;
  taluka: number;
  taluka_name?: string;
  village: number;
  village_name?: string;
  profile?: MemberProfile;
  membership_card?: MembershipCard;
  created_at: string;
  approved_at?: string;
}

export interface NewsCategory {
  id: number;
  name: string;
  slug: string;
}

export interface News {
  id: number;
  uuid: string;
  title: string;
  slug: string;
  category_name?: string;
  content: string;
  cover_url?: string;
  status: 'DRAFT' | 'PUBLISHED' | 'ARCHIVED';
  is_pinned: boolean;
  published_at?: string;
  created_at: string;
}

export interface FAQ {
  id: number;
  question: string;
  answer: string;
  display_order?: number;
}

export interface HomepageBanner {
  id: number;
  title: string;
  caption: string;
  target_url?: string;
  is_active?: boolean;
}

export interface Event {
  id: number;
  uuid: string;
  title: string;
  description: string;
  venue_address: string;
  map_link?: string;
  start_time: string;
  end_time?: string;
  banner_url?: string;
  status: 'UPCOMING' | 'COMPLETED' | 'CANCELLED';
  is_public: boolean;
  rsvps_count?: number;
}

export interface Meeting {
  id: number;
  uuid: string;
  subject: string;
  agenda: string;
  meeting_date: string;
  venue_or_link: string;
  status: 'SCHEDULED' | 'COMPLETED' | 'CANCELLED';
  created_at: string;
}

export interface GalleryAlbum {
  id: number;
  title: string;
  description?: string;
  created_at: string;
}

export interface GalleryVideo {
  id: number;
  title: string;
  description?: string;
  video_url: string;
  created_at: string;
}

export interface Donation {
  id: number;
  uuid: string;
  donor_name: string;
  phone_number: string;
  email?: string;
  amount: number;
  purpose: string;
  transaction_id: string;
  payment_method: string;
  receipt_url?: string;
  status: VerificationStatus;
  verified_at?: string;
  created_at: string;
}

export interface DashboardSummary {
  counters: {
    total_members: number;
    pending_members: number;
    approved_members: number;
    suspended_members: number;
    transferred_members: number;
    today_registrations: number;
    monthly_registrations: number;
  };
  financials: {
    total_verified_donations: number;
    total_donation_count: number;
  };
  breakdowns: {
    members_by_state: Array<{ id: number; name: string; code: string; member_count: number }>;
    top_districts: Array<{ id: number; name: string; state__name: string; member_count: number }>;
  };
  feeds: {
    recent_members: Array<any>;
    recent_donations: Array<any>;
    upcoming_events: Array<any>;
    latest_news: Array<any>;
  };
}
