FROM python:3.11
WORKDIR /log
COPY log.py .
RUN pip install requests
RUN pip install flask
ENV PYTHONUNBUFFERED=1
CMD ["python", "log.py"]