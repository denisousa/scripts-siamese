FROM python:3.8-slim

WORKDIR /siamese-experiment

COPY . /siamese-experiment

RUN pip install -r /siamese-experiment/requirements.txt

RUN mkdir -p dados

#VOLUME /siamese-experiment/dados

EXPOSE 5000

CMD ["python", "main_grid.py"]
