# Bharatiya Vadar Sena Management System (BVSMS)

Enterprise-grade Full Stack Web Application for **Bharatiya Vadar Sena**.

## Technology Stack

### Backend
- **Framework:** Python 3.11+ / Django 5.x / Django REST Framework
- **Database:** PostgreSQL 15+
- **Auth:** JWT (SimpleJWT) + SMS OTP Ready
- **Architecture:** Clean Architecture (Services, Selectors, Serializers)

### Frontend
- **Framework:** React 18 / TypeScript / Vite
- **Styling:** Tailwind CSS
- **State & Data Fetching:** TanStack Query (React Query) + Axios
- **Form Management:** React Hook Form + Zod validation

### Infrastructure
- **Containerization:** Docker & Docker Compose
- **Web Server:** Nginx + Gunicorn

---

## Directory Structure

```
vadar_sena/
├── backend/          # Django REST Framework API application
├── frontend/         # React + TypeScript + Vite SPA
├── docs/             # Project documentation & specs
├── docker/           # Containerization configuration
├── scripts/          # Automation & seed scripts
├── database/         # Database migration & schema files
├── api/              # API specifications & OpenAPI schema
└── .github/          # GitHub Workflows & CI/CD templates
```

---

## Quick Start (Development)

### Prerequisites
- Docker & Docker Compose
- Node.js 18+ (for local frontend dev)
- Python 3.11+ (for local backend dev)

### Setup & Run
1. Copy environment variables:
   ```bash
   cp backend/.env.example backend/.env
   ```
2. Launch containers:
   ```bash
   docker-compose up --build
   ```
3. Backend running at: `http://localhost:8000`
4. Frontend running at: `http://localhost:5173`
