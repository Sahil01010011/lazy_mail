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

#### 🔍 **Complete Email Parsing (Layer 3)**

- **MIME Parser** (`mime_parser.py`)
  - Full RFC 5322 compliant email parsing
  - Header extraction with proper encoding handling
  - Multi-part message support (text/html/mixed)
  - Attachment metadata extraction (names, types, counts)
  - Body extraction (plain text and HTML versions)
  - Date and identifier parsing

- **Header Analyzer** (`header_analyzer.py`)
  - **Authentication Verification**:
    - SPF (Sender Policy Framework) check
    - DKIM (DomainKeys Identified Mail) validation
    - DMARC (Domain-based Message Authentication) verification
  - **Anomaly Detection**:
    - Display name spoofing detection
    - Reply-To address mismatch detection
    - Sender domain analysis
    - Email hop counting via Received headers
  - **Risk Scoring**: 0-100 scale based on auth failures and anomalies

- **URL Extractor** (`url_extractor.py`)
  - Comprehensive URL extraction from text and HTML
  - **Threat Analysis**:
    - URL shortener detection (bit.ly, tinyurl, etc.)
    - Suspicious TLD identification (tk, ml, xyz, etc.)
    - Homograph attack detection (IDN/Unicode lookalikes)
    - Domain reputation checks
  - **Pattern Detection**:
    - Obfuscated URLs
    - Typosquatting attempts
    - Multiple redirects
  - Unique domain counting and analysis

- **HTML Normalizer** (`html_normalizer.py`)
  - Safe HTML parsing with BeautifulSoup4
  - **Security Sanitization**:
    - JavaScript removal
    - Iframe detection and removal
    - Form element identification
    - Dangerous object/embed removal
  - **Content Analysis**:
    - Text extraction from HTML
    - HTML-to-text ratio calculation
    - Urgent language detection (urgent, immediate, act now, etc.)
    - Financial term identification (payment, bank, account, etc.)
    - Personal info request detection (password, SSN, credit card, etc.)
  - **Risk Scoring**: Weighted scoring based on suspicious elements

#### 🗄️ **Robust Database Schema**

- **Messages Table** - Stores complete email data:
  - Email identifiers (Message-ID, account)
  - Full headers as JSON
  - Body content (text and HTML)
  - Attachment metadata
  - Authentication results (SPF/DKIM/DMARC)
  - Analysis status tracking
  - Timestamps (received, ingested, analyzed)

- **Verdicts Table** - Analysis results and decisions:
  - Classification (phishing, spam, clean, suspicious, BEC)
  - Confidence scores (0-1) and risk scores (0-100)
  - Rspamd integration results
  - Component scores (auth, URL, content, stylometry)
  - Detailed explanations and threat indicators
  - Action tracking (quarantine, label, alert)
  - Analyst feedback support

- **Features Table** - ML-ready feature extraction:
  - URL metrics (count, domains, suspicious TLDs, shorteners, homographs)
  - Content metrics (length, HTML ratio, JavaScript/iframe/form flags)
  - Lexical features (urgent words, financial terms, info requests)
  - Stylometric features (avg word length, sentence count, punctuation)
  - Header anomalies (display name mismatch, reply-to mismatch, hops)
  - Feature vectors for ML models

#### 🧪 **Comprehensive Testing Suite**

All parsing components include extensive test coverage:
- `test_mime_parser.py` - Email parsing validation
- `test_header_analyzer.py` - Authentication and anomaly tests
- `test_url_extractor.py` - URL threat detection tests
- `test_html_normalizer.py` - HTML sanitization tests
- `test_integration_parsing.py` - End-to-end parsing tests
- `test_email_analyzer.py` - Complete analysis pipeline tests
- `test_crud.py` - Database CRUD operations

#### 🚀 **RESTful API**

- **Health Endpoints**:
  - `GET /` - API information
  - `GET /api/v1/health/` - Quick API health check
  - `GET /api/v1/health/db` - Database connectivity check
  - `GET /api/v1/health/rspamd` - Rspamd service check
  - `GET /api/v1/health/all` - All services status

- **Message Endpoints**:
  - `GET /api/v1/messages` - List analyzed messages (paginated)
    - Supports filtering by `status` (pending, analyzing, completed, failed)
    - Pagination with `page` and `page_size` parameters
  - `GET /api/v1/messages/{id}` - Get message details with full analysis
  - `POST /api/v1/messages/analyze` - Analyze new email (Layer 4 integration ready)

