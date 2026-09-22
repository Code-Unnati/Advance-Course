FROM python:3.11-slim
WORKDIR /app
# Copy only the dependency list first, so Docker can cache this layer and skip reinstalling packages on every build unless requirements.txt itself has changed.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Now copy the rest of the application code.
COPY . .
EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
