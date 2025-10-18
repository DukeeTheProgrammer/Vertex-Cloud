# Vertex Cloud API

## Overview
Vertex Cloud API is a robust backend solution for personal cloud storage, developed with Python and the Django framework. It provides secure user authentication, file management, and session handling capabilities, utilizing SQLite for data persistence.

## Features
- **User Authentication**: Secure user registration and login functionalities for account management.
- **Session Management**: Generation and validation of unique API session keys to maintain user state and authorize requests.
- **File Storage**: Enables authenticated users to upload and store various file types securely.
- **File Retrieval**: Allows users to retrieve lists of their uploaded files and detailed information for individual files.
- **File Deletion**: Provides functionality for users to securely delete their uploaded files.
- **User Account Management**: Supports the deletion of user accounts along with their associated data.

## Getting Started
### Installation
To get a local copy up and running, follow these steps:

1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/DukeeTheProgrammer/Vertex-Cloud.git
    cd Vertex-Cloud/vertexcloud
    ```
2.  **Create a Python Virtual Environment**:
    ```bash
    python3 -m venv venv
    ```
3.  **Activate the Virtual Environment**:
    -   On macOS/Linux:
        ```bash
        source venv/bin/activate
        ```
    -   On Windows:
        ```bash
        venv\Scripts\activate
        ```
4.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
5.  **Apply Database Migrations**:
    ```bash
    python manage.py migrate
    ```
6.  **Create a Superuser (Optional)**:
    This is for accessing the Django Admin interface.
    ```bash
    python manage.py createsuperuser
    ```
7.  **Run the Development Server**:
    ```bash
    python manage.py runserver
    ```
    The API will then be accessible at `http://127.0.0.1:8000/`.

### Environment Variables
The following environment variables are required for the application to run correctly. For production deployments, it is highly recommended to externalize these.

*   `DJANGO_SETTINGS_MODULE`: Specifies the Django settings file.
    *   Example: `vertexcloud.settings` (This is typically set by `manage.py` and Gunicorn/WSGI server configurations.)
*   `SECRET_KEY`: A unique and unpredictable string used for cryptographic signing in Django. **Crucial for security in production.**
    *   Example: `export SECRET_KEY='your_highly_complex_and_random_secret_key_here'`
*   `DEBUG`: A boolean value to enable/disable debug mode. Should be `False` in production for security and performance.
    *   Example: `export DEBUG='False'`
*   `ALLOWED_HOSTS`: A comma-separated list of strings representing the host/domain names that this Django site can serve.
    *   Example: `export ALLOWED_HOSTS='localhost,127.0.0.1,yourdomain.com'`

## API Documentation
### Base URL
`http://127.0.0.1:8000/` (or your deployed domain)

### Endpoints
#### `GET /` or `POST /`
**Overview**: Checks the health and operational status of the API.
**Request**:
`No payload required.`

**Response**:
```json
{
  "status": true,
  "request method": "GET",
  "message": "Api is Running Correctly!",
  "runtime": "Active",
  "producer": "DukeeTheProgrammer"
}
```

**Errors**:
- `N/A`: This endpoint is designed to always return a success message for health verification.

#### `POST /signup/`
**Overview**: Registers a new user account with a unique username and email.
**Request**:
```json
{
  "username": "newuser",
  "email": "newuser@example.com",
  "password": "StrongPassword123"
}
```

**Response**:
```json
{
  "status": true,
  "session": true,
  "session_name": "current_user",
  "message": "New User newuser has been created successfully",
  "your session key": "generated_session_key_example"
}
```

**Errors**:
- `400 Bad Request`:
  - `{"status": false, "message": "Username already Exists"}`
  - `{"status": false, "message": "Email Already Exists"}`
  - `{"status": false, "message": "GET request method Not allowed on this Route"}`

#### `POST /login/`
**Overview**: Authenticates an existing user and establishes a new session, returning a session key.
**Request**:
```json
{
  "username": "existinguser",
  "password": "StrongPassword123"
}
```

