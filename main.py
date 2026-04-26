from fastapi import FastAPI, HTTPException, Cookie, Header
from typing import Optional
import pandas as pd
import os
import uuid
from datetime import datetime, timedelta

App = FastAPI()

# Almacenamiento de sesiones activas (en memoria)
active_sessions = {}

@App.get("/")
async def saludo():
    return "welcome to my login system"

@App.post("/createUser")
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

@App.get("/userAll")
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

@App.get("/validateIncome")
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
                "session_token": session_token  # Importante: devolver el token al cliente
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

@App.get("/isLogged")
async def isLogged(session_token: str):
    """
    Verifica si un usuario está logueado mediante su token de sesión.
    
    Args:
        session_token (str): Token de sesión obtenido durante el login
    
    Returns:
        dict: Estado de la sesión y datos del usuario si está logueado
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

