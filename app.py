import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.eggs import eggs_router
app = FastAPI()

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite solicitudes desde cualquier origen
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos HTTP (GET, POST, etc.)
    allow_headers=["*"],  # Permite todas las cabeceras
)


app.include_router(eggs_router)


