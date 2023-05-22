FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt install-redis.sh /app/
RUN pip3 install -r requirements.txt
COPY /src /app/
RUN chmod +x ./install-redis.sh && sh ./install-redis.sh

#ENTRYPOINT ["python3"] 
#CMD ["main.py"]

ENTRYPOINT ["tail", "-f", "/dev/null"]