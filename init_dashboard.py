import os
import subprocess

def initialize_grafana():
    # print("Initializing Grafana dashbord...")
    subprocess.run(["pipenv", "run", "python", "grafana/init.py"], check=True)
    return "Successful"

# Define your flow
def main_flow():
    initialize_grafana_result = initialize_grafana()
    print("Grafana initialized:", initialize_grafana_result)

# Run the flow
if __name__ == "__main__":
    main_flow()
