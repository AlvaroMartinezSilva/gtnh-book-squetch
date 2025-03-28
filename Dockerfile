# Imagen base oficial de Python
FROM python:3.12-slim

# Variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Crear directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y build-essential libpq-dev curl && rm -rf /var/lib/apt/lists/*

# Copiar archivos de proyecto
COPY . /app

# Instalar dependencias de Python
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Puerto por defecto de Streamlit
EXPOSE 8501

# Comando de ejecución
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
