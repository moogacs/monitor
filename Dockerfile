FROM python:3.8
WORKDIR /monitorSys
ADD ./requirements.txt ./
RUN pip install -r requirements.txt
COPY ./ /monitorSys
CMD ["python3","-u","./app.py"]