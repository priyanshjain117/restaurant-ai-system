# Use an official Python runtime as a parent image
FROM python:3.9

# Create a working directory
WORKDIR /code

# Copy requirements first to leverage Docker cache
COPY ./requirements.txt /code/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the rest of your application code
# This includes your 'models' folder and 'app.py'
COPY . .

# Set permissions for Hugging Face's user (UID 1000)
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

# Command to run the FastAPI app
# Note: Hugging Face expects the app on port 7860
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]