- **Interactive Documentation**:
  - Swagger UI at `/docs` - Try endpoints live
  - ReDoc at `/redoc` - Clean API reference

#### 📊 **Analysis Pipeline**

- **EmailAnalyzer** (`email_analyzer.py`) - Orchestrates all analysis layers:
  1. MIME parsing for structure extraction
  2. Header analysis for authentication
  3. URL extraction and threat detection
  4. HTML normalization and risk scoring
  5. Rspamd integration (when available)
  6. Combined risk calculation
  7. Final classification

- **AnalysisService** (`analysis_service.py`) - Database integration:
  - Coordinates analysis execution
  - Stores messages, verdicts, and features
  - Maintains analysis state
  - Provides transaction management

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

# List messages with pagination
curl "http://localhost:8000/api/v1/messages?page=1&page_size=10" | jq

# Filter messages by status
curl "http://localhost:8000/api/v1/messages?status=completed" | jq

# Get specific message
curl http://localhost:8000/api/v1/messages/{message-uuid} | jq

# Analyze an email (requires .eml file)
curl -X POST http://localhost:8000/api/v1/messages/analyze \
  -H "Content-Type: application/json" \
  -d @sample_email.json
```

### Using Parsing Components

The parsing components can be used independently or together:

```python
from app.parsing.mime_parser import MIMEParser
from app.parsing.header_analyzer import HeaderAnalyzer
from app.parsing.url_extractor import URLExtractor
from app.parsing.html_normalizer import HTMLNormalizer

# Parse an email
with open('email.eml', 'rb') as f:
    raw_email = f.read()

# 1. Parse MIME structure
parser = MIMEParser(raw_email)
email_data = parser.to_dict()
print(f"Subject: {email_data['subject']}")
print(f"From: {email_data['sender']}")
print(f"Attachments: {email_data['attachment_count']}")

# 2. Analyze headers for authentication
analyzer = HeaderAnalyzer(email_data['headers'])
auth_analysis = analyzer.get_analysis()
print(f"SPF: {auth_analysis['spf']['result']}")
print(f"DKIM: {auth_analysis['dkim']['result']}")
print(f"DMARC: {auth_analysis['dmarc']['result']}")
print(f"Risk Score: {analyzer.get_risk_score()}")

# 3. Extract and analyze URLs
url_extractor = URLExtractor(email_data['body_text'], email_data['body_html'])
url_data = url_extractor.to_dict()
print(f"URLs found: {url_data['url_count']}")
print(f"Suspicious URLs: {url_data['suspicious_url_count']}")
print(f"Homograph attacks: {url_data['homograph_count']}")

# 4. Normalize and analyze HTML
html_normalizer = HTMLNormalizer(email_data['body_html'])
html_data = html_normalizer.to_dict()
print(f"Clean text: {html_data['clean_text'][:100]}...")
print(f"Has JavaScript: {html_data['analysis']['has_javascript']}")
print(f"Risk Score: {html_normalizer.get_risk_score()}")
```

### Complete Analysis Example

```python
from app.analysis.email_analyzer import EmailAnalyzer

# Initialize analyzer
analyzer = EmailAnalyzer()

# Analyze email
with open('suspicious_email.eml', 'rb') as f:
    raw_email = f.read()

# Get complete analysis
analysis = await analyzer.analyze(raw_email)

# Access results
print(f"Classification: {analysis['verdict']['classification']}")
print(f"Confidence: {analysis['verdict']['confidence']}")
print(f"Risk Score: {analysis['verdict']['risk_score']}")
print(f"Explanation: {analysis['verdict']['explanation']}")

# Component scores
print(f"Header Risk: {analysis['analysis']['header']['risk_score']}")
print(f"URL Risk: {analysis['analysis']['url']['suspicious_url_count']}")
print(f"HTML Risk: {analysis['analysis']['html']['risk_score']}")
print(f"Rspamd Score: {analysis['analysis']['rspamd']['score']}")
```

### Database Integration Example

```python
from app.services.analysis_service import AnalysisService
from app.core.database import AsyncSessionLocal

# Initialize service
service = AnalysisService()

