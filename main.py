from fastapi import FastAPI, HTTPException, Cookie, Header
from typing import Optional
import pandas as pd
import os
import uuid
from datetime import datetime, timedelta

app = FastAPI()

# Almacenamiento de sesiones activas (en memoria)
active_sessions = {}

@app.get("/")
async def saludo():
    return "welcome to my login system"

@app.post("/createUser")
async def save_new_user(name: str, password: str, email: str, filename: str = "users.csv"):
    """
    Saves a new user to a text file.
    """
    try:
        userEntry = {
            "id": str(uuid.uuid4()),
            "name": name,
            "pass": password,
            "email": email
        }
        
        df_new = pd.DataFrame([userEntry])

        if os.path.exists(filename):
            df_existing = pd.read_csv(filename)
            df_combined = pd.concat([df_existing, df_new], ignore_index=True)
        else:
            df_combined = df_new

        df_combined.to_csv(filename, index=False, encoding="utf-8")
        return {"success": True, "message": "Usuario creado exitosamente"}
    except Exception as e:
        print(f"Error: {e}")
        return {"success": False, "message": str(e)}

@app.get("/userAll")
async def userAll():
    try:
        ruta = os.getcwd()
        file = os.path.join(ruta, "users.csv")

        if not os.path.exists(file):
            return {"message": "no hay archivo aun", "users": []}
        
        df = pd.read_csv(file)
        return {"users": df.to_dict(orient="records")}
    except Exception as e:
        print(f"Error: {e}")
        return {"success": False, "message": str(e)}

@app.get("/validateIncome")
async def validate_user(email: str, password: str, filename: str = "users.csv"):
    """
    Valida email y contraseña y crea una sesión si es correcto.
    """
    try:
        if not os.path.exists(filename):
            return {
                "success": False,
                "message": "No hay usuarios registrados aún"
            }
        
        df = pd.read_csv(filename)
        
        df["email"] = df["email"].astype(str).str.strip().str.lower()
        df["pass"] = df["pass"].astype(str).str.strip()
        
        email_clean = str(email).strip().lower()
        password_clean = str(password).strip()
        
        filtro = df[(df["email"] == email_clean) & (df["pass"] == password_clean)]
        
        if not filtro.empty:
            usuario = filtro.iloc[0].to_dict()
            
            # Crear token de sesión
            session_token = str(uuid.uuid4())
            
            # Guardar sesión activa
            active_sessions[session_token] = {
                "user_id": usuario["id"],
                "user_email": usuario["email"],
                "user_name": usuario["name"],
                "login_time": datetime.now().isoformat(),
                "expires": (datetime.now() + timedelta(hours=24)).isoformat()
            }
            
            # Remover contraseña por seguridad
            usuario.pop("pass", None)
            
            return {
                "success": True,
                "message": "Login exitoso",
                "user": usuario,
                "session_token": session_token
            }
        else:
            email_exists = df[df["email"] == email_clean]
            if not email_exists.empty:
                return {
                    "success": False,
                    "message": "Contraseña incorrecta"
                }
            else:
                return {
                    "success": False,
                    "message": "Email no registrado"
                }
        
    except Exception as e:
        print(f"Error en login: {e}")
        return {
            "success": False,
            "message": f"Error del sistema: {str(e)}"
        }

@app.get("/isLogged")
async def isLogged(session_token: str):
    """
    Verifica si un usuario está logueado mediante su token de sesión.
    """
    try:
        # Verificar si el token existe en las sesiones activas
        if session_token not in active_sessions:
            return {
                "logged": False,
                "message": "No hay sesión activa. Por favor, inicie sesión."
            }
        
        session = active_sessions[session_token]
        
        # Verificar si la sesión ha expirado
        expires = datetime.fromisoformat(session["expires"])
        if datetime.now() > expires:
            # Eliminar sesión expirada
            del active_sessions[session_token]
            return {
                "logged": False,
                "message": "La sesión ha expirado. Por favor, inicie sesión nuevamente."
            }
        
        # Sesión válida
        return {
            "logged": True,
            "message": "Sesión activa",
            "user": {
                "id": session["user_id"],
                "email": session["user_email"],
                "name": session["user_name"]
            },
            "login_time": session["login_time"],
            "expires_in": session["expires"]
        }
        
    except Exception as e:
        print(f"Error en isLogged: {e}")
        return {
            "logged": False,
            "message": f"Error del sistema: {str(e)}"
        }

