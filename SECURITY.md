# Security Policy

## Supported Versions

| Version | Supported |
| ------- | --------- |
| 1.0.x   | ✅ Yes    |
| < 1.0   | ❌ No     |

## Reporting a Vulnerability

If you discover a security vulnerability in this project, please `do not` open a public issue.

Instead, please report it via email to:

`security@denied.se`

You should receive a response within 48 hours. If the issue is confirmed, we will release a patch as soon as possible.

## Security Best Practices

- Always use a strong, randomly generated API key
- Store secrets (API keys, Discord webhooks) in environment variables or secret files
- Never commit `.env` files or `.secrets/` directory to version control
- Use a proxy service to protect your IP address when scraping
- Keep Docker and all container images updated

## Acknowledgments

We appreciate responsible disclosure. With your permission, we will acknowledge you in the release notes.

