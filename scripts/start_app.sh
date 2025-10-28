#!/bin/bash

echo "🚀 Starting CAP 9000 Code Assistant (Desktop App)..."
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

# Check if Flask is installed
if ! python3 -c "import flask" &> /dev/null; then
    echo "📦 Installing Flask..."
    pip3 install flask flask-cors
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js first."
    exit 1
fi

# Check and start Ollama if needed
echo ""
./check_ollama.sh
OLLAMA_STATUS=$?

if [ $OLLAMA_STATUS -ne 0 ]; then
    echo ""
    echo "⚠️  ATTENZIONE: Ollama non è disponibile"
    echo "L'applicazione si avvierà comunque, ma le risposte AI saranno limitate."
    echo ""
    read -p "Continuare comunque? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Check if dependencies are installed
if [ ! -d "frontend/node_modules" ]; then
    echo "📦 Installing dependencies..."
    cd frontend
    npm install
    cd ..
fi

# Build and start desktop app
echo ""
echo "🔨 Building and launching desktop application..."
cd frontend
npm run start
