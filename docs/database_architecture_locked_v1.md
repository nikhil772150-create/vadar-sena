# Final Database Architecture & Review Report (LOCKED v1.0)
## Bharatiya Vadar Sena Management System (BVSMS) — Version 1.0 (MVP)

**Review Body:** Chief Database Architect, Enterprise Solution Architect, Security Architect, Senior Backend Architect.

---

## 1. Executive Architectural Review & Refinements

### 1.1 Review of User & Member Architecture
- **Current Design:** `auth_users` (1 : 1) `members_member`.
- **Architectural Evaluation:**
  - *Can Admins exist without Member records?* **YES.** Super Admins, System Administrators, or external IT auditors should be pure system accounts (`auth_users`) without requiring dummy geographical member profiles.
  - *Should Member extend User?* **Decoupled 1-to-1 Relationship.** `auth_users` handles identity (phone, password, global system permissions), while `members_member` represents organizational identity (member ID, regional hierarchy node, approval status).
  - *Recommendation:* Keep `auth_users` as the root identity. A `members_member` record is created ONLY when a user registers as an organizational member. Administrative roles reference `auth_users` directly, enabling non-member Super Admins while allowing regional office bearers to be linked to their member profile.
  - *Priority:* **Critical** (Architectural foundation).

### 1.2 Review of Centralized Media Management
- **Current Design:** Decoupled photo fields in individual tables.
- **Architectural Evaluation:**
  - *Issue:* Fragmented upload logic, duplicated file cleanup, inconsistent thumbnail processing.
  - *Recommendation:* Introduce a centralized `media_assets` table (`id`, `uuid`, `file_path`, `file_name`, `file_type`, `mime_type`, `file_size`, `dimensions`, `storage_provider`, `created_at`). Specific domain tables (`cms_news`, `gallery_photos`, `members_profile`, `donations_donation`) maintain a foreign key `media_asset_id` $\rightarrow$ `media_assets(id)`.
  - *Priority:* **Recommended** (Improves storage security, thumbnail processing, and CDN transition).

### 1.3 Review of Master Data & Lookups
- **Current Design:** Ad-hoc strings or hardcoded choices.
- **Architectural Evaluation:**
  - *Recommendation:* Introduce standardized master catalogs:
    - `master_designations`: Official posts (President, Secretary, Treasurer, Committee Member).
    - `master_categories`: Reusable category tags for News, Events, and Gallery.
    - `master_professions` & `master_education`: Standardized dropdown lookups for member profiles.
  - *Priority:* **Recommended** (Prevents spelling typos and simplifies data aggregation).

### 1.4 Review of Address Architecture
- **Current Design:** Address fields embedded directly inside `members_profile`.
- **Architectural Evaluation:**
  - *Recommendation:* Keep administrative geographic links (`state_id`, `district_id`, `taluka_id`, `village_id`) embedded directly in `members_member` for fast regional RBAC query filtering. Embedded address fields in `members_profile` (Street, Landmark, Pincode) are optimal for v1.0. A standalone `addresses` entity is unnecessary overhead for v1.0.
  - *Priority:* **Optional / Maintain Current**.

### 1.5 Review of Settings Architecture
- **Current Design:** Single key-value settings table.
- **Architectural Evaluation:**
  - *Recommendation:* Split settings into specialized functional entities:
    - `system_settings`: Platform operational flags (Maintenance mode, SMS dev mode, Max upload size).
    - `cms_settings`: Website branding, logo media reference, helpline numbers, social media links, footer links.
  - *Priority:* **Recommended** (Isolates security settings from website CMS controls).

### 1.6 Review of Activity, Audit & Security Logging
- **Current Design:** Single audit log table.
- **Architectural Evaluation:**
  - *Recommendation:* Differentiate three distinct logging streams:
    - `system_audit_log`: Administrative data modifications (Who, What, When, Changes JSON).
    - `auth_login_history`: Security log of user logins, IP addresses, user agents, and failed attempts.
    - `auth_otp_logs`: Short-lived OTP dispatch, verification attempts, and rate-limiting blocks.
  - *Priority:* **Critical** (Security compliance & brute-force defense).