@app.get("/activeSessions")
async def lookActiveSessions():
    """
    Muestra todos los usuarios actualmente logueados (sesiones activas).
    
    Returns:
        dict: Lista de usuarios logueados con sus tokens y datos
    """
    try:
        # Limpiar sesiones expiradas primero
        expired_tokens = []
        for token, session in active_sessions.items():
            try:
                expires = datetime.fromisoformat(session["expires"])
                if datetime.now() > expires:
                    expired_tokens.append(token)
            except:
                expired_tokens.append(token)
        
        # Eliminar sesiones expiradas
        for token in expired_tokens:
            del active_sessions[token]
        
        if not active_sessions:
            return {
                "success": True,
                "message": "No hay usuarios logueados actualmente",
                "total_active": 0,
                "users": []
            }
        
        # Construir lista de usuarios logueados
        active_users_list = []
        for token, session in active_sessions.items():
            active_users_list.append({
                "session_token": token,
                "user_id": session["user_id"],
                "user_name": session["user_name"],
                "user_email": session["user_email"],
                "login_time": session["login_time"],
                "expires_at": session["expires"]
            })
        
        return {
            "success": True,
            "message": f"Hay {len(active_sessions)} usuario(s) logueado(s)",
            "total_active": len(active_sessions),
            "users": active_users_list
        }
        
    except Exception as e:
        print(f"Error en activeSessions: {e}")
        return {
            "success": False,
            "message": f"Error al obtener sesiones activas: {str(e)}"
        }

@app.get("/getUserToken")
async def get_user_token(user_email: str = None, user_name: str = None):
    """
    Obtiene el token de un usuario específico por email o nombre.
    
    Args:
        user_email (str, optional): Email del usuario
        user_name (str, optional): Nombre del usuario
    
    Returns:
        dict: Token del usuario si está logueado
    """
    try:
        if not user_email and not user_name:
            return {
                "success": False,
                "message": "Debe proporcionar user_email o user_name"
            }
        
        # Buscar sesión activa
        found_token = None
        found_session = None
        
        for token, session in active_sessions.items():
            if user_email and session["user_email"].lower() == user_email.lower():
                found_token = token
                found_session = session
                break
            elif user_name and session["user_name"].lower() == user_name.lower():
                found_token = token
                found_session = session
                break
        
        if found_token and found_session:
            return {
                "success": True,
                "message": "Token encontrado",
                "session_token": found_token,
                "user": {
                    "id": found_session["user_id"],
                    "name": found_session["user_name"],
                    "email": found_session["user_email"]
                },
                "login_time": found_session["login_time"],
                "expires_at": found_session["expires"]
            }
        else:
            return {
                "success": False,
                "message": "Usuario no está logueado actualmente"
            }
            
    except Exception as e:
        print(f"Error en getUserToken: {e}")
        return {
            "success": False,
            "message": f"Error: {str(e)}"
        }

@app.post("/logout")
async def logout(session_token: str):
    """
    Cierra la sesión de un usuario específico.
    """
    try:
        if session_token in active_sessions:
            user_name = active_sessions[session_token]["user_name"]
            del active_sessions[session_token]
            return {
                "success": True,
                "message": f"Sesión cerrada exitosamente para {user_name}"
            }
        else:
            return {
                "success": False,
                "message": "No se encontró una sesión activa con ese token"
            }
    except Exception as e:
        print(f"Error en logout: {e}")
        return {
            "success": False,
            "message": f"Error: {str(e)}"
        }

@app.post("/logoutAll")
async def logout_all():
    """
    Cierra todas las sesiones activas (logout de todos los usuarios).
    """
    try:
        total = len(active_sessions)
        active_sessions.clear()
        return {
            "success": True,
            "message": f"Se cerraron {total} sesión(es) activa(s)"
        }
    except Exception as e:
        print(f"Error en logoutAll: {e}")
        return {
            "success": False,
            "message": f"Error: {str(e)}"
        }