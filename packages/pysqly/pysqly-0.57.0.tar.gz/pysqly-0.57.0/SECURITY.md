# Security Policy

## Supported Versions

Use this section to tell people about which versions of your project are
currently being supported with security updates.

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Reporting a Vulnerability

The pySQLY team takes security issues seriously. We appreciate your efforts
to responsibly disclose your findings and will make every effort to acknowledge
your contributions.

To report a security issue, please email support@antonybailey.net with a
description of the issue, the steps you took to create the issue, affected
versions, and if known, mitigations for the issue.

We aim to respond to security reports within 48 hours. If for some reason you
don't get a response within that timeframe, please follow up via email to ensure
we received your original message.

After the initial reply to your report, the security team will keep you informed
of the progress towards a fix and full announcement, and may ask for additional
information or guidance.

## Security Best Practices for Using pySQLY

When using pySQLY in your applications, consider these security best practices:

1. **Always sanitize user inputs**: While pySQLY helps prevent SQL injection by
   using parameterized queries, it's still important to validate and sanitize all
   user inputs before processing them.

2. **Use principle of least privilege**: Configure your database users with
   the minimum required permissions for your application to function.

3. **Keep dependencies updated**: Regularly update pySQLY and its dependencies
   to ensure you have the latest security patches.

4. **Store connection strings securely**: Never hard-code database credentials in
   your source code. Use environment variables or a secure secret management system.

5. **Log responsibly**: Be careful not to log sensitive information like queries
   that might contain personal data or credentials.

Thank you for helping keep pySQLY and its community safe!
