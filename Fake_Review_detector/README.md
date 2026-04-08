AI Fake Review Detector : 

An AI-powered web application that detects whether a product review is fake or genuine using LLM analysis.

The application uses FastAPI for the backend, Streamlit for the frontend, and Groq LLM for intelligent review analysis. The entire project is containerized using Docker for easy deployment.

Features:

1 .Detect fake product reviews using AI

2 .LLM-powered analysis using Groq API

3 .Interactive UI built with Streamlit

4 .Fast backend API with FastAPI

5 .Fully containerized using Docker

6 .Stores review data using SQLite

Project Architecture :

User
 ↓
Streamlit Frontend
 ↓
FastAPI Backend
 ↓
Groq LLM API
 ↓
SQLite Database 

Project Structure :

final_project
│
├── backend
│   ├── database
│   ├── models
│   ├── routes
│   ├── services
│   ├── main.py
│   ├── database.db
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend
│   ├── streamlit.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md


Installation : 

Clone the repository:
git clone https://github.com/yourusername/Fake_Review_Detector.git


Environment Variables :

Create a .env file in the root directory.

Example:

GROQ_API_KEY=your_groq_api_key_here

You can get an API key from:

https://console.groq.com/  

Run With Docker (Build and start the application) :

command = docker compose up --build

Access the Application : 

Frontend (Streamlit):

http://localhost:8501

Backend API:

http://localhost:8000

API Documentation:

http://localhost:8000/docs

Example Review :

Try entering a review like:

This product is amazing and works perfectly!  or

Worst product ever. Totally useless.

The AI will analyze whether the review is fake or genuine.

Technologies Used :

1 .Python

2 .FastAPI

3 .Streamlit

4 .Groq LLM

5 .SQLite

6 .Docker

7 .Docker Compose
