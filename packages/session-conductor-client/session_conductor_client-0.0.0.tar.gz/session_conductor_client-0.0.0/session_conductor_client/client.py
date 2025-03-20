import threading
import time
import requests
import schedule


class SessionConductorClient:
    def __init__(self,module_name,module_key,session_conductor_url,heartbeat_interval=30):
        self.module_name = module_name
        self.module_key = module_key
        self.session_conductor_url = session_conductor_url
        self.heartbeat_interval = heartbeat_interval
        self.running = False
        self.thread = None

    def register_module(self):
        payload = {"module_name":self.module_name,"module_key":self.module_key}
        url = f"{self.session_conductor_url}/register-module"
        try:
            response =  requests.post(url,json=payload,timeout=5)
            if response.status_code == 200:
                print(f"[SessionConductor] Registered: {response.json()}")
            else:
                print(f"[SessionConductor] Registration failed: {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"[SessionConductor] Error registering module: {e}")

    def send_heartbeat(self):
        payload = {"module_name": self.module_name, "module_key": self.module_key}
        url = f"{self.session_conductor_url}/update-heartbeat"
        try:
            response = requests.post(url, json=payload, timeout=5)
            if response.status_code == 200:
                print(f"[SessionConductor] Heartbeat sent: {response.json()}")
            else:
                print(f"[SessionConductor] Heartbeat failed: {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"[SessionConductor] Error sending heartbeat: {e}")

    def start_heartbeat(self):
        if self.running:
            return

        self.running = True
        schedule.every(self.heartbeat_interval).seconds.do(self.send_heartbeat())

        def run_scheduler():
            while self.running:
                schedule.run_pending()
                time.sleep(1)

        self.thread = threading.Thread(target=run_scheduler(),daemon=True)
        self.thread.start()

    def stop_heartbeat(self):
        self.running = False
        if self.thread:
            self.thread.join()