**Response**:
```json
{
  "status": true,
  "session": true,
  "session_name": "current_user",
  "logged_in": true,
  "user": "existinguser",
  "session_key": "generated_session_key_example"
}
```

**Errors**:
- `400 Bad Request`:
  - `{"status": false, "message": "A severe Error Occured. Could not log you in. Try again", "current_user_status": false}` (Invalid credentials or other login failure)
  - `{"status": false, "message": "GET request method not allowed on this route."}`

#### `POST /delete/user/`
**Overview**: Deletes an authenticated user's account and flushes all associated sessions.
**Request**:
```json
{
  "key": "valid_session_key",
  "password": "current_user_password"
}
```

**Response**:
```json
{
  "status": true,
  "message": "User has been Deleted Successfully and all corresponding sessions has been flushed"
}
```

**Errors**:
- `401 Unauthorized`:
  - `{"status": false, "message": "You are not authorized to access this route, you must first be logged in"}`
- `400 Bad Request`:
  - `{"status": false, "message": "Invalid Key Credential"}`
  - `{"status": false, "message": "Invalid User Credentials"}`
  - `{"status": false, "message": "User details is invalid"}`
  - `{"status": false, "message": "Method not allowed."}` (If GET is attempted, although code supports it for params, POST is best practice for delete)

#### `POST /create/file/`
**Overview**: Uploads a new file to the cloud storage under the authenticated user's account.
**Request**:
`Content-Type: multipart/form-data`
*   `file`: (File) The actual file to upload.
*   `key`: (String) The user's session key for authorization.

**Response**:
```json
{
  "status": true,
  "message": "File Created Successfully! and has been saved.",
  "file_type": "image/jpeg",
  "filename": "my_photo.jpg",
  "file-type": "image/jpeg",
  "size": 51200,
  "producer": "DukeeTheProgrammer",
  "github_handle": "https://github.com/DukeeTheProgrammer/"
}
```

**Errors**:
- `401 Unauthorized`:
  - `{"status": false, "message": "Could not create file : -'filename.ext' - due to Invalid Key! #if you need a new key, use this endpoint '/token/' and register a new key or check if you have an existing one.", "producer": "DukeeTheProgrammer"}`
- `400 Bad Request`:
  - `{"status": false, "message": "GET method is not allowed on this Route"}`

#### `POST /get/files/`
**Overview**: Retrieves a list of all files uploaded by the authenticated user, including their details.
**Request**:
```json
{
  "key": "valid_session_key"
}
```

**Response**:
```json
{
  "file": {
    "document.pdf": {
      "id": 1,
      "url": "/media/static/files/document.pdf",
      "type": "application/pdf",
      "size": 102400,
      "created_at": "2025-10-14T00:00:00Z"
    },
    "image.png": {
      "id": 2,
      "url": "/media/static/files/image.png",
      "type": "image/png",
      "size": 51200,
      "created_at": "2025-10-14T00:00:00Z"
    }
  }
}
```

**Errors**:
- `401 Unauthorized`:
  - `{"status":false,"message":"Invalid Key entered For this user. You can use /token/ endpoint to create a new key"}`
  - `{"status":false, "message":"User credentail is not valid for this Operation"}`
- `404 Not Found`:
  - `{"status":false,"message":"No file is available under this User", "authorization":"user-token"}`
- `400 Bad Request`:
  - `{"status":false, "message":"GET request is not allowed on this Route"}`

#### `POST /token/`
**Overview**: Generates a new unique session key for an authenticated user. If a key already exists, it returns the existing one.
**Request**:
```json
{
  "username": "existinguser",
  "password": "StrongPassword123"
}
```

**Response**:
(If a new key is created)
```json
{
  "status": true,
  "message": "A new key has been created for you",
  "details": {
    "user": "existinguser",
    "key": "new_generated_session_key"
  }
}
```
(If an existing key is found)
```json
{
  "status": true,
  "message": "Your Existing Key is still available",
  "key": "existing_session_key"
}
```

**Errors**:
- `401 Unauthorized`:
  - `{"status":false,"message":"Invalid username or password!"}`
- `400 Bad Request`:
  - `{"status":false,"message":"Only POST request is available on this route"}`

