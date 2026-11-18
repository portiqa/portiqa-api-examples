"""Check the public response fixture and its canonical Postman request."""

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sample = json.loads((ROOT / "sample-responses/evaluation.success.json").read_text())
collection = json.loads((ROOT / "postman/portiqa.postman_collection.json").read_text())
request = collection["item"][0]["request"]
headers = {item["key"].lower(): item["value"] for item in request["header"]}
assert headers["portiqa-response-profile"] == "public"
payload = json.loads(request["body"]["raw"])

assert set(sample) == {"ok", "request_id", "evaluation"}
assert sample["ok"] is True and re.fullmatch("[a-f0-9]{32}", sample["request_id"])
evaluation = sample["evaluation"]
assert set(evaluation) == {
    "engine_version", "score", "health_score", "status", "status_key", "count",
    "max_position_weight", "max_position_ticker", "effective_positions",
    "top_sector", "top_sector_weight", "weighted_beta", "score_components",
    "component_assessments", "score_drivers", "coverage", "analysis_coverage",
    "portfolio_input", "holding_analysis", "weak_holdings", "diagnostics", "data_sources",
}
assert 0 <= evaluation["score"] <= 100
assert evaluation["score_components"] == {}
assessments = evaluation["component_assessments"]
assert set(assessments) == {"diversification", "risk", "quality", "signal", "trend", "macro"}
assert all(value in {"lower", "middle", "upper", None} for value in assessments.values())
assert 1 <= len(evaluation["score_drivers"]) <= 3
for driver in evaluation["score_drivers"]:
    assert set(driver) == {"component", "explanation"}
    assert driver["component"] in assessments and isinstance(driver["explanation"], str)
    assert driver["explanation"].strip()

positions = payload["positions"]
holdings = evaluation["holding_analysis"]
assert {row["ticker"] for row in holdings} == {row["ticker"] for row in positions}
for row in holdings:
    assert set(row) == {"ticker", "weight_pct", "sector", "signal", "signal_source"}
    assert set(row["signal_source"]) == {"status", "as_of_date"}
assert evaluation["weak_holdings"] == []
assert evaluation["analysis_coverage"]["analyzed_ticker_count"] == len(positions)
assert evaluation["portfolio_input"]["cash_balance"] == payload["cash_balance"]
assert evaluation["portfolio_input"]["holdings_value"] == sum(row["market_value"] for row in positions)
assert evaluation["diagnostics"]["risk_level"] == payload["risk_level"]
print("Public response sample matches the documented example request.")
