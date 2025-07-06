# Contributing to API CGI Scripts

Thank you for your interest in contributing to this project! This document provides guidelines and instructions for contributors.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How to Contribute](#how-to-contribute)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Pull Request Process](#pull-request-process)
- [Issue Reporting](#issue-reporting)

## Code of Conduct

By participating in this project, you agree to abide by our Code of Conduct:

- **Be respectful**: Treat all community members with respect and kindness
- **Be collaborative**: Work together constructively and help others learn
- **Be inclusive**: Welcome contributors of all backgrounds and experience levels
- **Be patient**: Understand that review processes take time
- **Be constructive**: Provide helpful feedback and suggestions

## How to Contribute

### Types of Contributions

We welcome various types of contributions:

- **Bug fixes**: Fix issues and improve stability
- **Feature additions**: Add new functionality
- **Documentation**: Improve or add documentation
- **Security improvements**: Enhance security measures
- **Performance optimizations**: Improve efficiency
- **Code quality**: Refactoring and cleanup

### Getting Started

1. **Fork the repository**
2. **Clone your fork locally**
3. **Create a feature branch**
4. **Make your changes**
5. **Test your changes**
6. **Submit a pull request**

## Development Setup

### Prerequisites

- Python 3.7 or higher
- MariaDB/MySQL server
- Git
- A text editor or IDE

### Local Environment Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/API.git
   cd API
   ```

2. **Create a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   cp env.example .env
   # Edit .env with your local database settings
   ```

5. **Set up local database:**
   ```sql
   CREATE DATABASE api_test;
   -- Run the database setup queries from SETUP.md
   ```

### Development Database

For development, you can use a local MariaDB/MySQL instance:

```bash
# Install MariaDB (Ubuntu/Debian)
sudo apt-get install mariadb-server mariadb-client

# Start MariaDB service
sudo systemctl start mariadb

# Create development database
sudo mysql -e "CREATE DATABASE api_development;"
```

## Coding Standards

### Python Style Guide

We follow [PEP 8](https://pep8.org/) with some project-specific guidelines:

#### Code Formatting

- **Line length**: Maximum 100 characters
- **Indentation**: 4 spaces (no tabs)
- **Imports**: Group in this order:
  1. Standard library imports
  2. Third-party imports
  3. Local application imports

#### Example:

```python
#!/usr/bin/env python3

import os
import sys
import json

import mariadb
from dotenv import load_dotenv

from utils.auth import verify_token
```

#### Naming Conventions

- **Variables and functions**: `snake_case`
- **Constants**: `UPPER_SNAKE_CASE`
- **Classes**: `PascalCase`
- **Private methods**: `_leading_underscore`

#### Documentation

- **Functions**: Include docstrings for all public functions
- **Classes**: Document class purpose and key methods
- **Modules**: Include module-level docstring

```python
def authenticate_user(username: str, password: str) -> dict:
    """
    Authenticate user credentials.
    
    Args:
        username (str): The username to authenticate
        password (str): The user's password
        
    Returns:
        dict: Authentication result with user data or error
        
    Raises:
        DatabaseError: If database connection fails
    """
    pass
```

### Security Guidelines

- **Never commit sensitive data**: Use environment variables
- **Validate all inputs**: Sanitize and validate user inputs
- **Use parameterized queries**: Prevent SQL injection
- **Error handling**: Don't expose sensitive information in errors
- **Authentication**: Implement proper token validation

### CGI-Specific Guidelines

- **Headers**: Always print proper HTTP headers
- **Error handling**: Use `cgitb.enable()` for debugging
- **Output**: Ensure proper JSON formatting
- **File permissions**: Maintain executable permissions (755)

## Testing Guidelines

### Testing Structure

Create tests in a `tests/` directory:

```
tests/
├── __init__.py
├── test_login.py
├── test_signup.py
├── test_delete_profile.py
└── test_utils.py
```

### Writing Tests

1. **Use descriptive test names:**
   ```python
   def test_login_with_valid_credentials_returns_success():
       pass
   
   def test_login_with_invalid_password_returns_error():
       pass
   ```

2. **Test both success and failure cases**
3. **Mock external dependencies (database, etc.)**
4. **Test security measures (rate limiting, input validation)**

### Running Tests

```bash
# Install testing dependencies
pip install pytest pytest-cov

# Run tests
pytest tests/

# Run with coverage
pytest --cov=cgi-bin tests/
```

## Pull Request Process

### Before Submitting

1. **Update documentation** if your changes affect user-facing features
2. **Add tests** for new functionality
3. **Ensure all tests pass**
4. **Check code style** with linting tools
5. **Update README.md** if needed

### PR Guidelines

1. **Clear title**: Use a descriptive title
2. **Detailed description**: Explain what changes you made and why
3. **Link issues**: Reference related issues with "Fixes #123"
4. **Small changes**: Keep PRs focused and manageable
5. **Tests included**: Ensure adequate test coverage

### PR Template

```markdown
## Description
Brief description of changes made.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Security improvement
- [ ] Performance improvement

## Testing
- [ ] Added tests for new functionality
- [ ] All existing tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No sensitive data exposed
```

### Review Process

1. **Automated checks**: CI will run tests and linting
2. **Code review**: Maintainers will review your code
3. **Feedback**: Address any requested changes
4. **Approval**: Once approved, your PR will be merged

## Issue Reporting

### Bug Reports

Use the bug report template and include:

- **Environment details**: OS, Python version, hosting provider
- **Steps to reproduce**: Clear, step-by-step instructions
- **Expected behavior**: What should happen
- **Actual behavior**: What actually happens
- **Error messages**: Include full error messages
- **Screenshots**: If applicable

### Feature Requests

Use the feature request template and include:

- **Problem description**: What problem does this solve?
- **Proposed solution**: How should this work?
- **Alternatives considered**: Other approaches you've thought of
- **Implementation details**: Technical considerations

### Security Issues

**Do not open public issues for security vulnerabilities.** Instead:

1. Email security details to: [INSERT_SECURITY_EMAIL]
2. Follow the process outlined in [SECURITY.md](SECURITY.md)
3. Allow time for responsible disclosure

## Development Workflow

### Branch Naming

- **Features**: `feature/description-of-feature`
- **Bug fixes**: `fix/description-of-fix`
- **Documentation**: `docs/description-of-changes`
- **Security**: `security/description-of-fix`

### Commit Messages

Follow conventional commit format:

```
type(scope): description

Examples:
feat(auth): add JWT token validation
fix(login): resolve rate limiting issue
docs(setup): update installation instructions
security(auth): fix password validation vulnerability
```

### Release Process

1. **Version bumping**: Use semantic versioning (MAJOR.MINOR.PATCH)
2. **Changelog**: Update CHANGELOG.md with changes
3. **Tag release**: Create git tag with version number
4. **Release notes**: Document changes and migration steps

## Getting Help

### Resources

- **Documentation**: Check existing docs first
- **Issues**: Search existing issues before creating new ones
- **Discussions**: Use GitHub Discussions for questions

### Contact

- **General questions**: Open a GitHub issue
- **Security concerns**: Email [INSERT_SECURITY_EMAIL]
- **Maintainers**: Tag @maintainer-username in issues

## Recognition

Contributors will be recognized in:

- **README.md**: Contributors section
- **Release notes**: Acknowledgment of contributions
- **Documentation**: Author attribution where appropriate

## License

By contributing to this project, you agree that your contributions will be licensed under the same license as the project.

---

Thank you for contributing to make this project better for everyone! 🎉
