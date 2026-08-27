# PORTIQA API examples

Public, dependency-light examples for integrating with the PORTIQA Portfolio
Analysis API.

## Quick start

1. Create an API key in the [PORTIQA dashboard](https://portiqa.ai/user/profile).
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

A successful request returns `ok: true` and an `evaluation` object. See the
[sanitized response](sample-responses/evaluation.success.json).

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
| `402` | Subscription is inactive |
| `405` | The endpoint was called with a method other than `POST` |
| `413` | The request exceeds the plan's ticker limit |
| `429` | The monthly request limit has been reached |
| `500` | Evaluation failed |
| `503` | Authentication service is temporarily unavailable |

Do not retry `400`, `401`, `402`, `405`, or `413` without changing the request.
Retry transient failures only with bounded exponential backoff.

## API descriptions

- [OpenAPI 3.1 contract](openapi/openapi.yaml)
- [Postman collection](postman/portiqa.postman_collection.json)
- [Sanitized response](sample-responses/evaluation.success.json)
- [Published documentation](https://portiqa.ai/docs/)

## Validate locally

```sh
python -m json.tool postman/portiqa.postman_collection.json > /dev/null
python -m json.tool sample-responses/evaluation.success.json > /dev/null
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
