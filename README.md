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

### 10. real time data handeling & visualization
This WebSocket API provides real-time updates for sensor data from various machines. The API sends updates every 20 seconds containing information about each machine's performance metrics.

## WebSocket Endpoint

- **Endpoint**: ws://<your-server-url>/ws/socket-server/dady/
- - **Response Example**:
  - **Response Body**:
    ```json
    {
    "data": [
        {
            "id": 4,
            "machine_name": "welding_robot_006",
            "timestamp": "2024-10-18T21:11:15.898000Z",
            "machine_type": "WeldingRobot",
            "vibration_level": 0.66,
            "temperature": 1446,
            "power_consumation": 5.6,
            "sensor_data": "{'machine_id': 'welding_robot_006', 'weld_current': 182.9, 'weld_voltage': 9.7, 'weld_time': 389, 'pressure_applied': 1665, 'arm_position': {'x': 113.3, 'y': 61.1, 'z': 132.6}, 'wire_feed_rate': 5.1, 'gas_flow_rate': 43.5, 'weld_strength_estimate': 184.9}"
        },
        {
            "id": 5,
            "machine_name": "cnc_milling_004",
            "timestamp": "2024-10-18T21:29:31.306000Z",
            "machine_type": "CNC_Machine",
            "vibration_level": 0.39,
            "temperature": 66,
            "power_consumation": 18.2,
            "sensor_data": "{'machine_id': 'cnc_milling_004', 'spindle_speed': 3627.4, 'tool_wear_level': 87.7, 'cut_depth': 8.1, 'feed_rate': 77.5, 'coolant_flow_rate': 0.44, 'material_hardness': 197.6, 'chip_load': 0.36}"
        },
        {
            "id": 6,
            "machine_name": "leak_test_005",
            "timestamp": "2024-10-18T21:29:35.064000Z",
            "machine_type": "LeakTestMachine",
            "vibration_level": 0.5,
            "temperature": 29,
            "power_consumation": 0.001,
            "sensor_data": "{'machine_id': 'leak_test_005', 'pressure_drop': 0.068, 'test_duration': 24, 'status': 'pass', 'fluid_type': 'hydraulic fluid', 'seal_condition': 'warning', 'test_cycle_count': 1511}"
        },
        {
            "id": 7,
            "machine_name": "agv_003",
            "timestamp": "2024-10-18T21:29:40.685000Z",
            "machine_type": "AGV",
            "vibration_level": 0.01,
            "temperature": 41,
            "power_consumation": 0.1,
            "sensor_data": "{'machine_id': 'agv_003', 'location': {'x': 174.3, 'y': 195.5, 'z': 55.8}, 'battery_level': 93, 'load_weight': 1438.2, 'distance_traveled': 1987.9, 'obstacle_detection': 'no', 'navigation_status': 'en_route', 'wheel_rotation_speed': 150.9}"
        }
    ]
    }