#### `GET /get/file/`
**Overview**: Retrieves detailed information for a specific file by its ID, belonging to the authenticated user.
**Request**:
`Query Parameters`:
*   `id`: (Integer) The unique identifier of the file.
*   `token`: (String) The user's session key for authorization.

**Response**:
```json
{
  "file": {
    "report.docx": {
      "id": 123,
      "url": "/media/static/files/report.docx",
      "type": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
      "size": 20480,
      "created_at": "2025-10-14T00:00:00Z"
    }
  }
}
```

**Errors**:
- `401 Unauthorized`:
  - `{"status":false,"message":"Invalid Token or Did you forget to add your token to your parameters?"}`
  - `{"status":false, "message":"Invalid Token Key. you can visit '/token/' for a new token key or get your existing ones"}`
- `404 Not Found`:
  - `{"status":false, "message":"File matching query does not exist."}` (If file ID is not found for the user)
- `400 Bad Request`:
  - `{"status":false, "message":"POST is not allowed on this Route"}`

#### `GET /delete/file`
**Overview**: Deletes a specific file by its ID from the authenticated user's storage.
**Request**:
`Query Parameters`:
*   `id`: (Integer) The unique identifier of the file to delete.
*   `key`: (String) The user's session key for authorization.

**Response**:
```json
{
  "status": true,
  "message": "File with id : '123' has been deleted",
  "authorization": "user-token"
}
```

**Errors**:
- `401 Unauthorized`:
  - `{"status":false, "message":"Route is locked due to No login credentials Found. Login to contnue"}`
  - `{"status":false, "message":"Invalid Token Key."}`
- `404 Not Found`:
  - `{"status":false, "message":"Could not delete file due to File not ex8sts or invalid id given"}`
- `400 Bad Request`:
  - `{"status":true, "message":"Resend The request User GET. post is currently not supported.", "authorization":"No Authorization. Page content has been locked"}` (Note: This is an internal message from `views.py` if a POST request is sent to this GET endpoint).

#### `POST /clear/session/`
**Overview**: Flushes the current user's Django session and logs them out.
**Request**:
```json
{
  "key": "valid_session_key"
}
```

**Response**:
```json
{
  "status": true,
  "message": "User : existinguser sessions has been Flushed and Now logged out."
}
```

**Errors**:
- `401 Unauthorized`:
  - `{"status":false, "message":"Invalid token Key"}`
  - `{"status":false, "message":"A token is required to access this Endpoint"}`
- `500 Internal Server Error`:
  - `{"status":false, "message":"[Error Message]"}` (for unexpected server errors during session flushing)

---

## Technologies Used

| Technology                   | Description                                         |
| :--------------------------- | :-------------------------------------------------- |
| Python                       | Core programming language for the backend           |
| Django                       | High-level Python web framework                     |
| SQLite                       | Lightweight, file-based relational database         |
| Gunicorn                     | WSGI HTTP Server for production deployment          |
| Whitenoise                   | Static file serving for Django applications         |
| `django-allauth`             | Comprehensive authentication system for Django      |
| `djangorestframework`        | Toolkit for building Web APIs in Django             |
| `djangorestframework_simplejwt` | JSON Web Token authentication for DRF APIs          |

## Contributing
We welcome contributions to Vertex Cloud API! To contribute:

*   Fork the repository.
*   Create a new branch for your feature or bug fix.
*   Make your changes following the existing code style.
*   Write clear, concise commit messages.
*   Submit a pull request detailing your changes.

## License
This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.

## Author Info
Developed by **DukeeTheProgrammer**

*   LinkedIn: [Your LinkedIn Profile]
*   Twitter: [Your Twitter Handle]
*   Portfolio: [Your Portfolio Link]

---

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.2-green.svg)](https://www.djangoproject.com/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://www.apache.org/licenses/LICENSE-2.0)

[![Readme was generated by Dokugen](https://img.shields.io/badge/Readme%20was%20generated%20by-Dokugen-brightgreen)](https://www.npmjs.com/package/dokugen)
