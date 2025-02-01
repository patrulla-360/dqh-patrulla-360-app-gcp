# Usa una imagen base ligera
FROM python:3.10-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos de la aplicación
COPY . /app

# Instala las dependencias
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt


# Define el comando de ejecución con Gunicorn
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:8080", "main:app"]
