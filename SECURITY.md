# Security policy

## Reporting a vulnerability

Report suspected vulnerabilities privately. Do not open a public issue, pull
request, or discussion containing exploit details, credentials, personal data,
or other sensitive information.

Use GitHub's private vulnerability reporting for this repository when it is
available. Otherwise, email [hello@portiqa.ai](mailto:hello@portiqa.ai) with the
subject `Security report: portiqa-api-examples`.

Include the affected file, endpoint, or contract version; impact; minimal steps
to reproduce; and a safe way to contact you. Do not include a live API key.
Revoke any credential that may have been disclosed and use a redacted value in
the report.

We will assess the report and coordinate remediation and disclosure with the
reporter. Please allow reasonable time for a fix before public disclosure.

## Supported versions

Security fixes are applied to the latest API contract and current examples on
the default branch. Older tags may not receive updates.

## Credential handling

PORTIQA API keys are secrets. Send them only in the HTTP `Authorization` header
with the Bearer scheme, and only from trusted server-side systems. Never embed a
key in client-side JavaScript, mobile binaries, URLs, screenshots, logs, test
fixtures, or committed configuration.