### 1.7 Review of Dashboard Analytics & Performance
- **Current Design:** On-the-fly SQL count aggregation.
- **Architectural Evaluation:**
  - *Recommendation:* Introduce a pre-aggregated summary table `analytics_regional_stats` (`id`, `state_id`, `district_id`, `taluka_id`, `village_id`, `total_members`, `approved_members`, `pending_members`, `updated_at`). This table is updated asynchronously via database triggers or background jobs, allowing the Admin Dashboard to load in $<50\text{ ms}$ regardless of database size.
  - *Priority:* **Recommended** (High concurrency performance).

---

## 2. Locked Entity List & Database Schema Specification (v1.0)

### Domain 1: Authentication & Identity
1. `auth_users`: Core user login entity (`id`, `uuid`, `phone_number`, `email`, `password_hash`, `user_type`, `is_active`, `is_staff`, `created_at`, `updated_at`).
2. `auth_roles`: Administrative role definitions (`id`, `name`, `code`, `description`).
3. `auth_user_roles`: User role assignments with scope binding (`id`, `user_id`, `role_id`, `state_id`, `district_id`, `taluka_id`, `village_id`, `assigned_at`).
4. `auth_otp_logs`: OTP delivery logs (`id`, `phone_number`, `otp_code_hash`, `purpose`, `is_verified`, `attempts`, `expires_at`, `created_at`).
5. `auth_login_history`: Security audit of login attempts (`id`, `user_id`, `ip_address`, `user_agent`, `status`, `created_at`).

### Domain 2: Geographic Hierarchy & Master Data
6. `org_states`: Indian States (`id`, `name`, `code`, `is_active`).
7. `org_districts`: Districts (`id`, `state_id`, `name`, `code`, `is_active`).
8. `org_talukas`: Talukas (`id`, `district_id`, `name`, `is_active`).
9. `org_villages`: Villages (`id`, `taluka_id`, `name`, `pin_code`, `is_active`).
10. `master_designations`: Office bearer post catalog (`id`, `title`, `level_scope`, `display_order`, `is_active`).
11. `master_categories`: Shared content categories (`id`, `name`, `slug`, `type`).

### Domain 3: Member Management & Digital Identity
12. `members_member`: Primary member entity (`id`, `uuid`, `user_id`, `membership_number`, `first_name`, `last_name`, `gender`, `date_of_birth`, `state_id`, `district_id`, `taluka_id`, `village_id`, `status`, `is_deleted`, `created_at`, `updated_at`).
13. `members_profile`: Profile details (`id`, `member_id`, `photo_asset_id`, `father_husband_name`, `blood_group`, `education`, `occupation`, `address_line`, `pincode`).
14. `members_document`: Uploaded ID proof (`id`, `member_id`, `document_type`, `document_number_encrypted`, `file_asset_id`, `verification_status`).
15. `members_card`: Issued membership card (`id`, `member_id`, `card_number`, `qr_token`, `issued_at`, `expires_at`, `is_active`).
16. `members_status_history`: Approval state transition audit (`id`, `member_id`, `previous_status`, `new_status`, `changed_by_user_id`, `remarks`, `created_at`).
17. `members_transfer_request`: Member regional relocation queue (`id`, `member_id`, `from_village_id`, `to_village_id`, `status`, `requested_at`, `approved_at`, `approved_by_user_id`).

### Domain 4: Office Bearers
18. `office_bearer_assignments`: Active & historical appointments (`id`, `member_id`, `designation_id`, `hierarchy_level`, `state_id`, `district_id`, `taluka_id`, `village_id`, `start_date`, `end_date`, `is_current`).

### Domain 5: Centralized Media Management
19. `media_assets`: Centralized media catalog (`id`, `uuid`, `file_path`, `file_name`, `mime_type`, `file_size`, `created_at`).

