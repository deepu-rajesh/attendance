# Attendance Application

This project is an Attendance Management System featuring a Django backend API and an Angular frontend interface.

## Prerequisites

Ensure you have the following installed on your machine:
- **Python 3.8+**
- **Node.js (18+ recommended) and npm**
- **Git** (optional, for version control)

---

## ⚙️ Backend Setup (Django)

The Django backend serves the REST API and manages the database.

### 1. Open a terminal and navigate to the project root:
```bash
# Example
cd path/to/attendance
```

### 2. Create and activate a virtual environment (Recommended):
It's a good practice to use a virtual environment to manage dependencies.

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

### 4. Apply database migrations:
This will set up your local SQLite database with the necessary tables.
```bash
python manage.py migrate
```

### 5. Run the backend development server:
```bash
python manage.py runserver
```
The Django server should now be running at `http://127.0.0.1:8000/`.

---

## 🎨 Frontend Setup (Angular)

The Angular frontend provides the user interface that communicates with the Django API.

### 1. Open a new terminal window and navigate to the frontend directory:
```bash
# From the project root
cd frontend
```

### 2. Install Node.js dependencies:
```bash
npm install
```

### 3. Run the Angular development server:
```bash
npm start
```
*(Alternatively, you can use `ng serve` if you have the Angular CLI installed globally)*

The frontend application should now be accessible in your web browser at `http://localhost:4200/`. The app will automatically reload if you change any of the source files.

---

## 🚀 Running the Full Stack

To run the complete application, you will need two separate terminal windows open at the same time:
1. One running `python manage.py runserver` from the root directory.
2. One running `npm start` from the `frontend` directory.
