from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.core.config import get_settings
from src.api.routes import simulation
from src.infrastructure.database.connection import init_db

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gerencia o ciclo de vida da aplicação"""
    # Startup
    await init_db()
    print(f"🏀 {settings.app_name} iniciado!")
    yield
    # Shutdown
    print("👋 Encerrando aplicação...")


app = FastAPI(
    title=settings.app_name,
    description="API para simular o encaixe de jogadores da NBA em diferentes times",
    version="1.0.0",
    lifespan=lifespan
)

# Configurar CORS para o frontend Angular
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4200",  # Angular dev server
        "http://127.0.0.1:4200"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar rotas
app.include_router(
    simulation.router,
    prefix=settings.api_prefix,
    tags=["Simulação"]
)


@app.get("/", tags=["Health"])
async def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "app": settings.app_name,
        "version": "1.0.0"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Endpoint de saúde da API"""
    return {"status": "healthy"}