import requests
state = {
    "uuid": "123",
    "day": 1,
    "health_status": {"hardware": 100, "system": 100, "storage": 100, "software": 100},
    "attributes": {"wealth": 1000, "cyber_sense": 0, "mental_state": 100},
    "inventory": [],
    "hidden_flags": {"net_assoc_trust": 0, "scam_counter": 0, "machine_flags": [], "history_tags": []}
}

req = requests.post('http://127.0.0.1:8000/api/event/next', json={'state': state, 'event_type': 'routine'})
data = req.json()
print("Event fetched:", req.status_code)

res = requests.post('http://127.0.0.1:8000/api/action/resolve', json={'state': data['state'], 'event': data['event'], 'option_id': data['event']['options'][0]['option_id']})
print("Action resolved:", res.status_code, res.text)
