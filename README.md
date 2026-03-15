## Employee salary calculations and stats with Flask

A simple REST API built using **Flask** and **SQLite** for managing employee data and calculating salary statistics.

---

## Features

* RESTful APIs to create and manage employee records
* RESTful APIs for net salary calculation and other salary statistics
* SQLite database using SQLAlchemy
* Unit tests using `unittest`

---

## Project Structure

```
incubyte-assessment/
├── app/            # Logic Implementation
│   └── models.py   # Database models
    └── routes.py   # APIs
├── app.py            # Main Flask application
├── config.py         # Configurations
├── tests/            # Unit tests
    └── test_employee_crud.py
    └── test_employee_salary.py
    └── test_models.py
    └── test_salary_stats.py
└── README.md
└── requirements.txt  # Package Dependencies
```

---

## Installation

### 1. Clone the repository

```
git clone https://github.com/remya154-ux/incubyte-assessment.git
```

### 2. Create virtual environment

```
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```
pip install -r requirements.txt
```

---

## Running the Application

Start the Flask server:

```
python app.py
```

The API will run at:

```
http://127.0.0.1:5000
```

---
## Running Tests and Coverage Report

Run unit tests using:

```
python -m coverage run --source=app --omit="*/__init__.py,*/tests/*" -m unittest discover
python -m coverage report
```

---

## Technologies Used

* Python
* Flask
* SQLAlchemy
* unittest

---
## Implementation Details
* Used ChatGPT to get the pre-written code for the routes & tests
* Test cases have also been written to just satisfy 100% code coverage
* All the endpoints were tested running the application and also using test cases
* Blueprints were not used considering the lightness of the application and since UI is not required
* WSGI, DB migrations have not been implemented since it's an assessment, and the app can be successfully run in localhost
---

## Please note
* Have used a public repo since had issues in pushing code to the Github classroom
* Certain additional folders like .idea got pushed out of nowhere which I am unable to delete. Please do not consider them during the evaluation. 