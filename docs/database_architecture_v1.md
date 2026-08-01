# Database Architecture Specification (Phase 2)
## Bharatiya Vadar Sena Management System (BVSMS) — Version 1.0 (MVP)

---

## 1. Complete List of Entities (Tables)

### 1.1 Authentication & RBAC Domain
1. `auth_users`: Central authentication identity table.
2. `auth_roles`: Administrative role definitions (Super Admin, State Admin, District Admin, Taluka Admin, Village Admin, Approved Member).
3. `auth_user_roles`: User role assignments with regional scope boundaries.
4. `auth_otp_logs`: Mobile OTP generation, delivery verification, and rate-limiting.
5. `auth_refresh_tokens`: Session lifecycle management and token revocation.

### 1.2 Organization Hierarchy Domain
6. `org_states`: Indian State administrative units.
7. `org_districts`: District units linked to parent State.
8. `org_talukas`: Taluka / Block units linked to parent District.
9. `org_villages`: Village / Ward units linked to parent Taluka.
10. `org_designations`: Official administrative posts catalog (President, Vice President, Secretary, Youth Leader, etc.).

### 1.3 Members Domain
11. `members_member`: Primary member business entity.
12. `members_profile`: Extended personal information, address, and emergency contact details.
13. `members_document`: Identity verification proof documents (Aadhaar / Voter ID reference).
14. `members_status_history`: Historical audit trail of state transitions (PENDING $\rightarrow$ APPROVED / REJECTED / SUSPENDED).
15. `members_card`: Digital membership card records and encrypted QR verification tokens.
16. `members_transfer_request`: Member relocation and regional transfer requests.

### 1.4 Office Bearers Domain
17. `office_bearer_assignments`: Assignments of active and historical office bearer posts per administrative node.

### 1.5 CMS & Dynamic Website Domain
18. `cms_news`: News articles and press releases.
19. `cms_news_categories`: Categories for news organizing.
20. `cms_pages`: Dynamic static pages (About Us, Vision & Mission, History, Policies).
21. `cms_faqs`: Frequently Asked Questions catalog.
22. `cms_banners`: Homepage announcement tickers and carousel banners.

### 23. Events & Meetings Domain
23. `events_event`: Public organizational events, rallies, and programs.
24. `events_rsvp`: Member attendance indication / RSVP records.
25. `meetings_meeting`: Internal administrative and committee meetings.
26. `meetings_invitee`: Targeted meeting invitations and attendance tracking.
27. `meetings_minutes`: Post-meeting recorded minutes and attachments.

### 28. Gallery Domain
28. `gallery_albums`: Photo albums and media groupings.
29. `gallery_photos`: Photo image assets with resolution variants.
30. `gallery_videos`: Video embed links (YouTube/Vimeo).

### 31. Financial & Donations Domain
31. `donations_donation`: Offline donation logs and receipt verification statuses.

### 32. Communications & System Domain
32. `comm_contact_inquiries`: Public Contact Form submissions and resolution logs.
33. `comm_notifications`: Targeted in-app alerts and broadcast notifications.
34. `system_audit_log`: Administrative security and operational audit trail.
35. `system_settings`: Platform runtime configuration key-value store.

---

## 2. Relationships Mapping

```
[org_states]
  └── [org_districts] (1 : N)
       └── [org_talukas] (1 : N)
            └── [org_villages] (1 : N)
                 └── [members_member] (1 : N)
                      ├── [auth_users] (1 : 1)
                      ├── [members_profile] (1 : 1)
                      ├── [members_document] (1 : N)
                      ├── [members_card] (1 : 1)
                      ├── [members_status_history] (1 : N)
                      ├── [members_transfer_request] (1 : N)
                      └── [office_bearer_assignments] (1 : N)

[cms_news] (1 : N) ──> [cms_news_categories]
[events_event] (1 : N) ──> [events_rsvp] <── (N : 1) [members_member]
[meetings_meeting] (1 : N) ──> [meetings_invitee] <── (N : 1) [members_member]
[gallery_albums] (1 : N) ──> [gallery_photos]
[donations_donation] (N : 1) ──> [members_member (optional)]
```

