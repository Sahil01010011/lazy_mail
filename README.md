# 🔒 LazyMail - Advanced Email Phishing Detection System

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-009688.svg)](https://fastapi.tiangolo.com)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://www.docker.com/)

> **⚠️ Project Status: In Active Development**  
> This is an ongoing project currently implementing Layer 3 (Email Parsing). Layers 4-5 are planned for future development.

A self-hosted, containerized email security platform that detects phishing, BEC (Business Email Compromise), and spam using a multi-layer analysis pipeline. Built with FastAPI, PostgreSQL, Redis, and Rspamd for high-precision threat detection with explainable AI decisions.

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture & Layers](#architecture--layers)
- [Current Status](#current-status)
- [Features](#features)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [API Documentation](#api-documentation)
- [Development](#development)
- [Technology Stack](#technology-stack)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

LazyMail is designed to provide enterprise-grade email security for organizations without relying on expensive third-party services. It analyzes emails through multiple detection layers:

- **Authentication Verification**: SPF, DKIM, DMARC checks
- **Content Analysis**: URL extraction, HTML sanitization, threat detection
- **Behavioral Detection**: Stylometry analysis for AI-generated phishing (planned)
- **Machine Learning**: Multi-layer classification with explainable decisions (planned)
- **Automated Actions**: Quarantine, labeling, and real-time alerts (planned)

### Key Benefits

✅ **Self-Hosted**: Complete control over your data and infrastructure  
✅ **Privacy-First**: No data leaves your environment  
✅ **Explainable**: Full visibility into detection decisions  
✅ **Extensible**: Modular architecture for custom rules and integrations  
✅ **Docker-Native**: Easy deployment with Docker Compose  

## 🏗️ Architecture & Layers

LazyMail follows a layered architecture approach, building complexity incrementally:

```
┌─────────────────────────────────────────────────────────────┐
│                    Layer 5: Automation ⏳                    │
│  - Celery workers for background processing                 │
│  - Gmail/IMAP ingestion with OAuth                          │
│  - Automated policy actions (quarantine, label)             │
│  - Real-time alert system                                   │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                 Layer 4: Analysis Pipeline ⏳                │
│  - Rspamd integration for spam scoring                      │
│  - ML-based phishing classification                         │
│  - Stylometry analysis for BEC detection                    │
│  - Combined risk scoring with explainability                │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│              Layer 3: Email Parsing ✅ [CURRENT]             │
│  ✓ Complete MIME parsing (headers, body, attachments)       │
│  ✓ URL extraction and threat analysis                       │
│  ✓ Email authentication verification (SPF/DKIM/DMARC)       │
│  ✓ HTML sanitization and risk scoring                       │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                  Layer 2: API Foundation ✅                  │
│  ✓ FastAPI with automatic API documentation                 │
│  ✓ Health check endpoints (API, DB, Rspamd)                 │
│  ✓ RESTful endpoints for message management                 │
│  ✓ Dependency injection pattern                             │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                  Layer 1: Infrastructure ✅                  │
│  ✓ Docker Compose orchestration                             │
│  ✓ PostgreSQL 16 with proper schema                         │
│  ✓ Redis for caching and task queues                        │
│  ✓ Rspamd for spam detection                                │
│  ✓ Async database connections                               │
└─────────────────────────────────────────────────────────────┘
```

**Legend**: ✅ Complete | ⏳ Planned

## 📊 Current Status

### ✅ Completed Components

#### Layer 1: Infrastructure
- Docker Compose setup with PostgreSQL, Redis, and Rspamd
- Database models with Alembic migrations
- Async SQLAlchemy configuration
- Health monitoring for all services

#### Layer 2: API Foundation
- FastAPI application with OpenAPI documentation
- RESTful endpoints (`/api/v1/messages`, `/api/v1/health`)
- Automatic API docs at `/docs` and `/redoc`
- Error handling and logging middleware
- CORS configuration

#### Layer 3: Email Parsing ← **YOU ARE HERE**
- **MIME Parser**: Full email parsing with header/body/attachment extraction
- **Header Analyzer**: SPF/DKIM/DMARC verification, sender anomaly detection
- **URL Extractor**: Domain analysis, homograph detection, threat indicators
- **HTML Normalizer**: Sanitization, risk scoring, suspicious pattern detection

### 🔄 In Progress
- Testing and refining email parsing components
- Documentation and code quality improvements

### ⏳ Upcoming (Layers 4-5)
- Rspamd HTTP client integration
- Machine learning classification models
- Stylometry analysis for BEC detection
- Celery workers for async processing
- Gmail/IMAP ingestion pipelines
- Automated action system
- Web dashboard (React)

## ✨ Features

### Current Capabilities

- **Email Analysis**
  - Parse raw email (.eml) files
  - Extract headers, body (plain text and HTML), attachments metadata
  - Verify SPF, DKIM, and DMARC authentication
  - Analyze sender addresses for anomalies
  - Detect Reply-To mismatches

- **URL & Content Security**
  - Extract and analyze all URLs from email content
  - Detect URL obfuscation and suspicious patterns
  - Identify shortened URLs and redirects
  - Homograph detection (IDN homograph attacks)
  - HTML sanitization with risk scoring

- **Risk Scoring**
  - Combined risk scores from multiple sources:
    - Authentication failures (SPF/DKIM/DMARC)
    - HTML content analysis (JavaScript, iframes, forms)
    - URL reputation and patterns
    - Header anomalies
  - Scores range from 0-100 with clear contributing factors

- **API Endpoints**
  - `GET /` - API information
  - `GET /api/v1/health/all` - Check all services
  - `GET /api/v1/messages` - List analyzed messages
  - `POST /api/v1/messages/analyze` - Analyze new emails
  - Full OpenAPI documentation at `/docs`

### Planned Features (Layers 4-5)

- 🔮 **Rspamd Integration**: Professional spam filtering with rule-based scoring
- 🤖 **ML Classification**: Machine learning models for phishing detection
- 📝 **Stylometry Analysis**: Detect AI-generated and impersonation attempts
- 📧 **Email Ingestion**: Automatic Gmail and IMAP polling
- ⚡ **Real-Time Processing**: Celery-based async task queue
- 🎯 **Automated Actions**: Auto-quarantine, labeling, and alerts
- 📊 **Web Dashboard**: React-based UI for email triage and analysis
- 🔔 **Alert System**: Webhook notifications for high-risk detections

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- Python 3.11+ (for local development)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Sahil01010011/lazy_mail.git
   cd lazy_mail
   ```

2. **Create environment configuration**
   ```bash
   cat > .env << EOF
   # Database
   POSTGRES_USER=lazymail
   POSTGRES_PASSWORD=changeme_secure_password
   POSTGRES_DB=lazymail
   POSTGRES_HOST=postgres
   POSTGRES_PORT=5432

   # Redis
   REDIS_HOST=redis
   REDIS_PORT=6379
   REDIS_PASSWORD=changeme_redis_password

   # Rspamd
   RSPAMD_HOST=rspamd
   RSPAMD_PORT=11334
   RSPAMD_CONTROLLER_PASSWORD=changeme_rspamd_password
   EOF
   ```

3. **Start the services**
   ```bash
   docker-compose up -d
   ```

4. **Verify all services are running**
   ```bash
   docker-compose ps
   ```

5. **Check health status**
   ```bash
   curl http://localhost:8000/api/v1/health/all
   ```

6. **Access API documentation**
   - OpenAPI (Swagger UI): http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### Running Migrations

```bash
# Enter the API container
docker-compose exec api bash

# Run migrations
alembic upgrade head

# Exit container
exit
```

### Testing the API

```bash
# Test health endpoint
curl http://localhost:8000/api/v1/health/all | jq

# List messages (will be empty initially)
curl http://localhost:8000/api/v1/messages | jq

# Analyze an email (requires .eml file)
curl -X POST http://localhost:8000/api/v1/messages/analyze \
  -H "Content-Type: application/json" \
  -d @sample_email.json
```

## 📁 Project Structure

```
lazy_mail/
├── docker-compose.yml          # Docker orchestration
├── .env                        # Environment configuration (create from template)
├── prd.md                      # Product requirements document
├── README.md                   # This file
│
├── infra/                      # Infrastructure configuration
│   ├── postgres/
│   │   └── init.sql           # Database initialization
│   └── rspamd/
│       ├── local.d/           # Rspamd local rules
│       └── workers.d/         # Rspamd worker config
│
├── notes/                      # Development notes
│   └── backend-workflow.txt   # Build order and rationale
│
└── services/
    └── api/                    # FastAPI service
        ├── Dockerfile
        ├── requirements.txt
        ├── alembic.ini        # Database migration config
        ├── alembic/
        │   └── versions/      # Migration files
        │
        ├── app/
        │   ├── main.py        # FastAPI application entry point
        │   │
        │   ├── core/          # Core configuration
        │   │   ├── config.py  # Settings management
        │   │   └── database.py # Database connection
        │   │
        │   ├── db/            # Database layer
        │   │   ├── models/    # SQLAlchemy models
        │   │   │   ├── message.py   # Email message model
        │   │   │   ├── verdict.py   # Analysis verdict model
        │   │   │   └── feature.py   # Feature extraction model
        │   │   └── base.py    # Model imports
        │   │
        │   ├── api/           # API layer
        │   │   └── v1/
        │   │       ├── router.py        # Main API router
        │   │       ├── routers/         # Endpoint routers
        │   │       │   ├── health.py    # Health checks
        │   │       │   └── messages.py  # Message endpoints
        │   │       ├── schemas/         # Pydantic schemas
        │   │       └── dependencies/    # Route dependencies
        │   │
        │   └── parsing/       # Email parsing utilities ← CURRENT FOCUS
        │       ├── mime_parser.py       # MIME email parser
        │       ├── header_analyzer.py   # Auth & header analysis
        │       ├── url_extractor.py     # URL extraction & analysis
        │       └── html_normalizer.py   # HTML sanitization
        │
        └── tests/             # Test suite
            └── ...
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root with the following variables:

```env
# Application
APP_NAME=LazyMail Phishing Detection
DEBUG=true

# PostgreSQL Database
POSTGRES_USER=lazymail
POSTGRES_PASSWORD=your_secure_password_here
POSTGRES_DB=lazymail
POSTGRES_HOST=postgres  # Use 'localhost' for local dev
POSTGRES_PORT=5432

# Redis
REDIS_HOST=redis  # Use 'localhost' for local dev
REDIS_PORT=6379
REDIS_PASSWORD=your_redis_password

# Rspamd
RSPAMD_HOST=rspamd  # Use 'localhost' for local dev
RSPAMD_PORT=11334
RSPAMD_CONTROLLER_PASSWORD=your_rspamd_password
```

### Docker Compose Services

- **postgres** (5432): PostgreSQL 16 database
- **redis** (6379): Redis cache and task queue
- **rspamd** (11334): Spam and phishing detection engine
- **api** (8000): FastAPI application (when added to docker-compose)

### Port Mapping

| Service    | Internal Port | External Port | Purpose                  |
|------------|---------------|---------------|--------------------------|
| API        | 8000          | 8000          | REST API & Documentation |
| PostgreSQL | 5432          | 5432          | Database                 |
| Redis      | 6379          | 6379          | Cache & Queue            |
| Rspamd     | 11334         | 11334         | Spam Detection API       |

## 📚 API Documentation

### Interactive Documentation

- **Swagger UI**: http://localhost:8000/docs
  - Interactive API testing interface
  - Request/response schemas
  - Try out endpoints directly

- **ReDoc**: http://localhost:8000/redoc
  - Clean, readable API reference
  - Detailed descriptions and examples

### Key Endpoints

#### Health Checks
```
GET /api/v1/health/          # Quick API health check
GET /api/v1/health/db        # Database connectivity
GET /api/v1/health/rspamd    # Rspamd connectivity
GET /api/v1/health/all       # All services status
```

#### Messages
```
GET  /api/v1/messages        # List analyzed messages
GET  /api/v1/messages/{id}   # Get message details
POST /api/v1/messages/analyze # Analyze new email
```

### Response Format

All API responses follow a consistent format:

```json
{
  "status": "success",
  "data": { ... },
  "message": "Optional message"
}
```

Error responses:
```json
{
  "detail": "Error description",
  "error": "Additional context (debug mode only)"
}
```

## 💻 Development

### Local Development Setup

1. **Install Python dependencies**
   ```bash
   cd services/api
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Start infrastructure services**
   ```bash
   docker-compose up -d postgres redis rspamd
   ```

3. **Update `.env` for local development**
   ```env
   POSTGRES_HOST=localhost
   REDIS_HOST=localhost
   RSPAMD_HOST=localhost
   ```

4. **Run database migrations**
   ```bash
   cd services/api
   alembic upgrade head
   ```

5. **Start the API server**
   ```bash
   cd services/api
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

### Running Tests

```bash
cd services/api
pytest tests/ -v
```

With coverage:
```bash
pytest tests/ --cov=app --cov-report=html
```

### Code Quality

```bash
# Format code (if black is installed)
black app/

# Lint code (if flake8 is installed)
flake8 app/

# Type checking (if mypy is installed)
mypy app/
```

### Database Migrations

```bash
# Create a new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# View migration history
alembic history
```

### Adding New Endpoints

1. Create a new router in `app/api/v1/routers/`
2. Define Pydantic schemas in `app/api/v1/schemas/`
3. Add database models in `app/db/models/` if needed
4. Register router in `app/api/v1/router.py`

Example:
```python
# app/api/v1/routers/my_router.py
from fastapi import APIRouter, Depends

router = APIRouter(prefix="/my-endpoint", tags=["MyFeature"])

@router.get("/")
async def list_items():
    return {"items": []}
```

## 🛠️ Technology Stack

### Backend
- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) 0.115.0 - Modern async Python web framework
- **Server**: [Uvicorn](https://www.uvicorn.org/) - Lightning-fast ASGI server
- **Database**: [PostgreSQL](https://www.postgresql.org/) 16 - Robust relational database
- **ORM**: [SQLAlchemy](https://www.sqlalchemy.org/) 2.0 - Async database toolkit
- **Migrations**: [Alembic](https://alembic.sqlalchemy.org/) - Database version control
- **Validation**: [Pydantic](https://docs.pydantic.dev/) 2.9 - Data validation

### Infrastructure
- **Containerization**: [Docker](https://www.docker.com/) & Docker Compose
- **Cache/Queue**: [Redis](https://redis.io/) 7 - In-memory data store
- **Spam Filter**: [Rspamd](https://rspamd.com/) - Advanced spam filtering
- **Task Queue**: [Celery](https://docs.celeryq.dev/) 5.4 (planned for Layer 5)

### Email Processing
- **MIME Parsing**: Python `email` library
- **URL Analysis**: `tldextract` for domain extraction
- **HTML Processing**: BeautifulSoup (planned) / Custom sanitizer
- **Auth Verification**: SPF/DKIM/DMARC validation

### Development Tools
- **Testing**: pytest, pytest-asyncio
- **HTTP Client**: httpx for async requests
- **Environment**: python-dotenv for config management

## 🗺️ Roadmap

### Phase 1: Foundation (✅ Complete)
- [x] Docker infrastructure setup
- [x] Database models and migrations
- [x] FastAPI application skeleton
- [x] Health check endpoints
- [x] Basic message storage

### Phase 2: Email Parsing (✅ Complete - Current)
- [x] MIME parser implementation
- [x] Header analysis with auth verification
- [x] URL extraction and threat detection
- [x] HTML sanitization and risk scoring
- [x] Integration with message API

### Phase 3: Analysis Pipeline (⏳ Next - Layer 4)
- [ ] Rspamd HTTP client integration
- [ ] Score normalization and combination
- [ ] ML model integration framework
- [ ] Stylometry feature extraction
- [ ] Verdict generation with explanations
- [ ] IOC (Indicator of Compromise) management

### Phase 4: Automation (⏳ Planned - Layer 5)
- [ ] Celery worker setup
- [ ] Gmail API integration with OAuth
- [ ] IMAP client for generic email servers
- [ ] Automated email ingestion pipeline
- [ ] Policy engine for automated actions
- [ ] Webhook alert system

### Phase 5: Dashboard & UX (⏳ Future)
- [ ] React-based web dashboard
- [ ] Email inbox view with risk scores
- [ ] Detailed threat analysis view
- [ ] One-click labeling (phish/benign/suspicious)
- [ ] Search and filtering capabilities
- [ ] Analytics and reporting

### Phase 6: Advanced Features (🔮 Vision)
- [ ] MISP connector for threat intelligence
- [ ] Model A/B testing framework
- [ ] Kubernetes deployment manifests
- [ ] RBAC and multi-tenant support
- [ ] Audit logging and compliance
- [ ] Custom rule engine
- [ ] Browser extension for Gmail

## 📖 Documentation Resources

- **PRD**: See `prd.md` for detailed product requirements
- **Build Workflow**: See `notes/backend-workflow.txt` for development order rationale
- **API Docs**: http://localhost:8000/docs (when running)
- **Database Schema**: Check `services/api/alembic/versions/` for migrations

## 🤝 Contributing

This is an ongoing personal project, but contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make your changes**
   - Follow existing code style
   - Add tests for new functionality
   - Update documentation as needed
4. **Commit your changes**
   ```bash
   git commit -m "Add amazing feature"
   ```
5. **Push to your fork**
   ```bash
   git push origin feature/amazing-feature
   ```
6. **Open a Pull Request**

### Development Guidelines

- Write clean, readable code with docstrings
- Follow FastAPI and SQLAlchemy best practices
- Add unit tests for new features
- Update API documentation for new endpoints
- Keep dependencies minimal and justified
- Use type hints for better IDE support

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) for the excellent web framework
- [Rspamd](https://rspamd.com/) for spam detection capabilities
- [SQLAlchemy](https://www.sqlalchemy.org/) for powerful ORM functionality
- The open-source community for inspiration and tools

## 📞 Contact & Support

- **Issues**: [GitHub Issues](https://github.com/Sahil01010011/lazy_mail/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Sahil01010011/lazy_mail/discussions)

---

**⚠️ Important Security Note**: This is a development project. Before using in production:
- Change all default passwords
- Enable authentication on all endpoints
- Review and harden Rspamd configuration
- Implement rate limiting
- Add proper logging and monitoring
- Conduct security audit

---

**Built with ❤️ by Sahil** | Last Updated: October 2024
