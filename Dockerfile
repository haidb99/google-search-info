FROM selenium/standalone-chrome:125.0
WORKDIR /app
USER root

# install python
COPY . .
RUN pip3 install --no-cache-dir -r requirements.txt
EXPOSE 9000
CMD ["python3", "app.py"]
