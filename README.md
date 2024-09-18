
# API Documentation

## Overview

This repository contains two APIs:

1. **Fake API**: This API simulates user and admin data and provides authentication through JWT.
2. **Main API**: This API communicates with the Fake API to sync data and stores the information in a Neo4j database. It also provides recommendations based on past purchases.

## Fake API

### Endpoints

- **POST /token**: Authenticate and get a JWT token.
- **GET /user**: Retrieve user information using the JWT token.
- **GET /admin**: Retrieve admin information using the JWT token.
- **GET /health**: Check the health of the API.

### User Data Response

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

### Admin Data Response

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

## Main API

### Endpoints

- **POST /token**: Authenticate and get a JWT token.
- **POST /sync/user**: Sync user data from the Fake API.
- **POST /sync/admin**: Sync admin data from the Fake API.
- **GET /recommendations/user/{name}**: Get purchase recommendations for a user based on past purchases.
- **GET /recommendations/admin/{name}**: Get recommendations for an admin based on activity.
- **POST /populate**: Populate the Neo4j database with example data.

### Recommendation Data

In the recommendation endpoints, you will get additional data such as:

- **Recommended Items**: A list of recommended items based on the user's past purchases.
- **Potential Discounts**: Any available discounts for the recommended items.
- **Trending Items**: Products that are trending in the same category as the user's past purchases.

```json
{
    "name": "John Doe",
    "recommendations": [
        {
            "item": "Wireless Mouse",
            "category": "Electronics",
            "recommended_price": 30,
            "trending": true,
            "discount": 10
        },
        {
            "item": "Gaming Headset",
            "category": "Electronics",
            "recommended_price": 80,
            "trending": false,
            "discount": 15
        }
    ]
}
```

## Web-Tivit

This repository also contains a frontend application inside the `web-tivit` folder. The frontend is built using **Quasar.js**, and it's automatically deployed to **GitHub Pages** with **PWA (Progressive Web App)** functionality enabled.

### Features:
- **Responsive design**: Works well on both desktop and mobile devices.
- **PWA support**: The app can be installed and used offline.
- **Automatic deployment**: The frontend is automatically deployed to GitHub Pages when pushed to the main branch.

## Local Development Setup

To set up this project locally, follow these steps:

### Backend (APIs)

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/yourrepo.git
    cd yourrepo
    ```

2. **Set up a virtual environment** (optional but recommended):
    ```bash
    python3 -m venv env
    source env/bin/activate  # On Windows use `env\Scriptsctivate`
    ```

3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Run the Fake API**:
    ```bash
    uvicorn fake_api:app --reload
    ```

5. **Run the Main API**:
    ```bash
    uvicorn main_api:app --reload
    ```

6. **Set up Neo4j**:
    - Download and install [Neo4j](https://neo4j.com/download/).
    - Start the Neo4j server.
    - Modify the `neo4j_uri`, `neo4j_user`, and `neo4j_password` environment variables in the `.env` file to match your local Neo4j instance.

### Frontend (Web-Tivit)

1. **Navigate to the frontend folder**:
    ```bash
    cd web-tivit
    ```

2. **Install Node.js dependencies**:
    ```bash
    npm install
    ```

3. **Run the Quasar development server**:
    ```bash
    quasar dev
    ```

4. **Build for production**:
    ```bash
    quasar build
    ```

5. **Deploy to GitHub Pages**:
    ```bash
    quasar build
    ```

## License

This project is licensed under the MIT License.
