FROM python:3.7

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

WORKDIR /app/sudoku

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
