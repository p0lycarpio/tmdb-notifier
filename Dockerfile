FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt /app
RUN pip3 install -r requirements.txt
COPY . /app/
RUN chmod +x ./install-redis.sh && sh ./install-redis.sh

ENTRYPOINT ["python3"] 
CMD ["src/main.py"]