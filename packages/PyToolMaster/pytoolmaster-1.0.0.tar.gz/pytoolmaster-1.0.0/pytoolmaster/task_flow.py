import schedule
import time
import subprocess

class Task:
    def __init__(self, name):
        self.name = name
        self.interval = None
    
    def every(self, interval):
        self.interval = interval
        return self
    
    def run(self, script_path):
        if self.interval.endswith("h"):
            schedule.every(int(self.interval[:-1])).hours.do(subprocess.run, ["python", script_path])
        elif self.interval.endswith("m"):
            schedule.every(int(self.interval[:-1])).minutes.do(subprocess.run, ["python", script_path])
        
        while True:
            schedule.run_pending()
            time.sleep(1)