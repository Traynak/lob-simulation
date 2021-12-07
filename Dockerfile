FROM python:3.7-slim

RUN pip install -r requirements.txt

ENTRYPOINT [ "python" ]
CMD [ "alerts.py" ]