# Analyze and store
async with AsyncSessionLocal() as db:
    with open('email.eml', 'rb') as f:
        raw_email = f.read()
    
    result = await service.analyze_and_store(
        db=db,
        raw_email=raw_email,
        source="manual_upload"
    )
    
    print(f"Message ID: {result['message_id']}")
    print(f"Verdict ID: {result['verdict_id']}")
    print(f"Classification: {result['analysis']['verdict']['classification']}")
```

## 📁 Project Structure

```
lazy_mail/
├── docker-compose.yml          # Docker orchestration
├── .env                        # Environment configuration (create from template)
├── .env.example                # Environment template
├── quickstart.sh               # Automated setup script
├── CHANGELOG.md                # Version history and changes
├── CONTRIBUTING.md             # Contribution guidelines
├── LICENSE                     # MIT License
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
        ├── requirements.txt   # Python dependencies
        ├── pytest.ini         # Pytest configuration
        ├── alembic.ini        # Database migration config
        ├── test_crud.py       # CRUD operation tests
        │
        ├── alembic/
        │   └── versions/      # Migration files
        │       └── e16e0688ed64_initial_schema.py  # Initial schema
        │
        ├── app/
        │   ├── main.py        # FastAPI application entry point
        │   │
        │   ├── core/          # Core configuration
        │   │   ├── config.py  # Settings management (Pydantic)
        │   │   └── database.py # Async SQLAlchemy connection
        │   │
        │   ├── db/            # Database layer
        │   │   ├── models/    # SQLAlchemy models
        │   │   │   ├── message.py   # Email storage (headers, body, auth)
        │   │   │   ├── verdict.py   # Analysis results & risk scores
        │   │   │   └── feature.py   # Extracted features for ML
        │   │   └── base.py    # Model imports & Base
        │   │
        │   ├── api/           # API layer (v1)
        │   │   └── v1/
        │   │       ├── router.py        # Main API router
        │   │       ├── routers/         # Endpoint routers
        │   │       │   ├── health.py    # Health checks (API/DB/Rspamd)
        │   │       │   └── messages.py  # Message CRUD & listing
        │   │       ├── schemas/         # Pydantic request/response schemas
        │   │       │   └── message.py   # Message schemas
        │   │       └── dependencies/    # Route dependencies
        │   │           └── db.py        # Database session injection
        │   │
        │   ├── parsing/       # Email parsing utilities ✅ COMPLETE
        │   │   ├── mime_parser.py       # RFC 5322 MIME parser
        │   │   ├── header_analyzer.py   # SPF/DKIM/DMARC + anomaly detection
        │   │   ├── url_extractor.py     # URL extraction + threat analysis
        │   │   └── html_normalizer.py   # HTML sanitization + risk scoring
        │   │
        │   ├── analysis/      # Analysis orchestration
        │   │   └── email_analyzer.py    # Complete email analysis pipeline
        │   │
        │   ├── services/      # Business logic services
        │   │   └── analysis_service.py  # Analysis + DB coordination
        │   │
        │   └── integrations/  # External service integrations
        │       └── rspamd_client.py     # Rspamd HTTP client
        │
        └── tests/             # Comprehensive test suite
            ├── conftest.py              # Pytest fixtures
            ├── test_mime_parser.py      # MIME parsing tests
            ├── test_header_analyzer.py  # Authentication & header tests
            ├── test_url_extractor.py    # URL extraction tests
            ├── test_html_normalizer.py  # HTML sanitization tests
            ├── test_email_analyzer.py   # Complete analysis tests
            ├── test_analysis_service.py # Service layer tests
            ├── test_integration_parsing.py # End-to-end parsing tests
            └── test_rspamd_client.py    # Rspamd integration tests
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

### Database Schema Overview

#### Messages Table
Stores complete email data with metadata:
```python
- id: UUID (PK)
- message_id: String (Unique, Indexed) - RFC 5322 Message-ID
- account_id: String (Indexed) - Gmail/IMAP account identifier
- subject: Text - Email subject line
- sender: String (Indexed) - From address
- recipients: JSON - List of To addresses
- cc, bcc: JSON - Carbon copy recipients
- reply_to: String - Reply-To address
- body_text: Text - Plain text body
- body_html: Text - HTML body
- headers: JSON - All email headers
- has_attachments: Boolean
- attachment_count: Integer
- attachment_names: JSON - List of filenames
- spf_result, dkim_result, dmarc_result: String - Auth results
- received_date: DateTime (TZ-aware)
- ingested_at: DateTime (TZ-aware, auto)
- analyzed_at: DateTime (TZ-aware)
- analysis_status: String (Indexed) - pending|analyzing|completed|failed
```

