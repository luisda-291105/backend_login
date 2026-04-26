# 📘 Documentación — Backend Login API
**Lenguaje:** Python · **Framework:** FastAPI

---

## 1. Iniciar el servidor

Guarda tu código en un archivo llamado `main.py`, luego ejecuta en la terminal:

```bash
uvicorn main:App --reload --host 127.0.0.1 --port 8000
```

**Salida esperada:**

```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

---

## 2. Abrir la documentación interactiva

Abre tu navegador y ve a: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

Verás los siguientes endpoints disponibles:

```
FastAPI - Swagger UI

┌─────────────────────────────────┐
│  GET    /                       │
│  POST   /createUser             │
│  GET    /userAll                │
│  GET    /validateIncome         │
│  GET    /isLogged               │
│  GET    /activeSessions         │
│  GET    /getUserToken           │
│  POST   /logout                 │
│  POST   /logoutAll              │
└─────────────────────────────────┘
```

---

## 3. Flujo de prueba paso a paso

### Paso 1 — Crear un usuario `POST /createUser`

Haz clic en `POST /createUser` → **Try it out** → completa los parámetros:

```json
{
  "name": "Juan Perez",
  "password": "123456",
  "email": "juan@email.com"
}
```

**Respuesta esperada:**

```json
{
  "success": true,
  "message": "Usuario creado exitosamente"
}
```

---

### Paso 2 — Crear otro usuario

Repite el Paso 1 con datos diferentes:

```json
{
  "name": "Maria Lopez",
  "password": "abcdef",
  "email": "maria@email.com"
}
```

---

### Paso 3 — Ver todos los usuarios `GET /userAll`

Haz clic en `GET /userAll` → **Try it out** → **Execute**.

**Respuesta esperada:**

```json
{
  "users": [
    {
      "id": "abc123...",
      "name": "Juan Perez",
      "pass": "123456",
      "email": "juan@email.com"
    },
    {
      "id": "def456...",
      "name": "Maria Lopez",
      "pass": "abcdef",
      "email": "maria@email.com"
    }
  ]
}
```

---

### Paso 4 — Login usuario 1 `GET /validateIncome`

Haz clic en `GET /validateIncome` → **Try it out** → completa:

```json
{
  "email": "juan@email.com",
  "password": "123456"
}
```

**Respuesta esperada:**

```json
{
  "success": true,
  "message": "Login exitoso",
  "user": {
    "id": "abc123...",
    "name": "Juan Perez",
    "email": "juan@email.com"
  },
  "session_token": "a1b2c3d4-e5f6-7890-1234-567890abcdef"
}
```

> ❗ **IMPORTANTE:** Copia el `session_token` — lo necesitarás para los siguientes pasos.

---

### Paso 5 — Login usuario 2

Repite el Paso 4 con Maria:

```json
{
  "email": "maria@email.com",
  "password": "abcdef"
}
```

Copia también este token.

---

### Paso 6 — Verificar usuario 1 logueado `GET /isLogged`

Haz clic en `GET /isLogged` → **Try it out** → pega el `session_token` de Juan:

```
session_token: a1b2c3d4-e5f6-7890-1234-567890abcdef
```

**Respuesta esperada:**

```json
{
  "logged": true,
  "message": "Sesión activa",
  "user": {
    "id": "abc123...",
    "email": "juan@email.com",
    "name": "Juan Perez"
  },
  "login_time": "2024-01-15T10:30:00",
  "expires_in": "2024-01-16T10:30:00"
}
```

---

### Paso 7 — Ver todos los usuarios logueados `GET /activeSessions`

Haz clic en `GET /activeSessions` → **Try it out** → **Execute**.

**Respuesta esperada:**

```json
{
  "success": true,
  "message": "Hay 2 usuario(s) logueado(s)",
  "total_active": 2,
  "users": [
    {
      "session_token": "a1b2c3d4...",
      "user_id": "abc123...",
      "user_name": "Juan Perez",
      "user_email": "juan@email.com",
      "login_time": "2024-01-15T10:30:00",
      "expires_at": "2024-01-16T10:30:00"
    },
    {
      "session_token": "e5f6g7h8...",
      "user_id": "def456...",
      "user_name": "Maria Lopez",
      "user_email": "maria@email.com",
      "login_time": "2024-01-15T10:31:00",
      "expires_at": "2024-01-16T10:31:00"
    }
  ]
}
```

---

### Paso 8 — Obtener token de usuario específico `GET /getUserToken`

Haz clic en `GET /getUserToken` → **Try it out** → buscar por email:

```
user_email: maria@email.com
```

**Respuesta esperada:**

```json
{
  "success": true,
  "message": "Token encontrado",
  "session_token": "e5f6g7h8...",
  "user": {
    "id": "def456...",
    "name": "Maria Lopez",
    "email": "maria@email.com"
  },
  "login_time": "2024-01-15T10:31:00",
  "expires_at": "2024-01-16T10:31:00"
}
```

---

### Paso 9 — Cerrar sesión de usuario 1 `POST /logout`

Haz clic en `POST /logout` → **Try it out** → pega el token de Juan:

```
session_token: a1b2c3d4-e5f6-7890-1234-567890abcdef
```

**Respuesta esperada:**

```json
{
  "success": true,
  "message": "Sesión cerrada exitosamente para Juan Perez"
}
```

---

### Paso 10 — Verificar sesiones activas nuevamente

Repite el Paso 7. Ahora debería mostrar solo 1 usuario (Maria):

```json
{
  "success": true,
  "message": "Hay 1 usuario(s) logueado(s)",
  "total_active": 1,
  "users": [
    {
      "session_token": "e5f6g7h8...",
      "user_name": "Maria Lopez"
    }
  ]
}
```

---

### Paso 11 — Cerrar todas las sesiones `POST /logoutAll`

Haz clic en `POST /logoutAll` → **Try it out** → **Execute**.

**Respuesta esperada:**

```json
{
  "success": true,
  "message": "Se cerraron 1 sesión(es) activa(s)"
}
```

---

## 4. Pruebas de error (casos negativos)

### Login con contraseña incorrecta

```json
// GET /validateIncome
{
  "email": "juan@email.com",
  "password": "wrongpassword"
}
```

**Respuesta:**

```json
{
  "success": false,
  "message": "Contraseña incorrecta"
}
```

---

### Verificar sesión con token inválido

```json
// GET /isLogged
{
  "session_token": "token-invalido"
}
```

**Respuesta:**

```json
{
  "logged": false,
  "message": "No hay sesión activa. Por favor, inicie sesión."
}
```

---

## 5. Script de prueba automático en Python

```python
# test_api.py
import requests

