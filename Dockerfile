FROM python:3.15.0a2-alpine3.22
WORKDIR /app
COPY targets-styled.py /app
COPY targets.json /app
RUN pip install flask
EXPOSE 5000
CMD ["chmod", "666", "targets.json"]
CMD ["python", "targets-styled.py"]