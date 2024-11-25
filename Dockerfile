FROM python:3.11-alpine

WORKDIR /app

COPY . .

# Set the environment variable for the Google application credentials
ENV GOOGLE_APPLICATION_CREDENTIALS=application-credentials.json

# Install dependencies
RUN pip install flask -r requirements.txt

EXPOSE 5000

CMD [ "python", "main.py" ]