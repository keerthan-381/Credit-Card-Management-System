# Credit Card Management System

A web-based application for managing credit cards and transactions built with React.js and Node.js.


## Features

- User authentication and profile management
- Credit card management (add and view)
- View credit card details and transaction history

## Tech Stack

### Frontend
- React.js
- React Router for navigation
- CSS for styling
- Fetch API for HTTP requests

### Backend
- Node.js
- MySQL Database

## Getting Started

### Prerequisites
- Node.js (v14 or higher)
- npm (Node Package Manager)
- MySQL Server

### Installation

1. Clone the repository:
```bash
git clone git@github.com:keerthan-381/Credit-Card-Management-System.git
```
Install Frontend Dependencies:
```
cd frontend
npm install
```

Install Backend Dependencies:
```
cd backend
npm install
```

Configuration
Frontend Configuration:

Create a .env file in the frontend directory

Add necessary environment variables:
```
REACT_APP_API_URL=http://localhost:5000
```

Backend Configuration:

Create a .env file in the backend directory

Configure your database credentials:
```
DB_HOST=localhost
DB_USER=your_username
DB_PASSWORD=your_password
DB_NAME=your_database_name
PORT=5000
```

Running the Application
Start the Backend Server:
```
cd backend
npm start
```

Start the Frontend Development Server:
```
cd frontend
npm start
```

The application will be available at http://localhost:3000

Usage
Register/Login to your account

View your profile and card details

Add new credit cards

View transaction history for each card

Track outstanding balances

Project Structure
```
project/
├── frontend/
│   ├── public/
│   │   ├── favicon.ico
│   │   ├── index.html
│   │   ├── manifest.json
│   │   └── robots.txt
│   └── src/
│       ├── App.css
│       ├── App.js
│       ├── Apptest.js
│       ├── Failed.js
│       ├── index.css
│       ├── index.js
│       ├── LoginSignup.js
│       ├── logo.svg
│       ├── reportWebVitals.js
│       ├── setupTests.js
│       ├── success.js
│       ├── TransactionDetails.js
│       └── UserDetails.js
└── backend/
    ├── app.py
    ├── create_db.py
    └── test_db.py
```


Acknowledgments
React.js Documentation

Node.js Documentation

MySQL Documentation


This README.md provides a comprehensive overview of your project, including:
- Project description and features
- Technology stack
- Installation and setup instructions
- Usage guidelines
- Project structure
- Contributing guidelines

You can customize this template further based on your specific project needs, such as:
- Adding more detailed API documentation
- Including screenshots of the application
- Adding specific coding standards
- Including testing instructions
- Adding deployment instructions


