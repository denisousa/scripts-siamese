FROM python:3.8-slim

WORKDIR /app

COPY . /app

RUN pip install -r /app/requirements.txt

EXPOSE 5000

CMD ["python", "main_grid.py"]
