import os
import json
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple


DATA_DIR = "data"
WEARABLE_DIR = os.path.join(DATA_DIR, "wearables")


def _ensure_dirs() -> None:
	os.makedirs(WEARABLE_DIR, exist_ok=True)


def _safe_id(user_email: Optional[str], anon_id: Optional[str]) -> str:
	if user_email:
		return user_email.replace("@", "_at_").replace(".", "_dot_")
	return (anon_id or "anonymous").replace(":", "_")


def user_wearable_path(user_email: Optional[str], anon_id: Optional[str] = None) -> str:
	_ensure_dirs()
	return os.path.join(WEARABLE_DIR, f"wearables_{_safe_id(user_email, anon_id)}.json")


def load_user_wearables(user_email: Optional[str], anon_id: Optional[str] = None) -> Dict[str, Any]:
	path = user_wearable_path(user_email, anon_id)
	if not os.path.exists(path):
		return {"consent": False, "providers": {}, "records": []}
	with open(path, "r", encoding="utf-8") as f:
		return json.load(f)


def save_user_wearables(user_email: Optional[str], data: Dict[str, Any], anon_id: Optional[str] = None) -> None:
	_ensure_dirs()
	path = user_wearable_path(user_email, anon_id)
	with open(path, "w", encoding="utf-8") as f:
		json.dump(data, f, indent=2)


def set_consent(user_email: Optional[str], consent: bool, anon_id: Optional[str] = None) -> Dict[str, Any]:
	data = load_user_wearables(user_email, anon_id)
	data["consent"] = bool(consent)
	data["consent_updated_at"] = datetime.utcnow().isoformat()
	save_user_wearables(user_email, data, anon_id)
	return data


def clear_user_wearables(user_email: Optional[str], anon_id: Optional[str] = None) -> None:
	path = user_wearable_path(user_email, anon_id)
	if os.path.exists(path):
		os.remove(path)


def append_records(user_email: Optional[str], new_records: List[Dict[str, Any]], provider: str, anon_id: Optional[str] = None) -> Dict[str, Any]:
	data = load_user_wearables(user_email, anon_id)
	if not data.get("consent"):
		raise PermissionError("Consent is required before storing wearable data.")
	# Normalize timestamps and provider
	normalized: List[Dict[str, Any]] = []
	for rec in new_records:
		if "timestamp" not in rec:
			continue
		try:
			parsed = datetime.fromisoformat(str(rec["timestamp"]).replace("Z", "+00:00"))
			rec_ts = parsed.isoformat()
		except Exception:
			rec_ts = str(rec["timestamp"])
		normalized.append({
			"timestamp": rec_ts,
			"provider": provider,
			"hrv_ms": rec.get("hrv_ms"),
			"resting_hr": rec.get("resting_hr"),
			"sleep_minutes": rec.get("sleep_minutes"),
			"sleep_efficiency": rec.get("sleep_efficiency"),
			"steps": rec.get("steps"),
			"active_minutes": rec.get("active_minutes"),
		})
	existing = {(r.get("timestamp"), r.get("provider")): i for i, r in enumerate(data.get("records", []))}
	for rec in normalized:
		key = (rec.get("timestamp"), rec.get("provider"))
		if key in existing:
			idx = existing[key]
			merged = {**data["records"][idx], **{k: v for k, v in rec.items() if v is not None}}
			data["records"][idx] = merged
		else:
			data.setdefault("records", []).append(rec)
	data.setdefault("providers", {}).setdefault(provider, {"connected": False})
	data["updated_at"] = datetime.utcnow().isoformat()
	save_user_wearables(user_email, data, anon_id)
	return data


def set_provider_connection(user_email: Optional[str], provider: str, connected: bool, anon_id: Optional[str] = None) -> Dict[str, Any]:
	data = load_user_wearables(user_email, anon_id)
	data.setdefault("providers", {}).setdefault(provider, {})["connected"] = bool(connected)
	data["updated_at"] = datetime.utcnow().isoformat()
	save_user_wearables(user_email, data, anon_id)
	return data


def set_goals(email: str, goals: dict, anon_id: Optional[str] = None) -> Dict[str, Any]:
    """Saves user-defined goals."""
    user_data = load_user_wearables(email, anon_id)
    user_data["goals"] = goals
    user_data["goals_updated_at"] = datetime.utcnow().isoformat()
    save_user_wearables(email, user_data, anon_id)
    return user_data
