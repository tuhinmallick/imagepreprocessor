FROM python:3.7-buster@sha256:65f08bc4dfb68700010a2ea85fd385de826f624ede6349b05a65aa857456f987
EXPOSE 8501
WORKDIR /code
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
RUN bash setup_docker.sh
CMD ["streamlit", "run", "src/app.py"]
