FROM python:3.10

# Ensure Python outputs are unbuffered (good for logging in Docker)
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app


COPY . .

RUN pip install --no-cache-dir -r requirements.txt

# No need to expose a port since it's a worker
CMD ["python", "app.py"]