BASE_URL = "http://127.0.0.1:8000"

def test_complete_flow():
    print("=== INICIANDO PRUEBAS ===\n")
    
    # 1. Crear usuario
    print("1. Creando usuario...")
    response = requests.post(
        f"{BASE_URL}/createUser",
        params={
            "name": "Test User",
            "password": "test123",
            "email": "test@email.com"
        }
    )
    print(f"   Respuesta: {response.json()}\n")
    
    # 2. Login
    print("2. Iniciando sesión...")
    response = requests.get(
        f"{BASE_URL}/validateIncome",
        params={"email": "test@email.com", "password": "test123"}
    )
    login_data = response.json()
    print(f"   Respuesta: {login_data}")
    
    token = login_data.get("session_token")
    print(f"   Token obtenido: {token}\n")
    
    # 3. Verificar sesión
    print("3. Verificando sesión...")
    response = requests.get(
        f"{BASE_URL}/isLogged",
        params={"session_token": token}
    )
    print(f"   Respuesta: {response.json()}\n")
    
    # 4. Ver todos los logueados
    print("4. Usuarios logueados...")
    response = requests.get(f"{BASE_URL}/activeSessions")
    print(f"   Respuesta: {response.json()}\n")
    
    # 5. Cerrar sesión
    print("5. Cerrando sesión...")
    response = requests.post(
        f"{BASE_URL}/logout",
        params={"session_token": token}
    )
    print(f"   Respuesta: {response.json()}\n")
    
    print("=== PRUEBAS COMPLETADAS ===")

if __name__ == "__main__":
    test_complete_flow()
```

---

## Resumen del flujo

```
1. Iniciar servidor    →  uvicorn main:App --reload
2. Abrir navegador     →  http://127.0.0.1:8000/docs
3. Crear usuario       →  POST /createUser
4. Login               →  GET  /validateIncome  (guardar token)
5. Verificar sesión    →  GET  /isLogged         (usar token)
6. Ver logueados       →  GET  /activeSessions
7. Buscar token        →  GET  /getUserToken
8. Cerrar sesión       →  POST /logout
9. Cerrar todos        →  POST /logoutAll
```