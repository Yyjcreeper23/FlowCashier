# ForeCashier

**ForeCashier** is a personal finance and cash flow forecasting web application. It helps you track income and expenses (both one-time and recurring) and visually projects your estimated bank balance for each day of the month on an interactive calendar.

---

## Table of Contents

1. [How It Works (Big Picture)](#-how-it-works-big-picture)
2. [Project Architecture](#-project-architecture)
3. [Prerequisites](#-prerequisites)
4. [Step-by-Step Setup Guide](#-step-by-step-setup-guide)
   - [Backend Setup (FastAPI & Python)](#1-backend-setup-fastapi--python)
   - [Frontend Setup (React & Vite)](#2-frontend-setup-react--vite)
5. [Understanding the Components](#-understanding-the-components)
   - [Frontend (The Face of the App)](#frontend-the-face-of-the-app)
   - [Backend (The Brain of the App)](#backend-the-brain-of-the-app)
   - [Database (The Memory of the App)](#database-the-memory-of-the-app)
6. [Data Flow: How Everything Connects](#-data-flow-how-everything-connects)
7. [API Reference Summary](#-api-reference-summary)
8. [Common Beginner FAQs & Troubleshooting](#-common-beginner-faqs--troubleshooting)

---

## How It Works (Big Picture)

Imagine you have a starting balance of **$1,000** at the beginning of the month:

- You pay rent of **$500** on the 1st of every month (_Monthly_ recurrence).
- You get paid a salary of **$1,200** on the 15th and 30th (_One Time_ or _Monthly_).
- You buy groceries for **$50** every Saturday (_Weekly_).

**ForeCashier** calculates what your balance will be on **every single day of that month**, highlights your **lowest** and **highest** balance points, and displays daily balance badges directly on a monthly calendar so you never accidentally overspend.

---

## Project Architecture

The project is divided into two distinct parts that communicate over HTTP requests and a local database:

1. **Frontend (`/frontend`)**: Built with **React** and **Vite**. This runs inside your web browser.
2. **Backend (`/backend`)**: Built with **Python** and **FastAPI**. This runs a local server that handles calculations and data storage.
3. **Database (`transaction.db`)**: A lightweight **SQLite** file managed via **SQLModel** (which connects Python classes directly to database tables).

---

## Prerequisites

Before you start, make sure you have the following installed on your computer:

- **Python 3.10+**: [Download Python](https://www.python.org/downloads/) (Make sure to check _"Add Python to PATH"_ during installation).
- **Node.js (v18+ or v20+) & npm**: [Download Node.js](https://nodejs.org/).

---

## Step-by-Step Setup Guide

You will need **two terminal windows**: one for the backend server and one for the frontend server.

### 1. Backend Setup (FastAPI & Python)

1. Open your first terminal and navigate to the `backend` folder:

   ```bash
   cd backend
   ```

2. Create a virtual environment (this creates an isolated space for Python libraries):
   - **Windows (PowerShell / Command Prompt)**:
     ```powershell
     python -m venv .venv
     ```
   - **macOS / Linux**:
     ```bash
     python3 -m venv .venv
     ```

3. Activate the virtual environment:
   - **Windows (PowerShell)**:
     ```powershell
     .venv\Scripts\Activate.ps1
     ```
     _(If you get a script execution policy error, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` first)_
   - **Windows (Command Prompt)**:
     ```cmd
     .venv\Scripts\activate.bat
     ```
   - **macOS / Linux**:
     ```bash
     source .venv/bin/activate
     ```

4. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

5. Start the backend development server:
   ```bash
   uvicorn main:app --reload
   ```

---

### 2. Frontend Setup (React & Vite)

1. Open your second terminal and navigate to the `frontend` folder:

   ```bash
   cd frontend
   ```

2. Install the JavaScript dependencies:

   ```bash
   npm install
   ```

3. Start the frontend development server:
   ```bash
   npm run dev
   ```
   > Open `http://localhost:5173` in your browser to use the app!

---

## Understanding the Components

### Frontend (The Face of the App)

Located in `frontend/src/`:

- **`App.jsx`**: The central React component. It:
  - Fetches the saved transactions from the backend when the page loads.
  - Keeps track of user inputs (like starting balance, selected month, transaction details).
  - Sends a request to the backend forecast engine and receives the calculated daily balances.
  - Renders the interactive calendar (powered by `react-calendar`) with colored balance tags on each date tile.
- **`CurrencyInput.jsx`**: A reusable input field designed specifically for entering monetary values cleanly.
- **`App.css`**: Styling rules for the dashboard layout, transaction modals, cards, and calendar indicators.

### Backend (The Brain of the App)

Located in `backend/`:

- **`main.py`**: The entry point of the server. It initializes FastAPI, enables **CORS** (Cross-Origin Resource Sharing, allowing the React frontend on port `5173` to talk to port `8000`), and mounts the routers.
- **`app/routers/transactions.py`**: Contains the API endpoints for managing transactions:
  - Add new transaction (`POST /api/transaction/`)
  - View all transactions (`GET /api/transaction/all`)
  - Update a transaction (`PATCH /api/transaction/{id}`, this is currently not used and is pending addition)
  - Delete a transaction (`DELETE /api/transaction/{id}`)
- **`app/routers/forecasts.py`**: Contains the forecast calculation endpoint (`POST /api/forecast`).
- **`app/forecast_builder.py`**: The mathematical forecast engine. It iterates through all days of the selected month (1 to 28/29/30/31), determines which recurring or one-time transactions fall on each day, adds or subtracts them from the running balance, and returns the daily projection along with the highest and lowest balance days.
- **`utils/recurring_freqs.py`**: Defines valid transaction recurrence types (`One Time`, `Daily`, `Weekly`, `Monthly`, `Yearly`).
- **`utils/converters.py`**: Helper functions to convert between Python `date` objects and human-friendly string formats.

### Database (The Memory of the App)

Located in `backend/app/`:

- **`database.py`**: Sets up the SQLite database connection using SQLModel. When the server starts up, `create_db_and_tables()` creates the `transaction.db` file automatically if it doesn't already exist.
- **`models.py`**: Defines data structures (schemas):
  - `Transaction`: The database table structure (includes fields: `tr_id`, `name`, `amount`, `date`, `recurring_freq`).
  - `ForecastRequest` & `ForecastResponse`: Structures used to validate data sent to and received from the forecast calculator.

---

## Data Flow: How Everything Connects

Here is an example of what happens under the hood when a new transaction is added:

```
[User clicks 'Add Transaction' in React UI]
                     │
                     ▼
[Frontend sends POST request with JSON body to http://localhost:8000/api/transaction/]
                     │
                     ▼
[FastAPI receives the request and validates data with TransactionBase model]
                     │
                     ▼
[transactions.py adds record to SQLite database via SQLModel session]
                     │
                     ▼
[FastAPI returns the saved transaction (including its new tr_id) back to React]
                     │
                     ▼
[React triggers recalculation by calling POST /api/forecast]
                     │
                     ▼
[forecast_builder.py recalculates daily balances for the month and returns them]
                     │
                     ▼
[React updates calendar badges and summary cards instantly on your screen]
```

---

## API Reference Summary

| Method   | Endpoint                   | Description                                                          |
| -------- | -------------------------- | -------------------------------------------------------------------- |
| `GET`    | `/api/health`              | Healthcheck to verify the backend server is running                  |
| `GET`    | `/api/transaction/all`     | Fetch all saved transactions                                         |
| `GET`    | `/api/transaction/{tr_id}` | Fetch a single transaction by ID                                     |
| `POST`   | `/api/transaction/`        | Create a new transaction                                             |
| `PATCH`  | `/api/transaction/{tr_id}` | Update fields of an existing transaction                             |
| `DELETE` | `/api/transaction/{tr_id}` | Delete a transaction                                                 |
| `POST`   | `/api/forecast`            | Calculate daily balances and highest/lowest points for a given month |

---

## Common Beginner FAQs & Troubleshooting

### 1. What does CORS error mean?

**CORS (Cross-Origin Resource Sharing)** is a browser security rule. Because your frontend runs on `http://localhost:5173` and your backend runs on `http://localhost:8000`, the browser considers them different "origins". In `backend/main.py`, we explicitly allow `http://localhost:5173` so the browser permits requests between them.

### 2. Where is my data saved?

All transactions are saved in `backend/app/transaction.db`. This is a self-contained SQLite file. You do not need to install any separate database software (like MySQL or PostgreSQL) to run this app locally.

### 3. How do recurring transactions work?

When building a forecast:

- **One Time**: Applied only on the exact transaction date.
- **Daily**: Applied on every day on or after the start date.
- **Weekly**: Applied every week on the same day of the week (e.g. every Wednesday).
- **Monthly**: Applied every month on the matching day number (e.g. the 15th) or the last day of the month if the month doesn't have that many days (e.g. 31st of February).
- **Yearly**: Applied once a year on the same month and day (e.g. every August 16th).

### 4. Do positive and negative amounts matter?

Yes!

- **Positive numbers** (e.g., `1500.00`) represent **Income**.
- **Negative numbers** (e.g., `-50.00`) represent **Expenses**.

---

## License

MIT License Copyright (c) 2026