#### Verdicts Table
Stores analysis results and risk assessments:
```python
- id: UUID (PK)
- message_id: UUID (FK, Indexed) → messages.id
- classification: String (Indexed) - phishing|spam|clean|suspicious|bec
- confidence: Float - 0.0 to 1.0
- risk_score: Float (Indexed) - 0 to 100
- rspamd_score: Float
- rspamd_action: String - reject|rewrite_subject|add_header|no_action
- rspamd_symbols: JSON - List of triggered rules
- auth_score: Float - SPF/DKIM/DMARC component
- url_score: Float - URL analysis component
- content_score: Float - Content analysis component
- stylometry_score: Float - Writing style component
- explanation: JSON - List of reasons for verdict
- threat_indicators: JSON - Specific IOCs found
- action_taken: String - quarantine|label|alert|none
- action_timestamp: DateTime
- analyst_label: String - Human feedback
- analyst_notes: Text
- created_at, updated_at: DateTime (auto)
```

#### Features Table
Stores extracted features for ML models:
```python
- id: UUID (PK)
- message_id: UUID (FK, Unique) → messages.id
# URL Features
- url_count, unique_domains: Integer
- suspicious_tlds, url_shorteners, homograph_count: Integer
- extracted_urls: JSON
# Content Features
- body_length: Integer
- html_to_text_ratio: Float
- has_javascript, has_iframes, has_forms: Integer (0/1)
# Lexical Features
- urgent_words, financial_terms, personal_info_requests: Integer
# Stylometric Features
- avg_word_length: Float
- sentence_count, exclamation_count, question_count: Integer
# Header Anomalies
- display_name_mismatch, reply_to_mismatch: Integer (0/1)
- received_hops: Integer
# ML Support
- feature_vector: JSON - Raw feature array
- extracted_at: DateTime (auto)
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
  - Request/response schemas with examples
  - Try out endpoints directly in browser
  - Full parameter documentation

- **ReDoc**: http://localhost:8000/redoc
  - Clean, readable API reference
  - Detailed descriptions and examples
  - Organized by tags and endpoints

### Key Endpoints

#### Root & Information
```
GET /                         # API information and available endpoints
```

#### Health Checks
```
GET /api/v1/health/          # Quick API health check
GET /api/v1/health/db        # Database connectivity test
GET /api/v1/health/rspamd    # Rspamd service connectivity test
GET /api/v1/health/all       # Comprehensive health check (all services)
```

**Example Response** (`/api/v1/health/all`):
```json
{
  "status": "healthy",
  "services": {
    "api": {"status": "healthy"},
    "database": {"status": "healthy"},
    "rspamd": {"status": "healthy"}
  }
}
```

#### Messages
```
GET  /api/v1/messages        # List analyzed messages (paginated)
  Query parameters:
    - page: int (default: 1) - Page number
    - page_size: int (default: 20, max: 100) - Items per page
    - status: str - Filter by analysis_status (pending|analyzing|completed|failed)

GET  /api/v1/messages/{id}   # Get message details with full analysis
  Path parameters:
    - id: UUID - Message ID

POST /api/v1/messages/analyze # Analyze new email (Layer 4 integration ready)
  Request body:
    - raw_email: bytes - Raw email content
```

**Example Response** (`GET /api/v1/messages`):
```json
{
  "messages": [
    {
      "id": "uuid",
      "message_id": "msg@example.com",
      "subject": "Important Update",
      "sender": "sender@example.com",
      "recipients": ["user@example.com"],
      "spf_result": "pass",
      "dkim_result": "pass",
      "dmarc_result": "pass",
      "analysis_status": "completed",
      "ingested_at": "2025-01-15T10:30:00Z",
      "analyzed_at": "2025-01-15T10:30:05Z"
    }
  ],
  "total": 150,
  "page": 1,
  "page_size": 20,
  "pages": 8
}
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

The project includes a comprehensive test suite covering all parsing and analysis components:

