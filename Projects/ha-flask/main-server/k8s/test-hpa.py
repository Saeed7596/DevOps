import httpx
import threading
import time
import json
import random
from threading import Lock

URL = "http://<minikube-ip>:port"
DURATION = 60
CONCURRENT_THREADS = 10
VERIFY_SSL = False
REQUEST_TYPE = "GET"
LOG_FILE = "load_test_results.log"

results = {
    "total_requests": 0,
    "success": 0,
    "failures": 0,
    "response_times": [],
}

lock = Lock()

def send_requests():
    global results
    end_time = time.time() + DURATION
    while time.time() < end_time:
        try:
            start_time_req = time.time()
            with httpx.Client(verify=VERIFY_SSL) as client:
                response = client.get(URL) if REQUEST_TYPE == "GET" else client.post(URL)
                response_time = time.time() - start_time_req

            with lock:
                results["total_requests"] += 1
                if response.status_code == 200:
                    results["success"] += 1
                    results["response_times"].append(response_time)
                else:
                    results["failures"] += 1
        except Exception as e:
            with lock:
                results["failures"] += 1
            with open(LOG_FILE, "a") as log:
                log.write(f"Error: {e}\n")

        time.sleep(random.uniform(0.1, 0.5))

threads = []

start_time_test = time.time()
for _ in range(CONCURRENT_THREADS):
    t = threading.Thread(target=send_requests)
    threads.append(t)
    t.start()

for t in threads:
    t.join()

end_time_test = time.time()

if results["response_times"]:
    avg_time = sum(results["response_times"]) / len(results["response_times"])
    min_time = min(results["response_times"])
    max_time = max(results["response_times"])
else:
    avg_time = min_time = max_time = 0

results_summary = {
    "Total Requests": results["total_requests"],
    "Successful Requests": results["success"],
    "Failed Requests": results["failures"],
    "Average Response Time (s)": avg_time,
    "Minimum Response Time (s)": min_time,
    "Maximum Response Time (s)": max_time,
    "Total Time Elapsed (s)": end_time_test - start_time_test,
}

print(json.dumps(results_summary, indent=4))

with open(LOG_FILE, "w") as log:
    log.write("Load Test Results:\n")
    log.write(json.dumps(results_summary, indent=4))
