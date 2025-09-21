# Security Policy

## Supported Versions

We actively support the following versions of the Docling Document Processing Application:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

We take security vulnerabilities seriously. If you discover a security vulnerability, please follow these steps:

### 1. **Do NOT** create a public GitHub issue

Security vulnerabilities should be reported privately to allow us to fix them before they are publicly disclosed.

### 2. Report via Email

Send an email to: **security@[your-domain].com** (replace with actual email)

Include the following information:
- Description of the vulnerability
- Steps to reproduce the issue
- Potential impact assessment
- Any suggested fixes (if you have them)

### 3. Response Timeline

- **Initial Response**: Within 48 hours
- **Status Update**: Within 7 days
- **Fix Timeline**: Varies based on severity (see below)

## Vulnerability Severity Levels

### Critical (Fix within 24-48 hours)
- Remote code execution
- SQL injection
- Authentication bypass
- Privilege escalation

### High (Fix within 1 week)
- Cross-site scripting (XSS)
- Cross-site request forgery (CSRF)
- Information disclosure
- File upload vulnerabilities

### Medium (Fix within 2 weeks)
- Denial of service
- Path traversal
- Weak cryptography

### Low (Fix within 1 month)
- Information leakage
- Minor configuration issues

## Security Best Practices for Users

### File Upload Security

1. **File Type Validation**
   - Only upload trusted documents
   - Be cautious with files from unknown sources
   - The application validates file types, but additional caution is recommended

2. **File Size Limits**
   - Respect the 50MB file size limit
   - Large files may consume significant system resources

3. **Content Scanning**
   - Consider scanning uploaded files with antivirus software
   - Be aware that document processing involves parsing file contents

### Network Security

1. **HTTPS Usage**
   - Always use HTTPS in production environments
   - Ensure SSL/TLS certificates are properly configured

2. **API Security**
   - Implement rate limiting for API endpoints
   - Use authentication tokens for sensitive operations
   - Monitor API usage for unusual patterns

### Deployment Security

1. **Environment Variables**
   - Store sensitive configuration in environment variables
   - Never commit secrets to version control
   - Use secure secret management systems in production

2. **Container Security**
   - Keep Docker images updated
   - Use minimal base images
   - Scan containers for vulnerabilities

3. **Access Control**
   - Implement proper user authentication and authorization
   - Use principle of least privilege
   - Regularly review access permissions

### Data Protection

1. **Document Handling**
   - Documents are processed in memory and temporary storage
   - Uploaded files are automatically cleaned up after processing
   - Consider data retention policies for your use case

2. **Logging**
   - Logs may contain file names and processing metadata
   - Ensure logs are stored securely
   - Implement log rotation and retention policies

3. **Model Security**
   - The IBM Granite Docling model is downloaded from HuggingFace
   - Verify model integrity if security is critical
   - Consider using private model repositories for sensitive environments

## Known Security Considerations

### Document Processing Risks

1. **Malicious Documents**
   - PDF and other document formats can contain embedded scripts
   - The Docling library includes protections, but risks remain
   - Consider sandboxing document processing in high-security environments

2. **Resource Consumption**
   - Large or complex documents may consume significant CPU/memory
   - Implement resource limits and monitoring
   - Consider rate limiting for document processing

3. **Model Dependencies**
   - The application depends on external ML models
   - Models are downloaded from HuggingFace Hub
   - Verify model sources in security-critical deployments

### Infrastructure Security

1. **Memory Usage**
   - Document processing requires significant memory (8GB+ recommended)
   - Memory may contain sensitive document content during processing
   - Ensure proper memory management and cleanup

2. **Temporary Files**
   - Temporary files are created during processing
   - Files are cleaned up automatically, but consider secure deletion
   - Monitor disk usage and cleanup processes

3. **Network Dependencies**
   - Initial setup requires internet access for model downloads
   - Consider offline deployment for air-gapped environments
   - Monitor network traffic for unusual patterns

## Security Updates

### Notification Process

1. **Security Advisories**
   - Critical security updates will be announced via GitHub Security Advisories
   - Subscribe to repository notifications for security updates

2. **Update Recommendations**
   - Apply security updates promptly
   - Test updates in staging environments before production deployment
   - Monitor security mailing lists for dependency vulnerabilities

### Dependency Management

1. **Regular Updates**
   - Keep all dependencies updated to latest secure versions
   - Monitor security advisories for Python and Node.js packages
   - Use automated dependency scanning tools

2. **Vulnerability Scanning**
   - Regularly scan dependencies for known vulnerabilities
   - Use tools like `pip-audit` for Python and `npm audit` for Node.js
   - Implement automated vulnerability scanning in CI/CD pipelines

## Incident Response

### If You Suspect a Security Breach

1. **Immediate Actions**
   - Isolate affected systems
   - Preserve logs and evidence
   - Contact security team immediately

2. **Assessment**
   - Determine scope and impact
   - Identify compromised data or systems
   - Document timeline of events

3. **Recovery**
   - Apply security patches
   - Reset credentials if necessary
   - Monitor for continued threats

## Security Resources

### Tools and Scanning

- **Python Security**: `pip-audit`, `bandit`, `safety`
- **Node.js Security**: `npm audit`, `yarn audit`
- **Container Security**: `docker scan`, `trivy`
- **Code Analysis**: `semgrep`, `CodeQL`

### Documentation

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Python Security Guidelines](https://python.org/dev/security/)
- [Node.js Security Best Practices](https://nodejs.org/en/docs/guides/security/)
- [Docker Security](https://docs.docker.com/engine/security/)

## Contact Information

For security-related questions or concerns:

- **Security Email**: security@[your-domain].com
- **General Issues**: Use GitHub Issues for non-security bugs
- **Documentation**: Check existing documentation first

## Acknowledgments

We appreciate the security research community and responsible disclosure of vulnerabilities. Contributors who report security issues will be acknowledged (with their permission) in our security advisories.

---

**Note**: This security policy is subject to updates. Please check regularly for the latest version.
