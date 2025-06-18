#!/bin/bash

# Toy Data Pipeline - Development Start Script

echo "🚀 Starting Toy Data Pipeline Development Environment..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    echo "❌ docker-compose is not installed. Please install it first."
    exit 1
fi

echo "📦 Starting services with Docker Compose..."
docker-compose up -d postgres redis

echo "⏳ Waiting for services to be ready..."
sleep 10

# Check if postgres is ready
echo "🔍 Checking PostgreSQL connection..."
until docker-compose exec postgres pg_isready -U postgres; do
    echo "⏳ Waiting for PostgreSQL..."
    sleep 2
done

# Check if redis is ready
echo "🔍 Checking Redis connection..."
until docker-compose exec redis redis-cli ping; do
    echo "⏳ Waiting for Redis..."
    sleep 2
done

echo "✅ Infrastructure services are ready!"

echo "🐍 Setting up Backend..."
cd backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating Python virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Run database migrations
echo "🗄️ Running database migrations..."
alembic upgrade head

echo "🚀 Starting Backend server..."
uvicorn main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Start Celery worker
echo "👷 Starting Celery worker..."
celery -A app.celery_app worker --loglevel=info &
CELERY_PID=$!

cd ..

echo "⚛️ Setting up Frontend..."
cd frontend

# Install dependencies
echo "📦 Installing Node.js dependencies..."
npm install

echo "🚀 Starting Frontend development server..."
npm run dev &
FRONTEND_PID=$!

cd ..

echo ""
echo "🎉 Development environment is ready!"
echo ""
echo "📍 Available services:"
echo "   🌐 Frontend:  http://localhost:3000"
echo "   🔧 Backend:   http://localhost:8000"
echo "   📚 API Docs:  http://localhost:8000/docs"
echo "   🌸 Flower:    http://localhost:5555"
echo ""
echo "💡 To stop all services, press Ctrl+C"

# Function to cleanup background processes
cleanup() {
    echo ""
    echo "🛑 Stopping services..."
    kill $BACKEND_PID $CELERY_PID $FRONTEND_PID 2>/dev/null
    docker-compose down
    echo "✅ All services stopped."
    exit 0
}

# Trap Ctrl+C and call cleanup
trap cleanup INT

# Wait for background processes
wait
