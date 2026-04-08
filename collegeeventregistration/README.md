 🎓 College Event Registration & Management System

An AI-enabled full-stack event management platform that allows students to register for college events and receive automated confirmations. Built using FastAPI, Streamlit, and SQLite. This system simulates a  institutional event platform with registration, admin dashboard, chat assistant, email notifications, and optional RAG support.

 🚀 Features

 👩‍🎓 Student Features

* Register for events
* View available events
* Real-time confirmation
* Chat support system
* QR code generation for entry
* Email confirmation

 🛠 Admin Features

* Create/manage events
* View registrations
* Monitor participants
* Admin dashboard
* Google Sheets sync

 🤖 AI / Smart Features

* Chat assistant system
* Retrieval-based responses (RAG)
* Rule-based automation
* Email automation
* Sheets integration

 🧠 Architecture

User → Streamlit UI → FastAPI Backend → Services → Database
↘ Chat/RAG
↘ Email
↘ Sheets

 🛠 Tech Stack

**Backend**

* FastAPI
* Python
* SQLAlchemy
* SQLite

**Frontend**

* Streamlit

**AI / Automation**

* RAG module
* Rule-based chat
* Email automation

**Integrations**

* Google Sheets API
* QR generation
* SMTP Email

 📁 Project Structure

college-event-registration-system/
│
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   ├── events.db
│   ├── credentials.json
│   ├── rules.txt
│   ├── string_qr.png
│   └── sheets.py
│
│   ├── database/
│   │   ├── db.py
│   │   └── deps.py
│   │
│   ├── models/
│   │   ├── tables.py
│   │   └── pydantic.py
│   │
│   ├── routes/
│   │   └── routes.py
│   │
│   └── services/
│       ├── auth.py
│       ├── data.py
│       ├── email_service.py
│       └── rag.py
│
├── frontend/
│   ├── student_app.py
│   ├── admin_dashboard.py
│   └── requirements.txt
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md

 ⚙️ Setup

 Clone repository

git clone https://github.com/YOUR_USERNAME/college-event-registration.git
cd college-event-registration

 Create virtual environment

python -m venv venv
venv\Scripts\activate

 Install dependencies

pip install fastapi uvicorn streamlit sqlalchemy pydantic requests

 ▶️ Run Backend

cd backend
uvicorn main:app --reload

Backend: http://localhost:8000
Docs: http://localhost:8000/docs

 ▶️ Run Frontend

cd frontend
streamlit run student_app.py

Admin dashboard:
streamlit run admin_dashboard.py

Run with Docker

1. Clone the repository

git clone https://github.com/yourusername/collegeeventregistration.git

2. Navigate to the project folder

cd collegeeventregistration

3. Start the containers

docker compose up --build

4. Open the applications

Student Portal:
http://localhost:8501

Admin Dashboard:
http://localhost:8502

Backend API:
http://localhost:8001/docs

 📡 API Endpoints

GET /events
POST /events
POST /register
POST /login
POST /chat

 🧠 How It Works

1. Student opens Streamlit UI
2. Events fetched from FastAPI
3. Student registers
4. Data stored in SQLite
5. Email + QR generated
6. Admin monitors dashboard

 📊 Dataset

No external dataset used. All data generated internally. Includes student registrations, events, chat messages, and admin activity. Stored in SQLite for demo use.

 🔒 Ethics & Privacy

* Educational project
* Stores only basic user data
* No third-party sharing
* Chat stored locally
* Avoid sensitive info
* Can add authentication & encryption

Focus on privacy, transparency, and responsible data handling.



