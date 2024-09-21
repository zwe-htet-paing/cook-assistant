from prefect import flow, task
import os
import subprocess

@task
def prepare_database():
    # print("Preparing the database...")
    subprocess.run(["pipenv", "run", "python", "src/db_prep.py"], check=True)
    return "Successful"

# Define your flow
@flow
def main_flow():
    prepare_database_result = prepare_database()
    print("Database prepared:", prepare_database_result)

# Run the flow
if __name__ == "__main__":
    main_flow()
