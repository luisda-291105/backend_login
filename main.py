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
async def userAll():
    try:
        ruta = os.getcwd()
        file = os.path.join(ruta , "users.csv")

        if not os.path.exists(file):
            return "no hay archivo aun"
        
        df = pd.read_csv(file)
        return df.to_dict(orient="records")
    except Exception as e:
        print(f"Error: {e}")  
        return False


@App.get("/validateIncome")
async def validate_user(email, password, filename="users.csv"):
    """
    Valida email y contraseña contra el archivo CSV.
    
    Args:
        email (str): Email del usuario
        password (str): Contraseña del usuario
        filename (str): Ruta del archivo CSV
    
    Returns:
        dict or str: Diccionario con datos del usuario si es válido, 
                     o mensaje de error si no
    """
    try:
        # Verificar si el archivo existe
        if not os.path.exists(filename):
            return "no hay archivo aun"
        
        # Leer el CSV
        df = pd.read_csv(filename)
        
        # Limpiar datos
        df["email"] = df["email"].astype(str).str.strip().str.lower()
        df["pass"] = df["pass"].astype(str).str.strip()
        
        # Limpiar email y password de entrada
        email_clean = str(email).strip().lower()
        password_clean = str(password).strip()
        
        # Buscar usuario que coincida con email Y contraseña
        filtro = df[(df["email"] == email_clean) & (df["pass"] == password_clean)]
        
        if not filtro.empty:
            # Devolver el primer usuario encontrado como diccionario
            usuario = filtro.iloc[0].to_dict()
            return usuario
        else:
            # Verificar si el email existe pero la contraseña es incorrecta
            email_exists = df[df["email"] == email_clean]
            if not email_exists.empty:
                return "contraseña incorrecta"
            else:
                return "email no registrado"
        
    except Exception as e:
        print(f"Error: {e}")
        return f"error en validación: {str(e)}"


    



