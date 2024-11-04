# Usar una imagen base de Python oficial más ligera
FROM python:3.8.20-slim

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar el archivo de requisitos e instalar las dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    rm -rf /root/.cache/pip

# Copiar el resto del código de la aplicación al directorio de trabajo
COPY . .

# Crear un usuario no root y cambiar a él
RUN useradd -m myuser
USER myuser

# Exponer el puerto en el que Flask se ejecutará
EXPOSE 5000

# Comando para ejecutar la aplicación
CMD ["flask", "run", "--host=0.0.0.0"]