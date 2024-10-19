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
### Get All Machines and Their Maintenance Information
- **Endpoint**: `GET /api/machines/`
- **Description**: Retrieves a list of all machines along with their maintenance information.
- **Response**:
    - **Status 200**: A list of machines with their maintenance details.
    - **Example Response**:
    ```json
    [
        {
            "machine": {
                "id": 1,
                "machine_type": "Welding Robot",
                "vibration_level": 0.5,
                "temperature": 75,
                "power_consumation": 120.5,
                "sensor_data": "..."
            },
            "maintenance_info": [
                {
                    "description": "Routine check",
                    "cost": 150.0,
                    "maintenance_date": "2024-10-01"
                }
            ]
        },
        ...
    ]
    ```

### Create a New Machine
- **Endpoint**: `POST /api/machines/`
- **Description**: Creates a new machine entry in the database.
- **Request Body**:
    ```json
    {
        "machine_type": "Welding Robot",
        "vibration_level": 0.5,
        "temperature": 75,
        "power_consumation": 120.5,
        "sensor_data": "{}"
    }
    ```
- **Response**:
    - **Status 201**: Machine created successfully.
    - **Status 400**: Validation errors.
    - **Example Error Response**:
    ```json
    {
        "machine_type": ["This field is required."]
    }
    ```

### Get Specific Machine and Its Maintenance Information
- **Endpoint**: `GET /api/machines/<int:id>`
- **Description**: Retrieves details of a specific machine along with its maintenance records.
- **URL Parameters**:
    - `id`: The ID of the machine.
- **Response**:
    - **Status 200**: Machine details with maintenance information.
    - **Example Response**:
    ```json
    {
        "machine": {
            "id": 1,
            "machine_type": "Welding Robot",
            "vibration_level": 0.5,
            "temperature": 75,
            "power_consumation": 120.5,
            "sensor_data": "..."
        },
        "maintenance_info": [
            {
                "description": "Routine check",
                "cost": 150.0,
                "maintenance_date": "2024-10-01"
            }
        ]
    }
    ```
    - **Status 404**: Machine does not exist.
    - **Example Error Response**:
    ```json
    {
        "Details": "Machine Does Not Exist"
    }
    ```

### Update Specific Machine Information
- **Endpoint**: `PUT /api/machines/<int:id>`
- **Description**: Updates the details of a specific machine.
- **URL Parameters**:
    - `id`: The ID of the machine to update.
- **Request Body**:
    ```json
    {
        "machine_type": "CNC Machine",
        "vibration_level": 0.3,
        "temperature": 70,
        "power_consumation": 115.0,
        "sensor_data": "{}"
    }
    ```
- **Response**:
    - **Status 200**: Machine updated successfully.
    - **Status 404**: Machine does not exist.
    - **Example Error Response**:
    ```json
    {
        "Details": "Machine Does Not Exist"
    }
    ```

### 5. Archive a Machine (No Implementation Yet)
- **Endpoint**: `DELETE /api/machines/<int:id>`
- **Description**: This endpoint is intended to archive a machine instead of deleting it from the database. Currently, there is no implementation for this endpoint.

---


### 6. Task Management

- **Endpoint**: `/api/tasks/`
- **Methods**: 
  - `GET`: Retrieve all tasks.
  - `POST`: Create a new task.

#### GET Method

- **Description**: Retrieve a list of all tasks.
- **Response**:
  - **Status Code**: `200 OK`
  - **Response Body**:
    ```json
    [
        {
            "task_name": "Sample Task",
            "task_description": "Description of the task",
            "task_deadline": "2024-01-01T10:00:00Z",
            "task_type": "routine"
        },
        ...
    ]
    ```

#### POST Method

- **Description**: Create a new task.
- **Request Body**:
  ```json
  {
      "task_name": "New Task",
      "task_description": "Description of the new task",
      "task_deadline": "2024-01-01T10:00:00Z",
      "task_type": "urgent"
  }
- **Response Body on success**:
    ```json
    [
        {
            "task_name": "New Task",
            "task_description": "Description of the new task",
            "task_deadline": "2024-01-01T10:00:00Z",
            "task_type": "urgent"
        },
        ...
    ]

- **Response Body on error**:
    ```json
    [
        {
            "task_name": ["This field is required."],
            "task_description": ["This field is required."],
            "task_deadline": ["This field is required."],
        },
        ...
    ]

### 7. Task Affection 
- **Endpoint**: `/api/affect_task/<int:id>/`
- **Methods**: 
  - `POST`: Assign a task to a user.

#### POST Method

- **Description**: Assign a task to a user by ID.
- **Request Body**:
  ```json
  {
      "task": 1 
  }
- **Response Body on success**:
    ```json
    [
        {
            "id": 1,
            "User_id": 1,
            "task_id": 1,
            "state": "pending"
        },
        ...
    ]
- **Response Body on error**:
    ```json
    [
        {
            "task": ["This field is required."],
            "Details": "Task Does Not Exist""],
        },
        ...
    ]
    ```

### 9. Task Management for Users

- **Endpoint**: `/api/tasks/<int:id>/`
- **Methods**: 
  - `GET`: Retrieve tasks assigned to a user.
  - `POST`: Update the state of a task.

#### GET Method
- **Description**: Retrieve tasks assigned to a specific user by user ID.
- **Response**:
  - **Status Code**: `200 OK`
  - **Response Body**:
    ```json
    [
    {
        "id": 1,
        "task_id": {
            "id": 1,
            "task_name": "Painting",
            "task_description": "painting the chassis of the car",
            "task_deadline": "2024-10-18T21:30:35Z",
            "task_type": "routine"
        },
        "state": "in progress",
        "User_id": 1
    },
    {
        "id": 2,
        "task_id": {
            "id": 1,
            "task_name": "Painting",
            "task_description": "painting the chassis of the car",
            "task_deadline": "2024-10-18T21:30:35Z",
            "task_type": "routine"
        },
        "state": "in progress",
        "User_id": 1
    }
    ]

#### PUT Method
- **Description**: Update the state of a task assigned to a user.
- **Response**:
  - **Status Code**: `200 OK`
  - **Response Body**:
    ```json
    {
        "User_id":1,
        "task_id":1,
        "state":"in progress"
    }
