// Server-side only: run with Node.js 18+.
// Never expose PORTIQA_API_KEY in browser or other client-side code.

const apiKey = process.env.PORTIQA_API_KEY?.trim();

if (!apiKey) {
  console.error('Set PORTIQA_API_KEY before running this example.');
  process.exit(2);
}

const controller = new AbortController();
const timeout = setTimeout(() => controller.abort(), 20_000);

try {
  const response = await fetch('https://portiqa.ai/evaluate', {
    method: 'POST',
    signal: controller.signal,
    headers: {
      Authorization: `Bearer ${apiKey}`,
      'Portiqa-Response-Profile': 'public',
      'Content-Type': 'application/json',
      Accept: 'application/json'
    },
    body: JSON.stringify({
      risk_level: 'medium',
      cash_balance: 5000,
      positions: [
        { ticker: 'AAPL', market_value: 25000 },
        { ticker: 'MSFT', market_value: 22000 },
        { ticker: 'NVDA', market_value: 8000 }
      ]
    })
  });

  const text = await response.text();
  let body;
  try {
    body = JSON.parse(text);
  } catch {
    throw new Error(`PORTIQA returned HTTP ${response.status} with non-JSON data.`);
  }

  if (!response.ok || body?.ok !== true || !body.evaluation ||
      typeof body.evaluation !== 'object' || Array.isArray(body.evaluation)) {
    throw new Error(`PORTIQA returned HTTP ${response.status}: ${JSON.stringify(body)}`);
  }

  console.log(JSON.stringify(body.evaluation, null, 2));
} catch (error) {
  const message = error?.name === 'AbortError'
    ? 'PORTIQA request timed out.'
    : (error instanceof Error ? error.message : String(error));
  console.error(message);
  process.exitCode = 1;
} finally {
  clearTimeout(timeout);
}
