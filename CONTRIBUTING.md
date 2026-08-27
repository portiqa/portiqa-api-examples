# Contributing

Thanks for helping improve the PORTIQA API examples.

For a small correction, open a focused pull request. For a new language,
contract change, or behavior change, open an issue first so the intended public
API can be confirmed.

Do not include proprietary engine code, internal documentation, production
data, customer information, credentials, or real portfolio results.

## Pull request checklist

- Keep examples dependency-light and suitable for a backend.
- Use only `Authorization: Bearer <token>` for authentication.
- Read credentials from `PORTIQA_API_KEY`; never add a real or realistic key.
- Keep the canonical request consistent across every example and API artifact.
- Keep API contract versions separate from `evaluation.engine_version`.
- Update `CHANGELOG.md` for user-visible changes.
- Run the validation commands in `README.md`.
- Explain any compatibility impact.

## Style

- Fail clearly for missing credentials, transport errors, non-2xx responses,
  non-JSON responses, and unexpected response envelopes.
- Use a finite network timeout.
- Do not log API keys or authorization headers.
- State explicitly when an example is server-side only.

## License status

The repository license is pending. By proposing a contribution, you confirm
that you have the right to submit it. Maintainers may wait to merge external
contributions until licensing terms are finalized.
