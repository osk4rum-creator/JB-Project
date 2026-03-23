import json
import os
import subprocess
from pydantic import BaseModel, Field, ValidationError
from src.machine import Machine
from src.logger import logger

class VMConfig(BaseModel):
    name: str = Field(..., min_length=1)
    os: str = Field(..., pattern="^(Ubuntu|CentOS)$")
    cpu: str = Field(..., pattern=r"^\d+vCPU$")
    ram: str = Field(..., pattern=r"^\d+GB$")

def get_bash_path():
    """Tries to find the bash executable on Windows."""
    paths = [
        r"C:\Program Files\Git\bin\bash.exe",
        r"C:\Program Files\Git\usr\bin\bash.exe",
        "bash" # Last resort: hope it's in the PATH
    ]
    for path in paths:
        if os.path.exists(path) or path == "bash":
            return path
    return None

def run_provisioning_script():
    """Executes the Bash script and logs the results."""
    bash_exec = get_bash_path()
    script_path = "scripts/setup_nginx.sh"
    
    if not os.path.exists(script_path):
        logger.error(f"Script not found: {script_path}")
        print(f"[ERROR] {script_path} is missing!")
        return

    logger.info(f"Using bash from: {bash_exec}")
    try:
        # Running the bash script via subprocess
        result = subprocess.run(
            [bash_exec, script_path], 
            check=True, 
            capture_output=True, 
            text=True
        )
        logger.info(f"Bash Output: {result.stdout.strip()}")
        print("[SUCCESS] Service installation complete.")
    except Exception as e:
        logger.error(f"Failed to run bash script: {e}")
        print(f"[ERROR] Could not run bash script. Check logs.")

def main():
    machines = []
    print("--- Infrastructure Provisioning Simulator ---")
    
    while True:
        name = input("\nEnter machine name (or 'done'): ").strip()
        if name.lower() == 'done': break
        
        vm_data = {
            "name": name,
            "os": input("OS (Ubuntu/CentOS): ").strip(),
            "cpu": input("CPU (e.g. 2vCPU): ").strip(),
            "ram": input("RAM (e.g. 4GB): ").strip()
        }
        try:
            val = VMConfig(**vm_data)
            new_machine = Machine(**val.dict())
            machines.append(new_machine.to_dict())
            logger.info(f"Added: {name}")
        except ValidationError as e:
            print(f"Invalid input: {e.errors()[0]['msg']}")

    if machines:
        os.makedirs('configs', exist_ok=True)
        with open("configs/instances.json", "w") as f:
            json.dump(machines, f, indent=4)
        run_provisioning_script()

if __name__ == "__main__":
    main()