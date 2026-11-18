# Changelog

The OpenAPI contract and the evaluator engine report their versions independently.

## 2026-11-18

- All four examples and the Postman collection request the public response profile.
- Updated the OpenAPI contract and sample response to illustrate score drivers,
  qualitative component assessments, holding exposures and data coverage.

## [1.0.0] - 2026-08-27

### Added

- Initial public OpenAPI 3.1 contract for `POST /evaluate`.
- Canonical `positions` request using `ticker` and `market_value`.
- Bearer-authenticated cURL, Python, Node.js, and PHP examples.
- Sanitized response fixture, Postman collection, and automated validation.

### Clarified

- OpenAPI `info.version` identifies the API contract, not the engine.
- JavaScript credentials must remain in a trusted server-side runtime.
- Unsupported HTTP methods return `405 Method Not Allowed`.

[1.0.0]: https://github.com/portiqa/portiqa-api-examples/releases/tag/v1.0.0
