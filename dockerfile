# Dockerfile
FROM python:3.11-slim

# Establecer directorio de trabajo
WORKDIR /app

# Copiar requirements.txt limpio
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto de la aplicación
COPY . .

# Exponer el puerto
EXPOSE 8001

# Comando para ejecutar la aplicación
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]