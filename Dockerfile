FROM python
WORKDIR /project
ADD . /project
RUN pip install -r requirements.txt
CMD ["python","app.py"]