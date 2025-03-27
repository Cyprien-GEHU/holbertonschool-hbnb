# HBnB - BL and API

# Part 2: Implementation of Business Logic and API Endpoints
In this project we have implemented the phase of the application based on the design developed in the previous part. We have focused on the Persistance, Business Logic, and Persistance Layers. This project is built using Python and Flask. Create the structure of the project, develop the classes that define the business logic, and implement the API endpoints. Also we set and manage users, places, reviews, and amenities.

# Project Structure

    hbnb/
    ├── app/
    │   ├── __init__.py
    │   ├── api/
    │   │   ├── __init__.py
    │   │   ├── v1/
    │   │       ├── __init__.py
    │   │       ├── users.py
    │   │       ├── places.py
    │   │       ├── reviews.py
    │   │       ├── amenities.py
    │   ├── models/
    │   │   ├── __init__.py
    │   │   ├── user.py
    │   │   ├── place.py
    │   │   ├── review.py
    │   │   ├── amenity.py
    │   │   ├── basemodel.py
    │   ├── services/
    │   │   ├── __init__.py
    │   │   ├── facade.py
    │   ├── persistence/
    │       ├── __init__.py
    │       ├── repository.py
    ├── run.py
    ├── config.py
    ├── requirements.txt
    ├── README.md



# Explaination of key Directories and files

.app/: Contains the main application components:

.api/: Handles API rounting and versioning.

.models/: Defines business logic classes, for User, Place, Review, and Amenities.

.services/: Implements the facade pattern to act as bridge beetween layers.

.persistence: Contains the in-memory repository that is intended to change for a database later

.run.py: Entry point of this application

.config.py: Configuration settings of the environment

.requirement: List of library needed to run the project

# Business logic layer explaination

## User

The user entity, he has a unique id and can create/interact with places review and amenity

### How to create a user:

Content-Type: application/json

    {
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com"
    }


Expected response:

    {
    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com"
    }

    // 201 Created

### Possible Status Codes:

201 Created: When the user is successfully created.
400 Bad Request: If the email is already registered or input data is invalid.

### Retrieve a User by ID

Content-Type: application/json

Expected Response:

    {
    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@x.com"
    }

    // 200 OK

### Possible Status Codes:

200 OK: When the user is successfully retrieved.
404 Not Found: If the user does not exist.

### Retrieve a List of Users

Content-Type: application/json

Expected Response:

    [
    {
        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com"
    },
    ...
    ]

// 200 OK

### Possible Status Codes:

200 OK: When the list of users is successfully retrieved.

### Update a User

Content-Type: application/json

    {
    "first_name": "Jane",
    "last_name": "Doe",
    "email": "jane.doe@example.com"
    }

Expected Response:

    {
    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "first_name": "Jane",
    "last_name": "Doe",
    "email": "jane.doe@example.com"
    }

// 200 OK

### Possible Status Codes:

200 OK: When the user is successfully updated.
404 Not Found: If the user does not exist.
400 Bad Request: If input data is invalid.

## Place

The place is created by users and own reviews and amenities

### Register a New Place

Content-Type: application/json

    {
    "title": "Cozy Apartment",
    "description": "A nice place to stay",
    "price": 100.0,
    "latitude": 37.7749,
    "longitude": -122.4194,
    "owner_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
    }

Expected Response:

    {
    "id": "1fa85f64-5717-4562-b3fc-2c963f66afa6",
    "title": "Cozy Apartment",
    "description": "A nice place to stay",
    "price": 100.0,
    "latitude": 37.7749,
    "longitude": -122.4194,
    "owner_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
    }

// 201 Created

### Possible Status Codes:

201 Created: When the place is successfully created.
400 Bad Request: If input data is invalid.

## Review

Reviews are created by the user to rate places

### Register a New Review

Content-Type: application/json

    {
    "text": "Great place to stay!",
    "rating": 5,
    "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "place_id": "1fa85f64-5717-4562-b3fc-2c963f66afa6"
    }

Expected Response:

    {
    "id": "2fa85f64-5717-4562-b3fc-2c963f66afa6",
    "text": "Great place to stay!",
    "rating": 5,
    "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "place_id": "1fa85f64-5717-4562-b3fc-2c963f66afa6"
    }

// 201 Created
### Possible Status Codes:

201 Created: When the review is successfully created.
400 Bad Request: If input data is invalid.

## Amenity

Amenities are create by users and add to the place by the user too

### Register a New Amenity

Content-Type: application/json

    {
    "name": "Wi-Fi"
    }

Expected Response:

    {
    "id": "1fa85f64-5717-4562-b3fc-2c963f66afa6",
    "name": "Wi-Fi"
    }

// 201 Created

### Possible Status Codes:

201 Created: When the amenity is successfully created.
400 Bad Request: If input data is invalid.


# Setup and Installation

# 1. Clone the repository:

    git clone https://github.com/Kraoshin/holbertonschool-hbnb.git

# 2. Install Requirements:

    pip install -r requirements.txt

# 3. Run the Application:

    python run.py