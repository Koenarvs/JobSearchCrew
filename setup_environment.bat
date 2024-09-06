@echo off
echo Updating Python, installing recommended libraries, frameworks, and services...

REM Check if Chocolatey is installed, if not, install it
where choco >nul 2>nul
if %errorlevel% neq 0 (
    echo Installing Chocolatey...
    @"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command "[System.Net.ServicePointManager]::SecurityProtocol = 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))" && SET "PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin"
)

REM Install Docker Desktop
choco install docker-desktop -y

REM Install Elasticsearch
choco install elasticsearch -y

REM Install Kibana
choco install kibana -y

REM Install PostgreSQL
choco install postgresql -y

REM Install Node.js and npm
choco install nodejs-lts -y

REM Update pip
python -m pip install --upgrade pip

REM Install recommended web frameworks
pip install fastapi uvicorn flask django flask-cors

REM Install CrewAI
pip install crewai

REM Install vector databases
pip install milvus qdrant-client

REM Install PostgreSQL adapter
pip install psycopg2-binary

REM Install NLP libraries
pip install spacy nltk

REM Install asynchronous libraries
pip install asyncio aiohttp

REM Install Docker SDK for Python
pip install docker

REM Install authentication libraries
pip install python-jose[cryptography] passlib[bcrypt]

REM Install logging and monitoring tools
pip install elasticsearch logstash kibana prometheus-client grafana-api

REM Install message queue libraries
pip install pika kafka-python

REM Install LLM API libraries
pip install openai anthropic llama-cpp-python google-generativeai azure-openai

REM Install additional useful libraries
pip install python-dotenv requests pydantic

REM Download spaCy English model
python -m spacy download en_core_web_sm

REM Download NLTK data
python -m nltk.downloader popular

REM Install Pandas
pip install pandas

REM Install Python linting and code quality tools
pip install pylint black isort mypy

REM Install React and related tools
npm install -g create-react-app redux react-redux react-router-dom axios eslint jest @testing-library/react @testing-library/jest-dom prettier

REM Install Yarn
choco install yarn -y

REM Install Docker containers for additional services
docker pull milvus/milvus:latest
docker pull qdrant/qdrant:latest
docker pull grafana/grafana:latest
docker pull prom/prometheus:latest
docker pull rabbitmq:3-management
docker pull wurstmeister/kafka:latest
docker pull wurstmeister/zookeeper:latest

REM Setup ESLint for React
npm init -y
npm install --save-dev eslint eslint-plugin-react eslint-plugin-react-hooks @typescript-eslint/eslint-plugin @typescript-eslint/parser
npx eslint --init

REM Generate Pylint configuration
pylint --generate-rcfile > .pylintrc

echo Installation complete. Please check for any errors above.
echo Note: You may need to restart your computer for some changes to take effect.
pause