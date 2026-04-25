from fastapi import FastAPI
import pandas as pd
import os
import uuid

App = FastAPI()

@App.get("/")
async def saludo():
    return "welcome to my login system"

@App.post("/createUser")
async def save_new_user(name : str, password : str, email : str, filename : str="users.csv"):
    """
    Saves a new user to a text file.
    
    Args:
        name (str): User's name
        password (str): User's password
        email (str): User's email
        filename (str): File to save user data (default: "users.txt")
    
    Returns:
        bool: True if successful, False if user already exists
    """
    try:
        # CORREGIDO: uuid.uuid4() con paréntesis
        userEntry = {
            "id": str(uuid.uuid4()),
            "name": name,
            "pass": password,
            "email": email
        }
         # CORREGIDO: Crear DataFrame con lista de diccionarios
        df_new = pd.DataFrame([userEntry])  # Importante: [userEntry] no userEntry solo

        # Verificar si el archivo existe
        if os.path.exists(filename):
            # Leer usuarios existentes
            df_existing = pd.read_csv(filename)
            # Concatenar (no sobrescribir)
            df_combined = pd.concat([df_existing, df_new], ignore_index=True)
        else:
            df_combined = df_new

        # Guardar (esto sí sobrescribe con TODOS los datos)
        df_combined.to_csv(filename, index=False, encoding="utf-8")
        return True
    except Exception as e:
        print(f"Error: {e}")  # Para depuración
        return False

@App.get("/userAll")
async def userAll( ):
    pass

@App.get("/validateIncome")
async def validateIncome(userEmail , UserPass):
    pass

    



