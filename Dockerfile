FROM python:3
WORKDIR /data
COPY requirements.txt /data/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /data/
RUN python manage.py migrate
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
