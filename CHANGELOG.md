# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial repository setup with comprehensive documentation
- Security policy and guidelines
- Contributing guidelines
- API documentation
- Setup instructions

## [1.0.0] - 2025-07-06

### Added
- Initial release of API CGI Scripts
- User authentication system with JWT tokens
- Login endpoint with rate limiting and account lockout
- User registration endpoint with validation
- Profile deletion endpoint with security confirmations
- Environment-based configuration
- CORS support for web applications
- Comprehensive error handling and logging
- Security measures against common vulnerabilities
- MariaDB/MySQL database integration
- HelioHost shared hosting compatibility

### Security
- Implemented rate limiting for login attempts
- Added account lockout mechanism
- Secure password hashing
- JWT token-based authentication
- Input validation and sanitization
- SQL injection prevention
- Environment variable protection

### Documentation
- Complete API documentation with examples
- Setup guide for HelioHost deployment
- Security policy and vulnerability reporting
- Contributing guidelines for developers
- Comprehensive README with quick start guide

## Security Updates

### [1.0.1] - TBD
- Security patches and improvements will be documented here

## Migration Guide

### From 0.x to 1.0.0
This is the initial stable release. No migration required.

## Support

For questions about changes or upgrades:
- Review this changelog
- Check the [Setup Guide](SETUP.md)
- Open an issue for assistance
- Review [API Documentation](API.md) for endpoint changes

---

**Note**: This project follows semantic versioning. Major version changes may include breaking changes that require migration steps.
