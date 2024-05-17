FROM selenium/standalone-chrome:125.0
WORKDIR /app
USER root

# install python
RUN apt-get update && apt-get install -y
RUN sudo apt install software-properties-common wget
RUN wget https://www.python.org/ftp/python/3.11.1/Python-3.11.1.tar.xz
RUN sudo tar -xf Python-3.11.1.tar.xz
RUN cd Python-3.11.1
RUN sudo ./configure --enable-optimizations
RUN sudo make altinstall

# project
RUN mkdir google-search-info
RUN cd google-search-info
COPY . .
RUN pip3 install --no-cache-dir -r requirements.txt
EXPOSE 9000
CMD ["python3", "app.py"]
