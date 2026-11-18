#!/usr/bin/env sh
set -eu

: "${PORTIQA_API_KEY:?Set PORTIQA_API_KEY before running this example}"

curl --fail-with-body --silent --show-error \
  --request POST 'https://portiqa.ai/evaluate' \
  --header "Authorization: Bearer ${PORTIQA_API_KEY}" \
  --header 'Portiqa-Response-Profile: public' \
  --header 'Content-Type: application/json' \
  --header 'Accept: application/json' \
  --connect-timeout 5 \
  --max-time 20 \
  --data '{
    "risk_level": "medium",
    "cash_balance": 5000,
    "positions": [
      {"ticker": "AAPL", "market_value": 25000},
      {"ticker": "MSFT", "market_value": 22000},
      {"ticker": "NVDA", "market_value": 8000}
    ]
  }'
