from ubuntu:16.04


RUN apt-get update && apt-get install -y \
    python3 \
    python3-setuptools \
    python3-pip


RUN pip install algorithmia==1.2.0 && \
    pip install requests==2.23.0

COPY entrypoint.py /entrypoint.py
COPY algorithmia_ci /algorithmia_ci
RUN chmod +x /entrypoint.py
ENTRYPOINT ["/entrypoint.py"]
