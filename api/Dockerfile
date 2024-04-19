FROM python:3.6
WORKDIR /api
COPY ./requirements.txt /api/requirements.txt
RUN pip install -r requirements.txt
COPY ./main.py /usr/share/nginx/api 
CMD [ "uvicorn", "main:app", "--host" "0.0.0.0", "--port", "8000" ]