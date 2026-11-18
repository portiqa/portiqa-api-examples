# PORTIQA API examples

Public, dependency-light examples for integrating with the PORTIQA Portfolio
Analysis API.

## Quick start

1. Sign in, accept the API usage disclaimer, and create an API key in the [PORTIQA dashboard](https://portiqa.ai/user/profile).
2. Export it as `PORTIQA_API_KEY` in the trusted server or terminal that will
   make the request.
3. Run an example from the repository root.

macOS or Linux:

```sh
export PORTIQA_API_KEY="your-api-key"
python examples/python/evaluate.py
```

PowerShell:

```powershell
$env:PORTIQA_API_KEY = "your-api-key"
python examples/python/evaluate.py
```

The [.env.example](.env.example) file documents the variable name. The examples
do not load `.env` files or require third-party packages.

## Endpoint and authentication

```http
POST https://portiqa.ai/evaluate
Authorization: Bearer <your-api-key>
Portiqa-Response-Profile: public
Content-Type: application/json
Accept: application/json
```

Authentication uses the standard HTTP Bearer scheme. Keep API keys in
server-side environment variables or a secrets manager. Never put a key in
browser JavaScript, a mobile application, a URL, analytics data, or a public
repository.

## Canonical request

New integrations should send a `positions` array. Every position contains a
`ticker` and a non-negative `market_value`; cash uses the same currency as the
position values.

```json
{
  "risk_level": "medium",
  "cash_balance": 5000,
  "positions": [
    { "ticker": "AAPL", "market_value": 25000 },
    { "ticker": "MSFT", "market_value": 22000 },
    { "ticker": "NVDA", "market_value": 8000 }
  ]
}
```

## Examples

| Runtime | Command | Dependencies |
| --- | --- | --- |
| cURL | `sh examples/curl/evaluate.sh` | cURL |
| Python 3.9+ | `python examples/python/evaluate.py` | Standard library |
| Node.js 18+ | `node examples/javascript/evaluate.mjs` | Built-in `fetch` |
| PHP 8.1+ | `php examples/php/evaluate.php` | cURL extension |

The JavaScript example is for Node.js or another trusted server-side runtime.
Do not copy it into frontend code: that would disclose the API key to users.
A browser client should call your backend, and your backend should call PORTIQA.

## Response and versioning

A successful request returns `ok: true`, a `request_id` and an `evaluation`
object. All four examples request the public response profile explicitly.
New accounts receive this profile by default. Existing integrations can try it
by sending `Portiqa-Response-Profile: public` on an individual request.

Read `evaluation.score` for the portfolio score out of 100 and `status` for its
label. `component_assessments` gives a band (`lower`, `middle`, or `upper`)
for each component, or `null` when evidence is insufficient. Each
`score_drivers` entry identifies a component and explains what to review.
`score_components` is an empty JSON object for compatibility.

The sample uses the request above with synthetic market data. All three
positions were analyzed, and two had a dated technical signal. Use
`analysis_coverage` for the share of invested value evaluated, `coverage` for
individual evidence types, and `data_sources` for available dates.
[Read the sample response](sample-responses/evaluation.success.json).

Two versions have different meanings:

- OpenAPI `info.version` is the **API contract version** used by clients.
- `evaluation.engine_version` is the **evaluator engine version** that produced
  an individual result.

Store `engine_version` with saved results. Scores may change when market data or
the evaluator engine changes even if the API contract does not.

## Errors

Errors use `ok: false` and a machine-readable `error` code. A human-readable
`message` may also be present.

| HTTP status | Meaning |
| --- | --- |
| `400` | Invalid JSON, missing positions, or no evaluable positions |
| `401` | Missing or invalid Bearer token |
| `403` | The account needs to accept the current API usage disclaimer |
| `405` | The endpoint was called with a method other than `POST` |
| `409` | An evaluation with the same idempotency key already completed |
| `413` | The request exceeds the body, position-row, or plan ticker limit |
| `429` | A short-window limit or monthly evaluation allowance has been reached |
| `500` | Evaluation failed |
| `503` | Authentication service is temporarily unavailable |

For a completed duplicate, read `original_request_id`. For a short-window
limit, follow `Retry-After`. The monthly allowance error includes `reset_at`.

## API descriptions

- [OpenAPI 3.1 contract](openapi/openapi.yaml)
- [Postman collection](postman/portiqa.postman_collection.json)
- [Public-profile response using synthetic market data](sample-responses/evaluation.success.json)
- [Published documentation](https://portiqa.ai/docs/)

## Validate locally

```sh
python -m json.tool postman/portiqa.postman_collection.json > /dev/null
python -m json.tool sample-responses/evaluation.success.json > /dev/null
python tests/validate_public_sample.py
node --check examples/javascript/evaluate.mjs
php -l examples/php/evaluate.php
sh -n examples/curl/evaluate.sh
```

The GitHub Actions workflow additionally lints the OpenAPI contract.

Read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request. Report
security issues privately as described in [SECURITY.md](SECURITY.md).

PORTIQA output is quantitative information, not investment advice. Review the
[financial disclaimer](https://portiqa.ai/legal/disclaimer.html).

## License

The examples, API description, and supporting files in this repository are
available under the [MIT License](LICENSE).
