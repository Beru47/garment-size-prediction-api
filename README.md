# FastAPI Application

This repository contains a FastAPI application.

## Prerequisites

Before you begin, make sure you have the following installed:
- Python 3.x (where x >= 9 recommended)
- pip (Python package installer)
- An internet connection to install dependencies

## Setup

1. **Clone the repository:**
   ```
   git clone https://github.com/Beru47/APi-internship-wefizz
   cd APi-internship-wefizz
   ```

2. **Create a virtual environment:**
   ```
   python -m venv venv
   ```
   If you prefer to specify a Python interpreter path:
   ```
   & "C:\path\to\your\python.exe" -m venv venv
   ```

3. **Activate the virtual environment:**

   On Windows:
   ```
   venv\Scripts\activate
   ```

   On macOS/Linux:
   ```
   source venv/bin/activate
   ```

4. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

5. **Database Connection Configuration:**

To configure the connection to your PostgreSQL database and potentially migrate to MySQL, use the following code in the "database.py" file by replacing the values within < > with your own connection information:
   ```
   SQLALCHEMY_DATABASE_URL = "postgresql://<username>:<password>@<host>/<database_name>"
   ```
   - <username>: Replace with the username of your database.
   - <password>: Replace with the password for this user.
   - <host>: Replace with the IP address or hostname of your database server.
   - <database_name>: Replace with the name of the database you wish to connect to.

To migrate to MySQL, simply change "postgresql://" in SQLALCHEMY_DATABASE_URL to "mysql+pymysql://" and adjust the connection details specific to MySQL, such as the IP address, username, password, and database name.

This configuration allows you to connect your application to an existing PostgreSQL database and prepares for a potential migration to MySQL by simply adjusting the connection URL.

6. **Configuring CORS for FastAPI:**

In order to ensure that your FastAPI application can handle requests from the appropriate origins, it is necessary to configure Cross-Origin Resource Sharing (CORS). This involves specifying the origins that are allowed to communicate with your backend.

By default, the origins list includes local addresses for development purposes:
   ```
   origins = [
    "http://127.0.0.1:5500",  
    "http://localhost:5500", 
    "http://localhost"
   ]
   ```
   
To allow your FastAPI server to accept requests from your production server or any other specific IP address, you need to add the server's IP address to this list. This is crucial for security and to prevent unwanted cross-origin requests.

Here is an example of how you can update the origins list to include your server's IP address in "main.py":
   ```
   origins = [
    "http://127.0.0.1:5500",
    "http://localhost:5500",
    "http://localhost",
    "http://<your_server_ip>"  # Add your server's IP address here
   ]

   app.add_middleware(
      CORSMiddleware,
      allow_origins=origins,
      allow_credentials=True,
      allow_methods=["POST", "GET"],
      allow_headers=["*"],
   )
   ```

This configuration that you will find in main.py ensures that your FastAPI application can securely handle requests from both local and specified remote origins, facilitating smooth and secure client-server communication.


7. **Running the Application**

   ```
   uvicorn app.main:app --reload
   ```

   This command starts the Uvicorn server with the app instance from `main.py` in the `app` directory. The `--reload` flag enables auto-reloading on code changes.

   Once the server has started, open your web browser and go to:

   [http://localhost:8000/docs](http://localhost:8000/docs)

   This URL will redirect you to the Swagger UI, where you can interact with the API endpoints.

Haythem @ 
