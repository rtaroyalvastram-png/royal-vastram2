@echo off
echo Starting Billing Management System...

start cmd /k "cd backend && call venv\Scripts\activate && uvicorn main:app --reload"
start cmd /k "cd frontend && npm run dev"

echo Servers started!
echo Frontend: http://localhost:5173
echo Backend: http://localhost:8000
