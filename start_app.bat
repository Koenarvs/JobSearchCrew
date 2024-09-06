@echo off
echo Starting the Job Search application...

REM Check if Docker is running
docker info > nul 2>&1
if %errorlevel% neq 0 (
    echo Docker is not running. Please start Docker Desktop and try again.
    exit /b 1
)

REM Generate requirements.txt
python generate_requirements.py

REM Run Python linting and code quality checks
echo Running Python code quality checks...
pylint **/*.py
black --check .
isort --check-only .
mypy .

REM Run ESLint on React code
echo Running ESLint on React code...
cd frontend
npx eslint .
cd ..

REM Build and start the backend containers
echo Starting backend services...
docker-compose up --build -d

REM Start the React frontend
echo Starting React frontend...
cd frontend
npm start

echo.
echo Job Search application is starting up.
echo Backend is accessible at http://localhost:5000
echo Frontend is accessible at http://localhost:3000
echo Kibana dashboard is available at http://localhost:5601
echo.
echo To stop the application, run: docker-compose down
echo To view logs, run: docker-compose logs -f