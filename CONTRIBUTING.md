# Contributing to LazyMail

Thank you for your interest in contributing to LazyMail! This document provides guidelines and instructions for contributing to the project.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Process](#development-process)
- [Project Architecture](#project-architecture)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Pull Request Process](#pull-request-process)
- [Areas to Contribute](#areas-to-contribute)

## 🤝 Code of Conduct

- Be respectful and inclusive
- Welcome newcomers and help them get started
- Focus on constructive feedback
- Prioritize the security and privacy of users

## 🚀 Getting Started

### Prerequisites

- Python 3.11 or higher
- Docker and Docker Compose
- Git
- Basic understanding of FastAPI and async Python

### Setting Up Development Environment

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/lazy_mail.git
   cd lazy_mail
   ```

2. **Set up Python environment**
   ```bash
   cd services/api
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your local settings
   ```

4. **Start infrastructure**
   ```bash
   docker-compose up -d postgres redis rspamd
   ```

5. **Run migrations**
   ```bash
   cd services/api
   alembic upgrade head
   ```

6. **Start development server**
   ```bash
   uvicorn app.main:app --reload
   ```

7. **Verify setup**
   - API: http://localhost:8000/docs
   - Health: http://localhost:8000/api/v1/health/all

## 🔄 Development Process

### Branching Strategy

- `main` - Production-ready code
- `develop` - Integration branch (future)
- `feature/*` - New features
- `bugfix/*` - Bug fixes
- `docs/*` - Documentation updates

### Workflow

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write code following style guidelines
   - Add/update tests
   - Update documentation

3. **Test your changes**
   ```bash
   pytest tests/ -v
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

   Use conventional commits:
   - `feat:` - New feature
   - `fix:` - Bug fix
   - `docs:` - Documentation only
   - `style:` - Code style (formatting, etc.)
   - `refactor:` - Code refactoring
   - `test:` - Adding or updating tests
   - `chore:` - Maintenance tasks

5. **Push and create PR**
   ```bash
   git push origin feature/your-feature-name
   ```

## 🏗️ Project Architecture

### Layer-Based Development

LazyMail follows a layered architecture. Understand the current layer before contributing:

```
Layer 1: Infrastructure ✅     → Docker, Database, Redis
Layer 2: API Foundation ✅     → FastAPI, Endpoints
Layer 3: Email Parsing ✅      → MIME, Headers, URLs (CURRENT)
Layer 4: Analysis Pipeline ⏳  → Rspamd, ML, Scoring
Layer 5: Automation ⏳         → Celery, Ingestion, Actions
```

### Directory Structure

```
services/api/
├── app/
│   ├── main.py              # FastAPI app entry point
│   ├── core/                # Core configuration
│   │   ├── config.py        # Settings
│   │   └── database.py      # DB connection
│   ├── db/                  # Database layer
│   │   ├── models/          # SQLAlchemy models
│   │   └── base.py          # Model registry
│   ├── api/                 # API layer
│   │   └── v1/
│   │       ├── routers/     # Endpoint routers
│   │       ├── schemas/     # Pydantic schemas
│   │       └── dependencies/ # DI patterns
│   └── parsing/             # Email parsing (Layer 3)
│       ├── mime_parser.py
│       ├── header_analyzer.py
│       ├── url_extractor.py
│       └── html_normalizer.py
└── tests/                   # Test suite
```

### Key Patterns

1. **Dependency Injection**: Use FastAPI's DI for database sessions
2. **Async/Await**: All I/O operations should be async
3. **Pydantic Models**: For request/response validation
4. **SQLAlchemy Models**: For database entities
5. **Type Hints**: Use Python type hints everywhere

## 📝 Coding Standards

### Python Style

- **PEP 8**: Follow Python style guide
- **Line Length**: Max 100 characters (not strict)
- **Docstrings**: Use Google-style docstrings
- **Type Hints**: Always include type hints

### Code Example

```python
"""Module description."""
from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.api.v1.schemas.message import MessageResponse

router = APIRouter(prefix="/messages", tags=["Messages"])


@router.get("/", response_model=List[MessageResponse])
async def list_messages(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
) -> List[MessageResponse]:
    """
    List all analyzed messages.
    
    Args:
        skip: Number of records to skip (pagination)
        limit: Maximum number of records to return
        db: Database session
        
    Returns:
        List of message responses
    """
    # Implementation here
    pass
```

### Documentation

- Document all public functions and classes
- Include usage examples for complex features
- Update README.md when adding major features
- Keep API documentation in sync with code

## 🧪 Testing Guidelines

### Test Structure

```
tests/
├── unit/                    # Unit tests
│   ├── test_parsing.py
│   └── test_analysis.py
├── integration/             # Integration tests
│   └── test_api.py
└── fixtures/                # Test data
    └── sample_emails/
```

### Writing Tests

```python
import pytest
from app.parsing.mime_parser import MIMEParser


def test_parse_simple_email():
    """Test parsing a simple text email."""
    email_content = """From: sender@example.com
To: receiver@example.com
Subject: Test Email

Hello World!
"""
    parser = MIMEParser(email_content)
    assert parser.get_from() == "sender@example.com"
    assert parser.get_subject() == "Test Email"


@pytest.mark.asyncio
async def test_health_endpoint(client):
    """Test health check endpoint."""
    response = await client.get("/api/v1/health/")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
```

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/unit/test_parsing.py -v

# Run with coverage
pytest tests/ --cov=app --cov-report=html

# Run only unit tests
pytest tests/unit/ -v

# Run with output
pytest tests/ -v -s
```

### Test Coverage

- Aim for 80%+ code coverage
- Focus on critical paths and edge cases
- Don't test framework code (FastAPI, SQLAlchemy)
- Test error handling and validation

## 📥 Pull Request Process

### Before Submitting

1. **Test your changes**
   ```bash
   pytest tests/ -v
   ```

2. **Check code quality** (optional but recommended)
   ```bash
   # Format code
   black app/
   
   # Lint
   flake8 app/
   
   # Type check
   mypy app/
   ```

3. **Update documentation**
   - Update README.md if needed
   - Add docstrings to new functions
   - Update API documentation

4. **Commit messages**
   - Use conventional commits format
   - Write clear, descriptive messages
   - Reference issues if applicable

### PR Template

When creating a PR, include:

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] All tests pass
- [ ] Added new tests
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] No new warnings or errors
- [ ] Tested in Docker environment
```

### Review Process

1. Automated checks will run (when set up)
2. Maintainer will review your code
3. Address feedback and update PR
4. Once approved, PR will be merged

## 🎯 Areas to Contribute

### Current Focus (Layer 3)

- **Email Parsing Improvements**
  - Add more test cases with real email samples
  - Improve URL extraction accuracy
  - Enhance HTML sanitization
  - Better attachment handling

- **Documentation**
  - Add more code examples
  - Create video tutorials
  - Improve API documentation
  - Write deployment guides

### Upcoming (Layer 4)

- **Rspamd Integration**
  - HTTP client implementation
  - Response parsing
  - Score combination logic

- **Machine Learning**
  - Feature extraction pipeline
  - Model training scripts
  - Model evaluation tools

### Future (Layer 5)

- **Email Ingestion**
  - Gmail API client
  - IMAP client
  - OAuth flow implementation

- **Automation**
  - Celery task definitions
  - Policy engine
  - Alert system

### General Improvements

- **Testing**: Add more unit and integration tests
- **Performance**: Optimize database queries
- **Security**: Security audit and improvements
- **DevOps**: CI/CD pipeline setup
- **Monitoring**: Logging and metrics

## 🐛 Bug Reports

### Before Reporting

1. Check existing issues
2. Verify it's reproducible
3. Test on latest version

### Report Template

```markdown
**Describe the bug**
Clear description of the issue

**To Reproduce**
Steps to reproduce:
1. Go to '...'
2. Click on '...'
3. See error

**Expected behavior**
What should happen

**Environment**
- OS: [e.g., Ubuntu 22.04]
- Python: [e.g., 3.11]
- Docker: [e.g., 24.0.0]

**Additional context**
Logs, screenshots, etc.
```

## 💡 Feature Requests

We welcome feature suggestions! Please:

1. Check if it aligns with the project roadmap
2. Explain the use case and benefits
3. Consider implementation complexity
4. Be open to discussion and iteration

## 📞 Getting Help

- **Documentation**: Check README.md first
- **Issues**: Search existing issues
- **Discussions**: Use GitHub Discussions for questions
- **Discord**: (Coming soon)

## 🙏 Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md (to be created)
- Credited in release notes
- Mentioned in project documentation

Thank you for contributing to LazyMail! Together we're building better email security. 🚀
