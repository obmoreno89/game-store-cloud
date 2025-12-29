# 1. Usamos una imagen ligera de Python
FROM python:3.11-slim

# --- AGREGADO AQUÍ ---
# Instalamos curl para que el Healthcheck de Docker funcione
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# 2. Definimos el directorio de trabajo raíz dentro del contenedor
WORKDIR /app

# 3. Copiamos el archivo de dependencias
COPY requirements.txt .

# 4. Instalamos las librerías
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiamos todo el contenido de tu carpeta local al contenedor
COPY . .

# 6. El comando de ejecución
CMD ["python", "-m", "uvicorn", "app.core.main:app", "--host", "0.0.0.0", "--port", "8000"]