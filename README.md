# ApiLogin-ACT

# Instrucciones para ejecutar la API

## Requisitos previos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

## Instalación

1. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Crear archivo .env** (opcional, pero recomendado):
   ```bash
   # .env
   DATABASE_URL=sqlite:///site.db
   JWT_SECRET_KEY=tu-clave-super-secreta-aqui
   ACCESS_TOKEN_EXPIRES=15
   REFRESH_TOKEN_EXPIRES=7
   FLASK_DEBUG=true
   ```

3. **Ejecutar migraciones** (si es necesario):
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

## Ejecución

```bash
python3 app.py
```

La API estará disponible en: `http://localhost:5000`

## Estructura de rutas disponibles:

- `POST /auth/register` - Registro de usuario
- `POST /auth/login` - Login de usuario
- `POST /auth/refresh` - Renovar token de acceso
- `GET /auth/me` - Obtener información del usuario actual

## Pruebas rápidas con curl:

### Registro:
```bash
curl -X POST http://localhost:5000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password123"}'
```

### Login:
```bash
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password123"}'
```

### Usuario actual (requiere token):
```bash
curl -X GET http://localhost:5000/auth/me \
  -H "Authorization: Bearer TU_TOKEN_AQUI"
```