# Setup Guide

This comprehensive guide will help you set up and deploy the API CGI Scripts on HelioHost or similar shared hosting providers.

## Prerequisites

Before you begin, ensure you have:

- A HelioHost account (or compatible shared hosting with Python CGI support)
- FTP/SFTP access to your hosting account
- Python 3.x support on your hosting provider
- MariaDB/MySQL database access
- A text editor or IDE for configuration

## Quick Start

```bash
# 1. Clone the repository
git clone <repository-url>
cd API

# 2. Copy environment file
cp env.example .env

# 3. Configure your environment (see detailed steps below)
# Edit .env with your database and security settings

# 4. Upload to your hosting provider
# See deployment section for detailed instructions
```

## Detailed Setup Instructions

### Step 1: Environment Configuration

1. **Copy the environment template:**
   ```bash
   cp env.example .env
   ```

2. **Configure database settings:**
   ```env
   DB_HOST=localhost
   DB_USER=your_heliohost_db_username
   DB_PASSWORD=your_secure_db_password
   DB_NAME=your_database_name
   ```

3. **Generate security keys:**
   ```bash
   # Generate a secure JWT secret (32+ characters)
   python3 -c "import secrets; print(secrets.token_urlsafe(32))"
   ```
   
   Add to `.env`:
   ```env
   JWT_SECRET_KEY=your_generated_jwt_secret_here
   API_SECRET_KEY=your_api_secret_key_here
   ```

4. **Configure CORS settings:**
   ```env
   # Replace with your actual domain(s)
   ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
   ```

5. **Set environment type:**
   ```env
   ENVIRONMENT=production
   DEBUG=False
   ```

### Step 2: Database Setup

1. **Create database tables:**
   ```sql
   CREATE TABLE users (
       id INT AUTO_INCREMENT PRIMARY KEY,
       username VARCHAR(255) UNIQUE NOT NULL,
       email VARCHAR(255) UNIQUE NOT NULL,
       password_hash VARCHAR(255) NOT NULL,
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
       updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
   );

   CREATE TABLE login_attempts (
       id INT AUTO_INCREMENT PRIMARY KEY,
       username VARCHAR(255),
       ip_address VARCHAR(45),
       attempt_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
       success BOOLEAN DEFAULT FALSE,
       INDEX idx_username_time (username, attempt_time),
       INDEX idx_ip_time (ip_address, attempt_time)
   );
   ```

2. **Create database user with minimal permissions:**
   ```sql
   CREATE USER 'api_user'@'localhost' IDENTIFIED BY 'secure_password';
   GRANT SELECT, INSERT, UPDATE, DELETE ON your_database.users TO 'api_user'@'localhost';
   GRANT SELECT, INSERT, UPDATE, DELETE ON your_database.login_attempts TO 'api_user'@'localhost';
   FLUSH PRIVILEGES;
   ```

### Step 3: Local Development (Optional)

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up local testing environment:**
   ```bash
   # For local testing, you might want to use a local database
   # Update .env with local database settings for development
   ```

### Step 4: Deployment to HelioHost

#### Upload Files

1. **Connect via FTP/SFTP to your HelioHost account**

2. **Upload project structure:**
   ```
   httpdocs/
   ├── cgi-bin/
   │   └── scripts/
   │       ├── login.py
   │       ├── signup.py
   │       └── delete_profile.py
   └── .env
   ```

3. **Set proper file permissions:**
   ```bash
   chmod 755 httpdocs/cgi-bin/scripts/*.py
   chmod 644 httpdocs/.env
   ```

#### Configure HelioHost Settings

1. **Python Path Configuration:**
   - Ensure Python 3.x is available
   - Check the shebang line in Python files: `#!/usr/bin/env python3`

2. **Install Python packages:**
   ```bash
   # On HelioHost, you might need to install packages locally
   pip3 install --user mariadb python-dotenv
   ```

### Step 5: Testing Your Setup

1. **Test the login endpoint:**
   ```bash
   curl -X POST https://yourdomain.helioho.st/cgi-bin/scripts/login.py \
        -H "Content-Type: application/json" \
        -d '{"username":"testuser","password":"testpass"}'
   ```

2. **Check for common issues:**
   - Verify file permissions (755 for .py files)
   - Check error logs in HelioHost control panel
   - Ensure database connection is working
   - Verify CORS settings for your frontend domain

## Environment Variables Reference

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `DB_HOST` | Database hostname | Yes | localhost |
| `DB_USER` | Database username | Yes | - |
| `DB_PASSWORD` | Database password | Yes | - |
| `DB_NAME` | Database name | Yes | - |
| `JWT_SECRET_KEY` | JWT signing key (32+ chars) | Yes | - |
| `API_SECRET_KEY` | Additional API security | Yes | - |
| `LOCKOUT_THRESHOLD` | Failed login attempts before lockout | No | 5 |
| `LOCKOUT_DURATION` | Lockout duration in seconds | No | 1800 |
| `ALLOWED_ORIGINS` | CORS allowed origins | Yes | - |
| `ENVIRONMENT` | Environment type | No | production |
| `DEBUG` | Enable debug mode | No | False |

## Troubleshooting

### Common Issues

1. **500 Internal Server Error:**
   - Check file permissions (should be 755 for .py files)
   - Verify Python shebang line
   - Check error logs in hosting control panel

2. **Database Connection Errors:**
   - Verify database credentials in `.env`
   - Ensure database user has proper permissions
   - Check if MariaDB module is installed

3. **CORS Errors:**
   - Update `ALLOWED_ORIGINS` in `.env`
   - Ensure your frontend domain is included

4. **Authentication Issues:**
   - Verify JWT_SECRET_KEY is set and secure
   - Check password hashing implementation
   - Ensure user exists in database

### Getting Help

1. **Check error logs:** HelioHost control panel → Error Logs
2. **Enable CGI debugging:** Add `cgitb.enable()` to scripts
3. **Test database connection:** Create a simple test script
4. **Verify permissions:** Use FTP client to check file permissions

## Production Checklist

Before going live, ensure:

- [ ] All environment variables are configured
- [ ] Database tables are created
- [ ] File permissions are set correctly (755 for .py files)
- [ ] CORS origins are configured for your domain
- [ ] JWT secret keys are secure and unique
- [ ] Debug mode is disabled
- [ ] HTTPS is configured (if available)
- [ ] Rate limiting is properly configured
- [ ] Error monitoring is in place

## Next Steps

After successful setup:
1. Review the [API Documentation](API.md) for endpoint details
2. Configure your frontend to use the API endpoints
3. Set up monitoring and logging
4. Review security settings in [SECURITY.md](SECURITY.md)
5. Consider implementing additional security measures

---

**Need Help?** Open an issue in this repository or check our [Contributing Guidelines](CONTRIBUTING.md).
