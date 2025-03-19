import os
import argparse
from migmanager.scheduler import GPUScheduler
from migmanager.monitor import monitor_jobs
from migmanager.utils import get_available_mig_devices

def main():
    # Load user-defined parameters
    parser = argparse.ArgumentParser(description="Run MIG-based GPU jobs dynamically.")
    parser.add_argument("--jobs", type=int, default=12, help="Total number of jobs to run.")
    parser.add_argument("--gpu-auto-detect", action="store_true", help="Auto-detect available MIG devices.")
    parser.add_argument("--log-dir", type=str, default="./logs", help="Directory for log files.")
    parser.add_argument("--command", type=str, required=True, help="Command to run on GPUs.")

    args = parser.parse_args()

    # Detect MIG devices dynamically
    if args.gpu_auto_detect:
        MIG_DEVICES = get_available_mig_devices()
        if not MIG_DEVICES:
            raise RuntimeError("No MIG devices detected. Please check your setup.")
    else:
        MIG_DEVICES = os.getenv("MIG_DEVICES", "").split(",") if os.getenv("MIG_DEVICES") else []

    # Initialize GPU Scheduler
    scheduler = GPUScheduler(log_dir=args.log_dir)
    scheduler.set_mig_devices(MIG_DEVICES)

    # Add jobs dynamically
    for job_id in range(1, args.jobs + 1):
        scheduler.add_job(job_id, args.command)

    # Start first batch of jobs
    scheduler.run()

    # Define job completion success criteria
    def success_criteria(log_contents):
        return "Saved to output_test_metro" in log_contents or "Job completed successfully" in log_contents

    # Start monitoring for remaining jobs
    monitor_jobs(scheduler, success_criteria)

# Ensure script runs correctly when called as CLI
if __name__ == "__main__":
    main()
