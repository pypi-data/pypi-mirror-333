import os
import subprocess
import threading
import time

class GPUScheduler:
    def __init__(self, log_dir="./logs"):
        self.mig_devices = []
        self.total_jobs = []
        self.running_jobs = {}
        self.completed_jobs = set()
        self.log_dir = log_dir
        os.makedirs(self.log_dir, exist_ok=True)

    def set_mig_devices(self, mig_devices):
        """ Set available MIG devices dynamically. """
        self.mig_devices = mig_devices

    def add_job(self, job_id, command):
        """ Add a job to the queue. """
        self.total_jobs.append((job_id, command))

    def start_job(self, job_id, command, mig_id):
        """ Start a job on a specific MIG device. """
        log_file = os.path.join(self.log_dir, f"{job_id}_mig_{mig_id}.log")
        full_command = f"CUDA_VISIBLE_DEVICES={mig_id} {command} > {log_file} 2>&1 &"
        subprocess.Popen(full_command, shell=True)
        self.running_jobs[mig_id] = (job_id, log_file)
        print(f"🚀 Started Job {job_id} on {mig_id}, logging to {log_file}")

    def run(self):
        """ Start the first batch of jobs based on available MIG devices. """
        for i in range(min(len(self.mig_devices), len(self.total_jobs))):
            job_id, command = self.total_jobs.pop(0)
            self.start_job(job_id, command, self.mig_devices[i])
