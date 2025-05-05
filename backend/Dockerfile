FROM python:3.9

WORKDIR /app

COPY requirements.txt .  
RUN ls -l requirements.txt  # Debug: Check if file exists

RUN pip install --no-cache-dir -r requirements.txt

COPY . .  
EXPOSE 5000

CMD ["python", "run_code.py"]
