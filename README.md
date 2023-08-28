# Social Media Application

This repository contains the code for your Django application, along with Docker Compose configuration to run it using Docker containers.

## Prerequisites

Before you begin, ensure you have the following installed:

- Docker: [Install Docker](https://docs.docker.com/get-docker/)
- Docker Compose: [Install Docker Compose](https://docs.docker.com/compose/install/)

## Getting Started

Follow these steps to run your Django application using Docker:

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/avinashravi96/social_media.git
   cd social_media
2. Build and start the Docker containers:
    ```
    docker-compose build
    docker-compose up
    ```
3. Access the Social Media application in a web browser at http://localhost:8000.

4. To stop the containers, press Ctrl + C, and then run:
    ```
    docker-compose down
    ```
5. Django Admin
To access the Django admin interface, you need to create a superuser:
    ```
    docker-compose exec web python manage.py createsuperuser
    ```
6. Follow the prompts to create a superuser account.
7. Access the Django admin interface at http://localhost:8000/admin/.
8. Postman Documentation:
https://documenter.getpostman.com/view/6060124/2s9Y5ZuMXx

Note: For all the API request use login api to generate token
Add Authorization as header in request with sample payload like below:
```
curl --location 'http://127.0.0.1:8000/api/users/search?q=test' \
--header 'Authorization: Token f76f8405a04491bc387f9291cb18ec961e1c89f6'
```
## Signup API Payload
```
curl --location 'http://127.0.0.1:8000/api/signup' \
--header 'Content-Type: application/json' \
--data-raw '{
  "username": "test13",
  "email": "test@email.com",
  "password": "Qwerty123",
  "first_name": "star",
  "last_name": "lord"
}'
```

## Login API Payload
```
curl --location 'http://127.0.0.1:8000/api/login' \
--header 'Content-Type: application/json' \
--data '{
    "username": "test1",
    "password": "Qwerty123"
}'
```

