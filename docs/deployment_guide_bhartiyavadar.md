# Production Deployment Guide for `bhartiyavadar.com`

This guide explains step-by-step how to deploy the **Bharatiya Vadar Sena (BVS)** web application to a live cloud server so anyone on mobile, laptop, and desktop can access it worldwide under the custom domain **`bhartiyavadar.com`**.

---

## Phase 1: Purchase Domain Name (`bhartiyavadar.com`)

1. Go to any domain registrar such as **GoDaddy**, **Hostinger**, **Namecheap**, or **Cloudflare**.
2. Search and buy the domain: **`bhartiyavadar.com`**.
3. Keep the registrar dashboard open (you will need to update DNS records in Phase 3).

---

## Phase 2: Rent a Public Cloud VPS (Server)

1. Rent a Linux Virtual Private Server (VPS) from a cloud hosting provider:
   - **Recommended Providers**: Hostinger VPS (₹400–600/month), AWS EC2 (t3.small), DigitalOcean ($6–12/month), or Hetzner.
   - **Operating System**: **Ubuntu 22.04 LTS**.
   - **Minimum Hardware Requirements**: 2 GB RAM, 1-2 vCPU, 20 GB SSD storage.
2. Note down your **Server Public IP Address** (e.g. `123.45.67.89`).

---

## Phase 3: Point Domain DNS to your Server IP

1. Open your domain control panel (GoDaddy / Hostinger / Namecheap).
2. Go to **DNS Management / DNS Records**.
3. Add/Edit the following **A Records**:

| Type | Name / Host | Value / Target (Points To) | TTL |
| :--- | :--- | :--- | :--- |
| **A Record** | `@` | `YOUR_SERVER_IP` (e.g., `123.45.67.89`) | 3600 / Automatic |
| **A Record** | `www` | `YOUR_SERVER_IP` (e.g., `123.45.67.89`) | 3600 / Automatic |

*Note: DNS propagation usually takes 5 to 15 minutes.*

---

## Phase 4: Server Initial Setup & Code Upload

Connect to your VPS via SSH from your computer terminal:
```bash
ssh root@YOUR_SERVER_IP
```

Update system packages and install Docker:
```bash
# 1. Update system
apt update && apt upgrade -y

# 2. Install Docker & Docker Compose
apt install -y docker.io docker-compose git curl certbot python3-certbot-nginx

# 3. Enable & start Docker service
systemctl enable --now docker
```

Clone your project repository onto the server:
```bash
git clone https://github.com/your-username/vadar_sena.git /var/www/vadar_sena
cd /var/www/vadar_sena
```

---

## Phase 5: Launch Production Containers

Run Docker Compose in production mode:
```bash
docker-compose -f docker-compose.prod.yml up -d --build
```

Run Django migrations and create SuperAdmin user:
```bash
# Run database migrations
docker exec -it bvsms_prod_backend python manage.py migrate

# Seed initial state/district organization data
docker exec -it bvsms_prod_backend python manage.py shell -c "from apps.organization.models import State, District; s, _ = State.objects.get_or_create(name='Maharashtra', code='MH'); District.objects.get_or_create(name='Pune', state=s); print('Seeded Maharashtra & Pune')"

# Create SuperAdmin User (Phone: 9876543210 / Password: adminpassword123)
docker exec -it bvsms_prod_backend python manage.py shell -c "from apps.authentication.models import User; u, _ = User.objects.get_or_create(phone_number='9876543210'); u.set_password('adminpassword123'); u.user_type='SUPERADMIN'; u.is_staff=True; u.is_superuser=True; u.save(); print('SuperAdmin created successfully!')"
```

---

## Phase 6: Enable Free SSL/HTTPS Certificate (Let's Encrypt)

To secure your website with HTTPS (`https://bhartiyavadar.com`):

```bash
# 1. Stop temporary Nginx port binding
docker-compose -f docker-compose.prod.yml stop frontend

# 2. Generate SSL Certificate via Certbot
certbot certonly --standalone -d bhartiyavadar.com -d www.bhartiyavadar.com

# 3. Mount SSL certs and restart containers
docker-compose -f docker-compose.prod.yml up -d
```

---

## Accessing the Live Website

- **Public Website**: `https://bhartiyavadar.com` (Accessible on mobile, laptop, and tablet worldwide)
- **Admin Control Panel**: `https://bhartiyavadar.com/login`
  - **Phone**: `9876543210`
  - **Password**: `adminpassword123`
