# Widget

## Overview

This Django application has simple CRUD functionality for the Widget model.

## Launching API

To launch the API, run the command `python manage.py runserver` within this directory (`aweber-challenge-django`).

This will launch the django server, and you can view the API endpoint for interacting with the widget model at `localhost:8000` once the server is available.

## CRUD Operations

CRUD operations can either be performed in three ways:

- Using the browsable API endpoint at `localhost:8000`
- Sending HTTP requests to `localhost:8000` using postman, curl, or any similar method
- By going to the admin console for this django server, at `localhost:8000/admin`. Must have administrative credentials to access this console.

## API Documentation

While the django server is available, visit `localhost:8000/docs` to view the Open API documentation.