---

## 3. One-to-One (1:1) Relationships
- `auth_users` $\leftrightarrow$ `members_member`: Every member profile links to exactly one user authentication record.
- `members_member` $\leftrightarrow$ `members_profile`: Every member has exactly one extended profile record.
- `members_member` $\leftrightarrow$ `members_card`: Every approved member possesses exactly one active digital membership card.

## 4. One-to-Many (1:N) Relationships
- `org_states` $\rightarrow$ `org_districts`: One State contains many Districts.
- `org_districts` $\rightarrow$ `org_talukas`: One District contains many Talukas.
- `org_talukas` $\rightarrow$ `org_villages`: One Taluka contains many Villages.
- `org_villages` $\rightarrow$ `members_member`: One Village contains many registered members.
- `members_member` $\rightarrow$ `members_status_history`: One member accumulates status transition logs over time.
- `gallery_albums` $\rightarrow$ `gallery_photos`: One album contains many photos.

## 5. Many-to-Many (N:M) Relationships
- `members_member` $\leftrightarrow$ `events_event`: Members RSVP to multiple events; resolved via `events_rsvp`.
- `members_member` $\leftrightarrow$ `meetings_meeting`: Members are invited to multiple meetings; resolved via `meetings_invitee`.
- `auth_users` $\leftrightarrow$ `auth_roles`: Users can hold administrative roles across different geographic scopes; resolved via `auth_user_roles`.

---

## 6. Data Dictionary (Key Tables)

### 6.1 Entity: `auth_users`
- **Purpose:** Primary user account authentication identity.
- **Fields:**
  - `id` (BigInt, PK, Auto-Increment)
  - `uuid` (UUID, Unique, Default: `gen_random_uuid()`)
  - `phone_number` (VarChar(15), Unique, Not Null, Validation: `/^[6-9]\d{9}$/`)
  - `email` (VarChar(254), Nullable, Validation: Email RFC 5322)
  - `password_hash` (VarChar(255), Not Null, Argon2/PBKDF2)
  - `user_type` (VarChar(20), Not Null, Default: `'MEMBER'`, Enum: MEMBER/ADMIN/SUPERADMIN)
  - `is_active` (Boolean, Not Null, Default: `true`)
  - `is_staff` (Boolean, Not Null, Default: `false`)
  - `created_at` (TimestampTZ, Not Null, Default: `CURRENT_TIMESTAMP`)
  - `updated_at` (TimestampTZ, Not Null, Default: `CURRENT_TIMESTAMP`)

### 6.2 Entity: `members_member`
- **Purpose:** Core member record linking user account to geographic hierarchy.
- **Fields:**
  - `id` (BigInt, PK, Auto-Increment)
  - `uuid` (UUID, Unique, Default: `gen_random_uuid()`)
  - `user_id` (BigInt, FK $\rightarrow$ `auth_users.id`, Unique, Not Null)
  - `membership_number` (VarChar(30), Unique, Nullable, Format: `BVS-MH-PN-001234`)
  - `first_name` (VarChar(100), Not Null, Validation: 2-100 chars)
  - `last_name` (VarChar(100), Not Null, Validation: 2-100 chars)
  - `gender` (VarChar(10), Not Null, Enum: MALE/FEMALE/OTHER)
  - `date_of_birth` (Date, Not Null, Validation: Age $\ge 18$)
  - `state_id` (SmallInt, FK $\rightarrow$ `org_states.id`, Not Null)
  - `district_id` (Integer, FK $\rightarrow$ `org_districts.id`, Not Null)
  - `taluka_id` (Integer, FK $\rightarrow$ `org_talukas.id`, Not Null)
  - `village_id` (Integer, FK $\rightarrow$ `org_villages.id`, Not Null)
  - `status` (VarChar(20), Not Null, Default: `'PENDING'`, Enum: PENDING/APPROVED/REJECTED/SUSPENDED)
  - `is_deleted` (Boolean, Not Null, Default: `false`)
  - `created_at` (TimestampTZ, Not Null, Default: `CURRENT_TIMESTAMP`)
  - `updated_at` (TimestampTZ, Not Null, Default: `CURRENT_TIMESTAMP`)

