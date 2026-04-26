# Imagen ligera oficial
FROM python:3.11-slim

# Directorio de trabajo
WORKDIR /app

# Copiar dependencias primero (mejora caché de Docker)
COPY requirements.txt .

# Instalar librerías
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del proyecto
COPY . .

# Exponer puerto (Flask por defecto)
EXPOSE 8001

# Comando de arranque
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]