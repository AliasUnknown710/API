# API CGI Scripts

This repository contains Python CGI scripts for handling API requests on HelioHost.

## Setup

1. Upload files to your HelioHost account:
   - Place `cgi-bin/` folder in `httpdocs/`
   - Set permissions on `.py` files to 755

2. Create your `.env` file based on `.env.example`

3. Ensure your database is set up with the required tables

## Endpoints

- `POST /cgi-bin/login.py` - User login
- `DELETE /cgi-bin/delete_profile.py` - Delete user profile

## File Permissions

Make sure CGI scripts are executable:
```bash
chmod 755 httpdocs/cgi-bin/*.py
```