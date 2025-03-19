import os
import time

def check_job_completion(log_file, success_criteria):
    """ Check if a job is completed by scanning its log file. """
    if os.path.exists(log_file):
        with open(log_file, "r") as f:
            logs = f.read()
            return success_criteria(logs)
    return False

def monitor_jobs(scheduler, success_criteria):
    """ Monitor running jobs, free MIG devices, and assign new jobs dynamically. """
    while scheduler.total_jobs or scheduler.running_jobs:
        completed_migs = []

        for mig_id, (job_id, log_file) in list(scheduler.running_jobs.items()):
            if check_job_completion(log_file, success_criteria):
                print(f"✅ Job {job_id} on {mig_id} completed. Freeing up MIG device.")
                completed_migs.append(mig_id)
                scheduler.completed_jobs.add(job_id)
                del scheduler.running_jobs[mig_id]

        # Assign new jobs to free MIG devices
        for mig_id in completed_migs:
            if scheduler.total_jobs:
                next_job_id, next_command = scheduler.total_jobs.pop(0)
                scheduler.start_job(next_job_id, next_command, mig_id)

        time.sleep(5)  # Poll every 5 seconds

    print(f"🎉 All jobs completed successfully!")