```bash
cd services/api

# Run all tests
pytest tests/ -v

# Run specific test modules
pytest tests/test_mime_parser.py -v          # MIME parsing tests
pytest tests/test_header_analyzer.py -v      # Authentication & header tests
pytest tests/test_url_extractor.py -v        # URL extraction tests
pytest tests/test_html_normalizer.py -v      # HTML sanitization tests
pytest tests/test_email_analyzer.py -v       # Complete analysis pipeline
pytest tests/test_integration_parsing.py -v  # End-to-end integration tests

# Run with detailed output
pytest tests/ -vv --tb=short

# Run with coverage report
pytest tests/ --cov=app --cov-report=html --cov-report=term

# Run specific test function
pytest tests/test_header_analyzer.py::test_authentication_checks -v
```

**Test Coverage Highlights**:
- ✅ MIME parsing with various email formats
- ✅ SPF/DKIM/DMARC authentication checks
- ✅ Display name spoofing detection
- ✅ URL extraction and homograph detection
- ✅ HTML sanitization and risk scoring
- ✅ Complete email analysis pipeline
- ✅ Database CRUD operations

**Running Manual CRUD Tests**:
```bash
cd services/api
python test_crud.py
```

This demonstrates creating messages and verdicts with full relationship support.

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

The project uses Alembic for database schema versioning:

```bash
# View current migration status
alembic current

# View migration history
alembic history --verbose

# Create a new migration (after model changes)
alembic revision --autogenerate -m "Description of changes"

# Apply migrations (upgrade to latest)
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# Rollback to specific version
alembic downgrade <revision_id>

# View SQL without applying (dry run)
alembic upgrade head --sql
```

**Current Schema** (v1 - Initial):
- ✅ `messages` table - Complete email storage
- ✅ `verdicts` table - Analysis results and risk scores
- ✅ `features` table - Extracted features for ML
- ✅ Foreign key relationships with CASCADE delete
- ✅ Indexes on frequently queried columns

