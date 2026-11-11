#!/usr/bin/env python3
import subprocess
from pathlib import Path

# Points to the directory where Docker containers are located (~/docker)
BASE_DIR = Path.home() / "docker"

def run_command(cmd, cwd=None):
    try:
        subprocess.run(cmd, check=True, cwd=cwd)
    except subprocess.CalledProcessError as e:
        print(f"\n[!] Command failed with exit code {e.returncode}: {' '.join(cmd)}\n")

def update_stacks():
    print(f"=== Starting Docker Updates in {BASE_DIR} ===\n")
    
    for item in sorted(BASE_DIR.iterdir()):
        if item.is_dir():
            # Check if directory contains a compose file
            has_compose = (item / "docker-compose.yml").exists() or (item / "compose.yaml").exists()
            
            if has_compose:
                print(f"--------------------------------------------------")
                print(f"  Updating stack: {item.name}")
                print(f"--------------------------------------------------")
                
                # Pull new images
                print(f"-> Pulling images for {item.name}...")
                run_command(["docker", "compose", "pull"], cwd=item)
                
                # Recreate containers if updated
                print(f"-> Starting containers for {item.name}...")
                run_command(["docker", "compose", "up", "-d"], cwd=item)
                print()

    # Step 3: Prune unused images globally
    print("--------------------------------------------------")
    print("  Pruning old dangling images...")
    print("--------------------------------------------------")
    run_command(["docker", "image", "prune", "-f"])
    
    print("\n=== All stacks updated and cleaned up successfully! ===")

if __name__ == "__main__":
    update_stacks()
