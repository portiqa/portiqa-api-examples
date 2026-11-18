<?php
declare(strict_types=1);

$apiKey = trim((string) getenv('PORTIQA_API_KEY'));
if ($apiKey === '') {
    fwrite(STDERR, "Set PORTIQA_API_KEY before running this example.\n");
    exit(2);
}

$payload = json_encode([
    'risk_level' => 'medium',
    'cash_balance' => 5000,
    'positions' => [
        ['ticker' => 'AAPL', 'market_value' => 25000],
        ['ticker' => 'MSFT', 'market_value' => 22000],
        ['ticker' => 'NVDA', 'market_value' => 8000],
    ],
], JSON_THROW_ON_ERROR);

$handle = curl_init('https://portiqa.ai/evaluate');
if ($handle === false) {
    fwrite(STDERR, "Could not initialize cURL.\n");
    exit(1);
}

curl_setopt_array($handle, [
    CURLOPT_POST => true,
    CURLOPT_POSTFIELDS => $payload,
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_CONNECTTIMEOUT => 5,
    CURLOPT_TIMEOUT => 20,
    CURLOPT_HTTPHEADER => [
        'Authorization: Bearer ' . $apiKey,
        'Portiqa-Response-Profile: public',
        'Content-Type: application/json',
        'Accept: application/json',
    ],
]);

$raw = curl_exec($handle);
$status = (int) curl_getinfo($handle, CURLINFO_HTTP_CODE);
$transportError = curl_error($handle);
curl_close($handle);

if ($raw === false) {
    fwrite(STDERR, "Could not reach PORTIQA: {$transportError}\n");
    exit(1);
}

try {
    $body = json_decode((string) $raw, flags: JSON_THROW_ON_ERROR);
} catch (JsonException) {
    fwrite(STDERR, "PORTIQA returned HTTP {$status} with non-JSON data.\n");
    exit(1);
}

if ($status < 200 || $status >= 300 || ($body->ok ?? false) !== true || !is_object($body->evaluation ?? null)) {
    fwrite(STDERR, "PORTIQA returned HTTP {$status}: {$raw}\n");
    exit(1);
}

echo json_encode($body->evaluation, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES | JSON_THROW_ON_ERROR) . PHP_EOL;
