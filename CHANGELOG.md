# Changelog

All notable changes to LazyMail will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Layer 3: Email Parsing (Current Focus)
- Complete MIME email parsing
- Header analysis with SPF/DKIM/DMARC verification
- URL extraction and threat detection
- HTML sanitization and risk scoring

## [0.3.0] - 2024-10-05

### Added - Layer 3: Email Parsing
- MIME parser for email headers, body, and attachments
- Header analyzer for authentication verification (SPF, DKIM, DMARC)
- URL extractor with threat analysis and homograph detection
- HTML normalizer with sanitization and risk scoring
- Risk scoring system for emails based on multiple factors

### Documentation
- Comprehensive README.md with architecture overview
- CONTRIBUTING.md with development guidelines
- .env.example template for configuration
- quickstart.sh script for automated setup
- MIT LICENSE added

## [0.2.0] - 2024-10-04

### Added - Layer 2: API Foundation
- FastAPI application with auto-generated documentation
- Health check endpoints for all services
- RESTful API structure with versioning
- Message management endpoints
- Dependency injection pattern implementation
- CORS middleware configuration
- Global exception handling
- Logging configuration

### Database
- Message model for email storage
- Verdict model for analysis results
- Feature model for extracted features
- Alembic migrations system

## [0.1.0] - 2024-10-03

### Added - Layer 1: Infrastructure
- Docker Compose orchestration
- PostgreSQL 16 database setup
- Redis 7 for caching and queues
- Rspamd integration for spam detection
- Environment configuration management
- Async SQLAlchemy database connections
- Health monitoring system

### Project Structure
- Initial project scaffolding
- Product requirements document (prd.md)
- Development workflow notes
- Basic .gitignore configuration

## Planned Features

### [0.4.0] - Layer 4: Analysis Pipeline (Upcoming)
- [ ] Rspamd HTTP client integration
- [ ] ML-based phishing classification
- [ ] Stylometry analysis for BEC detection
- [ ] Combined risk scoring with explainability
- [ ] Verdict generation system
- [ ] IOC (Indicator of Compromise) management

### [0.5.0] - Layer 5: Automation (Planned)
- [ ] Celery workers for background processing
- [ ] Gmail API integration with OAuth
- [ ] IMAP client for generic email servers
- [ ] Automated email ingestion pipeline
- [ ] Policy engine for automated actions
- [ ] Webhook alert system
- [ ] Quarantine and labeling automation

### [1.0.0] - Production Release (Vision)
- [ ] React-based web dashboard
- [ ] Real-time monitoring and alerts
- [ ] Complete test coverage
- [ ] Performance optimizations
- [ ] Security hardening
- [ ] Production deployment guides
- [ ] CI/CD pipeline

---

**Legend:**
- ✅ Complete
- ⏳ In Progress
- 🔮 Planned
- 🐛 Bug Fix
- 🔐 Security
- 📝 Documentation

[Unreleased]: https://github.com/Sahil01010011/lazy_mail/compare/v0.3.0...HEAD
[0.3.0]: https://github.com/Sahil01010011/lazy_mail/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/Sahil01010011/lazy_mail/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/Sahil01010011/lazy_mail/releases/tag/v0.1.0
