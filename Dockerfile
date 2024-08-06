FROM python:3.12.3

RUN mkdir /app
 
WORKDIR /app
 
COPY ./requirements.txt /app/requirements.txt
 
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
 
COPY ./src /app/src

CMD ["uvicorn", "app.src.main.main:app", "--reload"]