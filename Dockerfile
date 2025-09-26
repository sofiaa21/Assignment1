FROM ubuntu:24.04

# Install Python 3, pip, and venv
RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-venv build-essential && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . /app

# Create and activate virtual environment, install pycryptodome
RUN python3 -m venv /venv && \
    /venv/bin/pip install --no-cache-dir pycryptodome

# Use the virtual environment's Python to run both tests
CMD /venv/bin/python aes_ctr.py && /venv/bin/python ind-cca_test.py