# Load Testing Scripts in Python

This document provides detailed documentation for three Python scripts designed for load testing servers. Each script is progressively enhanced to support different functionalities, such as handling HTTPS requests, measuring performance metrics, and increasing test concurrency. The scripts are categorized as follows:

1. **Basic Load Testing Script**
2. **HTTPS Load Testing Script**
3. **Advanced Load Testing Script**

---

## 1. Basic Load Testing Script

### Description
This script performs a simple load test by sending multiple HTTP requests to a server. It uses a single thread and measures response times for analysis.

### Features
- Sends HTTP GET requests to a specified server.
- Measures response time for each request.
- Logs failures in case of connection errors.

### Code
```python
import requests
import time

# Configuration
URL = "http://yourserver.com"  # Replace with your server's URL
NUM_REQUESTS = 1000  # Total number of requests to send

# Statistics
success_count = 0
failure_count = 0
response_times = []

# Sending requests
for _ in range(NUM_REQUESTS):
    try:
        start_time = time.time()
        response = requests.get(URL)
        response_time = time.time() - start_time

        if response.status_code == 200:
            success_count += 1
            response_times.append(response_time)
        else:
            failure_count += 1
    except Exception as e:
        failure_count += 1
        print(f"Request failed: {e}")

# Results
print(f"Total Requests: {NUM_REQUESTS}")
print(f"Successful Requests: {success_count}")
print(f"Failed Requests: {failure_count}")
if response_times:
    print(f"Average Response Time: {sum(response_times) / len(response_times):.2f} seconds")
```

### Usage
1. Replace `http://yourserver.com` with the target server URL.
2. Run the script to observe results in the console.

---

## 2. HTTPS Load Testing Script

### Description
This script builds upon the basic script by adding support for HTTPS requests. It also allows users to ignore SSL certificate validation for testing purposes.

### Features
- Supports HTTPS requests.
- Allows disabling SSL verification for self-signed or invalid certificates.

### Code
```python
import requests
import time

# Configuration
URL = "https://yourserver.com"  # Replace with your HTTPS server's URL
NUM_REQUESTS = 1000  # Total number of requests to send
VERIFY_SSL = False  # Set to True to verify SSL certificates

# Statistics
success_count = 0
failure_count = 0
response_times = []

# Sending requests
for _ in range(NUM_REQUESTS):
    try:
        start_time = time.time()
        response = requests.get(URL, verify=VERIFY_SSL)
        response_time = time.time() - start_time

        if response.status_code == 200:
            success_count += 1
            response_times.append(response_time)
        else:
            failure_count += 1
    except Exception as e:
        failure_count += 1
        print(f"Request failed: {e}")

# Results
print(f"Total Requests: {NUM_REQUESTS}")
print(f"Successful Requests: {success_count}")
print(f"Failed Requests: {failure_count}")
if response_times:
    print(f"Average Response Time: {sum(response_times) / len(response_times):.2f} seconds")
```

### Usage
1. Replace `https://yourserver.com` with the target HTTPS server URL.
2. Set `VERIFY_SSL` to `False` if the server uses a self-signed certificate.
3. Run the script to observe results in the console.

---

## 3. Advanced Load Testing Script

### Description
This advanced script is designed for concurrent load testing with multiple threads. It supports both HTTP and HTTPS requests, collects detailed performance metrics, and logs results for further analysis.

### Features
- Supports concurrent requests using threads.
- Handles both GET and POST requests.
- Collects detailed metrics (average, minimum, and maximum response times).
- Logs results and errors to a file.

### Code
```python
import httpx
import threading
import time
import json

# Configuration
URL = "https://yourserver.com"  # Replace with your server's URL
NUM_REQUESTS = 1000  # Total number of requests to send
CONCURRENT_THREADS = 10  # Number of concurrent threads
VERIFY_SSL = False  # Set to True to verify SSL certificates
REQUEST_TYPE = "GET"  # Type of request: GET or POST
POST_DATA = {"key": "value"}  # Data for POST requests (if needed)
LOG_FILE = "load_test_results.log"  # Log file path

# Statistics
results = {
    "total_requests": 0,
    "success": 0,
    "failures": 0,
    "response_times": [],
}

# Request function
def send_requests():
    global results
    for _ in range(NUM_REQUESTS // CONCURRENT_THREADS):
        try:
            start_time = time.time()
            with httpx.Client(verify=VERIFY_SSL) as client:
                if REQUEST_TYPE.upper() == "POST":
                    response = client.post(URL, json=POST_DATA)
                else:  # Default to GET
                    response = client.get(URL)
                response_time = time.time() - start_time

                results["total_requests"] += 1
                if response.status_code == 200:
                    results["success"] += 1
                    results["response_times"].append(response_time)
                else:
                    results["failures"] += 1
        except Exception as e:
            results["failures"] += 1
            with open(LOG_FILE, "a") as log:
                log.write(f"Error: {e}\n")

# Running the test
start_time = time.time()
threads = []

for _ in range(CONCURRENT_THREADS):
    thread = threading.Thread(target=send_requests)
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

end_time = time.time()

# Final metrics
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
    "Total Time Elapsed (s)": end_time - start_time,
}

# Print and log results
print(json.dumps(results_summary, indent=4))

with open(LOG_FILE, "w") as log:
    log.write("Load Test Results:\n")
    log.write(json.dumps(results_summary, indent=4))
```

### Usage
1. Replace `https://yourserver.com` with the target server URL.
2. Set `REQUEST_TYPE` to either `GET` or `POST`.
3. Adjust `NUM_REQUESTS` and `CONCURRENT_THREADS` based on your load testing requirements.
4. Run the script to generate results and logs.

---

## Comparison of Scripts

| Feature                         | Basic Script | HTTPS Script | Advanced Script |
|---------------------------------|--------------|--------------|-----------------|
| Supports HTTPS                 | No           | Yes          | Yes             |
| Concurrent Requests            | No           | No           | Yes             |
| Detailed Metrics               | Partial      | Partial      | Yes             |
| Supports POST Requests         | No           | No           | Yes             |
| Logs Results                   | No           | No           | Yes             |

