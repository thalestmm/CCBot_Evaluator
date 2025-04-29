import logging
import subprocess
import os
import sys
from typing import Tuple

logging.basicConfig(level=logging.INFO)

DELIVERABLES_DIR = "./deliverables"

def main_run(filepath: str):
    res = subprocess.run([sys.executable, filepath, "config/run_config.yaml", "results/output.csv"],
                          capture_output=True, text=True)
    return res

def test_run(filepath: str) -> Tuple[bool, int]:
    # Test 1: Verify file doesn't overwrite the CSV file
    orig_len = len(open("config/test.csv").readlines())
    subprocess.run([sys.executable, filepath, "config/test_config.yaml", "config/test.csv"])
    new_len = len(open("config/test.csv").readlines())

    if new_len != orig_len + 1:
        return False, 1

    # Test 2: Verify data types appended to the CSV file
    with open("config/test.csv") as f:
        lines = f.readlines()
        added_line = lines[-1]
        score = added_line.split(",")[1]
        try:
            score = float(score)
        except ValueError:
            return False, 2

    return True, 0



for filename in os.listdir(DELIVERABLES_DIR):
    if filename.endswith('.py'):
        file_path = os.path.join(DELIVERABLES_DIR, filename)
        logging.info(f"Running {filename}...")

        test_result = test_run(file_path)
        if not test_result[0]:
            logging.error(f"File {filename} failed on test {test_result[1]}")
            break

        result = main_run(file_path)

        if result.stderr:
            logging.error(f"Error from {filename}: {result.stderr}")