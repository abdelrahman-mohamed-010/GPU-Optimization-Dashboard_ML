FROM python:3.8-slim

RUN pip install numpy pandas

COPY simulate_cluster.py /simulate_cluster.py

WORKDIR /

ENTRYPOINT ["python3", "/simulate_cluster.py"]