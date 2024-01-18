# FastAPI + RQ

[FastAPI](https://fastapi.tiangolo.com/) application with [RQ](https://python-rq.org/) as a job
queue to handle "heavy" (for a REST API) operations.

In a very light setup, with a very friendly Python library causing minimal code changes, we can get
the benefits of a queue to process longer jobs in background.

## Notes

- We could even set a success/error callback to the jobs which posts a message to SNS, for example.
- This would work nicely with a decorator that runs heavy functions as jobs, and returns their id.
- The workers and the dashboard could be deployed to ECS as services. All they need is access to the
Redis database. The workers need the same environment as the API -- with the same Docker image as
the workers, the API can be hosted in Lambda.
  - In this setup, while the Lambda API scales "indefinitely", the workers might be a big
  bottleneck, as they only process one job at a time. Auto scaling this workers would be ideal.

## Questions

1. How can we take advantage os FastAPI's Response Models (responsible for validating and typing the API
responses, as well as generating OpenAPI specification which is fed to automatic docs) in this setup?
    1. Maybe, for fetching job outputs, we would need a different endpoint for each different response
    model. In case of success, we return 200 with the populated response model. In case of failure,
    return the appropriate status code and message.
2. How do we take advantage of FastAPI exception handlers to return the correct HTTP status codes
and error messages now that exceptions occur in the worker, and we only get a string with exception
info?
