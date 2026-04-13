# Spendly - Expense Tracker

A modern web-based expense tracking application built with Flask, designed to help users manage their personal finances.

## Project Overview

Spendly is a Flask-powered expense tracker that allows users to:
- Register and authenticate accounts
- Track expenses with full CRUD operations (Create, Read, Update, Delete)
- View expense dashboards with clean, responsive UI
- Manage personal financial data securely

## Current Status

The project is currently in development with the following features implemented:

### ✅ Completed
- **Flask Web Framework**: Basic routing and template rendering
- **User Authentication System**: Login and registration forms
- **Database Integration**: SQLite database with user storage
- **Responsive UI**: Clean, modern interface using CSS Flexbox
- **Template Structure**: Base layout with extendable blocks

### 🔧 In Progress
- Expense management functionality (add, edit, delete expenses)
- User profile management
- Expense categorization
- Dashboard with expense summaries

### 📋 Planned
- Data visualization (charts/graphs)
- Budget tracking features
- Export functionality (CSV, PDF)
- Multi-currency support
- Mobile-responsive design

## Tech Stack

- **Backend**: Python 3.14 with Flask
- **Database**: SQLite with SQLAlchemy support
- **Frontend**: HTML5, CSS3, JavaScript (ES6)
- **Styling**: CSS Flexbox for layout
- **Authentication**: Custom session-based auth

## Project Structure

```
spendly/
├── app.py              # Flask application routes and logic
├── main.py             # Application entry point
├── database/           # Database-related modules
│   ├── __init__.py
│   └── db.py           # Database connection and operations
├── templates/          # HTML templates
│   ├── base.html       # Master layout template
│   ├── landing.html    # Homepage
│   ├── login.html      # Login page
│   └── register.html   # Registration page
├── static/             # Static assets
│   ├── css/style.css   # Application styles
│   └── js/main.js      # Client-side scripts
└── pyproject.toml      # Project dependencies
```

## Getting Started

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py
```

3. Open your browser and navigate to `http://localhost:5000`

## Key Features

### User Authentication
- Secure login and registration
- Session-based authentication
- Protected routes for authenticated users

### Expense Management
- Add new expenses with amount, category, and description
- Edit existing expenses
- Delete unwanted expenses
- View expense history

### Dashboard
- Overview of all expenses
- Expense categorization
- Monthly/weekly expense summaries

## Development Notes

- The project follows a Flask MVC pattern
- Templates use Jinja2 templating engine
- CSS uses Flexbox for responsive layout
- Database operations are handled through helper functions
- Git workflow includes regular commits for feature branches

## Contributing

This is a learning project focused on understanding Flask development, database integration, and building web applications. All contributions should align with the project's educational goals.

## License

MIT License - feel free to use and modify for educational purposes.