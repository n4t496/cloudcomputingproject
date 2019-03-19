FROM python:3.7-alpine
WORKDIR /myapp
COPY . /myapp
RUN pip install -r requirements.txt
RUN pip install requests
EXPOSE 80
CMD ["python", "myapp.py"]
