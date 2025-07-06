# API Documentation

This document provides comprehensive documentation for the API CGI Scripts, including endpoints, request/response formats, authentication, and usage examples.

## Table of Contents

- [Overview](#overview)
- [Authentication](#authentication)
- [Rate Limiting](#rate-limiting)
- [Endpoints](#endpoints)
- [Error Handling](#error-handling)
- [Examples](#examples)
- [SDKs and Libraries](#sdks-and-libraries)

## Overview

### Base URL

```
https://yourdomain.helioho.st/cgi-bin/scripts/
```

### Content Type

All requests and responses use `application/json` content type.

### CORS

The API supports Cross-Origin Resource Sharing (CORS) for configured domains. Set your allowed origins in the `.env` file:

```env
ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

## Authentication

### JWT Tokens

This API uses JSON Web Tokens (JWT) for authentication. After successful login, you'll receive a token that must be included in subsequent requests.

#### Token Format

```http
Authorization: Bearer <your-jwt-token>
```

#### Token Expiration

- **Default expiration**: 24 hours
- **Refresh**: Re-authenticate when token expires
- **Security**: Tokens are signed with a secure secret key

## Rate Limiting

### Login Attempts

- **Threshold**: 5 failed attempts per username
- **Lockout Duration**: 30 minutes (1800 seconds)
- **Reset**: Automatic after lockout period

### Global Rate Limiting

Rate limiting is implemented to prevent abuse:

- **Per IP**: Configurable limits based on endpoint
- **Per User**: Authenticated user limits
- **Lockout**: Temporary blocks for excessive requests

## Endpoints

### POST /login.py

Authenticate user credentials and receive a JWT token.

#### Request

```http
POST /cgi-bin/scripts/login.py
Content-Type: application/json
```

```json
{
    "username": "string",
    "password": "string"
}
```

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `username` | string | Yes | User's username or email |
| `password` | string | Yes | User's password |

#### Response

**Success (200 OK):**

```json
{
    "success": true,
    "message": "Login successful",
    "data": {
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        "user": {
            "id": 123,
            "username": "johndoe",
            "email": "john@example.com",
            "created_at": "2024-01-15T10:30:00Z"
        },
        "expires_at": "2024-01-16T10:30:00Z"
    }
}
```

**Error (400 Bad Request):**

```json
{
    "success": false,
    "error": "INVALID_CREDENTIALS",
    "message": "Invalid username or password",
    "details": {
        "attempts_remaining": 3
    }
}
```

**Error (429 Too Many Requests):**

```json
{
    "success": false,
    "error": "ACCOUNT_LOCKED",
    "message": "Account temporarily locked due to too many failed attempts",
    "details": {
        "locked_until": "2024-01-15T11:00:00Z",
        "lockout_duration": 1800
    }
}
```

#### cURL Example

```bash
curl -X POST https://yourdomain.helioho.st/cgi-bin/scripts/login.py \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "password": "securepassword"
  }'
```

### POST /signup.py

Register a new user account.

#### Request

```http
POST /cgi-bin/scripts/signup.py
Content-Type: application/json
```

```json
{
    "username": "string",
    "email": "string",
    "password": "string",
    "confirm_password": "string"
}
```

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `username` | string | Yes | Desired username (3-50 characters) |
| `email` | string | Yes | Valid email address |
| `password` | string | Yes | Password (minimum 8 characters) |
| `confirm_password` | string | Yes | Must match password |

#### Response

**Success (201 Created):**

```json
{
    "success": true,
    "message": "Account created successfully",
    "data": {
        "user": {
            "id": 124,
            "username": "newuser",
            "email": "newuser@example.com",
            "created_at": "2024-01-15T10:35:00Z"
        }
    }
}
```

**Error (400 Bad Request):**

```json
{
    "success": false,
    "error": "VALIDATION_ERROR",
    "message": "Username already exists",
    "details": {
        "field": "username",
        "code": "ALREADY_EXISTS"
    }
}
```

#### cURL Example

```bash
curl -X POST https://yourdomain.helioho.st/cgi-bin/scripts/signup.py \
  -H "Content-Type: application/json" \
  -d '{
    "username": "newuser",
    "email": "newuser@example.com",
    "password": "securepassword123",
    "confirm_password": "securepassword123"
  }'
```

### DELETE /delete_profile.py

Delete the authenticated user's profile and all associated data.

#### Request

```http
DELETE /cgi-bin/scripts/delete_profile.py
Content-Type: application/json
Authorization: Bearer <jwt-token>
```

```json
{
    "password": "string",
    "confirmation": "DELETE_MY_ACCOUNT"
}
```

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `password` | string | Yes | Current password for verification |
| `confirmation` | string | Yes | Must be exactly "DELETE_MY_ACCOUNT" |

#### Headers

| Header | Value | Required |
|--------|-------|----------|
| `Authorization` | `Bearer <jwt-token>` | Yes |

#### Response

**Success (200 OK):**

```json
{
    "success": true,
    "message": "Account deleted successfully",
    "data": {
        "deleted_at": "2024-01-15T10:40:00Z",
        "username": "deleteduser"
    }
}
```

**Error (401 Unauthorized):**

```json
{
    "success": false,
    "error": "UNAUTHORIZED",
    "message": "Invalid or expired token"
}
```

**Error (403 Forbidden):**

```json
{
    "success": false,
    "error": "INVALID_PASSWORD",
    "message": "Current password is incorrect"
}
```

#### cURL Example

```bash
curl -X DELETE https://yourdomain.helioho.st/cgi-bin/scripts/delete_profile.py \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -d '{
    "password": "currentpassword",
    "confirmation": "DELETE_MY_ACCOUNT"
  }'
```

## Error Handling

### Standard Error Response

All errors follow a consistent format:

```json
{
    "success": false,
    "error": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": {
        "additional": "context-specific information"
    }
}
```

### Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `INVALID_CREDENTIALS` | 400 | Wrong username/password |
| `ACCOUNT_LOCKED` | 429 | Too many failed login attempts |
| `VALIDATION_ERROR` | 400 | Input validation failed |
| `UNAUTHORIZED` | 401 | Missing or invalid token |
| `FORBIDDEN` | 403 | Valid token, insufficient permissions |
| `NOT_FOUND` | 404 | Resource not found |
| `SERVER_ERROR` | 500 | Internal server error |
| `DATABASE_ERROR` | 500 | Database connection/query error |

### HTTP Status Codes

- **200 OK**: Request successful
- **201 Created**: Resource created successfully
- **400 Bad Request**: Invalid request data
- **401 Unauthorized**: Authentication required
- **403 Forbidden**: Access denied
- **404 Not Found**: Resource not found
- **429 Too Many Requests**: Rate limit exceeded
- **500 Internal Server Error**: Server error

## Examples

### JavaScript/Fetch API

```javascript
// Login example
async function login(username, password) {
    try {
        const response = await fetch('/cgi-bin/scripts/login.py', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password })
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Store token for future requests
            localStorage.setItem('auth_token', data.data.token);
            return data.data.user;
        } else {
            throw new Error(data.message);
        }
    } catch (error) {
        console.error('Login failed:', error);
        throw error;
    }
}

// Authenticated request example
async function deleteProfile(password) {
    const token = localStorage.getItem('auth_token');
    
    const response = await fetch('/cgi-bin/scripts/delete_profile.py', {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
            password: password,
            confirmation: 'DELETE_MY_ACCOUNT'
        })
    });
    
    return response.json();
}
```

### Python Requests

```python
import requests
import json

