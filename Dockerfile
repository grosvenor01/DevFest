from python:3.11.10-slim-bullseye

WORKDIR /app 

COPY rqts.txt rqts.txt

RUN pip install -r rqts.txt

COPY . .
CMD ["python" , "manage.py" , "runserver" , "0.0.0.0:8000"]
