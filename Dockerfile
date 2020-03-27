from ubuntu:16.04


RUN apt-get update && apt-get install -y \
    python3 \
    python3-setuptools \
    python3-pip


RUN pip3 install algorithmia==1.2.1 && \
    pip3 install algorithmia-api-client==1.1.0
    pip3 install requests==2.23.0

COPY entrypoint.py /entrypoint.py
COPY algorithmia_ci /algorithmia_ci
RUN chmod +x /entrypoint.py
ENTRYPOINT ["/entrypoint.py"]
