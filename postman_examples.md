# Ejemplos de API para Postman

## Base URL
```
http://localhost:5000
```

## 1. Registro de Usuario (POST)

**Endpoint:** `POST /auth/register`

**Headers:**
```
Content-Type: application/json
```

**Body (raw JSON):**
```json
{
    "email": "usuario@ejemplo.com",
    "password": "mipassword123"
}
```

**Respuesta exitosa (201):**
```json
{
    "message": "User registered successfully",
    "user": {
        "id": 1,
        "username": "usuario@ejemplo.com",
        "email": "usuario@ejemplo.com",
        "created_at": "2025-09-25T10:30:00.000000"
    },
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

## 2. Login de Usuario (POST)

**Endpoint:** `POST /auth/login`

**Headers:**
```
Content-Type: application/json
```

**Body (raw JSON):**
```json
{
    "email": "usuario@ejemplo.com",
    "password": "mipassword123"
}
```

**Respuesta exitosa (200):**
```json
{
    "message": "Login successful",
    "user": {
        "id": 1,
        "username": "usuario@ejemplo.com",
        "email": "usuario@ejemplo.com",
        "created_at": "2025-09-25T10:30:00.000000"
    },
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

## 3. Renovar Token (POST)

**Endpoint:** `POST /auth/refresh`

**Headers:**
```
Content-Type: application/json
Authorization: Bearer [REFRESH_TOKEN_AQUI]
```

**Body:** (Vacío)

**Respuesta exitosa (200):**
```json
{
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

## 4. Obtener Usuario Actual (GET)

**Endpoint:** `GET /auth/me`

**Headers:**
```
Authorization: Bearer [ACCESS_TOKEN_AQUI]
```

**Respuesta exitosa (200):**
```json
{
    "user": {
        "id": 1,
        "username": "usuario@ejemplo.com",
        "email": "usuario@ejemplo.com",
        "created_at": "2025-09-25T10:30:00.000000"
    }
}
```

## Errores Comunes

### Error de validación (400):
```json
{
    "error": "Missing or empty fields: email, password"
}
```

### Error de email inválido (400):
```json
{
    "error": "Invalid email address: The email address is not valid"
}
```

### Error de contraseña débil (400):
```json
{
    "error": "Password must be at least 6 characters long"
}
```

### Error de email ya registrado (400):
```json
{
    "error": "Email already registered"
}
```

### Error de credenciales inválidas (401):
```json
{
    "error": "Invalid email or password"
}
```

### Error de token expirado (401):
```json
{
    "error": "Token has expired"
}
```

### Error de token faltante (401):
```json
{
    "error": "Authorization token required"
}
```

## Configuración en Postman

1. **Variables de entorno:**
   - Crea una variable `base_url` con valor `http://localhost:5000`
   - Crea variables `access_token` y `refresh_token` para almacenar los tokens

2. **Scripts de prueba** (pestaña Tests en cada request):
   ```javascript
   // Para registro y login
   if (pm.response.code === 200 || pm.response.code === 201) {
       var jsonData = pm.response.json();
       pm.environment.set("access_token", jsonData.access_token);
       pm.environment.set("refresh_token", jsonData.refresh_token);
   }
   ```

3. **Header automático:**
   - En requests protegidos, usa: `Bearer {{access_token}}`