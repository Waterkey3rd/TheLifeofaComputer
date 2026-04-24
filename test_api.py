import requests

res = requests.post("http://localhost:8000/api/event/next", json={"state": {"day": 1, "attributes": {"mental_state": 100, "wealth": 100, "cyber_sense": 10}, "health_status": {"hardware": 100, "system": 100, "storage": 100, "software": 100, "hardware_details": {"cpu": 100, "ram": 100, "disk": 100, "screen": 100, "fan": 100, "shell": 100}}, "hidden_flags": {"history_tags": []}}, "event_type": "routine"})
print(res.status_code)
print(res.text)

res2 = requests.post("http://localhost:8000/api/event/next/")
print("with slash:", res2.status_code)

res3 = requests.post("http://localhost:8000//api/event/next")
print("double slash:", res3.status_code)
