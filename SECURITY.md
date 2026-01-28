# Security Policy

## Sensitive Data Protection

This project uses environment variables for sensitive data. **NEVER commit:**
- `.env` file (contains real API keys and secrets)
- API keys or tokens
- Database credentials
- JWT secrets

## Setup Instructions

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Fill in your actual values in `.env`:
   - `JWT_SECRET`: Generate a strong random secret
   - `OPENAI_API_KEY`: Add your OpenAI API key
   - `DATABASE_URL`: Configure your database connection

## Reporting Security Issues

If you discover a security vulnerability, please email: [your-email@example.com]

**Do not** create public GitHub issues for security vulnerabilities.

## Best Practices

- Always use environment variables for secrets
- Rotate API keys regularly
- Use strong, unique JWT secrets in production
- Enable HTTPS in production
- Keep dependencies updated
