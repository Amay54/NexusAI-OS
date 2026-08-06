# Security Policy — NexusAI OS

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| v0.5.x  | :white_check_mark: |
| v0.4.x  | :x:                |
| < 0.4.0 | :x:                |

## Reporting a Vulnerability

We take the security of NexusAI OS seriously. If you discover a security vulnerability, please follow these steps:

1. **Do NOT open a public GitHub issue.**
2. Send an email to `security@nexusai.os` detailing the vulnerability, steps to reproduce, and impact.
3. Our security team will acknowledge receipt within 24 hours and issue a patch release within 7 days.

## Security Architecture Highlights
- **JWT Authentication**: Microservice endpoints enforce signed JWT token validation.
- **Isolated Code Execution**: Python sandbox execution runs in isolated sub-processes with strict timeout limits.
- **Zero Third-Party Dependency Data Transmission**: All LLM routing uses local free endpoints or user-controlled API keys.
