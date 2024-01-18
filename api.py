from time import sleep
from random import random

from fastapi import FastAPI, HTTPException
from redis import Redis
from rq import Queue
from rq.decorators import job


app = FastAPI()
rq_queue = Queue(connection=Redis(host="redis"))


@job(rq_queue)
def _heavy_work(n: int):
    print("Doing some heavy work that might fail...")
    sleep(n)
    if random() < .3:
        raise RuntimeError("Oops...")
    print("Done")
    return f"Heavy work done for {n} seconds"


@app.post("/job")
def create_job(delay: int):
    job = _heavy_work.delay(delay)
    return {
        "job_id": job.id,
    }


@app.get("/job/{job_id}")
def get_job_status(job_id: str):
    job = rq_queue.fetch_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    if job.get_status() == "failed":
        raise HTTPException(
            status_code=500,
            detail=f"Job failed with exception: {job.exc_info}")

    if job.get_status() != "finished":
        return {
            "status": job.get_status()
        }

    return {
        "status": job.get_status(),
        "result": job.result
    }
