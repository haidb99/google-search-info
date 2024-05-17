FROM selenium/standalone-chrome:125.0
WORKDIR /app
USER root

# install python
RUN apt-get update && \
    apt-get install -y software-properties-common wget build-essential libssl-dev zlib1g-dev \
    libncurses5-dev libnss3-dev libreadline-dev libffi-dev curl && \
    wget https://www.python.org/ftp/python/3.11.1/Python-3.11.1.tar.xz && \
    tar -xf Python-3.11.1.tar.xz && \
    cd Python-3.11.1 && \
    ./configure --enable-optimizations && \
    make altinstall && \
    rm -rf /var/lib/apt/lists/* && \
    rm /app/Python-3.11.1.tar.xz \
    cd /app
# project
RUN mkdir google-search-info
RUN cd google-search-info
COPY . .
RUN pip3 install --no-cache-dir -r requirements.txt
EXPOSE 9000
CMD ["python3", "app.py"]
