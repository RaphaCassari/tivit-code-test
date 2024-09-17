
# API Documentation

## Overview
This project contains two APIs:
1. **Fake API**: Simulates user and admin data retrieval and token-based authentication.
2. **Main API**: Calls the Fake API, syncs user/admin data into a Neo4j database, and provides recommendations based on the data.

---

## Fake API

### Base URL
`http://localhost:8000`

### Endpoints

#### 1. `/token`
- **Method**: POST
- **Description**: Authenticates a user and returns a JWT token.
- **Request**:
    - `username`: string (required)
    - `password`: string (required)
- **Response**:
    ```json
    {
        "access_token": "<token>"
    }
    ```

#### 2. `/user`
- **Method**: GET
- **Description**: Returns user data.
- **Headers**: 
    - `Authorization`: Bearer `<token>`
- **Response**:
    ```json
    {
        "message": "Hello, user!",
        "data": {
            "name": "John Doe",
            "email": "john@example.com",
            "purchases": [
                {
                    "id": 1,
                    "item": "Laptop",
                    "price": 2500
                },
                {
                    "id": 2,
                    "item": "Smartphone",
                    "price": 1200
                }
            ]
        }
    }
    ```

#### 3. `/admin`
- **Method**: GET
- **Description**: Returns admin data.
- **Headers**: 
    - `Authorization`: Bearer `<token>`
- **Response**:
    ```json
    {
        "message": "Hello, admin!",
        "data": {
            "name": "Admin Master",
            "email": "admin@example.com",
            "reports": [
                {
                    "id": 1,
                    "title": "Monthly Sales",
                    "status": "Completed"
                },
                {
                    "id": 2,
                    "title": "User Activity",
                    "status": "Pending"
                }
            ]
        }
    }
    ```

---

## Main API

### Base URL
`http://localhost:8001`

### Endpoints

#### 1. `/token`
- **Method**: POST
- **Description**: Returns JWT token for authentication.
- **Request**:
    - `username`: string (required)
    - `password`: string (required)
- **Response**:
    ```json
    {
        "access_token": "<token>"
    }
    ```

#### 2. `/sync-user`
- **Method**: GET
- **Description**: Syncs user data from the Fake API to Neo4j.
- **Request**:
    - `username`: string (required)
    - `password`: string (required)
- **Response**:
    ```json
    {
        "status": "success",
        "data": {
            "name": "John Doe",
            "email": "john@example.com",
            "purchases": [
                {
                    "id": 1,
                    "item": "Laptop",
                    "price": 2500
                },
                {
                    "id": 2,
                    "item": "Smartphone",
                    "price": 1200
                }
            ]
        }
    }
    ```

#### 3. `/sync-admin`
- **Method**: GET
- **Description**: Syncs admin data from the Fake API to Neo4j.
- **Request**:
    - `username`: string (required)
    - `password`: string (required)
- **Response**:
    ```json
    {
        "status": "success",
        "data": {
            "name": "Admin Master",
            "email": "admin@example.com",
            "reports": [
                {
                    "id": 1,
                    "title": "Monthly Sales",
                    "status": "Completed"
                },
                {
                    "id": 2,
                    "title": "User Activity",
                    "status": "Pending"
                }
            ]
        }
    }
    ```

#### 4. `/user-recommendations`
- **Method**: GET
- **Description**: Provides recommendations for the user based on past purchases.
- **Request**:
    - `name`: string (required)
- **Response**:
    ```json
    {
        "recommendations": [
            {
                "item": "Tablet",
                "price": 700,
                "category": "Electronics",
                "image": "image-url-placeholder"
            }
        ]
    }
    ```

#### 5. `/admin-recommendations`
- **Method**: GET
- **Description**: Provides report recommendations for the admin based on past reports.
- **Request**:
    - `name`: string (required)
- **Response**:
    ```json
    {
        "recommendations": [
            {
                "title": "Monthly Sales",
                "status": "Completed",
                "creation_date": "2024-01-05",
                "priority": "High"
            }
        ]
    }
    ```

#### 6. `/populate-db`
- **Method**: POST
- **Description**: Populates the Neo4j database with sample data for testing.
- **Response**:
    ```json
    {
        "message": "Database populated successfully"
    }
    ```

---

## Neo4j Database
This API interacts with a Neo4j database to store and retrieve information about users, their purchases, admins, and reports. Recommendations are generated based on past data.

---

## Technologies Used
- **FastAPI**: For the web framework.
- **Neo4j**: As the database for storing user and admin data.
- **JWT**: For authentication between the main API and the Fake API.
- **Python**: For backend development.

## Setup Instructions

1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`
3. Run the Fake API: `uvicorn fake_api:app --reload --port 8000`
4. Run the Main API: `uvicorn main_api:app --reload --port 8001`
5. Ensure Neo4j is running and update the credentials in the Main API if necessary.
6. Use the `/populate-db` route to seed the database with sample data.

---

## Future Improvements
- Implement pagination for large datasets.
- Enhance security with role-based access control.
- Add caching for faster responses.
- Support for more detailed analytics and insights for admins.

---

## License
This project is licensed under the MIT License - see the LICENSE file for details.