### 6.3 Entity: `members_card`
- **Purpose:** Digital membership card metadata and QR token verification.
- **Fields:**
  - `id` (BigInt, PK, Auto-Increment)
  - `member_id` (BigInt, FK $\rightarrow$ `members_member.id`, Unique, Not Null)
  - `card_number` (VarChar(40), Unique, Not Null)
  - `qr_token` (VarChar(128), Unique, Not Null)
  - `issued_at` (TimestampTZ, Not Null, Default: `CURRENT_TIMESTAMP`)
  - `expires_at` (TimestampTZ, Nullable)
  - `is_active` (Boolean, Not Null, Default: `true`)

### 6.4 Entity: `office_bearer_assignments`
- **Purpose:** Active and historical office bearer post appointments.
- **Fields:**
  - `id` (BigInt, PK, Auto-Increment)
  - `member_id` (BigInt, FK $\rightarrow$ `members_member.id`, Not Null)
  - `designation_id` (Integer, FK $\rightarrow$ `org_designations.id`, Not Null)
  - `hierarchy_level` (VarChar(20), Not Null, Enum: STATE/DISTRICT/TALUKA/VILLAGE)
  - `state_id` (SmallInt, FK $\rightarrow$ `org_states.id`, Nullable)
  - `district_id` (Integer, FK $\rightarrow$ `org_districts.id`, Nullable)
  - `taluka_id` (Integer, FK $\rightarrow$ `org_talukas.id`, Nullable)
  - `village_id` (Integer, FK $\rightarrow$ `org_villages.id`, Nullable)
  - `start_date` (Date, Not Null)
  - `end_date` (Date, Nullable)
  - `is_current` (Boolean, Not Null, Default: `true`)

---

## 7. Index Strategy
- `auth_users`: Unique Index on `phone_number`.
- `members_member`: Composite Index on `(state_id, district_id, taluka_id, village_id, status)` for fast regional admin filtering. Full-text search index on `(first_name, last_name, phone_number)`.
- `office_bearer_assignments`: Composite Index on `(hierarchy_level, state_id, district_id, taluka_id, village_id, is_current)`.
- `cms_news`: Composite Index on `(status, published_at DESC)`.

---

## 8. Soft Delete Strategy
- Table entities (`members_member`, `cms_news`, `events_event`, `donations_donation`) include `is_deleted` (Boolean, default `false`) and `deleted_at` (TimestampTZ, nullable).
- API selectors explicitly filter `is_deleted=false`. Hard deletes are forbidden via API endpoints.

---

## 9. Audit Fields
- All operational tables contain `created_at` (TimestampTZ) and `updated_at` (TimestampTZ).
- Data modification tables contain `created_by_id` (FK $\rightarrow$ `auth_users.id`) and `updated_by_id` (FK $\rightarrow$ `auth_users.id`).
- All administrative transactions recorded in `system_audit_log` with `actor_id`, `ip_address`, `action_type`, `entity_name`, `entity_id`, and `changes_json`.

---

## 10. Future Expansion Strategy (v2.0 Preparedness)
- Payment Gateway support embedded in `donations_donation` (`gateway_name`, `transaction_ref`, `payment_mode`).
- Multi-language dynamic CMS support prepared via JSONB field structures.
- Background worker push/SMS alert queues enabled via dispatch status flags on `comm_notifications`.

---

## Quality Review Verification
- **Zero Circular Dependencies:** Top-down hierarchy (`State` $\rightarrow$ `District` $\rightarrow$ `Taluka` $\rightarrow$ `Village` $\rightarrow$ `Member`).
- **3NF Normalization:** Zero redundant geographic strings stored in member records; all geographic data joined via indexed foreign keys.
- **Data Integrity Constraints:** Foreign key cascading behavior set to `ON DELETE PROTECT` for structural records.

---
*Phase 2 Database Design Specification complete.*
