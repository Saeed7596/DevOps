import time
import json
import subprocess

MONGO_HOST = "mongodb://url"
ZABBIX_SERVER = "zabbix-server-or-proxy-ip"
ZABBIX_HOST = "host-name"
ZABBIX_ITEM = "mongodb_status"
SLOW_OPS_JS = "/home/monitoring/mongodb_status_slow_ops.js"
SERVER_STATUS_JS = "/home/monitoring/mongodb_status_server_status.js"

DATA = {
    "slow_ops": [],
    "slow_ops_count": 0,
    "serverStatus": None,
}

def update_slow_ops():
    global DATA
    try:
        result = subprocess.run(['mongosh', MONGO_HOST, '--quiet', '--file', SLOW_OPS_JS],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            print("Error: Unable to retrieve MongoDB slow operations")
            return None

        try:
            NEW_DATA = json.loads(result.stdout)
            if "slow_ops" in NEW_DATA:
                DATA["slow_ops"].extend(NEW_DATA["slow_ops"])
                DATA["slow_ops_count"] = len(DATA["slow_ops"])
            else:
                print("Warning: 'slow_ops' key not found in the retrieved data")
        except json.JSONDecodeError as e:
            print(f"JSON parsing error in update_slow_ops: {e}")
            return None

    except Exception as e:
        print(f"Error in update_slow_ops: {str(e)}")


def update_server_status():
    global DATA
    try:
        result = subprocess.run(['mongosh', MONGO_HOST, '--quiet', '--file', SERVER_STATUS_JS],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            print("Error: Unable to retrieve MongoDB server status")
            return None

        try:
            NEW_DATA = json.loads(result.stdout)
            if "serverStatus" in NEW_DATA:
                DATA["serverStatus"] = NEW_DATA["serverStatus"]
            else:
                print("Warning: 'serverStatus' key not found in the retrieved data")
        except json.JSONDecodeError as e:
            print(f"JSON parsing error in update_server_status: {e}")
            return None

    except Exception as e:
        print(f"Error in update_server_status: {str(e)}")

def send_to_zabbix():
    try:
        json_data = json.dumps(DATA)

        result = subprocess.run(
            ['zabbix_sender', '-z', ZABBIX_SERVER, '-s', ZABBIX_HOST, '-k', ZABBIX_ITEM, '-o', json_data],
            check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )

        if result.returncode == 0:
            print("Data sent to Zabbix successfully")
        else:
            print(f"Error: Failed to send data to Zabbix. Return code: {result.returncode}")
            print(f"stderr: {result.stderr}")

    except subprocess.CalledProcessError as e:
        print(f"Error sending data to Zabbix: {str(e)}")
        print(f"stderr: {e.stderr}")


def main():
    global DATA
    start_time = time.time()
    while True:
        update_slow_ops()

        if time.time() - start_time >= 60:
            update_server_status()
            send_to_zabbix()
            DATA={
                "slow_ops": [],
                "slow_ops_count": 0,
                "serverStatus": None,
            }
            start_time = time.time()

        time.sleep(1)

if __name__ == "__main__":
    main()
