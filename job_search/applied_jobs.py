import json
import os


APPLIED_FILE = "applied_jobs.json"


def load_applied_jobs():
    if not os.path.exists(APPLIED_FILE):
        return set()

    with open(APPLIED_FILE, "r") as f:
        return set(json.load(f))


def save_applied_job(job_id):
    applied = load_applied_jobs()
    applied.add(job_id)

    with open(APPLIED_FILE, "w") as f:
        json.dump(list(applied), f)


def is_applied(job_id):
    return job_id in load_applied_jobs()