**Schema Features**:
- UUID primary keys for all tables
- JSON columns for flexible data (headers, features, explanations)
- Proper timezone-aware datetime handling
- Automatic timestamp management (server defaults)
- Indexed columns for query performance
- Cascading deletes for referential integrity

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
- **ORM**: [SQLAlchemy](https://www.sqlalchemy.org/) 2.0 - Async database toolkit with full ORM support
- **Migrations**: [Alembic](https://alembic.sqlalchemy.org/) 1.13 - Database version control
- **Validation**: [Pydantic](https://docs.pydantic.dev/) 2.9 - Data validation and settings
- **Config**: [Pydantic Settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/) 2.5 - Settings management

### Infrastructure
- **Containerization**: [Docker](https://www.docker.com/) & Docker Compose - Container orchestration
- **Cache/Queue**: [Redis](https://redis.io/) 7 - In-memory data store
- **Spam Filter**: [Rspamd](https://rspamd.com/) - Advanced spam filtering engine
- **Task Queue**: [Celery](https://docs.celeryq.dev/) 5.4 (planned for Layer 5)
- **Database Driver**: [asyncpg](https://github.com/MagicStack/asyncpg) 0.29 - Fast PostgreSQL driver

### Email Processing & Analysis
- **MIME Parsing**: Python `email` library (RFC 5322 compliant)
- **HTML Processing**: [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/) - HTML parsing and sanitization
- **URL Analysis**: [tldextract](https://github.com/john-kurkowski/tldextract) - Domain extraction and TLD parsing
- **Auth Verification**: Custom SPF/DKIM/DMARC validation
- **Pattern Matching**: Python `re` (regex) for threat pattern detection

### Development & Testing
- **Testing Framework**: [pytest](https://pytest.org/) 8.3 - Powerful testing framework
- **Async Testing**: [pytest-asyncio](https://pytest-asyncio.readthedocs.io/) 0.24 - Async test support
- **HTTP Client**: [httpx](https://www.python-httpx.org/) 0.27 - Async HTTP requests
- **Environment**: [python-dotenv](https://github.com/theskumar/python-dotenv) 1.0 - Environment variable management
- **Database Testing**: SQLAlchemy with async session fixtures

### Code Quality (Optional)
- **Formatting**: [black](https://black.readthedocs.io/) - Opinionated code formatter
- **Linting**: [flake8](https://flake8.pycqa.org/) - Style guide enforcement
- **Type Checking**: [mypy](https://mypy-lang.org/) - Static type checker

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

### Project Documentation

- **README.md** (this file) - Complete project overview and setup guide
- **CHANGELOG.md** - Version history and detailed change log
- **CONTRIBUTING.md** - Contribution guidelines and development workflow
- **LICENSE** - MIT License terms
- **PRD** (if available) - Product requirements document

### API Documentation

- **OpenAPI (Swagger UI)**: http://localhost:8000/docs
  - Interactive API documentation
  - Try endpoints in real-time
  - View request/response schemas
  
- **ReDoc**: http://localhost:8000/redoc
  - Alternative API documentation
  - Clean, organized layout
  - Better for reference

### Database Documentation

- **Schema Migrations**: `services/api/alembic/versions/`
  - `e16e0688ed64_initial_schema.py` - Initial schema with all tables
  
- **Model Definitions**: `services/api/app/db/models/`
  - `message.py` - Email storage model
  - `verdict.py` - Analysis results model
  - `feature.py` - Feature extraction model

### Code Documentation

All major components include comprehensive docstrings:

- **Parsing Components**:
  - `MIMEParser` - RFC 5322 email parsing
  - `HeaderAnalyzer` - Authentication and anomaly detection
  - `URLExtractor` - URL extraction and threat analysis
  - `HTMLNormalizer` - HTML sanitization and scoring

- **Analysis Components**:
  - `EmailAnalyzer` - Complete analysis orchestration
  - `AnalysisService` - Database integration service
  - `RspamdClient` - Rspamd HTTP client

### Developer Notes

- **Build Workflow**: `notes/backend-workflow.txt`
  - Explains the layer-by-layer build approach
  - Rationale for technology choices
  - Development order and dependencies

### External Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy 2.0 Documentation](https://docs.sqlalchemy.org/en/20/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Rspamd Documentation](https://rspamd.com/doc/)
- [RFC 5322 - Internet Message Format](https://tools.ietf.org/html/rfc5322)

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

#### Code Organization

The project follows a clear layered architecture:

1. **Models Layer** (`app/db/models/`): SQLAlchemy ORM models
2. **Parsing Layer** (`app/parsing/`): Email parsing and feature extraction
3. **Analysis Layer** (`app/analysis/`): Multi-component analysis orchestration
4. **Service Layer** (`app/services/`): Business logic and database coordination
5. **API Layer** (`app/api/v1/`): RESTful endpoints and request handling
6. **Integration Layer** (`app/integrations/`): External service clients

#### Best Practices

- **Type Hints**: Use Python type hints for all function signatures
- **Async/Await**: Use async patterns for I/O operations (DB, HTTP)
- **Docstrings**: Write clear docstrings for classes and public methods
- **Error Handling**: Use try-except with proper logging
- **Testing**: Write tests for all new features and bug fixes
- **Logging**: Use the `logging` module, not print statements
- **Pydantic**: Use Pydantic models for data validation
- **DRY Principle**: Avoid code duplication, create reusable utilities

#### Adding New Features

**Example: Adding a New Parser Component**

1. **Create the parser** in `app/parsing/`:
   ```python
   # app/parsing/my_parser.py
   class MyParser:
       def __init__(self, data: str):
           self.data = data
       
       def parse(self) -> Dict[str, Any]:
           """Parse and return structured data."""
           return {"parsed": True}
       
       def to_dict(self) -> Dict[str, Any]:
           """Export as dictionary."""
           return self.parse()
   ```

2. **Write tests** in `tests/`:
   ```python
   # tests/test_my_parser.py
   from app.parsing.my_parser import MyParser
   
   def test_my_parser():
       parser = MyParser("test data")
       result = parser.parse()
       assert result["parsed"] is True
   ```

3. **Integrate into EmailAnalyzer** in `app/analysis/email_analyzer.py`:
   ```python
   from app.parsing.my_parser import MyParser
   
   async def analyze(self, raw_email: bytes):
       # ... existing parsing ...
       my_parser = MyParser(data)
       my_results = my_parser.to_dict()
       # Include in analysis results
   ```

4. **Update database models** if needed in `app/db/models/`

5. **Create migration** if schema changed:
   ```bash
   alembic revision --autogenerate -m "Add my_parser fields"
   alembic upgrade head
   ```

**Example: Adding a New API Endpoint**

1. **Create router** in `app/api/v1/routers/`:
   ```python
   # app/api/v1/routers/my_endpoint.py
   from fastapi import APIRouter, Depends
   from sqlalchemy.ext.asyncio import AsyncSession
   from app.api.v1.dependencies.db import get_db
   
   router = APIRouter(prefix="/my-endpoint", tags=["MyFeature"])
   
   @router.get("/")
   async def list_items(db: AsyncSession = Depends(get_db)):
       """List all items."""
       return {"items": []}
   ```

2. **Define schemas** in `app/api/v1/schemas/`:
   ```python
   # app/api/v1/schemas/my_schema.py
   from pydantic import BaseModel
   from typing import List
   
   class ItemResponse(BaseModel):
       id: str
       name: str
       
       class Config:
           from_attributes = True
   ```

3. **Register router** in `app/api/v1/router.py`:
   ```python
   from app.api.v1.routers import my_endpoint
   
   api_router.include_router(my_endpoint.router)
   ```

4. **Test the endpoint**:
   ```bash
   # Start server
   uvicorn app.main:app --reload
   
   # Test with curl
   curl http://localhost:8000/api/v1/my-endpoint/
   
   # Check docs
   open http://localhost:8000/docs
   ```

#### Code Quality Tools

```bash
# Format code with black
black app/ tests/

# Check style with flake8
flake8 app/ tests/ --max-line-length=120

# Type check with mypy
mypy app/ --ignore-missing-imports

# Run all checks
black app/ && flake8 app/ && mypy app/ && pytest tests/
```

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
- **Documentation**: This README and inline code documentation

## 🐛 Troubleshooting

### Common Issues

**Database Connection Errors**
```bash
# Check if PostgreSQL is running
docker-compose ps postgres

# View PostgreSQL logs
docker-compose logs postgres

# Restart PostgreSQL
docker-compose restart postgres

# Test connection manually
docker-compose exec postgres psql -U lazymail -d lazymail
```

**Migration Issues**
```bash
# Check current migration version
alembic current

# View pending migrations
alembic heads

# Stamp database to specific version (if needed)
alembic stamp head

# Downgrade and reapply
alembic downgrade -1
alembic upgrade head
```

**API Not Starting**
```bash
# Check if port 8000 is already in use
lsof -i :8000

# View API logs
docker-compose logs api

# Check environment variables
cd services/api && python -c "from app.core.config import settings; print(settings.POSTGRES_HOST)"

# Start in debug mode
cd services/api && uvicorn app.main:app --reload --log-level debug
```

**Tests Failing**
```bash
# Clear pytest cache
pytest --cache-clear

# Run tests with verbose output
pytest tests/ -vv --tb=long

# Run single test for debugging
pytest tests/test_mime_parser.py::test_basic_parsing -vv

# Check test dependencies
pip list | grep pytest
```

**Import Errors**
```bash
# Ensure you're in the right directory
cd services/api

# Check Python path
python -c "import sys; print(sys.path)"

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Verify installation
python -c "from app.parsing.mime_parser import MIMEParser; print('OK')"
```

### Performance Tips

- Use connection pooling for database (already configured)
- Enable Redis caching for repeated queries
- Use pagination for large result sets
- Index frequently queried columns (already done)
- Monitor slow queries with PostgreSQL logs
- Use async/await patterns consistently

### Getting Help

1. Check this README and CONTRIBUTING.md
2. Search existing GitHub Issues
3. Review test files for usage examples
4. Check API docs at `/docs` when server is running
5. Open a new GitHub Issue with:
   - Clear problem description
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details (OS, Python version, Docker version)
   - Relevant logs

---

**⚠️ Important Security Note**: This is a development project. Before using in production:
- Change all default passwords in `.env`
- Enable authentication on all endpoints
- Review and harden Rspamd configuration
- Implement rate limiting and request validation
- Add comprehensive logging and monitoring
- Conduct thorough security audit
- Review OWASP security guidelines
- Implement proper secret management

---

**Built with ❤️ by Sahil** | [GitHub](https://github.com/Sahil01010011/lazy_mail) | Last Updated: January 2025 | Version: 0.3.0
