Issue Tracker
This is a full-stack web application for tracking issues. It includes a backend API built with Python and FastAPI, and a frontend user interface built with Angular.

Features
Create, Read, Update, and Delete (CRUD) issues: Users can create new issues, view a list of existing issues, edit existing issues, and delete issues.

Search and filter: The issue list can be searched by title and filtered by status, priority, and assignee.

Sort: The issue list can be sorted by ID, title, status, priority, assignee, and last updated date.

Pagination: The issue list is paginated to handle a large number of issues.

Modal forms: Issue creation and editing are handled in a modal form, providing a seamless user experience.

Technologies Used
Backend
Python: The primary programming language for the backend.

FastAPI: A modern, fast (high-performance) web framework for building APIs with Python.

SQLAlchemy: A SQL toolkit and Object-Relational Mapper (ORM) for Python.

SQLite: The database used for storing issue data.

Frontend
Angular: A platform for building mobile and desktop web applications.

TypeScript: A typed superset of JavaScript that compiles to plain JavaScript.

HTML & CSS: The standard markup and styling languages for creating web pages.

Getting Started
Prerequisites
Python 3.7+

Node.js and npm

Angular CLI

Backend Setup
Clone the repository:

Bash

git clone https://github.com/your-username/issue-tracker.git
cd issue-tracker
Install Python dependencies:

Bash

pip install -r requirements.txt
Run the backend server:

Bash

uvicorn main:app --reload
The backend API will be running at http://localhost:8000.

Frontend Setup
Navigate to the src directory:

Bash

cd src
Install npm packages:

Bash

npm install
Run the Angular development server:

Bash

ng serve
The frontend application will be running at http://localhost:4200.

Database
The application uses a SQLite database, which is created automatically as issuetracker.db when the backend is started for the first time. The database schema is defined in database.py.

Project Structure
Backend (main.py, database.py)
main.py: Contains the FastAPI application and all the API endpoints for managing issues.

database.py: Defines the database schema using SQLAlchemy and provides functions for interacting with the database.

Frontend (src/app)
src/app/issue-list: Contains the main component for displaying the list of issues, along with filtering, sorting, and pagination controls.

src/app/issue-detail: Contains the component for displaying the details of a single issue.

src/app/issue.service.ts: An Angular service that handles all communication with the backend API.

src/app/issue.ts: Defines the Issue interface, which represents the structure of an issue object.