### Domain 6: CMS & Dynamic Website
20. `cms_news`: Articles & press releases (`id`, `uuid`, `title`, `slug`, `category_id`, `content`, `cover_asset_id`, `target_scope`, `state_id`, `district_id`, `status`, `published_at`, `is_deleted`).
21. `cms_pages`: Dynamic static pages (`id`, `slug`, `title`, `content`, `meta_title`, `meta_description`, `updated_at`).
22. `cms_faqs`: Frequently Asked Questions (`id`, `question`, `answer`, `display_order`, `is_active`).
23. `cms_banners`: Homepage slider & banners (`id`, `title`, `image_asset_id`, `link_url`, `display_order`, `is_active`).

### Domain 7: Events & Meetings
24. `events_event`: Public events & rallies (`id`, `uuid`, `title`, `description`, `banner_asset_id`, `start_time`, `end_time`, `venue_address`, `map_link`, `target_scope`, `state_id`, `district_id`, `is_public`, `is_deleted`).
25. `events_rsvp`: Member attendance indication (`id`, `event_id`, `member_id`, `rsvp_status`, `created_at`).
26. `meetings_meeting`: Internal committee meetings (`id`, `uuid`, `subject`, `agenda`, `meeting_date`, `venue_or_link`, `target_role_id`, `hierarchy_level`, `created_by_user_id`).
27. `meetings_invitee`: Meeting participant invitations (`id`, `meeting_id`, `member_id`, `attendance_status`).
28. `meetings_minutes`: Post-meeting recorded notes (`id`, `meeting_id`, `minutes_text`, `attachment_asset_id`, `created_at`).

### Domain 8: Gallery
29. `gallery_albums`: Photo albums (`id`, `uuid`, `title`, `description`, `cover_asset_id`, `event_id`, `created_at`).
30. `gallery_photos`: Album photo assets (`id`, `album_id`, `media_asset_id`, `caption`, `display_order`).
31. `gallery_videos`: Video embed links (`id`, `album_id`, `title`, `video_url`, `platform`).

### Domain 9: Financial & Donations
32. `donations_donation`: Donation records & receipt verification (`id`, `uuid`, `donor_name`, `donor_phone`, `donor_email`, `amount`, `payment_reference`, `receipt_asset_id`, `verification_status`, `verified_by_user_id`, `created_at`).

### Domain 10: Communications & Notifications
33. `comm_contact_inquiries`: Public inquiries (`id`, `name`, `phone`, `email`, `subject`, `message`, `resolution_status`, `resolved_by_user_id`, `created_at`).
34. `comm_notifications`: Targeted in-app alerts (`id`, `recipient_user_id`, `title`, `message`, `link_url`, `is_read`, `created_at`).

### Domain 11: Audit, Analytics & Settings
35. `system_audit_log`: System modification log (`id`, `actor_user_id`, `ip_address`, `action_type`, `entity_name`, `entity_id`, `changes_json`, `created_at`).
36. `system_settings`: Platform operational flags (`id`, `key`, `value`, `description`, `updated_at`).
37. `cms_settings`: Website branding & contact details (`id`, `key`, `value`, `description`, `updated_at`).
38. `analytics_regional_stats`: Pre-aggregated counts (`id`, `state_id`, `district_id`, `taluka_id`, `village_id`, `total_members`, `approved_members`, `pending_members`, `updated_at`).

---

## 3. Final Database Decision

### **DECISION: APPROVED WITH CHANGES (SCHEMA LOCKED)**

**Reasoning:** The refined 38-entity relational database architecture is normalized (3NF), secure, performance-optimized, and completely locked for **BVSMS Version 1.0 (MVP)**. It cleanly supports all functional modules, RBAC administrative scoping, digital ID verification, media management, pre-aggregated dashboard performance, and audit logging.

---
*Database Architecture officially LOCKED. Ready to begin Phase 3: Backend Foundation Development.*
