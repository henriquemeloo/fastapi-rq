FROM python:3.11-slim

RUN pip install rq-dashboard==0.6.7

ENTRYPOINT [ "rq-dashboard" ]