BASE_URL = 'https://yourdomain.helioho.st/cgi-bin/scripts'

def login(username, password):
    url = f'{BASE_URL}/login.py'
    data = {
        'username': username,
        'password': password
    }
    
    response = requests.post(url, json=data)
    
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

def delete_profile(token, password):
    url = f'{BASE_URL}/delete_profile.py'
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    data = {
        'password': password,
        'confirmation': 'DELETE_MY_ACCOUNT'
    }
    
    response = requests.delete(url, headers=headers, json=data)
    return response.json()

# Usage
try:
    login_result = login('johndoe', 'password123')
    token = login_result['data']['token']
    
    delete_result = delete_profile(token, 'password123')
    print('Account deleted:', delete_result['success'])
    
except requests.RequestException as e:
    print(f'API Error: {e}')
```

### PHP cURL

```php
<?php

function apiRequest($url, $data = null, $method = 'POST', $token = null) {
    $ch = curl_init();
    
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_CUSTOMREQUEST, $method);
    
    $headers = ['Content-Type: application/json'];
    if ($token) {
        $headers[] = "Authorization: Bearer $token";
    }
    curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
    
    if ($data) {
        curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));
    }
    
    $result = curl_exec($ch);
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);
    
    return [
        'data' => json_decode($result, true),
        'status' => $httpCode
    ];
}

// Login
$loginData = [
    'username' => 'johndoe',
    'password' => 'password123'
];

$result = apiRequest('/cgi-bin/scripts/login.py', $loginData);

if ($result['status'] === 200 && $result['data']['success']) {
    $token = $result['data']['data']['token'];
    echo "Login successful. Token: $token\n";
} else {
    echo "Login failed: " . $result['data']['message'] . "\n";
}
?>
```

## SDKs and Libraries

### Recommended Libraries

#### JavaScript
- **Axios**: HTTP client with interceptors for token handling
- **Fetch API**: Native browser API

#### Python
- **requests**: HTTP library for Python
- **httpx**: Modern async HTTP client

#### PHP
- **Guzzle**: HTTP client library
- **cURL**: Built-in PHP extension

### Token Management

Implement automatic token refresh and error handling:

```javascript
class APIClient {
    constructor(baseURL) {
        this.baseURL = baseURL;
        this.token = localStorage.getItem('auth_token');
    }
    
    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const config = {
            ...options,
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            }
        };
        
        if (this.token) {
            config.headers.Authorization = `Bearer ${this.token}`;
        }
        
        const response = await fetch(url, config);
        
        if (response.status === 401) {
            // Token expired, redirect to login
            this.logout();
            throw new Error('Authentication required');
        }
        
        return response.json();
    }
    
    logout() {
        this.token = null;
        localStorage.removeItem('auth_token');
        // Redirect to login page
    }
}
```

## Security Considerations

### Input Validation

- All inputs are validated server-side
- SQL injection prevention through parameterized queries
- XSS protection through proper encoding

### Authentication Security

- JWT tokens are signed and verified
- Password hashing using secure algorithms
- Rate limiting prevents brute force attacks

### HTTPS

Always use HTTPS in production to protect:
- Authentication tokens
- User credentials
- Sensitive data

## Support

For API support and questions:

- **Documentation**: Check this API documentation
- **Issues**: Open a GitHub issue for bugs
- **Security**: Report security issues via [SECURITY.md](SECURITY.md)

---

**Last Updated**: July 2025
