## Endpoints
### Authentication (register) 

- **Endpoint**: `http://localhost:8000/api/register/`
- **Method**: POST
- **Description**: Register a user.
- **Example Request (Create)**:
    ```json
    {
        "username": "your name",
        "email": "email@gmail.com",
        "password": "your password",
    }
    ```
    
### Authentication (login) 

- **Endpoint**: `http://localhost:8000/api/login/`
- **Method**: POST
- **Description**: login a user and generate a unique token for him.
- **Example Request (Create)**:
    ```json
    {
        "username": "your name",
        "password": "your password",
    }
    ```
