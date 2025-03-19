import subprocess
import re

def get_available_mig_devices():
    """
    Detect available MIG devices using `nvidia-smi -L`.
    
    Returns:
        List of available MIG device UUIDs.
    """
    try:
        result = subprocess.run(["nvidia-smi", "-L"], capture_output=True, text=True)
        devices = []
        for line in result.stdout.split("\n"):
            match = re.search(r"(MIG-[\w-]+)", line)  # Extract MIG device IDs
            if match:
                devices.append(match.group(1))
        if not devices:
            print("⚠️ Warning: No MIG devices detected via nvidia-smi.")
        return devices
    except Exception as e:
        print(f"⚠️ Error detecting MIG devices: {e}")
        return []

def check_mig_usage():
    """Check currently free MIG devices dynamically."""
    try:
        result = subprocess.run(["nvidia-smi", "pmon", "-c", "1"], capture_output=True, text=True)
        busy_migs = set(re.findall(r"(MIG-[\w-]+)", result.stdout))
        all_migs = set(get_available_mig_devices())
        return list(all_migs - busy_migs)
    except Exception as e:
        print(f"⚠️ Error checking MIG usage: {e}")
        return []

def is_mig_available(mig_id):
    """Check if a specific MIG device is free."""
    return mig_id in check_mig_usage()


import subprocess
import re

def get_cuda_index_from_mig(mig_id):
    """
    Convert a MIG UUID to its corresponding CUDA device index.
    """
    try:
        result = subprocess.run(["nvidia-smi", "--query-gpu=index,name,uuid", "--format=csv,noheader"], 
                                capture_output=True, text=True)
        for line in result.stdout.split("\n"):
            parts = line.split(", ")
            if len(parts) == 3 and parts[2] == mig_id:
                return parts[0]  # Return the CUDA index corresponding to MIG UUID
    except Exception as e:
        print(f"⚠️ Error mapping MIG device: {e}")
    
    return None  # If mapping fails
